# Phishing Detection Algorithm

This Python script is designed to detect phishing attempts in emails. It uses various checks and scores to determine the likelihood of an email being a phishing attempt.

## How it works

The script performs the following checks:

1. **Sender's Email Address**: The script checks if the email address is valid, free, disposable, a role email, a catchall email, SMTP valid, deliverable, and its quality score. Each check contributes to the overall score.

2. **Links in Email**: The script checks the risk score of all URLs found in the email. The risk score contributes to the overall score.

3. **SPF Record Check**: The script checks the SPF record of the email. If the SPF record passes, the overall score is increased.

4. **DKIM Check**: The script checks the DKIM of the email. If the DKIM check passes, the overall score is increased.

5. **DMARC Check**: The script checks the DMARC of the email. If the DMARC check passes, the overall score is increased.

6. **Content Analysis**: The script checks the content of the email for phishing keywords. If any are found, the email is marked as not safe.

7. **Unusual Message Behaviour**: The script checks the sending time of the email. If the email was sent at an unusual time, it is marked as phishy.

8. **Reply-To Field**: The script checks the Reply-To field of the email. If the Reply-To ID does not match the Sender ID, the email is marked as phishy.

9. **IP Reputation of the Sender**: The script checks the reputation of the sender's IP address. The reputation score contributes to the overall score.

10. **IP Reputation of the SMTPS IP**: The script checks the reputation of the SMTPS IP. The reputation score contributes to the overall score.

## Score Range and Interpretation

- 0-20: High Risk
    - Strongly indicates phishing. Avoid interaction and report immediately.
- 21-40: Moderate Risk
    - Multiple worrisome signs. Validate the email's authenticity and be cautious with interactions
- 41-70: Low Risk
    - Some questionable elements detected. Proceed with caution
- 71-100: Highly Safe
    - Appears trustworthy with proper authentication and no suspicious content.

## Requirements

The script requires the following Python packages:

- `requests`
- `json`
- `os`
- `math`
- `urllib.parse`

## Setup 

This project uses Poetry for dependency management. Follow these steps to set up the project:

1. Install Poetry (if not already installed):
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

2. Clone the repository:
    ```bash
    git clone https://github.com/chanleeip/Phishing_Detection_Algorithm.git
    cd Phishing_Detection_Algorithm
    ```

3. Install dependencies using Poetry:
    ```bash
    poetry install
    ```

4. Create a `.env` file in the project root and add the following API keys:
    ```env
    EMAIL_VALIDATION="your-email-validation-api-key"
    URL_VALIDATION="your-url-validation-api-key"
    IP_VALIDATION="your-ip-validation-api-key"
    ```

    *Get your API keys from the following URLs:*
    - [Email Validation API-www.abstractapi.com](https://www.abstractapi.com/api/email-verification-validation-api)
    - [URL Validation API-www.ipqualityscore.com](https://www.ipqualityscore.com)
    - [IP Validation API-www.abuseipdb.com](https://abuseipdb.com)

## Usage

To use the script, run it with Poetry:
```bash
poetry run python3 cli.py
```

## Setup and Usage with Docker

This project uses Poetry for dependency management and Docker for containerization. Follow these steps to set up and run the project:

1. Install Docker (if not already installed).

2. Clone the repository:
    ```bash
    git clone https://github.com/chanleeip/Phishing_Detection_Algorithm.git
    cd Phishing_Detection_Algorithm
    ```
3. Create a `.env` file in the project root and add the following API keys:
    ```env
    EMAIL_VALIDATION="your-email-validation-api-key"
    URL_VALIDATION="your-url-validation-api-key"
    IP_VALIDATION="your-ip-validation-api-key"
    ```

    *Get your API keys from the following URLs:*
    - [Email Validation API-www.abstractapi.com](https://www.abstractapi.com/api/email-verification-validation-api)
    - [URL Validation API-www.ipqualityscore.com](https://www.ipqualityscore.com)
    - [IP Validation API-www.abuseipdb.com](https://abuseipdb.com)


4. Build the Docker image (replace `<name>` with your desired image name):
    The .env file should be present in the root folder
    ```bash
    docker build -t <name> --build-arg ENV_FILE=.env -f Dockerfile .
    ```

5. Run the Docker container (replace `<container_name>` and `<name>` with your desired container and image names):
    ```bash
    docker run -it -v "$(pwd):/host" --name <container_name> <name> bash
    ```

6. Inside the container, activate the virtual environment:
    ```bash
    source .venv/bin/activate
    ```

7. Run the script using Poetry:
    ```bash
    poetry run python3 cli.py --path /host/<path_of_files>
    ```

## Note

This script is a basic implementation and may not catch all phishing attempts. Always be vigilant when opening emails and never click on links or attachments from unknown senders.


