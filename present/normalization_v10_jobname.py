import pandas as pd
import os
import time, random
from dotenv import load_dotenv
# import openai
import re
import json
from openai import OpenAI

path = 'C:/Users/hoeeun/Desktop/Crawling_master/normalization/data/'

# 크롤링 병합 결과 출력하기
new = pd.read_csv(path + 'for_check.csv')
# print(new.head())

total = len(new)

## chat-GPT활용
load_dotenv()
client = OpenAI(
    api_key=os.getenv("openai.api_key")
)


##프롬프트 입력해서 GPT돌리기
def infer_ai(Text):
    Primary = ['Not AI', 'Data scientist', 'Data enginner', 'Machinelearning/Deeplearning researcher', 'Machinelearning/Deeplearning enginner', 'Applied AI Service developer', 'AI serive planner', 'AI artist']

    job_dic = {
        'Not AI' : ['design', 'DSP/NPU/AP/VHDL/Verilog', 'instructor', 'software development', 'SoC','business', 'management', 'electrical/electronic','machine vision', 'semiconductor'],
        'Data scientist' : ['answering business questions using analytics','prediction model', 'analysis report','SQL'],
        'Data enginner' : ['Hadoop','Airflow','distributed system','build data pipelines, aggregation, storage, monitoring'],
        'Machinelearning/Deeplearning researcher' : ['thesis','research','train prediction models','report describing'],
        'Machinelearning/Deeplearning enginner' : ['train/deploy prediction models','prediction system running on real data'],
        'Applied AI Service developer' : ['OpenAI','Responsible for all AI-related development work regardless of researcher or engineer'],
        'AI serive planner' : ['Service planning using AI'],
        'AI artist' : ['chat-gpt','generative AI','Midjourney','Stable Diffusion']
    }
    job_plus = "\n".join([f"{job} secondary categories : {detail}" for job, detail in job_dic.items()])

    delimiter = "####"

    Prompt = f"""
    #Order
    You are an AI job master. You will be provided with the text.
    The text will be delimited with {delimiter} characters.
    Classify each text into a primary category and a secondary category.

    #Queries
    Primary categories: [{', '.join(Primary)}]

    {job_plus}

    Provide your output in json format with the keys: primary and secondary.
    Make sure to choose the category accurately.
    """

    messages = [{'role': 'system', 'content': Prompt},
                {'role': 'user', 'content': f'{delimiter}{Text}.'}]

    print(f"messages here:{messages}")

    chat = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages,
        response_format ={"type": "json_object"},
        temperature=0)

    reply = chat.choices[0].message.content
    reply = json.loads(reply)
    print(f'ChatGPT: {reply}')

    try:
        jobname = reply['primary']
        reason = reply['secondary']
    except Exception as e:
        jobname = "Error"
        reason = "Error"

    print('------Here------' + '\n', f'{i}/{total}\n jobname:{jobname} reason:{reason} ')
    return (jobname, reason)


# 직무 선택 반복문
for i in range(total):
    try:
        Text = new.loc[i, 'main'] + new.loc[i, 'require']
        Text = re.sub(r'\d+\.', "", Text)
        Text = re.sub(r"[^\w\s~]", "", Text).replace('ㆍ', '')
        Text = re.sub(r'\t', '', Text)

        jobname,reason = infer_ai(Text)
        time.sleep(random.uniform(3, 5))

        if jobname:
            new.loc[i, 'reason'] = reason
            new.loc[i, 'jobname'] = jobname
        else:
            new.loc[i, 'reason'] = "Error"
            new.loc[i, 'jobname'] = "Error"
        print("=" * 100)
    except:
        pass

new.to_csv(path + "for_check_v10.csv", index=False)
