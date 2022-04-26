import requests
from fake_useragent import UserAgent
import csv


agent = UserAgent()
url = 'https://auto.ru/-/ajax/forms/getBreadcrumbsPublicApi/'
headers = '''
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: ru,en;q=0.9
Connection: keep-alive
Content-Length: 80
content-type: application/json
Cookie: suid=73c7c70f08b0767cd94f36a145f8c7da.c39130504114ad170eb12a3c91e6b2c1; autoruuid=g6262dd5c2dd4ri6m8706bqtdufvvspf.40a9d9dd5ce2d16f3c14c269d089c0a4; _ym_uid=165064636572443001; autoru_sid=a%3Ag6262dd5c2dd4ri6m8706bqtdufvvspf.40a9d9dd5ce2d16f3c14c269d089c0a4%7C1650738155598.604800.KP7HHr7TYD6w2dXRRDShiA.B8-UxTABwpmLQZoMfO4gkjjVw24zVBI-WX-kEaLvKC8; yuidlt=1; yandexuid=9639773051636521624; my=YwA%3D; ys=svt.1%23def_bro.1%23ead.2FECB7CF%23wprid.1650734730086484-13132958001665223905-vla1-4628-vla-l7-balancer-8080-BAL-6300%23ybzcc.ru%23newsca.native_cache; gdpr=0; _ym_isad=2; Session_id=3:1650738190.5.0.1636545597870:HTGkBQ:4c.1.2:1|1415118969.0.2|61:3941.668247.p7nnQRD37ewOgpRUCW6QgQaCCrE; yandex_login=foozydestroy; i=fzXgQhOsFSkQkkEjhkXkzCPT5gVMaUBBufx3evisqQPmQUYpbFc5gY8j1RLa3gg63+nEVfwGswbcewM/VrfY0vuzhXY=; mda2_beacon=1650738190333; _yasc=Pr/ITtgQBGKhPOYeDaMgYarYOPhJ2vp6a3UEx5wt/5B15bZDAXA=; cycada=b+f2zfJJm2Hp81RK2asezvR8iFryWOnEzP3Xqx05xoM=; _csrf_token=a5df350bb9460d2cb60daf53a581a3d5c7f6248db9aad943; _ym_d=1650785015
Host: auto.ru
Origin: https://auto.ru
Referer: https://auto.ru/moto/add/
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="98", "Yandex";v="22"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: same-origin
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.2.644 Yowser/2.5 Safari/537.36
x-client-app-version: 7ee9e5e5846
x-client-date: 1650785018073
x-csrf-token: a5df350bb9460d2cb60daf53a581a3d5c7f6248db9aad943
x-page-request-id: c819df64f1ff7a539e0209f5be255b49
x-requested-with: XMLHttpRequest
x-retpath-y: https://auto.ru/moto/add/
'''.strip().split('\n')

with open('data_auto.csv', 'w') as F:
    writer = csv.writer(F)
    writer.writerow([
        'Type', 'Mark', 'Model'
    ])


category_list = ['MOTORCYCLE', 'ATV', 'SCOOTERS', 'SNOWMOBILE']
dict_headers = {}


for header in headers:
    key, value = header.split(': ')
    dict_headers[key] = value

count = 0
marks_dict = {}


for i in category_list:
    params = {"category": "moto", "catalog_filter": [{}], "moto_category": i, "rid": 225}
    response = requests.post(url=url, json=params, headers=dict_headers).json()
    marks_list = list()
    for j in range(len(response[0]['entities'])):
        marks_list.append(response[0]['entities'][j]['id'])
        marks_dict[i] = marks_list

marks_model_dict = {}


for marks in marks_dict.items():
    moto_category = marks[0]
    marks_model_list = list()
    for mark in marks[1]:
        model_list = list()
        models_dict = {}
        params_model = {"category": "moto", "catalog_filter": [{"mark": mark}], "moto_category": moto_category, "rid": 225}
        response_model = requests.post(url=url, json=params_model, headers=dict_headers).json()
        for i in range(len(response_model[0]['entities'])):
            model_list.append(response_model[0]['entities'][i]['id'])
        models_dict[mark] = model_list
        marks_model_list.append(models_dict)
    marks_model_dict[moto_category] = marks_model_list

with open('data_auto.csv', 'a') as F:
    writer = csv.writer(F)
    for i in marks_model_dict:
        for j in range(len(marks_model_dict[i])):
            for k in marks_model_dict[i][j]:
                for x in marks_model_dict[i][j][k]:
                    writer.writerow([i, k, x])