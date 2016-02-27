import urllib.request
from bs4 import BeautifulSoup
import html2text

def GetHTMLData(url):
        html_data = urllib.request.urlopen(url).read().decode("utf-8")
        parsed_html = BeautifulSoup(html_data, 'html.parser')
        title = parsed_html.head.title.text[:-10]
        description = html2text.html2text(parsed_html.body.find('p', attrs={'id':'eow-description'}).prettify())
        return title, description
