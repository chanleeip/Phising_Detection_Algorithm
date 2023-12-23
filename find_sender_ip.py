import os
import re
from email import policy
from email.parser import BytesParser

def read_files_and_find_sender_ip(directory_path):
    if not os.path.isdir(directory_path):
        print(f"The provided path '{directory_path}' is not a directory.")
        return


    # Loop through files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        # print(file_path)


        # Read the content of the file
        with open(file_path, 'rb') as file:
            file_content = BytesParser(policy=policy.default).parse(file)
            a=file_content.get('Authentication-Results', '')
            b=re.findall(r'\((.*?)\)',a)
            c=(re.findall(r'[0-9.]+',b[0]))
            print(c[0])
            
    

# Example usage
directory_path = '/Users/admin/Downloads/Phishing_Email _Samples'

read_files_and_find_sender_ip(directory_path)
