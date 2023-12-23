import os
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup

def read_files_and_find_links(eml_file_path):
    if not os.path.exists(eml_file_path):
        print(f"file doesnt exist")
        return

    with open(eml_file_path, 'rb') as file:
        file_content = BytesParser(policy=policy.default).parse(file)
        for part in file_content.iter_parts():
            if part.get_content_type() == 'text/html':
                html_content = part.get_content()
                soup = BeautifulSoup(html_content, 'html.parser')
                for a_tag in soup.find_all('a'):
                    href_attribute = a_tag.get('href')
                    print(f"Found link: {href_attribute}")
                break  
        else:
            print("No HTML part found in the email body.")

            
    


file_path = '/Users/admin/Downloads/Phishing_Email _Samples/sample-13.eml'

read_files_and_find_links(file_path)