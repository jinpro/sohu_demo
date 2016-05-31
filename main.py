import urllib2
import datetime
import re

#记录访问过的链接
visited_urls = []

#存储日志
def save_log(url, time_str, error):
    #url:str 错误的url
    #time_str:str 错误发生的时间
    #error:str 错误的原因
    f = open("log", "a")
    f.write("%s, %s, %s"%(url, time_str, error))
    f.close()

#获取当前时间
def current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#递归抓取网页
def crawling(url, base_url):
    #判断url是否访问过
    if url in visited_urls:
        return
    f_handle = None
    #访问链接, 发生异常后记录错误
    try:
        f_handle = urllib2.urlopen(url)
        visited_urls.append(url)
    except Exception, e:
        save_log(url, current_time(), e)
        return
    #如果未发生异常, 打印网页为可连接的
    print url + " is connected."
    #读取网页内容, 并用正则表达式解析出url
    html_text = f_handle.read()
    link_pattern = re.compile("<a.*href=\"(.+?)\"")
    #获取一个网页上所有和m.sohu.com相关的url, 遍历过滤无关的url, 递归访问
    urls = link_pattern.findall(html_text)
    for sub_url in urls:
        if sub_url == '/':
            continue
        if sub_url == '#':
            continue
        if sub_url.startswith("http") and sub_url.find("m.sohu.com") != -1:
            crawling(sub_url, base_url)
        elif sub_url.startswith("/"):
            crawling(base_url + sub_url, base_url)


if __name__ == '__main__':
    crawling("http://m.sohu.com", "http://m.sohu.com")


