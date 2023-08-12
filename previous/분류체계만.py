## chat-GPT활용

## 크롤링 병합 결과 출력하기
new = pd.read_csv('data/20230516.csv')
## 프롬프트에 넣을 system content
with open('data/system_prompt.txt', 'r', encoding='utf-8') as f:
    system = f.read()
## 프롬프트에 넣을 few shot content
with open('data/fewshot_prompt.txt', 'r', encoding='utf-8') as f:
    fewshot = f.read()

for i in range(0,13,3):
    questions = [
        "Q1:" + new.loc[i, 'requireElement'] ,
        "Q2:" + new.loc[i+1, 'requireElement'],
        "Q3:" + new.loc[i+2, 'requireElement']
    ]

    try:
        print('*'*100)
        print(i)
        time.sleep(random.uniform(25, 30)) #무료 사용으로 1분에 3개 가능

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {'role': 'system', 'content': system},
                {'role': 'system', 'content': fewshot},
                *[{'role': 'user', 'content': question} for question in questions]
            ],
            #max_tokens = 100 이상치가 있기때문에 조절 어려움
        )
        result = completion.choices[0].message['content']
        #result = completion.choices[0].message['content'].strip()
        print(result)  # 결과
        #new.loc[i, 'gpt'] = result #결과 나눠서 정리 필요


    except Exception as e:
        print(f"An error occurred: {str(e)}")
        pass