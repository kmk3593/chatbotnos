from flask import Flask, request, jsonify
import json
import requests
from bs4 import BeautifulSoup

# 메인 로직!! 
def cals(opt_operator, number01, number02):
    if opt_operator == "addition":
        return number01 + number02
    elif opt_operator == "subtraction": 
        return number01 - number02
    elif opt_operator == "multiplication":
        return number01 * number02
    elif opt_operator == "division":
        return number01 / number02

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World777788888888'

# 카카오톡 텍스트형 응답
@app.route('/api/sayHello', methods=['POST'])
def sayHello():
    body = request.get_json() # 사용자가 입력한 데이터
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "반가워!!!!! hello I'm Ryan"
                    }
                }
            ]
        }
    }

    return responseBody


# 카카오톡 이미지형 응답
@app.route('/api/showHello', methods=['POST'])
def showHello():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleImage": {
                        "imageUrl": "https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
                        "altText": "hello I'm Ryan"
                    }
                }
            ]
        }
    }

    return responseBody


# # 카카오톡 Calculator 계산기 응답
# @app.route('/api/calCulator', methods=['POST'])
# def calCulator():
#     body = request.get_json()
#     print(body)
#     params_df = body['action']['params']
#     print(type(params_df))
#     opt_operator = params_df['operators']
#     number01 = json.loads(params_df['sys_number01'])['amount']
#     number02 = json.loads(params_df['sys_number02'])['amount']

#     print(opt_operator, type(opt_operator), number01, type(number01))

#     answer_text = str(cals(opt_operator, number01, number02))
    
#     responseBody = {
#         "version": "2.0",
#         "template": {
#             "outputs": [
#                 {
#                     "simpleText": {
#                         "text": answer_text
#                     }
#                 }
#             ]
#         }
#     }

#     return responseBody



# 카카오톡 계산기
@app.route('/api/calCulator', methods=['POST'])
def calCulator():
    body = request.get_json() # 사용자가 입력한 데이터
    print(body)
    params_df = body['action']['params']
    print(type(params_df))
    opt_operator = params_df['operators']
    number01 = json.loads(params_df['sys_number01'])['amount']
    number02 = json.loads(params_df['sys_number02'])['amount']

    print(opt_operator, type(opt_operator), number01, type(number01))

    answer_text = str(cals(opt_operator, number01, number02))

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer_text
                    }
                }
            ]
        }
    }

    return responseBody





# 카카오톡 하락주 top30
@app.route('/api/deScend', methods=['POST'])
def deScend():
    # # 거래상위 
    url = "https://finance.naver.com/sise/sise_fall.naver"
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        title1 = soup.select('th')    
        col_list = []
        for i in range(len(title1)):
            if (title1[i].text == "종목명") or (title1[i].text == "현재가") or (title1[i].text == "등락률"):
                col_list.append(title1[i].text)
  
        title2 = soup.findAll("a", class_="tltle")
        title_list = []
        for i in range(len(title2)):
            title_list.append(title2[i].text)

            if i == 29 : 
                break
  
        title3 = soup.find_all("td", class_="number")
        data_list = []
        for i in range(len(title3)):
            j = divmod(i, 10)
            if (j[1] == 0) or (j[1] == 2):
                data_list.append(title3[i].text.strip())
            if len(data_list) == 60 :
                break
    
        step01_list = []
        for i in range(len(title_list)):
            step01_list.append(title_list[i])
            for j in range(len(data_list)):
                k = divmod(j, 2)
                if k[0] == i :
                    step01_list.append(data_list[j])
   
        topactive_list = []
        for i in range(len(col_list)):
            topactive_list.append(col_list[i])
        for i in range(len(step01_list)):
            topactive_list.append(step01_list[i])

    else:
        print(response.status_code)
    

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": step01_list
                    }
                }
            ]
        }
    }

    return jsonify(responseBody)