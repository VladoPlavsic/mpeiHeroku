from app.db.repositories.parsers import string_or_null, list_to_string

def insert_news_check_query(date, url) -> str:
    return \
        f"SELECT (news.check_if_news_can_be_created({string_or_null(date, url)})) AS yes"

def insert_news_master_query(date, title, short_desc, content, url, object_key, preview_image_url) -> str:
    return \
        f"SELECT (news.insert_news_master({string_or_null(date, title, short_desc, content, url, object_key, preview_image_url)})).*"

def insert_news_slave_query(fk, medium) -> str:
    orders, urls, keys = map(list, zip( *((media.order, media.url, media.object_key) for media in medium)))

    orders = ','.join(map(str,orders))
    urls = ','.join(map(str,urls))
    keys = ','.join(map(str,keys))

    return \
        f"SELECT (news.insert_news_slave({fk}, '{{{orders}}}'::int[], '{{{keys}}}', '{{{urls}}}')).*"

