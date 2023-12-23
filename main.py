import find_from_email
import os
import requests
import json
# all_files
directory_path = '/Users/admin/Downloads/Phishing_Email _Samples'
files_dict={}
for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        files_dict[filename]=' '




res = requests.get("https://emailvalidation.abstractapi.com/v1/?api_key=d125e6f49c764b6abc44caf939c95b6f&email=rpewu@cfyy43yo35.com")
response=json.loads(res.content)
scores = {
   "is_valid_format": 2 if response["is_valid_format"]["value"] else -2,
    "is_free_email": 2 if response["is_free_email"]["value"] else 0,
    "is_disposable_email": -2 if response["is_disposable_email"]["value"] else 2,
    "is_role_email": 2 if response["is_role_email"]["value"] else -2,
    "is_catchall_email": -2 if response["is_catchall_email"]["value"] else 2,
    # "is_mx_found": 2 if response["is_mx_found"]["value"] else -2,
    "is_smtp_valid": 2 if response["is_smtp_valid"]["value"] else -2,
    "deliverability": 2 if response["deliverability"]== "DELIVERABLE" else -2,
    "quality_score": float(response.get("quality_score")) * 10 # Convert quality_score to a score out of 10
}
# print(response["is_valid_format"]["value"] and
#         response["is_free_email"]["value"] and
#         not response["is_disposable_email"]["value"] and
#         not response["is_role_email"]["value"] and
#         not response["is_catchall_email"]["value"] and
#         response["is_mx_found"]["value"] and
#         response["is_smtp_valid"]["value"] and
#         response["deliverability"] == "DELIVERABLE" and
#         float(response["quality_score"]) >= 0.8)

overall_score = sum(scores[key] for key in scores.keys())
print(overall_score)
# print("helo world\n")
# res=json.loads(response.content)
# print(res['autocorrect'])
