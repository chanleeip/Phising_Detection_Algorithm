import email
from email import policy
from email.parser import BytesParser

def extract_body_from_eml(file_path):
    with open(file_path, 'rb') as eml_file:
        # Parse the .eml file
        msg = BytesParser(policy=policy.default).parse(eml_file)

        if msg.is_multipart():
            for part in msg.iter_parts():
                if part.get_content_type() == 'text/plain':
                    return part.get_payload(decode=True).decode('utf-8', errors='ignore')
                elif part.get_content_type() == 'text/html':
                    return part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
        # If the email is not multipart, directly extract the body
            return msg.get_payload(decode=True).decode('utf-8', errors='ignore')
    
# print(extract_body_from_eml("/Users/admin/Downloads/Phishing_Email _Samples/sample-2070.eml"))