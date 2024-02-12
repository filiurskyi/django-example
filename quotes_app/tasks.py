from celery import shared_task

from .service.soup import (get_authors, get_authors_urls, get_quote_urls,
                           get_quotes, get_tags)


@shared_task()
def main_scrape():
    base_url = "https://quotes.toscrape.com/"
    pages_urls = get_quote_urls(base_url)
    print(pages_urls)
    for q_url in pages_urls:
        print("processing url ", q_url)

        author_urls = get_authors_urls(base_url + q_url)

        for a_url in author_urls:
            get_authors(base_url + a_url)

        get_tags(base_url + q_url)
        get_quotes(base_url + q_url)


# run celery with:       celery -A quotes_proj worker --loglevel=INFO --pool solo
