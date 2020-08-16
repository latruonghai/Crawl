import bs4
import requests
import pandas as pd
import codecs
import os

class Crawl:

    def __init__(self, url, mode):
        self.url = url
        self.mode = mode
        #self.is_sarcasm = is_sarcasm

    def get_page_content(self):
        page = requests.get(self.url)
        return bs4.BeautifulSoup(page.text, "html.parser")

    def read_file(self):
        file = codecs.open(self.url, 'r')
        file1 = file.read()
        file1 = str(file1)
        return bs4.BeautifulSoup(file1, "html.parser")

    def parser_link(self):
        soup = self.get_page_content()
        box = soup.findAll('span', class_="_2iem")
        print(soup)

    def get_mode(self):
        self.mode = self.mode.lower()
        switch_mode = {"post": "parser_post()", 'like': 'parser_file_like()'}
        self.mode = switch_mode[self.mode]

    # To crawl who posted to the page according to files
    # '.html''s from the page on Facebook.
    # Example:
    # In the page named 'GXVN' I request a file '.html' from Facebook
    # Then I use 'parser_post' function to find who posted on that Facebook page.
    # The function will return 2 list:
    #   1. Links to Facebook user's profile who have been posting to Facebook page.
    #   2. Their name.
    def parser_post(self):
        soup = self.read_file()
        links = soup.findAll('div', class_="qzhwtbm6 knvmm38d")
        Links = [l.find('a',
                        class_="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p") for l in links]
        link = []
        name = []
        for l in Links:
            if l != None:
                li = l.get("href")
                n = l.text
                if li.find("hashtag") == -1:
                    link.append(li)
                    name.append(n)
            get_true_string(link)
        self.Link = link
        self.Name = name

    def parser_file_like(self):
        soup = self.read_file()
        print(soup)
        # Tìm các box chứa mục cần tìm
        #box = soup.findAll('div',class_="card__text")
        # Tìm link trong nó nếu có
        links = soup.find('div',
        class_="a8s20v7p k5wvi7nf buofh1pr pfnyh3mw l9j0dhe7 du4w35lb")
        links = links.findAll('a', 
        class_="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p")
        if len(links) > 0:
            link = [l.find('a').get("href") for l in links]
            get_true_string(link)
            print(link)
        #headlines = [head.find('h2',class_="card__headline__text").text for head in box]
        headlines = [head.text for head in links]
        self.Link = link
        self.Name = headlines
        #self.is_sarcasm = [1]*len(link)


def get_csv(listCrawl):
    data1 = listCrawl[0]
    for i in range(len(listCrawl)):
        data1 = data1.append(listCrawl[i])
    path = os.getcwd() + '/data'
    print(path)
    filename = input("Nhap vao file name: ")
    result = data1.to_csv(path + '/' +
                          filename + ".csv", header=True, index=None)
    return result


def get_true_string(strings):
    for i in range(len(strings)):
        if strings[i].find('__') != -1:
            index = strings[i].find('__')
            strings[i] = strings[i].replace(
                strings[i], strings[i][0:index])


def get_df(Crawl):
    papers = {"Name": Crawl.Name,
              "Link": Crawl.Link}
    data = pd.DataFrame(papers)
    return data


def get_Crawl(path):
    mode = input("Nhap vao kieu can quet")
    """for url in lists:
        crawl = Crawl(url, mode)
        crawl.get_mode()
        eval('crawl.' + crawl.mode)
        data = get_df(crawl)
        yield data
"""
    for folder, subfolder, files in os.walk(path):
        for file in files:
            url = path + '/' + file
            crawl = Crawl(url,mode)
            crawl.get_mode()
            eval('crawl.'+crawl.mode)
            data=get_df(crawl)
            yield data
if __name__ == "__main__":
    lists = ["GXVN13.html"]
    path = os.getcwd() + '/src'
    listCrawl = list(get_Crawl(path))
    result = get_csv(listCrawl)
    print("Done")
