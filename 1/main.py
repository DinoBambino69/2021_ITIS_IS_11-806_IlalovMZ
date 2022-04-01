import requests
import bs4
from urllib.parse import urlparse
import cld2


class Crawler:
    def __init__(self, url):
        self.count_pages = 100
        self.count_words = 1000
        self.url = url
        self.visited_urls = []
        self.hrefs: list = []

    def clear_HTML(self, html):
        bs = bs4.BeautifulSoup(html, 'html.parser').text
        res = ' '.join(bs.split())
        return res

    def check_url(self, url):
        parse = urlparse(url)
        return bool(parse.netloc) and bool(parse.scheme)

    def get_len(self, str):
        strs = str.split(" ")
        return len(strs)

    def get_hrefs(self, request):
        hrefs = []
        soup = bs4.BeautifulSoup(request.content, "html.parser")
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                continue
            if href in hrefs:
                continue
            if href in self.hrefs:
                continue
            if self.check_url(href):
                hrefs.append(href)
        return hrefs

    def start(self):
        if self.check_url(self.url):
            self.hrefs.append(self.url)
            self.visited_urls.append(self.url)
            page_number = 0
            counter = 0
            file_result = open('index.txt', 'w', errors="ignore")

            while page_number < self.count_pages:
                current_page = self.hrefs[counter]
                print(f"Page {counter}: {current_page}")
                try:
                    if self.check_url(current_page) and current_page is not None and not any(
                            x in current_page for x in [".pdf"]):
                        request = requests.get(current_page)
                        self.hrefs += self.get_hrefs(request)
                        text = self.clear_HTML(request.text)
                        length = self.get_len(text)
                        detect = cld2.detect(text)
                        if length >= self.count_words and detect.details[0].percent >= 95 and detect.details[0].language_name == 'RUSSIAN':
                            page_number += 1
                            counter += 1
                            self.visited_urls.append(current_page)
                            file_page = open(f"files/{page_number}.txt", 'wb')
                            file_page.write(text.encode("utf-8"))
                            file_result.write(str({f"url-{page_number}": current_page}))
                            file_result.write("\n")
                        else:
                            counter += 1
                    else:
                        counter += 1
                        continue
                except Exception as e:
                    print(e)
                    counter += 1


if __name__ == "__main__":
    url = 'https://kpfu.ru/'
    crawler = Crawler(url)
    crawler.start()
