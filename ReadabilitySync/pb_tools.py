#coding: utf-8
import os
from shutil import copy, rmtree
import sqlite3


def archive_and_delete_finished_books(device_path, archive_path, db_path=None):
    """ Copies finished books to archive and deletes them from PocketBook"""
    db_path = db_path or os.path.join(device_path, 'system', 'explorer-2', 'explorer-2.db')
    if not os.path.exists(db_path):
        raise EnvironmentError(u'No db found in %s' % db_path)
    finished_books = get_finished_books(db_path=db_path)
    copy_books_to_archive(finished_books, device_path, archive_path)
    delete_books_from_device(finished_books, device_path, dry_run=False)


def get_finished_books(db_path, base_path='', with_full_path=True, max_unread_pages=2, skip_prefix=True, path_prefix='/mnt/ext1/'):
    """ Return relative path to files, that has already been completely finished"""
    db_connection = sqlite3.connect(db_path)
    raw_finished_books_ids = db_connection.execute(
        'SELECT bookid FROM books_settings WHERE npage - cpage < ?',
        [max_unread_pages]
    ).fetchall()

    finished_books_ids = make_flat(raw_finished_books_ids, cast_to_str=True)
    if not finished_books_ids:
        return []
    book_query = 'SELECT path, filename FROM books WHERE id IN (?)'
    query_args = [
        ', '.join(finished_books_ids)
    ]
    if base_path:
        book_query += " AND path LIKE ?"
        query_args.append(base_path + '%')
    books_raw = db_connection.execute(book_query, query_args).fetchall()
    if skip_prefix:
        path_handler = lambda path: path[len(path_prefix):] if path.startswith(path_prefix) else path
    else:
        path_handler = lambda path: path
    books = [path_handler(b[0]) if with_full_path else b[1] for b in books_raw]
    return books


def copy_books_to_archive(finished_books, device_path, archive_path):
    for relative_path in finished_books:
        from_path = os.path.join(device_path, relative_path)
        copy(from_path, archive_path)
        print 'Archived: %s' % os.path.basename(relative_path)


def delete_books_from_device(finished_books, device_path, dry_run=True):
    for relative_path in finished_books:
        from_path = os.path.join(device_path, relative_path)
        print 'Deleted: %s' % os.path.basename(relative_path)
        if not dry_run:
            rmtree(from_path)


def make_flat(not_flat_list, cast_to_str=False):
    """ [(1, ), (2, ), (3, )] -> [1, 2, 3]"""
    flat_list = []
    for element in not_flat_list:
        for sub_element in element:
            flat_list.append(str(sub_element) if cast_to_str else sub_element)
    return flat_list
