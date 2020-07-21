import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
import re
import json
from urllib.parse import urlencode
from  instaparser import config #должен быть создан вручную и содержит приватные переменные



class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']

    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    graphql_url = 'https://www.instagram.com/graphql/query/'
    followers_hash = 'c76146de99bb02f6415203be841dd25a'

    #переменные должны быть определены в файле instaparser/config.py
    insta_login = config.INSTAGRAM_LOGIN    #логин инстаграмм, от имени которого парсим
    insta_psw = config.INSTAGRAM_ENCRYPTED_PASSWORD #зашифрованный пароль
    target_accounts = config.TARGET_ACCOUNTS #список (list) целевых аккаунтов, которые будем парсить

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text) #csrf с стартовой страницы
        yield scrapy.FormRequest(                         #авторизуемся
            url=self.insta_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.insta_login, 'enc_password': self.insta_psw},
            headers={'X-CSRFToken': csrf_token}
        )

    def login(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            for account in self.target_accounts:    #переходим на каждую страницу целевых аккаунтов для парсинга
                yield response.follow(
                    f'/{account}',
                    callback=self.user_parse,
                    cb_kwargs={'username': account}
                )

        print(2)

    def user_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'user_id': user_id,
                     'include_reel': True,
                     'fetch_mutual': True,
                     'first': 24
                     }

        url_followers = f'{self.graphql_url}?query_hash={self.followers_hash}&{urlencode(variables)}'

        url_followers = 'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"377955141","include_reel":true,"fetch_mutual":true,"first":24}'

        yield response.follow(
            url_followers,
            callback=self.followers_parse,
            cb_kwargs={'username': username, 'user_id': user_id}
        )

        print(3)

    def followers_parse(self, response: HtmlResponse, username, user_id):

        print(4)

    #Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    #Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')