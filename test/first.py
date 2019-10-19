from django.test import Client

c = Client()
response = c.post('/register/',
                  {
                      'username': 'test-user',
                      'email': 'dacoda.strack@gmail.com',
                      'password1': 'dacoda-test-password',
                      'password2': 'dacoda-test-password'
                  })

c.post('/login/',
       {
           'username': 'test-user',
           'password': 'dacoda-test-password'
       })

c.post('/search/goo/誰')
c.post('/search/larousse/qui')

# Parse response to get the text id
c.post('/text/', 
       {
           'contents': '<p>韓国紙・朝鮮日報は１８日、天皇陛下が即位を宣言する「即位礼正殿せいでんの儀」参列のため２２～２４日に訪日する韓国の李洛淵イナギョン首相が安倍首相と会談する際、１１月の国際会議に合わせた安倍首相と文在寅ムンジェイン韓国大統領との日韓首脳会談の開催を提案すると報じた。</p>',
           'source': ''
       })

response = c.get('/search/goo辞書/開催')

# Parse response, grab the first result, then feed into the next post
c.post('/_word-relations/',
       {
           'reading': '開催',
           'definition': ,
           'text': ,
           'source': ,
           'begin': ,
           'end':
       })

# function orihime_csrf_cookie()
# {
    # grep -E 'orihime-beta.dacodastrack.com.*csrftoken' /tmp/cookies | awk '{print $7}'
# }
# 
# curl \
    # -c /tmp/cookies \
    # -b /tmp/cookies \
    # https://orihime-beta.dacodastrack.com/login/
# 
# curl \
    # -c /tmp/cookies \
    # -b /tmp/cookies \
    # -d "username=test-user&password=dacoda-test-password&csrfmiddlewaretoken=$(orihime_csrf_cookie)" \
    # https://orihime-beta.dacodastrack.com/login/
# 
# curl -v \
    # -c /tmp/cookies \
    # -b /tmp/cookies \
    # -d "contents=誰だお前&source=&csrfmiddlewaretoken=$(orihime_csrf_cookie)" \
    # https://orihime-beta.dacodastrack.com/text/
