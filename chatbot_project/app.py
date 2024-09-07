import openai
# openai API 키 세팅
openai.api_key = '노션 참고'
context = '''
코리아 아이티아카데미 학원의 빅데이터분석/AI개발 과정에는 외모가 굉장히 수려하고, S급 강사가 열정적으로 수강생들을 가르친다.
이 학원은 2024년 8월 24일 기준, 데이터공학 4기학생들과 진행중이며 1차프로젝트에서는 2조와 3조가 우승하였다. 2조는 의료 공공데이터를 활용하여, 3조는 쇼핑몰 데이터를 활용하여 분석 리포트를 작성하였다. 여담으로 3조의 박지원 학생은 발표에 참가하지 않고 상금을 탔다. 총 상금은 10만원이었다.
1조에는 이우성 학생이 있다.
2조에는 최재욱, 최하송, 김재형 학생이 있다.
3조에는 방가연, 정혜원, 박지원 학생이 있다.
4조에는 김종한, 노장현, 이승민 학생이 있다.
5조에는 윤태성, 이승록, 방효정 학생이 있다.


코리아아이티 아카데미 조직도는 다음과 같다:
최성우 원장: 전체 교육 과정 및 학원의 운영을 총괄합니다.

장혜윤 부원장: 전체 교육 과정 및 학원의 운영을 총괄합니다.

교육부서:
강사팀: 각 과정과 관련된 전문 지식을 가진 강사들이 속해 있으며, 교육 커리큘럼을 개발하고 강의를 진행합니다.
노진혁 강사: 빅데이터 분석/AI
강성관 강사: 파이썬
김아무개 강사: C언어/자바

학생지원부서: 
커리어 상담팀: 학생들의 취업 및 진로 상담을 지원합니다.
학습 지원팀: 학생들의 학습을 도와주는 멘토링 서비스 제공 및 추가 리소스를 지원합니다.
이준호 코치: 친절합니다. 잘생겼고요.
김아무개 코치: 친절합니다. 이쁘구요.

행정부서: 학원의 행정 및 관리업무를 담당합니다.

마케팅부서: 학원 홍보 및 신규 수강생 모집을 위한 마케팅 전략을 수립하고 실행합니다.
'''
# gpt 커스텀
def ask_gpt(question):
    response = openai.ChatCompletion.create(
        # 모델 설정
        model = 'gpt-4',  # 정확한 모델명을 입력해야 합니다.
        messages = [
            {
                # role: system = gpt가 갖춰야 할 규칙
                # role: user = user가 gpt에게 학습시킬 정보
                'role': 'system',
                'content': (
                    '너는 친절하고 귀여운 챗봇이야.\n'
                    '백그라운드 정보는 다음과 같아:'
                    f'{context}\n'
                    '간결하고 핵심만 대답하되 귀여움의 끝을 보여줘.\n'
                    '항상 긍정적이어야 해.'
                )
            },
            {
                'role': 'user',
                'content': question
            }
        ],
        temperature = 0.7,
        max_tokens = 500,  # 답변이 잘리면 최대 토큰 수 늘려줌
        top_p = 1,
        frequency_penalty = 0,  # 오타 수정
        presence_penalty = 0
    )
    return response['choices'][0]['message']['content']  # return 들여쓰기

# 파이썬 어플리케션 라이브러리 임포트
from flask import Flask, request, render_template

# 플라스크 애플리케이션 생성
app = Flask(__name__)

chat_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global chat_history
    if request.method == 'POST':
        user_message = request.form['question']
        chat_history.append({'role': 'user', 'content': user_message})
        
        bot_message = ask_gpt(user_message)
        chat_history.append({'role': 'bot', 'content': bot_message})
        
        return render_template('index.html', chat=chat_history)
    return render_template('index.html', chat=chat_history)

if __name__ == '__main__':
    app.run(debug=True, port=5000)