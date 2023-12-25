import os
import re
from email import policy
from email.parser import BytesParser

def read_files_and_find_sender_ip(eml_file_path):
    if not os.path.exists(eml_file_path):
        print(f"file not exists")
        return


# Loop through files in the directory

    with open(eml_file_path, 'rb') as file:
        file_content = BytesParser(policy=policy.default).parse(file)
        a=file_content.get('Authentication-Results', '')
        b=re.findall(r'\((.*?)\)',a)
        c=(re.findall(r'[0-9.]+',b[0]))
        return(c[0])
            
    

# Example usage
# file_path = '/Users/admin/Downloads/Phishing_Email _Samples/sample-995.eml'

# print(read_files_and_find_sender_ip(file_path))
