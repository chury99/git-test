import os, sys
import requests
import json
import pickle

# 에러 발생 시 파일로 출력
# folder_log = 'C:\\Users\\chury\\iCloudDrive\\python_log'
# sys.stderr = open(file=os.path.join(folder_log, 'error_kakao.log'), mode='wt', encoding='utf-8')

class kakaoAPIcontrol():
    def __init__(self):
        self.file_token = os.path.join('D:\\분봉데이터_local\\_run_data', 'dic_tokens.pkl')
        self.dic_tokens = pickle.load(open(self.file_token, 'rb'))

        self.rest_api_key = 'ea88fb57af2a241e89402b7216dc9ce3'
        self.admin_key = 'e75b9a5d1442e2e2fc06699e5667cef4'


    def search_daum(self, s_query):
        url = 'https://dapi.kakao.com/v2/search/web'
        header = {'authorization': 'KakaoAK ea88fb57af2a241e89402b7216dc9ce3'}
        param = {'query': s_query}

        response = requests.get(url=url, headers=header, params=param)

        assert response.status_code == 200, 'Kakao API Authorization Error'
        return response.json()


    def send_message_2me(self, s_user, s_text, s_url=''):
        self.dic_tokens = self._refresh_tokens()
        tokens = self.dic_tokens[s_user]
        access_token = tokens['access_token']

        if s_url == '':
            button_title = '네이버 연결'
        else:
            button_title = '차트 확인'

        url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
        header = {'Authorization': f'Bearer {access_token}'}
        post = {'object_type': 'text',
                'text': s_text,
                'link': {'web_url': s_url,
                         'mobile_web_url': s_url},
                'button_title': button_title}
        data = {'template_object': json.dumps(post)}

        response = requests.post(url=url, headers=header, data=data)

        assert response.status_code == 200, 'Send Message Fail'
        return response.json()


    def send_message(self, s_user, s_friend, s_text, s_url=''):
        self.dic_tokens = self._refresh_tokens()
        tokens = self.dic_tokens[s_user]
        access_token = tokens['access_token']
        uuid = self._get_uuid(s_user=s_user, s_friend=s_friend)

        if s_url == '':
            button_title = '네이버 연결'
        else:
            button_title = '차트 확인'

        url = 'https://kapi.kakao.com/v1/api/talk/friends/message/default/send'
        header = {'Authorization': f'Bearer {access_token}'}
        post = {'object_type': 'text',
                'text': s_text,
                'link': {'web_url': s_url,
                         'mobile_web_url': s_url},
                'button_title': button_title}
        data = {'receiver_uuids': f'["{uuid}"]',
                'template_object': json.dumps(post)}

        response = requests.post(url=url, headers=header, data=data)

        assert response.status_code == 200, 'Send Message Fail'
        return response.json()


    def _get_uuid(self, s_user, s_friend):
        '''수신한 친구목록에서 uuid 추출하여 반환 (친구는 팀원에 추가 후 access token을 발급받은 후에 검색 가능)'''
        # self.dic_tokens = pickle.load(open(self.file_token, 'rb'))
        tokens = self.dic_tokens[s_user]
        # tokens = json.load(open(self.file_token, 'r'))
        access_token = tokens['access_token']

        url = 'https://kapi.kakao.com/v1/api/talk/friends'
        header = {'Authorization': f'Bearer {access_token}'}

        response = requests.get(url=url, headers=header)

        li_friends = response.json()['elements']
        uuid = ''
        for i in range(len(li_friends)):
            dic = li_friends[i]
            if s_friend in dic['profile_nickname']:
                uuid = dic['uuid']

        assert response.status_code == 200, 'Send Message Fail'
        assert uuid != '', 'Friend is not exist'
        return uuid


    def _login_at_browser(self):
        '''브라우저를 통해 인증 코드 생성 (로그인 완료 후 나오는 주소창에서 코드 복사해서 _get_token의 code에 입력)'''
        import webbrowser
        url = 'https://kauth.kakao.com/oauth/authorize'
        webbrowser.open(f'{url}?client_id={self.rest_api_key}&'
                        f'redirect_uri=http://goniee.com&'
                        f'response_type=code&'
                        f'scope=talk_message,friends')


    def _get_token(self, s_user, auth_code):
        '''신규로 토큰 받아와서 저장 (인증 코드는 1회만 사용 가능, 재실행 시 인증코드 다시 생성 필요)'''
        url = 'https://kauth.kakao.com/oauth/token'
        data = {'grant_type': 'authorization_code',
                'client_id': f'{self.rest_api_key}',
                'redirection_uri': 'https://localhost.com',
                'code': auth_code}

        response = requests.post(url=url, data=data)
        tokens = response.json()

        self.dic_tokens[s_user] = tokens
        pickle.dump(self.dic_tokens, open(self.file_token, 'wb'))

        # json.dump(tokens, open(self.file_token + 'manul', 'w'))
        # json.dump(tokens, open(self.file_token, 'w'))


    def _refresh_tokens(self):
        '''저장된 토큰을 불러와서 새로운 access/refresh 토큰을 받아와서 저장'''
        # 토큰 읽어오기
        # self.dic_tokens = pickle.load(open(self.file_token, 'rb'))
        # tokens = json.load(open(self.file_token, 'r'))

        for s_user in self.dic_tokens.keys():
            tokens = self.dic_tokens[s_user]

            # 갱신 요청
            url = 'https://kauth.kakao.com/oauth/token'
            data = {'grant_type': 'refresh_token',
                    'client_id': f'{self.rest_api_key}',
                    'refresh_token': tokens['refresh_token']}

            response = requests.post(url=url, data=data)
            token_new = response.json()

            # 토큰 저장 (access_token은 무조건 갱신, refresh_token은 있을때만 갱신)
            if response.status_code == 200:
                tokens['access_token'] = token_new['access_token']
                if 'refresh_token' in token_new:
                    tokens['refresh_token'] = token_new['refresh_token']

            self.dic_tokens[s_user] = tokens
            pickle.dump(self.dic_tokens, open(self.file_token, 'wb'))
            # json.dump(tokens, open(self.file_token, 'w'))

        return self.dic_tokens


#######################################################################################################################
if __name__ == '__main__':
    k = kakaoAPIcontrol()
    k._refresh_tokens()

    # k._login_at_browser()
    # k._get_token(s_user='백마눌',
    #              auth_code='7WCFsRk-snrYlzNvfzW6dM5cmcUyBxvu0BOlYa8avknWFXwYJVqMR5CUHV1TS5YNKPPpagopyNgAAAF3NEqzBA')

    # result = k.search_daum(s_query='다음에서 검색')
    # result = k.send_message_2me(s_user='여봉이', s_text='나에게 카카오톡 메세지 보내기')
    # result = k.send_message(s_user='알림봇', s_friend='백마눌', s_text='다른 친구에게 카카오톡 메세지 보내기', s_url='http://goniee.com')

    # result = k.send_message(s_user='알림봇', s_friend='여봉이', s_text='테스트_20210801')

    pass
