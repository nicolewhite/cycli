import requests
import re

def parse_text_from_html(html, prefix, postfix):
    data = []

    while True:
        start = html.find(prefix)

        if start == -1:
            break

        end = html.find(postfix, start + len(prefix))

        datum = html[start + len(prefix):end]
        data.append(datum)

        html = html[end + len(postfix):]

    return data

def get_github_gist_urls(html):
    prefix = 'http://gist.neo4j.org/?'
    postfix = '">'

    ids = parse_text_from_html(html, prefix, postfix)
    urls = ["https://gist.github.com/" + id for id in ids]

    return urls

def get_raw_url(gist_url):
    html = requests.get(gist_url).text
    prefix = '<div class="file-actions">\n\n          <a href="'
    postfix = '" class="btn btn-sm ">Raw</a>'

    urls = parse_text_from_html(html, prefix, postfix)
    urls = ["https://gist.githubusercontent.com" + url for url in urls]
    return urls[0] if urls else None

def get_queries(raw_url):
    html = requests.get(raw_url).text
    prefix = "[source,cypher]\n----\n"
    postfix = "----"

    queries = parse_text_from_html(html, prefix, postfix)

    return queries

def remove_strings(query):
    query = re.sub(r"'.*?'", "", query)
    query = re.sub(r'".*?"', "", query)
    query = re.sub(r'`.*?`', "", query)
    return query

def remove_comments(query):
    query = re.sub(r"//.*?\n", "", query)
    return query

def remove_rels(query):
    query = re.sub(r"\[.*?\]", "", query)
    return query

def remove_misc(query):
    query = query.replace("\n", " ")
    query = query.replace("\r", " ")
    query = query.replace("-", "")
    query = query.replace(">", "")
    query = query.replace("<", "")
    return query

def clean_query(query):
    query = " " + query + " "
    query = query.upper()
    return query

def isolate_keywords(query):
    query = remove_strings(query)
    query = remove_comments(query)
    query = remove_rels(query)
    query = remove_misc(query)
    query = clean_query(query)
    return query

def get_all_queries():
    wiki = "https://github.com/neo4j-contrib/graphgist/wiki"
    urls = get_github_gist_urls(requests.get(wiki).text)
    urls = list(set(urls))
    urls = [url for url in urls if url]
    raw_urls = [get_raw_url(url) for url in urls]
    raw_urls = [raw_url for raw_url in raw_urls if raw_url]

    queries = []

    for raw_url in raw_urls:
        try:
            queries.extend(get_queries(raw_url))
        except Exception as e:
            print(e)
            print(raw_url)
            continue

    isolated = [isolate_keywords(query) for query in queries]

    return isolated