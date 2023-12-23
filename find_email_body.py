import email
from email import policy
from email.parser import BytesParser

def extract_body_from_eml(file_path):
    with open(file_path, 'rb') as eml_file:
        # Parse the .eml file
        msg = BytesParser(policy=policy.default).parse(eml_file)

        # Get the plain text body part
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                return (part.get_payload())
        
# extract_body_from_eml("/Users/admin/Downloads/Phishing_Email _Samples/sample-13.eml")