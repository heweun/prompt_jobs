import pandas as pd
import os, re, time, random
from dotenv import load_dotenv
import openai

#파일 경로
old_data = pd.read_csv('./data/0717rocket.csv')

#특정 날짜만 확인해보자
old_data = old_data[old_data['crawlingDate'] == '2023-07-17']

#인덱스 일치하는 데이터만 준비시키기
index_list = [line for line in old_data.index.astype(str)]

path = './data/info_rocketpunch_txt'
file_list = os.listdir(path)
file_list_csv = [file for file in file_list if re.findall(r'^(\d+)', file)[0] in index_list]

## chat-GPT활용
load_dotenv()
openai.api_key = os.getenv("openai.api_key")

##프롬프트 입력해서 GPT돌리기
def parser_job(Text):

    delimiter = "'''"

    Prompt = f"""
    #Order
    Extract relevant information from the text delimited by triple quotes.
    Your task is to present this information in a specific format to aid individuals in their job hunting endeavors.
    If you encounter insufficient information, respond honestly that you don't know.
    Avoid generating answers.
    Stick to the information available in the text.
    Don't repeating the explanation.
    Follow this format:
    
    #Format
    -<job name> Relate to the job name.
    -<main duties> Relate to the main duties. up to 20 words. 
    -<job qualifications> Relate to the job qualifications. up to 20 words. 
    
    Text:
    """

    Assistant = f"""Okay. I understand. I must follow the format.
    I'll respond without reiterating the explanation.
    I assure you that I will not extract any information unrelated to the 'job name', 'main duties', or 'job qualifications'. 
    Furthermore, I will not using fictitious expressions. Answer in Korean.
    """

    messages = [{'role': 'system', 'content': Prompt},
                {'role': 'user', 'content': f'{delimiter}{Text}{delimiter}.'},
                {'role': 'assistant', 'content': Assistant}
                ]

    print(f"messages here:{messages}")

    chat = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0613',
        messages=messages,
        temperature=0
    )

    reply = chat.choices[0].message.content
    print(f'ChatGPT: {reply}', '\n')

    try:
        jobname = reply.split('-')[1].strip()
        mainduties = reply.split('-')[2].strip()
        jobrequirements = reply.split('-')[3].strip()
    except Exception as e:
        jobname = "Error"
        mainduties = "Error"
        jobrequirements = "Error"

    print('------Here------' + '\n', f'jobname:{jobname}, mainduties:{mainduties}, jobrequirements:{jobrequirements}')
    return (jobname, mainduties, jobrequirements)


# 직무 선택 반복문
for file in file_list_csv:
    print(file)
    try:
        text = pd.read_table(f'{path}/{file}')
        num = int(re.findall(r'^(\d+)', file)[0])

        Text = str(text)
        Text = re.sub(r'\d+\.', "", Text)
        Text = re.sub(r"[^\w\s]", "", Text).replace('ㆍ', '')

        jobname, mainduties, jobrequirements = parser_job(Text)
        time.sleep(random.uniform(3, 5))

        if jobname :
            old_data.loc[num, 'job'] = jobname
            old_data.loc[num, 'main'] = mainduties
            old_data.loc[num, 'require'] = jobrequirements
        else:
            old_data.loc[num, 'job'] = "Error"
            old_data.loc[num, 'main'] = "Error"
            old_data.loc[num, 'require'] = "Error"
        print("=" * 100)
    except:
        pass

old_data.to_csv("./data/0717rocket_v2.csv", index=False)