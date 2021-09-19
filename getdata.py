from lxml import etree
import requests
import brotli
# f = open("test.html","r",encoding="utf-8") #读取文件
# f = f.read()#把文件内容转化为字符串


# proxy = requests.get("http://tiqu.linksocket.com:81/abroad?num=1&type=2&lb=1&sb=0&flow=1&regions=gb&port=1&n=0").json()
# proxydata = proxy['data']
# print(proxydata[0])
# proxyip = proxydata[0]["ip"]
# proxyport = proxydata[0]["port"]
from lxml.etree import tostring

proxyip = "127.0.0.1"
proxyport = "1082"
proxies = {
    'http': proxyip + ":" + str(proxyport),
    'https': proxyip + ":" + str(proxyport),
}

def Parsing_data(keywords,num,flag, work_log):
    OnePageResulr = []
    url = "https://www.indeed.com/jobs?q={}&l=&start={}".format(keywords,num)
    work_log.emit("srart "+url)
    # print(url)
    payload = {}
    headers = {
        'authority': 'www.indeed.com',
        'method': 'GET',
        'path': '/jobs?q=123&l=',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'CTK=1f9vs1n8qo14s801; CSRF=isTjSkGWEulX5SLho7Z97VQhIeNjlUXm; INDEED_CSRF_TOKEN=pZCCCcXuhjoWgolovw6V8abRkWoSqliE; LV="LA=1625623096:CV=1625623096:TS=1625623096"; UD="LA=1625623096:CV=1625623096:TS=1625623096"; _ga=GA1.2.1309184079.1625623099; _gid=GA1.2.1739826411.1625623099; SURF=nlavwB9tWKoOaBln5O7l7ckyS9MtZqTY; NCR=1; CTK=1f9vavqvgo27s800; indeed_rcc="LV:CTK:UD"; JSESSIONID=A3902BBFB3BE8E61FBA605A1F21C2EB6; _gali=whatWhereFormId; ac="4KuEwN7GEeuxovGRyrPg2g#4KzkUN7GEeuxovGRyrPg2g"; JSESSIONID=8B81043F216977E9B74B471836A95F22; RQ="q=&l=123&ts=1625670927358&pts=1625641404175"; UD="LA=1625670927:CV=1625670927:TS=1625670927:SG=798b555ea65ea664908395096eb302ae"; indeed_rcc="LV:CTK:UD:RQ"; jaSerpCount=3',
        'dnt': '1',
        'referer': 'https://www.indeed.com/',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response.encoding = 'utf8'
    data1 = response.text
    html = etree.HTML(data1)
    joblist = html.xpath('//*[@id="mosaic-provider-jobcards"]/a')
    for _i, job in enumerate(joblist):
        tmp = []
        curl = job.xpath('@href')
        companyurl = "https://www.indeed.com" + curl[0]

        jobTitlename = job.xpath('.//h2[contains(@class, "jobTitle jobTitle-color-purple")]')[0].xpath('.//span/@title')[0]

        jobsnippet = job.xpath('.//div[contains(@class, "job-snippet")]')[0]

        try:
            jobsnippettext = jobsnippet.xpath('.//li/text()')[0]

        except:
            try:
                jobsnippettext = jobsnippet.xpath('.//ul/li/text()')[0]

            except:
                # print(tostring(jobsnippet))
                # print(companyurl)
                jobsnippettext = jobsnippet.xpath('.//text()')[0]


        companyNamec = job.xpath('.//span[contains(@class, "companyName")]')[0]
        try:
            companyName = companyNamec.xpath('.//a/text()')[0]
        except:
            companyName = companyNamec.xpath('.//text()')[0]
        tmp.append(flag)
        tmp.append(jobTitlename)
        tmp.append(jobsnippettext)
        tmp.append(companyName)
        tmp.append(companyurl)
        flag+=1

        OnePageResulr.append(tmp)
        # print(url,jobTitlename,jobsnippettext,companyName)
        # print(OnePageResulr)
    return OnePageResulr

if __name__ == '__main__':
    Parsing_data()

