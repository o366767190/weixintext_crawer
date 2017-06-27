#coding:utf-8
'''
Created on 2017年6月27日

@author: Shinelon
'''
import urllib.request
import re
import time
#伪装浏览器
headers = ('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
opener = urllib.request.build_opener()
opener.addheaders =[headers]
urllib.request.install_opener(opener)
#设置代理
def use_proxy(proxy_addr,url):
    try:
        import urllib.request
        proxy =urllib.request.ProxyHandler({'http':proxy_addr})
        opener = urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        data = urllib.request.urlopen(url).read().decode('utf-8')
        return data
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
        time.sleep(10)
    except Exception as e:
        print('Exception:'+str(e))
        time.sleep(1)
        
urllist = []
#爬取函数
def geturllist(key,pagestart,pageend,proxy):
    try:
        page = pagestart#page的初始化
        #编码
        keycode = urllib.request.quote(key)
        pagecode = urllib.request.quote('&page')
        #for循环
        for page in range(pagestart,pageend+1):
            url = 'http://weixin.sogou.com/weixin?type=2&query='+keycode+pagecode+str(page)#注意这里URL不能写错
            #使用代理爬取内容
            data1 = use_proxy(proxy, url)#注意这里使用代理爬取方法得到的是一个list
            #print(data1)
            #文章链接的正则表达式
            urllistpat = '<div class="txt-box">.*?(http://.*?)"'#这个正则表达式匹配的结构就是一个url吗？？
            urllist.append(re.compile(urllistpat,re.S).findall(data1))
            #print(urllist)
            print('共获取到'+str(len(urllist))+"个文章的地址")
            return urllist       
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
        time.sleep(10)
    except Exception as e:
        print('Exception:'+str(e))
        time.sleep(1)

#从list中提取列文章的url并爬取内容
def getcontent(urllist,proxy):
    i = 0
    #为了将内容在本地以html的形式保存起来，我们首先要写一部分的Html,并且将这一部分
    html1 = '''
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>微信文章页面</title>
    </head>
    <body>'''
    fh = open('C:\Users\Shinelon\Documents\GitHub\weixintext_crawer\text.html','wb')
    fh.write(html1).encode('utf-8')
    fh.close()
    #再次以追加写入的方式打开
    fh = open('C:\Users\Shinelon\Documents\GitHub\weixintext_crawer\text.html','ab')
    #爬取urllist中的内容
    for i in range(0,len(urllist)):
        for j in range(0,len(urllist[i])):
            url = urllist[i][j]
            #将这里的url处理成真实url
            url = url.replace('amp;','')
            data=use_proxy(proxy, url)
            titlepat = '<h2 id="activity-name" class="rich_media_title">(.*?)</hh2>'
            contentpat = 'id="js_content">(.*?)id="js_sg_bat"'
             
geturllist('编程   ', 1, 2, '180.118.242.70:808')
            
        
        
    
    