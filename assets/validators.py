"""
form data validation tools.
By : Mahmoud Elshobaky (mahmoud.elshobaky@gmail.com).
"""

import re

# validate phone number
PHONE_RE = re.compile(r"\d")
def valid_phone(phone):
    return phone and PHONE_RE.match(phone)

# validate name
#NAME_RE = re.compile(r'^[^\W_]+(-[^\W_]+)?$',re.U)
NAME_RE = re.compile(r'\w',re.U)
def valid_name(name):
    return name and NAME_RE.match(name)

# validate password
PASS_RE = re.compile(r'[A-Za-z0-9@#$%^&+=]+')
def valid_password(password):
    return len(password) >= 8 and PASS_RE.match(password)

# validate email
EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return email and EMAIL_RE.match(email)

# validate url
URL_RE = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
def valid_url(url):
    return url and URL_RE.match(url)
