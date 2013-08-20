from epub_tools import get_epub_info
import os
import readability
from os import listdir
from os.path import isfile, join


def get_readability_api(api_key=None, api_secret=None, username=None, password=None):
    """ Authorise in Readability API"""
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
    """ Returns Readability readins list"""
    articles = []
    for b in rdd.get_bookmarks():
        articles.append({
            'title': b.article.title,
            'id': b.article.url,
        })
    return articles

def get_sync_dir():
    """ Return dir that should be synced with readability account"""
    return os.environ.get('READABILITY_SYNC_DIR',  '~/sync_test')  # TODO Get from user params

def validate_dir(dir, validate_existance=True, validate_read_rights=True, vallidat_write_rights=True):
    """ Raisies error if dir doesn't exist or now rw rights"""
    return True  # TODO

def get_books_from_dir(dir):
    """ Returns info about books currently in dir"""
    books = [f for f in listdir(dir) if isfile(join(dir,f)) and f.split('.')[-1] == 'epub']
    books_info = [get_epub_info(b) for b in books]
    for book in books_info:
        finished = get_finished_in_percents(book)
        if finished:
            book['percents_finished'] = finsihed
    return books_info

def get_finished_in_percents(book_info):
    """ Retrieve info about how many of book already been read (if possible)"""
    return 0  # TODO

def delete_books_not_in_bookmarks(dir, books, bookmarks):
    """ Deletes books in folder, but not in readability"""
    for book in books:
        if not book['title'] in [a['title'] for a in bookmarks]:
            pass  # TODO delete book

def delete_finished_books(dir, books):
    for book in books:
        if book.get('percents_finished', '') == 100:
            pass  # TODO delete_book

def download_new_books(rdd, dir, books, bookmarks):
    """ Download books in readability, but not in folder"""
    for bookmark in bookmarks:
        if not bookmark['title'] in [b['title'] for b in books]:
            pass  # TODO download book

rdd = get_readability_api()
bookmarks = get_readabitily_bookmarks(rdd)
sync_dir = get_sync_dir()
validate_dir(sync_dir)
books = get_books_from_dir(sync_dir)
delete_books_not_in_bookmarks(sync_dir, books, bookmarks)
download_new_books(rdd, sync_dir, books, bookmarks)
