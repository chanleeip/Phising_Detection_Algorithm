import os
import re
from email import policy
from email.parser import BytesParser

def read_files_and_find_dkim_check(eml_file_path):
    if not os.path.exists(eml_file_path):
        print(f"file not exist")
        return


    with open(eml_file_path, 'rb') as file:
        file_content = BytesParser(policy=policy.default).parse(file)
        a=file_content.get('Authentication-Results', '')
        b=re.findall(r'dmarc=([^\s)]+)',a)
        return(b[0])
            
    

# Example usage
file_path = '/Users/admin/Downloads/Phishing_Email _Samples/sample-13.eml'

# read_files_and_find_dkim_check(file_path)
