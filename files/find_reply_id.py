import os
import re
import email
from email import policy
from email.parser import BytesParser

def read_files_and_find_reply_id(eml_file_path):
    if not os.path.exists(eml_file_path):
        print(f"Tfile not exist")
        return

    with open(eml_file_path, 'rb') as file:
        file_content = BytesParser(policy=policy.default).parse(file)
        a=file_content.get('Reply-To', '')
        return(a)

    

# Example usage
# file_path = '/Users/admin/Downloads/Phishing_Email _Samples/sample-13.eml'

# read_files_and_find_reply_id(file_path)
