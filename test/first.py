from django.test import Client

c = Client()
response = c.post('/register/',
                  {
                      'username': 'test-user',
                      'email': 'dacoda.strack@gmail.com',
                      'password1': 'dacoda-test-password',
                      'password2': 'dacoda-test-password'
                  })

c.post('/search/goo/誰')
c.post('/search/larousse/qui')
response = c.post('/text/', 
       {
           'contents': '韓国紙・朝鮮日報は１８日、天皇陛下が即位を宣言する「即位礼正殿せいでんの儀」参列のため２２～２４日に訪日する韓国の李洛淵イナギョン首相が安倍首相と会談する際、１１月の国際会議に合わせた安倍首相と文在寅ムンジェイン韓国大統領との日韓首脳会談の開催を提案すると報じた。',
           'source': ''
       })

