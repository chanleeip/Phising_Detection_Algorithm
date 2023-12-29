from files import find_links
import os
import requests
import json
from files import find_spf
from files import find_dkim_check
from files import find_dkim_dmarc
from urllib.parse import quote_plus
from files.phisingwords import keywords
from files import find_sending_time
from files import find_email_body
from files import find_reply_id
from files import find_from_email
from files import find_sender_ip
from files import find_smpts_sender_domain
import os
from tqdm import tqdm


def run_script(path_given):
                
        given_path = path_given
        files_dict={}
        files_path={}
        if os.path.isdir(given_path):
                for filename in os.listdir(given_path):
                        file_path = os.path.join(given_path, filename)
                        files_dict[filename] = {"details": {"sender_id": {}, "links_present": [],"IP_adress_details":{},"IMTPS_IP_adress_details":{}}, "score": {}}
                        files_path[file_path]=" "
        elif os.path.isfile(given_path):
                files_dict[os.path.basename(given_path)]=" "
                files_path[given_path]=" "
                files_dict = {os.path.basename(given_path): {"details": {"sender_id": {}, "links_present": []}, "score": {}} }
        else:
                print("Error")

        # print(files_path)

        ''' Senders Email Address - (20 points)
                        Higher is Better'''
        # print(files_dict)
        for i in files_path.keys():
                tqdm.write("Processing Email Adress")
                # print(i)
                email_id=find_from_email.read_files_and_find_from_email(i)
                if email_id:
                        res = requests.get(f"https://emailvalidation.abstractapi.com/v1/?api_key={os.environ.get('EMAIL_VALIDATION')}&email={email_id}")
                        response=json.loads(res.content)
                        # print(response)
                        # print(f"https://emailvalidation.abstractapi.com/v1/?api_key={os.environ.get('EMAIL_VALIDATION')}&email={email_id}")
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

                        if response["is_valid_format"]["value"]:
                                files_dict[os.path.basename(i)]["details"]["sender_id"]["Valid_format"] = "Yes"
                        else:
                                files_dict[os.path.basename(i)]["details"]["sender_id"]["Valid_format"] = "No"
                        if response["is_free_email"]["value"]:
                                files_dict[os.path.basename(i)]["details"]["sender_id"]["Free-Email"] = "Yes"
                        else:
                                files_dict[os.path.basename(i)]["details"]["sender_id"]["Free-Email"] = "No"
                        if response["is_disposable_email"]["value"] :
                                files_dict[os.path.basename(i)]["details"]["sender_id"]["Is-Disposable-Email"] = "Yes"
                        else:
                                files_dict[os.path.basename(i)]["details"]["sender_id"]["Is-Disposable-Email"] = "No"
                        if response["is_role_email"]["value"]:
                                files_dict[os.path.basename(i)]["details"]["sender_id"]["Is-Role-Email"] = "Yes"
                        else:
                                files_dict[os.path.basename(i)]["details"]["sender_id"]["Is-Role-Email"] = "No"
                        if response["is_catchall_email"]["value"] :
                                files_dict[os.path.basename(i)]["details"]["sender_id"]["Is-Catchall-Email"] = "Yes"
                        else:
                                files_dict[os.path.basename(i)]["details"]["sender_id"]["Is-Catchall-Email"] = "No"
                        if  response["is_smtp_valid"]["value"]:
                                files_dict[os.path.basename(i)]["details"]["sender_id"]["SMTP-Valid"] = "Yes"
                        else:
                                files_dict[os.path.basename(i)]["details"]["sender_id"]["SMTP-Valid"] = "No"
                        if  response["deliverability"]== "DELIVERABLE":
                                files_dict[os.path.basename(i)]["details"]["sender_id"]["Deliverable"] = "Yes"
                        else:
                                files_dict[os.path.basename(i)]["details"]["sender_id"]["Deliverable"] = "No"


                        overall_score = sum(scores[key] for key in scores.keys())
                        files_dict[os.path.basename(i)]["score"]=int(overall_score)
                else:
                        print("email not found")
                        files_dict[os.path.basename(i)]["score"]=int(0)
                tqdm.write("10% Completed")   

                '''Links in Email - (25 points) 
                        Higher is better'''

                tqdm.write("Processing Links present in Email")

                urls=find_links.read_file_and_find_links(i)
                # print(urls)
                index=0
                for op,j in enumerate(urls):
                        # print(j)
                        # files_dict[os.path.basename(i)]["details"]["links_present"].append(j)
                        encoded_url1=quote_plus(j)
                        # print(len(urls))
                        res=requests.get(f"https://www.ipqualityscore.com/api/json/url/{os.environ.get('URL_VALIDATION')}/{encoded_url1}")
                        response=(json.loads(res.content))
                        # print(response)
                        if(response.get("success",True)):
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

                                if response["success"]:
                                        link_details={"URL":j,"Success":"Yes"}
                                        files_dict[os.path.basename(i)]["details"]["links_present"].append(link_details)
                                else:
                                        link_details={"URL":j,"Success":"No"}
                                        files_dict[os.path.basename(i)]["details"]["links_present"].append(link_details)
                                if response["unsafe"]:
                                        files_dict[os.path.basename(i)]["details"]["links_present"][index]["Unsafe"]= "Yes"
                                else:
                                        files_dict[os.path.basename(i)]["details"]["links_present"][index]["Unsafe"]= "No"
                                if response["dns_valid"] :
                                        files_dict[os.path.basename(i)]["details"]["links_present"][index]["DNS_valid"]= "Yes"
                                else:
                                        files_dict[os.path.basename(i)]["details"]["links_present"][index]["DNS_valid"]= "No"
                                if response["parking"]:
                                        files_dict[os.path.basename(i)]["details"]["links_present"][index]["Parking"] = "Yes"
                                else:
                                        files_dict[os.path.basename(i)]["details"]["links_present"][index]["Parking"] = "No"
                                if response["spamming"]:
                                        files_dict[os.path.basename(i)]["details"]["links_present"][index]["Spam"]= "Yes"
                                else:
                                        files_dict[os.path.basename(i)]["details"]["links_present"][index]["Spam"] = "No"
                                if  response["malware"]:
                                        files_dict[os.path.basename(i)]["details"]["links_present"][index]["Malware"] = "Yes"
                                else:
                                        files_dict[os.path.basename(i)]["details"]["links_present"][index]["Malware"] = "No"
                                if  response["phishing"]:
                                        files_dict[os.path.basename(i)]["details"]["links_present"][index]["Phishing"] = "Yes"
                                else:
                                        files_dict[os.path.basename(i)]["details"]["links_present"][index]["Phishing"] = "No"
                                if  response["suspicious"]:
                                        files_dict[os.path.basename(i)]["details"]["links_present"][index]["Suspicious"] = "Yes"
                                else:
                                        files_dict[os.path.basename(i)]["details"]["links_present"][index]["Suspicious"] = "No"
                                files_dict[os.path.basename(i)]["details"]["links_present"][index]["Risk_Score"] = response["risk_score"]

                                # print(files_dict)
                                overall_score = sum(scores[key] for key in scores.keys())
                                # files_dict[os.path.basename(i)]["score"]=10
                                files_dict[os.path.basename(i)]["score"]=int(files_dict[os.path.basename(i)]["score"])+int(overall_score)
                                index+=1

                        tqdm.write("20% Completed") 
        # print(files_dict)
                
                '''SPF Record Check (15 points)
                        Higher is Better'''
                tqdm.write("Checking SPF Record Check")
                status=find_spf.read_files_and_find_spf_record(i)
                if status=="pass":
                        overall_score=10
                        files_dict[os.path.basename(i)]["details"]["SPF_Record_Check"] = "Pass"
                else:
                        overall_score=-10
                        files_dict[os.path.basename(i)]["details"]["SPF_Record_Check"]= "Fail/Error"

                # files_dict[os.path.basename(i)]["score"]=15
                files_dict[os.path.basename(i)]["score"]=int(files_dict[os.path.basename(i)]["score"])+int(overall_score)
                tqdm.write("30% Completed") 

                '''DKIM CHECK (15 points)
                        #Higher is Better'''
                tqdm.write("Checking DKIM Record ")
                status=find_dkim_check.read_file_and_find_dkim_check(i)
                if status=="pass":
                        overall_score=15
                        files_dict[os.path.basename(i)]["details"]["DKIM_check"] = "Pass"
                else:
                        overall_score-15
                        files_dict[os.path.basename(i)]["details"]["DKIM_check"] = "Fail/Error"

                files_dict[os.path.basename(i)]["score"]=int(files_dict[os.path.basename(i)]["score"])+int(overall_score)
                tqdm.write("40% Completed") 
                
                '''DMARC CHECK (10 points)
                        HIgher is Better'''
                tqdm.write("Checking DMARC Record ")
                status=find_dkim_dmarc.read_files_and_find_dkim_check(i)
                if status=="pass":
                        overall_score=10
                        files_dict[os.path.basename(i)]["details"]["DMARC_check"] = "Pass"
                else:
                        overall_score=-10
                        files_dict[os.path.basename(i)]["details"]["DMARC_check"] = "Fail/Error"

                files_dict[os.path.basename(i)]["score"]=int(files_dict[os.path.basename(i)]["score"])+int(overall_score)
                tqdm.write("50% Completed") 
                
                '''Content Analysis (25 points)
                        #Higher is Better'''
                tqdm.write("Checking Content of the Email for any Phishing/Scam Keywords")
                content=find_email_body.extract_body_from_eml(i)
                # print(content)
                found_keywords = [keyword for keyword in keywords["phishing_keywords"] if keyword in content]

                if found_keywords:
                        overall_score=-10
                        files_dict[os.path.basename(i)]["details"]["Any_Phishing_Keyword_Found"] = "Yes"
                else:
                        overall_score=25
                        files_dict[os.path.basename(i)]["details"]["Any_Phishing_Keyword_Found"] = "No"
                files_dict[os.path.basename(i)]["score"]=int(files_dict[os.path.basename(i)]["score"])+int(overall_score)
                tqdm.write("70% Completed") 


                '''Unsual message behaviour (15 points)'''
                tqdm.write("Checking whether the Email was sent in unusual time")
                time=find_sending_time.extract_sending_time(i)
                hour = time.hour
                if 22 < hour or (0 <= hour < 8):
                        print("Phishy Time Detected:")
                        overall_score=-10
                        files_dict[os.path.basename(i)]["details"]["Sending_Time"] = "Unusual"
                else:
                        print("Safe Time:")
                        overall_score=15
                        files_dict[os.path.basename(i)]["details"]["Sending_Time"] = "Normal"
                files_dict[os.path.basename(i)]["score"]=int(files_dict[os.path.basename(i)]["score"])+int(overall_score)
                tqdm.write("80% Completed") 

                

                '''Reply to Field (10 points)'''
                tqdm.write("Checking whether the replyt-to email-id and sender emai-id is same")
                reply_id=find_reply_id.read_files_and_find_reply_id(i)
                sender_id=find_from_email.read_files_and_find_from_email(i)
                if reply_id == sender_id:
                        print("not phisy")
                        overall_score=10
                        files_dict[os.path.basename(i)]["details"]["Mismatch_btw_reply-to_and_sender"] = "Yes"
                else:
                        print("phisy")
                        overall_score=-10
                        files_dict[os.path.basename(i)]["details"]["Mismatch_btw_reply-to_and_sender"] = "No"
                files_dict[os.path.basename(i)]["score"]=int(files_dict[os.path.basename(i)]["score"])+int(overall_score)
                tqdm.write("85% Completed") 
                
                '''IP reputation of the sender-ipadress (10 points)'''
                tqdm.write("Checking Reputation of the Sender-IP adress")
                sender_ip=find_sender_ip.read_files_and_find_sender_ip(i)
                # print(sender_ip)
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
                # print(respone)
                if "data" in respone:
                        ipAdress={"ip-adress":respone["data"]["ipAddress"],
                                "isPublic":respone["data"]["isPublic"],
                                "Is_It_Whitelisted":respone["data"]["isWhitelisted"],
                                "Risk_Score":respone["data"]["abuseConfidenceScore"],
                                "Usage_Type":respone["data"]["usageType"],
                                "Domain_name":respone["data"]["domain"],
                                "Is_it_Tor":respone["data"]["isTor"],
                                "Total_Reports_previous":respone["data"]["totalReports"],
                                "Last_report_date":respone["data"]["lastReportedAt"]
                                }
                        files_dict[os.path.basename(i)]["details"]["IP_adress_details"] = ipAdress
                        score=(10-(respone["data"]["abuseConfidenceScore"]/10))
                        # files_dict[os.path.basename(i)]["score"]=10
                        files_dict[os.path.basename(i)]["score"]=int(files_dict[os.path.basename(i)]["score"])+int(score)
                else:
                        ipAdress={"ip-adress":"not found"}
                        files_dict[os.path.basename(i)]["details"]["IP_adress_details"] = ipAdress
                        score=-10
                        files_dict[os.path.basename(i)]["score"]=int(files_dict[os.path.basename(i)]["score"])+int(score) 

                '''IP reputation of the sender-impts-ip (10 points) '''
                tqdm.write("Checking Reputation of Sender IMPTS-IP")
                sender_smtps__ip=find_smpts_sender_domain.read_files_and_find_smpts_server_domain(i)
                url1=sender_smtps__ip.strip(';')
                # print(url1)
                encoded_url1=quote_plus(url1)
                res=requests.get(f"https://www.ipqualityscore.com/api/json/url/{os.environ.get('URL_VALIDATION')}/{encoded_url1}")
                response=(json.loads(res.content))
                # print(response)
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

                ipAdress={"Safe":"Yes" if response["unsafe"] else "No",
                        "Domain_name":response["domain"],
                        # "IP_address":response["ip_address"],
                        "server_name":response["server"],
                        "dns_valid":"Yes" if response["dns_valid"]else "No",
                        "Domain_name":response["domain"],
                        "spamming":response["spamming"],
                        "malware":response["malware"],
                        "phishing":response["phishing"],
                        "suspicious":response["suspicious"],
                        "malicious_score":response["risk_score"]
                        }
                files_dict[os.path.basename(i)]["details"]["IMTPS_IP_adress_details"] = ipAdress
                overall_score = sum(scores[key] for key in scores.keys())
                files_dict[os.path.basename(i)]["score"]=int(files_dict[os.path.basename(i)]["score"])+int(overall_score)
                tqdm.write("100% Completed") 
        return (json.dumps(files_dict,indent=2), files_dict[os.path.basename(i)]["score"])

