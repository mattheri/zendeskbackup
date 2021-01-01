import requests
import os
import datetime
from decouple import config
import base64
import json
import re

zendesk_HC_URL = '{}'.format(config('ZENDESK_URL'))
token = '{}'.format(config('TOKEN'))
user = '{}'.format(config('USER'))
credentials = '{user}/token:{token}'.format(user=user, token=token)
language = 'en-US'

date = datetime.date.today()
backup_path = os.path.join(str(date))

if (not os.path.exists(backup_path)):
    os.makedirs(backup_path)

endpoint = zendesk_HC_URL + "/api/v2/help_center/{locale}/articles.json".format(locale=language.lower())

credentials_byte = credentials.encode('ascii')
base_64 = base64.b64encode(credentials_byte)
base64_credentials = base_64.decode('ascii')

while endpoint:
    response = requests.get(endpoint, headers={"Authorization": "Basic {credentials}".format(credentials=base64_credentials)})
    if (response.status_code != 200):
        print('Failed with error {}'.format(response.status_code))
        exit()
    data = response.json()

    for article in data['articles']:
        if (article['body'] is None):
            continue
        title = r"{title}".format(title=article['title'])
        sanitized_title = re.sub(r'[#/?%*{}\\<>\*$!\'":@+`|=]+', ' ', title)
        filename = '{title}.json'.format(title=sanitized_title)

        with open(os.path.join(backup_path, filename), mode='w', encoding='utf-8') as file:
            json.dump(article, file, ensure_ascii=False, indent=4)

    endpoint = data['next_page']