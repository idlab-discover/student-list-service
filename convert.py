import csv
import os
from ldap3 import SIMPLE, Server, Connection, ALL

# LDAP connection
server = Server(host=os.getenv("LDAP_HOST"), port=int(os.getenv("LDAP_PORT")), use_ssl=True, get_info=ALL)
conn = Connection(
    server,
    user=os.getenv("LDAP_USER"),
    password=os.getenv("LDAP_PASS"),
    authentication=SIMPLE,
    lazy=True,
    auto_bind=True,
)


def ldap_convert(students):
    """Look up the usernames the students provided

    Args:
        students (list of dict): dict should contain keys "studentNumber" and "email"

    Returns:
        list of dict: original dict with added "username" key
    """

    # Create OR query to search for all the provided students
    query = "(|"

    for student in students:
        query += f"(&(ugentStudentID={student['studentNumber']})(mail={student['email']}))"

    query += ")"

    # 500 is the default page size for UGent LDAP
    entries = conn.extend.standard.paged_search(
        "ou=people,dc=UGent,dc=be",
        query,
        attributes=["uid", "mail", "ugentStudentID"],
        paged_size=500,
    )

    students_with_username = []

    # Paged search: https://ldap3.readthedocs.io/en/latest/searches.html#simple-paged-search, https://ldap3.readthedocs.io/en/latest/tutorial_searches.html#simple-paged-search
    for entry in entries:
        attributes = entry["attributes"]
        students_with_username.append(
            {
                "studentNumber": attributes["ugentStudentID"][0],
                "email": attributes["mail"][0],
                "username": attributes["uid"][0],
            }
        )

    return students_with_username


def process_csv(filename):
    """Processes the CSV located at uploads/{filename}

    Args:
        filename (str): filename of the uploaded CSV

    Returns:
        str: filename of the converted CSV in the outputs directory
    """

    converted_students = None

    with open(os.path.join("uploads", filename)) as csvfile:
        csv_reader = csv.DictReader(csvfile)

        student_input_dicts = []

        for row in csv_reader:
            student_input_dicts.append(
                {
                    "studentNumber": row["OrgDefinedId"].replace("#", ""),
                    "email": row["Email"],
                }
            )

        converted_students = ldap_convert(student_input_dicts)

    output_filename = f"converted_{filename}"

    with open(os.path.join("uploads", filename)) as original_csv, open(os.path.join("outputs", output_filename), "w") as converted_csv:
        original_csv_reader = csv.DictReader(original_csv)
        converted_csv_writer = csv.DictWriter(converted_csv, fieldnames=original_csv_reader.fieldnames)

        converted_csv_writer.writeheader()

        for row in original_csv_reader:
            student_username = next(student for student in converted_students if student["email"] == row["Email"])["username"]

            row["Username"] = f"#{student_username}"
            converted_csv_writer.writerow(row)

    return output_filename
