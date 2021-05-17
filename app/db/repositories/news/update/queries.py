from app.db.repositories.parsers import list_to_string, string_or_null

def update_news_links_query(keys, links) -> str:
    keys = list_to_string(keys)
    links = list_to_string(links)
    return \
        f"SELECT news.update_news_sharing_links('{{{keys}}}', '{{{links}}}')"

def update_news_images_links_query(keys, links) -> str:
    keys = list_to_string(keys)
    links = list_to_string(links)
    return \
        f"SELECT news.update_news_images_sharing_links('{{{keys}}}', '{{{links}}}')"

def update_news_metadata_query(id:int, date: str,title: str, short_desc: str, content: str, url: str, cloud_key: str, preview_image_url: str) -> str:
    return \
        f"SELECT (news.update_news_metadata({id}, {string_or_null(date, title, short_desc, content, url, cloud_key, preview_image_url)})).*"


