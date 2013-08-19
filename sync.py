import os
import readability


api_key = os.environ.get('READABILITY_API_KEY', '')
api_secret = os.environ.get('READABILITY_API_SECRET', '')
username = os.environ.get('READABILITY_USERNAME', '')
password = os.environ.get('READABILITY_PASSWORD', '')

token = readability.xauth(api_key, api_secret, username, password)
rdd = readability.oauth(api_key, api_secret, token=token)
for b in rdd.get_bookmarks():
    print b.article.title
print dir(rdd.get_bookmarks()[0].article)
