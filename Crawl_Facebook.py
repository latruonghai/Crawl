import bs4
import pandas as pd
import codecs

class Crawl:
    
    def __init__(self, url, is_sarcasm=[], Article=[], Headline=[]):
        self.url = url
        self.is_sarcasm = is_sarcasm
        self.Article = Article
        self.Headline = Headline

    def read_file(self):
        file = codecs.open(self.url, 'r')
        file1 = file.read()
        file1 = str(file1)
        return bs4.BeautifulSoup(file1, "html.parser")

    def parser(self):
        soup = self.read_file()
        # Tìm các box chứa mục cần tìm
        #box = soup.findAll('div',class_="card__text")
        # Tìm link trong nó nếu có
        links = soup.findAll('a',
        class_="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p")

        print(links)
        if len(links) > 0:
            link = [l.get('href') for l in links]
        #headlines = [head.find('h2',class_="card__headline__text").text for head in box]
        headlines = [head.text for head in links]
        self.Article = link
        self.Headline = headlines
        self.is_sarcasm = [1]*len(link)


def get_df(Crawl):
    papers = {"Article": Crawl.Article,
              "Headline": Crawl.Headline, "is_sarcasm": Crawl.is_sarcasm}
    data = pd.DataFrame(papers)
    return data


def get_Crawl(lists):
    for url in lists:
        crawl = Crawl(url)
        crawl.parser()
        data = get_df(crawl)
        yield data


def get_csv(listCrawl):
    data1 = listCrawl[0]
    for i in range(len(listCrawl)):
        data1 = data1.append(listCrawl[i])
    filename = input("Nhap vao file name: ")
    result = data1.to_csv(filename + ".csv", header=True, index=None)
    return result


if __name__ == "__main__":
    lists = ["result.html"]
    listCrawl = list(get_Crawl(lists))
    result = get_csv(listCrawl)
