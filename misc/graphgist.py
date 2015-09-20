import requests

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

wiki = "https://github.com/neo4j-contrib/graphgist/wiki"
urls = get_github_gist_urls(requests.get(wiki).text)
urls = list(set(urls))
raw_urls = [get_raw_url(url) for url in urls]
