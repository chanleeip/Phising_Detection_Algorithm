import os
from email import policy
from email.parser import BytesParser

def read_files_and_find_spf_record(eml_file_path):
    if not os.path.exists(eml_file_path):
        print(f"file not exists")
        return

    with open(eml_file_path, 'rb') as file:
        file_content = BytesParser(policy=policy.default).parse(file)
        a=file_content.get('Received-SPF', '')
        b=a.split()
        # print(b[0])
        return(b[0])
    
            
    

# Example usage
file_path = '/Users/admin/Downloads/Phishing_Email _Samples/sample-001.eml'

# read_files_and_find_spf_record(file_path)
