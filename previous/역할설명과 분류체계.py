with open('data/role_system_prompt.txt', 'r', encoding='utf-8') as f:  ## 프롬프트에 넣을 system content
    system = f.read()

for i in range(0, 5):
    try:
        print('*' * 100)
        print(i)
        time.sleep(random.uniform(25, 30))  # 무료 사용으로 1분에 3개 가능

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {'role': 'system', 'content': system},
                {'role': 'user', 'content': "Seed words:" + new.loc[i, 'requireElement']+ '\n' + 'category:'},
            ],
            # max_tokens = 100 이상치가 있기때문에 조절 어려움
        )
        result = completion.choices[0].message['content']
        # result = completion.choices[0].message['content'].strip()
        print(result)  # 결과
        # new.loc[i, 'gpt'] = result


    except Exception as e:
        print(f"An error occurred: {str(e)}")
        pass