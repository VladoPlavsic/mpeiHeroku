def delete_news_query(id: int) -> str:
    return \
        f"SELECT news.delete_news({id}) AS cloud_key"
