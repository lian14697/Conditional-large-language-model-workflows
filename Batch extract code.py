import json
import os
import re
import time
from difflib import SequenceMatcher
import pandas as pd


df = pd.read_csv(r'E:\llm-Colorectal_cancer\deepseek.csv')
print(f"Diagnosis Report：{df.iloc[0,2]}\nReport Description：{df.iloc[0,3]}")
print(df.shape)


Path = 'E:\\llm-Colorectal_cancer\\deepseek\\'
batch = 'deepseek'

import requests
import json
for i in range(0,df.shape[0]):   # range(0,df.shape[0])
    # 定义API的URL
    url = 'http://localhost:4000/api/v1/chat/completions'
    
    headers = {
        'Authorization': 'Bearer fastgpt-kBKBZTM1XXCjjM4oVgJwPyX7qkaTf8VbSeQT538SrKlz6F5DjaF8HV', 
        'Content-Type': 'application/json'
    }

    data = {
        "chatId": "111",
        "stream": False, 
        "detail": False, 
        "messages": [
            {
                "content":"Diagnosis Report:" + df.iloc[i,2] + "\n" + "Report Description:" + df.iloc[i,3], 
                "role": "user"
            }
        ]
    }
    
    success = False
    attempts = 0
    max_attempts = 100

    while not success and attempts < max_attempts:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print(response.json()['choices'][0]['message']['content'])
            with open(Path + batch +"_" + str(i+1) + df.iloc[i, 1] + '_output.txt', 'w') as f:
                f.write(response.json()['choices'][0]['message']['content'])
            success = True
        else:
            print("Error:", response.status_code, response.text)
            attempts += 1
            if attempts < max_attempts:
                print("Retrying in 10 seconds...")
                time.sleep(10)


