from epub_tools import get_epub_info
import os
import readability
from os import listdir
from os.path import isfile, join


def get_readability_api(api_key=None, api_secret=None, username=None, password=None):
    if not api_key:
        api_key = os.environ.get('READABILITY_API_KEY', '')
    if not api_secret:
        api_secret = os.environ.get('READABILITY_API_SECRET', '')
    if not username:
        username = os.environ.get('READABILITY_USERNAME', '')
    if not password:
        password = os.environ.get('READABILITY_PASSWORD', '')

    token = readability.xauth(api_key, api_secret, username, password)
    rdd = readability.oauth(api_key, api_secret, token=token)
    return rdd

def get_readability_bookmarks(rdd):
    articles = []
    for b in rdd.get_bookmarks():
        articles.append({
            'title': b.article.title,
            'id': b.article.url,
        })
    return articles

def get_sync_dir():
    return '~/sync_test'

def get_books_from_dir(dir):
    books = [f for f in listdir(dir) if isfile(join(dir,f)) and f.split('.')[-1] == 'epub']
    books_info = [get_epub_info(b) for b in books]
    return books_info

def delete_books_not_in_bookmarks(dir, books, bookmarks):
    for book in books:
        if not book['title'] in [a['title'] for a in bookmarks]:
            pass  # TODO delete book
def download_new_books(dir, books, bookmarks):
    for bookmark in bookmarks:
        if not bookmark['title'] in [b['title'] for b in books]:
            pass  # TODO download book

rdd = get_readability_api()
bookmarks = get_readabitily_bookmarks(rdd)
sync_dir = get_sync_dir()
books = get_books_from_dir(sync_dir)
delete_books_not_in_bookmarks(sync_dir, books, bookmarks)
download_new_books(sync_dir, books, bookmarks)
