import find_links
import os
import requests
import json
import find_spf
import math
import find_dkim_check
import find_dkim_dmarc
from urllib.parse import quote_plus
from phisingwords import keywords
import find_sending_time
import find_email_body
import find_reply_id
import find_from_email
import find_sender_ip
import find_smpts_sender_domain
import os
# all_files


given_path = '/Users/admin/Downloads/Phishing_Email _Samples/sample-13.eml'
files_dict={}
files_path={}
if os.path.isdir(given_path):
        for filename in os.listdir(given_path):
                file_path = os.path.join(given_path, filename)
                files_dict[filename]=' '
                files_path[file_path]=" "
elif os.path.isfile(given_path):
        files_dict[os.path.basename(given_path)]=" "
        files_path[given_path]=" "
else:
        print("Error")



#Senders Email Address - (20 points)
        #Higher is Better
for i in files_path.keys():
        print(i)
        email_id=find_from_email.read_files_and_find_from_email("/Users/admin/Downloads/Phishing_Email _Samples/sample-2222.eml")
        res = requests.get(f"https://emailvalidation.abstractapi.com/v1/?api_key={os.environ.get('EMAIL_VALIDATION')}&email={email_id}")
        response=json.loads(res.content)
        print(f"https://emailvalidation.abstractapi.com/v1/?api_key={os.environ.get('EMAIL_VALIDATION')}&email={email_id}")
        scores = {
        "is_valid_format": 2 if response["is_valid_format"]["value"] else -2,
        "is_free_email": 2 if response["is_free_email"]["value"] else 0,
        "is_disposable_email": -2 if response["is_disposable_email"]["value"] else 2,
        "is_role_email": 2 if response["is_role_email"]["value"] else -2,
        "is_catchall_email": -2 if response["is_catchall_email"]["value"] else 2,
        "is_smtp_valid": 2 if response["is_smtp_valid"]["value"] else -2,
        "deliverability": 2 if response["deliverability"]== "DELIVERABLE" else -2,
        "quality_score": float(response.get("quality_score")) * 10 
        }

        overall_score = sum(scores[key] for key in scores.keys())
        print(overall_score)
        files_dict[os.path.basename(i)]=overall_score

# Links in Email - (25 points)
#         Higher is better

        urls=find_links.read_file_and_find_links(i)
        print(urls)
        encoded_url1=quote_plus(urls)
        res=requests.get(f"https://www.ipqualityscore.com/api/json/url/{os.environ.get('URL_VALIDATION')}/{encoded_url1}")
        response=(json.loads(res.content))
        print(response)
        scores = {
        #    "success": 2 if response["success"] else -4,
        #     "unsafe": -4 if response["unsafe"]else 2,
        #     "dns_valid": 1 if response["dns_valid"]else -2,
        #     "parking": 0 if response["parking"]else -2,
        #     "spamming": -4 if response["spamming"]else 2,
        #     "malware": -4 if response["malware"] else 2,
        #     "phishing": -4 if response["phishing"] else 2,
        #     "suspicious": -4 if response["suspicious"] else 2,
                "risk_score":float(25-(response["risk_score"]/4))
        }
        overall_score = sum(scores[key] for key in scores.keys())
        files_dict[os.path.basename(i)]=overall_score


# #SPF Record Check (15 points)
#         #Higher is Better
        status=find_spf.read_files_and_find_spf_record(i)
        if status=="Pass":
                overall_score=15
        else:
                overall_score=0

        files_dict[os.path.basename(i)]=overall_score
#DKIM CHECK (15 points)
        #Higher is Better
        status=find_dkim_check.read_file_and_find_dkim_check(i)
        if status=="Pass":
                overall_score=15
        else:
                overall_score=0

        files_dict[os.path.basename(i)]=overall_score
        
#DMARC CHECK (10 points)
        #HIgher is Better
        status=find_dkim_dmarc.read_files_and_find_dkim_check(i)
        if status=="Pass":
                overall_score=10
        else:
                overall_score=0

        files_dict[os.path.basename(i)]=overall_score
        
#Content Analysis (25 points)
        #Higher is Better
        content=find_email_body.extract_body_from_eml(i)
        found_keywords = [keyword for keyword in keywords["phishing_keywords"] if keyword in content]

        if found_keywords:
                overall_score=10
        else:
                overall_score=0
        files_dict[os.path.basename(i)]=overall_score


#Unsual message behaviour (15 points)
        time=find_sending_time.extract_sending_time(i)
        hour = time.hour
        if 22 < hour or (0 <= hour < 8):
                print("Phishy Time Detected:")
                overall_score=10
        else:
                print("Safe Time:")
                overall_score=0
        files_dict[os.path.basename(i)]=overall_score

        

#Reply to Field (10 points)
        reply_id=find_reply_id.read_files_and_find_reply_id(i)
        sender_id=find_from_email.read_files_and_find_from_email(i)
        if reply_id == sender_id:
                print("not phisy")
                overall_score=10
        else:
                print("phisy")
                overall_score=0
        files_dict[os.path.basename(i)]=overall_score
        
# #IP reputation of the sender-ipadress (10 points)
        
        sender_ip=find_sender_ip.read_files_and_find_sender_ip(i)
        print(sender_ip)
        url = 'https://api.abuseipdb.com/api/v2/check'

        querystring = {
            'ipAddress': sender_ip,
            'maxAgeInDays': '120'
        }

        headers = {
            'Accept': 'application/json',
            'Key': os.environ.get("IP_VALIDATION")
        }
        res=requests.request(method='GET', url=url, headers=headers, params=querystring)
        respone=(json.loads(res.text))
        score=(10-(respone["abuseConfidenceScore"]/10))
        files_dict[os.path.basename(i)]=score

#IP reputation of the sender-impts-ip (10 points)
        
        sender_smtps__ip=find_smpts_sender_domain.read_files_and_find_smpts_server_domain(i)
        url1=sender_smtps__ip.strip(';')
        print(url1)
        encoded_url1=quote_plus(url1)
        res=requests.get(f"https://www.ipqualityscore.com/api/json/url/{os.environ.get('URL_VALIDATION')}/{encoded_url1}")
        response=(json.loads(res.content))
        scores = {
        #    "success": 2 if response["success"] else -4,
        #     "unsafe": -4 if response["unsafe"]else 2,
        #     "dns_valid": 1 if response["dns_valid"]else -2,
        #     "parking": 0 if response["parking"]else -2,
        #     "spamming": -4 if response["spamming"]else 2,
        #     "malware": -4 if response["malware"] else 2,
        #     "phishing": -4 if response["phishing"] else 2,
        #     "suspicious": -4 if response["suspicious"] else 2,
                "risk_score":float(25-(response["risk_score"]/4))
        }
        overall_score = sum(scores[key] for key in scores.keys())
        files_dict[os.path.basename(i)]=overall_score