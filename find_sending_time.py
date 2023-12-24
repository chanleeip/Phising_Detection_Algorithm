import email
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
def extract_sending_time(file_path):
    with open(file_path, 'rb') as eml_file:
        msg = BytesParser(policy=policy.default).parse(eml_file)
        date_header = msg.get('Date')
        datetime_obj = parsedate_to_datetime(date_header)

        if datetime_obj:
            return datetime_obj

# # Example usage
# eml_file_path = '/Users/admin/Downloads/Phishing_Email _Samples/sample-001.eml'
# sending_time = extract_sending_time(eml_file_path)

# print("Sending Time:", sending_time)
