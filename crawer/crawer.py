#coding:utf-8
'''
Created on 2017年6月27日

@author: Shinelon
'''
import urllib.request
import re
import time
from _weakref import proxy
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
            data1 = use_proxy(proxy, url)
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
    fh = open('C:/Users/Shinelon/Documents/GitHub/weixintext_crawer/text.html','wb')
    fh.write(html1.encode('utf-8'))
    fh.close()
    #再次以追加写入的方式打开
    fh = open('C:/Users/Shinelon/Documents/GitHub/weixintext_crawer/text.html','ab')
    #爬取urllist中的内容
    for i in range(0,len(urllist)):
        for j in range(0,len(urllist[i])):
            try:
                url = urllist[i][j]
                #将这里的url处理成真实url
                url = url.replace('amp;','')
                data=use_proxy(proxy, url)
                titlepat = '<h2 id="activity-name" class="rich_media_title">(.*?)</h2>'
                contentpat = '<div id="js_content" class="rich_media_content ">(.*?)</div>'
                thistitle = re.compile(titlepat,re.S).findall(data)
                thiscontent = re.compile(contentpat, re.S).findall(data)
                #初始化标题内容
                thistitle ='此次没有获取到'
                thiscontent ='此次没有获取到'
                if thistitle != []:
                    thistitle = thistitle[0]
                if thiscontent != []:
                    thiscontent = thiscontent[0]
                #将标题与内容汇总并赋值给alldata
                alldata = '<p>标题为："+thistitle+"</p><p>内容为:"+thiscontent+"</p><br>'
                fh.write(alldata.enccode('utf-8'))
                print('第'+str(i)+'个网页(url)的第'+str(j)+'次处理')
            except urllib.error.URLError as e:
                if hasattr(e, 'code'):
                    print(e.code)
                if hasattr(e, 'reason'):
                    print(e.reason)
                time.sleep(10)
            except Exception as e:
                print('Exception:'+str(e))
                time.sleep(1)
    #爬取写入完成后关闭文件
    fh.close()
    html2 = '''
    </body>
    </html>
    '''
    #写入html2
    fh = open('C:/Users/Shinelon/Documents/GitHub/weixintext_crawer/text.html','ab')
    fh.write(html2.encode('utf-8'))#注意这里不要忘记了编码
    fh.close()
    

key='物联网'
proxy1 = '112.82.137.31:808'
proxy2 = '111.76.227.249:808'
pagestart = 1
pageend = 2
urllist = geturllist(key, pagestart, pageend, proxy1)
getcontent(urllist, proxy2)

            
        
        
    
    