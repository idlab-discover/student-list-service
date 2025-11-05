# Student List Service

Simple web server to convert exported Ufora (D2L Brightspace) student list containing Azure Entra ID usernames to a student list with UGent GitHub usernames.


![Preview](docs/img/preview.png)


## Usage

### Hosted

A hosted version of the service is available at http://ghtt.ugent.be/. Accessible inside the UGent Network (either directly or through VPN).

Please use the "Contact us" button on the bottom of the page if you encounter any issues.

### Local

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

