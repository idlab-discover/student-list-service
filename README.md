# Student List Service

Simple web server to convert exported Ufora (D2L Brightspace) student list containing Azure Entra ID usernames to a student list with UGent GitHub usernames.


![Preview](docs/img/preview.png)


## Usage

We recommend to use a Python virtual environment.


1. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Update the `.env` file with the provided credentials.

3. Start the app:

    ```bash
    flask run
    ```

4. The app should now be accessible at http://localhost:5000/

