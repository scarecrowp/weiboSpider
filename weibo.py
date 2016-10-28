# coding: utf-8
import urllib2
import re
import json
import csv
from bs4 import BeautifulSoup
import codecs
cookie = 'SINAGLOBAL=674332752823.8296.1444439311014; SSOLoginState=1477033633; wvr=6; _s_tentry=login.sina.com.cn; Apache=9710476368499.25.1477033646435; ULV=1477033646441:20:1:1:9710476368499.25.1477033646435:1471324921934; ULOGIN_IMG=14770336612731; login_sid_t=476b1d2fb9cd015acbb3a7a84b2cf327; UOR=developer.baidu.com,widget.weibo.com,login.sina.com.cn; SCF=AqliVXtf4Pe66qfvumAmHTUPB1o_gZQTktsys8qHcbBIQnaBzxJlV-NXobmpmgQZk7w3hluFfSGVgB2YlrmNWnY.; SUB=_2A251FsWoDeTxGedJ4lUW-CrEyziIHXVWZbBgrDV8PUNbmtBeLWXdkW8raK4yHGs_c2pI9vz-cd-5A9eLUw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5a44_asFynclfP5xSxg2HO5JpX5KMhUgL.Fo2N1KMN1hBRehB2dJLoIpXLxKMLBKnLB.zLxKnL12BL1h.LxKBLB.2LB.87M5tt; SUHB=0OMl_GV7uBH86Q; ALF=1509157233'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0',
    'cookie': cookie
}
#
def visit():
    result = []
    pagecount = 22636/20+1
    lastPage = [40,41,43,44,45,46,47,48,49,50]
    csvFile = open("weibo.csv", 'ab')
    writer = csv.writer(csvFile,dialect='excel')

    for i in range(16,51):
        url = 'http://s.weibo.com/user/%25E5%258C%25BB%25E7%2594%259F&auth=per_vip&page='+str(i)
        req = urllib2.Request(url, headers=headers)
        text = urllib2.urlopen(req).read()
    #<a class=\"W_texta W_fb\" target=\"_blank\" href=\”(.+?)\” title=\"\u5c0f\u513f\u5916\u79d1\u88f4\u533b\u751f\" uid=\”(.+?)\” suda-data=\"key=tblog_search_user&value=user_feed_page_name\”>(.+?)
        # print the title, check if you login to weibo sucessfully
        pat_title = re.compile(r'view\((.+?)\)</script>')
        r = pat_title.findall(text)
        data = json.loads(r[2])
       # print data['html']
        html = data['html']

        soup = BeautifulSoup(html,'html.parser')
        print(i)
        if soup.find_all('p','code_tit'):
            print('结束:' + str(i))
            break;
        else:
            print soup
            for pd in soup.find_all('div','person_detail'):
                row = []
                name = pd.p.a['title'].encode('utf-8').strip()
                if name:
                    home = pd.p.a['href'].encode('utf-8').strip()
                    print 'name:'+name

                    info = ''+pd.find('p', {'class': 'person_card'}).contents[0].encode('utf-8').strip()+''
                    person_num =''+pd.find('p', {'class': 'person_num'}).findAll('span')[1].a.contents[0].encode('utf-8').strip()+''#person_num
                   # print(person_num)
                    # csvFile.write(name+';')
                    # csvFile.write(home)
                    #csvFile.write('\n')
                    row.append(name)#微博名称
                    row.append(home)#微博地址
                    row.append(info)
                    row.append(person_num)
                    writer.writerow(row)
                else:
                    print('结束:'+str(i))
                    return
            #row.append(u'a's)
            #row.append(u'b')
            #print pd.find('p', {'class': 'person_card'}).contents[0]
            #row.append(pd.find('p', {'class': 'person_card'}).contents[0].encode('utf-8').strip())
            #result.append(row)

            #writer.writerow([name, home])
            #print row
            #print '-'+pd.p.a['title']
    #doc = re.compile(r'<div class="person_detail">(.+?)')

    #write_data(result, 'weibo.csv')
def write_data(data, name):
    file_name = name
    with open(file_name, 'wb') as f:
            f_csv = csv.writer(f,dialect='excel')
            f_csv.writerows(data)
if __name__ == '__main__':
    visit() 

