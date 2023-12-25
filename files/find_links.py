import os
from email import policy,message_from_string
from email.parser import BytesParser
from bs4 import BeautifulSoup
import re
from html import unescape
from quopri import decodestring

def read_file_and_find_links(eml_file_path):
    if not os.path.exists(eml_file_path):
        print(f"file doesnt exist")
        return

    with open(eml_file_path, 'r') as file:
        content = file.read()
        html_match = re.search(r'<html\b[^>]*>.*?<\/html>',content,re.DOTALL | re.IGNORECASE)
        # print(html_match)
        if html_match is not None:
            extracted_html = html_match.group(0)
            soup = BeautifulSoup(extracted_html, 'html.parser')
            href_tags = soup.find_all('a', href=True)
            # print(href_tags)
            href_values = [tag.get('href') for tag in href_tags]
            # print(type(href_values))
            return href_values
     
        
    with open(eml_file_path, 'rb') as file:
            file_content = BytesParser(policy=policy.default).parse(file)
            for part in file_content.iter_parts():
                if part.get_content_type() == 'text/html':
                    html_content = part.get_content()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    for a_tag in soup.find_all('a'):
                        href_attribute = [a_tag.get('href')]
                        # print(type(href_attribute[0]))
                        return(href_attribute)
                    break  
            
    with open(eml_file_path,'r')as file:
        a_tags_match = re.findall(r'<a[^>]*\s*href\s*=\s*["\'](.*?)["\']', content, re.DOTALL | re.IGNORECASE)
        # print(type(a_tags_match[0]))
        return [a_tags_match]
        # else:
        #     extracted_html = html_match.group(0)
        #     soup = BeautifulSoup(extracted_html, 'html.parser')
        #     href_tags = soup.find_all('a', href=True)
        #     href_values = [tag.get('href') for tag in href_tags]
        #     return href_values  

        # print(content)
        # file_content = BytesParser(policy=policy.default).parse(file)
        # href_values = [re.search(r'href="(.*?)"', str(tag)).group(0) for tag in href_tags]
        # print(href_values)
        # print(extracted_html)
        # file_content = message_from_string(extracted_html, policy=policy.default)
        # print(file_content)
        # print(file_content.get_content_type())
        # href_values = re.findall(r'<a[^>]*\s+href=["\'](.*?)["\'][^>]*>', extracted_html, re.IGNORECASE)
        # print(href_values)
        # print(file_content)
        # for part in file_content.iter_parts():
        #     print(part)
        #     if part.get_content_type() == 'html':
        #         html_content = part.get_content()
        #         soup = BeautifulSoup(html_content, 'html.parser')
        #         for a_tag in soup.find_all('a'):
        #             href_attribute = a_tag.get('href')
        #             print(href_attribute)
        #             return(href_attribute)
                   
        #         break  
        # else:
        #     print("none")
        #     return("No HTML part found in the email body.")

            
    


file_path = '/Users/admin/Downloads/Phishing_Email _Samples/sample-998.eml'

# print(read_file_and_find_links(file_path))