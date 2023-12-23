import os
from email import policy
from email.parser import BytesParser

def read_files_and_find_spf_record(directory_path):
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
            a=file_content.get('Received-SPF', '')
            b=a.split()
            print(b[0])
            
    

# Example usage
directory_path = '/Users/admin/Downloads/Phishing_Email _Samples'
regex_pattern = r'From:'  # Example regex for a social security number

read_files_and_find_spf_record(directory_path)
