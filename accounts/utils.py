import base64
import hashlib
import hmac
import time
import requests
import json
from config.settings.base import SMS_ACCESS_KEY, SMS_SECRET_KEY, SMS_SERVICE_ID, SMS_FROM_NUMBER


def make_signature(access_key, secret_key, timestamp):
    method = "POST"
    uri = "/sms/v2/services/%s/messages" % SMS_SERVICE_ID

    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signing_key = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signing_key


def send_sms(auth_number, phone_number):
    timestamp = str(int(time.time() * 1000))
    access_key = SMS_ACCESS_KEY
    secret_key = SMS_SECRET_KEY
    secret_key = bytes(secret_key, 'UTF-8')
    signature = make_signature(access_key, secret_key, timestamp)

    url = "https://sens.apigw.ntruss.com/sms/v2/services/%s/messages" % SMS_SERVICE_ID
    content = {
        "type": "SMS",
        "from": SMS_FROM_NUMBER,
        "content": "[테스트] 인증 번호 [%d]를 입력해주세요." % auth_number,
        "messages":[
            {
                "to": phone_number
            }
        ]
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": access_key,
        "x-ncp-apigw-signature-v2": signature
    }
    res = requests.post(url, headers=headers, data=json.dumps(content))
