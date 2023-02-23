import requests
import pymysql
from lxml import etree

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30",
            "Referer":"http://www.chongqu.com.cn/chongwudaquan/"}

prefix = "http://www.chongqu.com.cn/"

id = 0

#从网站1获得每个宠物具体信息所在的url
def getUrls(page,headers=headers):
    url = f"http://www.chongqu.com.cn/chongwudaquan/list_22_{page}.html"
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    tree = etree.HTML(response.text)
    return tree.xpath('//p[@class="info-t"]/a/@href')

#从网站2获得每个宠物具体信息所在的url
def getUrls_2():
    urls = []
    prefix = "https://www.mengchong.cn/daquan/"
    r = requests.get(prefix,headers=headers)
    r.encoding = r.apparent_encoding
    tree = etree.HTML(r.text)
    for i in range(3,10):
        raw = tree.xpath(f"//ul[@class='in_hotstar cwdaquan'][{i}]/a/@href")
        urls.extend([prefix[:-8] + i for i in raw])
    return urls

#从网站1获取猫和犬类信息
def getData_cat_and_dog(url,headers=headers):
    try:
        # exception_urls = []
        data = {}
        response = requests.get(url,headers=headers)
        response.encoding = response.apparent_encoding
        tree = etree.HTML(response.text)

        # get features
        flags = tree.xpath('//ul[@class="list fl"]//span[@class="flag"]/text()')
        for i in range(len(flags)):
            part = tree.xpath(f'//ul[@class="list fl"]/li[{i+1}]/span[@class="part"]/text()')
            if part:
                data[flags[i][:-1]] = part[0]
            else:
                data[flags[i][:-1]] = '--'

        # get stars
        score_flags = tree.xpath('//ul[@class="list"]//span[@class="flag"]/text()')
        for i in range(len(score_flags)):
            score = tree.xpath(f'//ul[@class="list"]/li[{i+1}]/span[@class="part"]/i/@class')[0]
            if score[-1] == '0':
                data[score_flags[i][:-1]] = '5.0'
            else:
                data[score_flags[i][:-1]] = str(int(score[-1])/2)

        # get price
        price = tree.xpath('//ul[@class="list fl"]/node()')[19].text[69:-19]
        if price and price[-1] == '元':
            data['价格'] = price
        else:
            data['价格'] = '--'

        # get basic_intro
        paras = tree.xpath('//div[@id="j-basic"]/div[@class="pet-info-txt"][2]/p/text()')
        origin = '\n'.join([para.strip() for para in paras if para.strip()])
        if not origin:
            paras = tree.xpath('//div[@id="j-basic"]/div[@class="pet-info-txt"][2]//span/text()')
            origin = '\n'.join([para.strip() for para in paras if para.strip()])
            if not origin:
                paras = tree.xpath('//div[@id="j-basic"]/div[@class="pet-info-txt"][1]/p/text()')
                origin = '\n'.join([para.strip() for para in paras if para.strip()])
                if not origin:
                    origin = '--'
        data['发展起源'] = origin

        # get species
        if data['中文名'][-1] in ['猫','比']:
            data['宠物类别'] = '猫'
        else:
            data['宠物类别'] = '犬'

        # get characteristics
        char_full = []
        char_flags = tree.xpath('//div[@id="j-spec"]/div[@class="pet-info-t"]/text()')
        for i in range(len(char_flags)):
            char_full.append(char_flags[i])
            char_full.extend(tree.xpath(f'//div[@id="j-spec"]/div[@class="pet-info-txt"][{i+1}]/*/text()'))
        chars = '\n'.join([char.strip() for char in char_full])
        if chars:
            data['品种特点'] = ''.join(chars)
        else:
            data['品种特点'] = '--'
            # print(url)
        
        # get picture urls
        pic_urls = []
        for url in tree.xpath('//div[@class="pet-info-txt"]//img/@src'):
            if url[0] == 'h':
                pic_urls.append(url)
            else:
                pic_urls.append(prefix + url)
        if pic_urls:
            data['图片链接'] = str(pic_urls)
        else:
            pic_urls = [ prefix + url for url in tree.xpath('//div[@class="pet-info-t"]//img/@src')]
            if not pic_urls:
                data['图片链接'] = '--'
            data['图片链接'] = str(pic_urls)

        # get knowledge
        char_full = []
        char_flags = tree.xpath('//div[@id="j-know"]/div[@class="pet-info-t"]/text()')
        for i in range(len(char_flags)):
            char_full.append(char_flags[i])
            char_full.extend(tree.xpath(f'//div[@id="j-know"]/div[@class="pet-info-txt"][{i+1}]/*/text()'))
        chars = '\n'.join([char.strip() for char in char_full])
        if chars:
            data['养宠知识'] = ''.join(chars)
        else:
            data['养宠知识'] = '--'
            # print(url)
        
        # get attention
        char_full = []
        char_flags = tree.xpath('//div[@id="j-attention"]/div[@class="pet-info-t"]/text()')
        for i in range(len(char_flags)):
            char_full.append(char_flags[i])
            char_full.extend(tree.xpath(f'//div[@id="j-attention"]/div[@class="pet-info-txt"][{i+1}]/*/text()'))
        chars = '\n'.join([char.strip() for char in char_full])
        if chars:
            data['注意事项'] = ''.join(chars)
        else:
            data['注意事项'] = '--'

        global id
        data['ID'] = id
        id += 1

        # print(data)
        return data

    except Exception as e:
        print(f"异常页面：{url}",repr(e))
        # exception_urls.append(url)

#从网站2获取其他宠物信息
def getData_others(url):
    data = {}
    r = requests.get(url,headers=headers)
    r.encoding = r.apparent_encoding
    tree = etree.HTML(r.text)

    flags = tree.xpath("//ul[@class='cwintro_left']//span/text()") + tree.xpath("//ul[@class='cwintro_right']//span/text()")
    # print(flags)
    contents = []
    for i in range(len(flags)):
        if i<5 :
            content_i = tree.xpath(f"//ul[@class='cwintro_left']//li[{i+1}]/i/text()")
        else:
            content_i = tree.xpath(f"//ul[@class='cwintro_right']//li[{i-4}]/i/text()")
        # print(content_i)
        if content_i:
            contents.append(content_i[0])
        else:
            contents.append('--')
        if flags[i]=='全名：':
            data['中文名'] = contents[i]
        elif flags[i]=='毛发：':
            data['毛长'] = contents[i]
        else:
            if flags[i][0] != '饲':
                data[flags[i][:-1]] = contents[i]
        data['英文名'] = data['体味程度'] = data['体重'] = data['肩高'] = data['毛色'] = data['耐热程度'] = data['耐寒程度'] = data['友善程度'] = data['粘人程度'] = data['运动量'] = data['护家程度']= data['口水程度'] = data['关爱需求']= data['养宠知识']= data['注意事项']= data['发展起源']='--'

    # print(data['中文名'][-1])

    if data['中文名'][-1] in ('鱼','鲤','虾'):
        data['宠物类别'] = '鱼'
    elif data['中文名'][-1] in ('鸟','鹉','雀','哥','鸫'):
        data['宠物类别'] = '鸟'
    elif data['中文名'][-1] in ('鼠','鼯') or data['中文名'][:-1] == '荷兰':
        data['宠物类别'] = '鼠'
    elif data['中文名'][-1] == '猪':
        data['宠物类别'] = '猪'
    elif data['中文名'][-1] == '兔':
        data['宠物类别'] = '兔'
    elif data['中文名'][-1] == '龟':
        data['宠物类别'] = '龟'
    else:
        data['宠物类别'] = '其他爬宠'

    score = tree.xpath("//ul[@class='score']//code/@class")
    score_flag = ['掉毛程度','喜叫程度','美容程度','干净程度','智商','饲养难度','可训程度','综合']
    for i in range(7):
        if i != 3:
            if score[i][-1].isdigit():
                data[score_flag[i]] = str(int(score[i][-1])/2)
            else:
                data[score_flag[i]] = '--'
    
    data['品种特点'] = '\n'.join(tree.xpath("//div[@class='cwmain']//p/text()"))

    data['图片链接'] = str(["https://www.mengchong.cn" + tree.xpath("//div[@class='page_chongwu_left']//@*")[1]])

    global id
    data['ID'] = id
    id += 1

    # print(data)
    return data

#将信息写入数据库操作
def insertData(datalist):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='pwz20011121',
        db='test',  
        charset='utf8')

    cursor = conn.cursor() 

    cols = ','.join(key for key in datalist[0].keys())
    placeholders = ','.join(f'%({key})s' for key in datalist[0].keys())
    sql_line = f'INSERT INTO pet_data ({cols}) VALUES ({placeholders})'
    for i in range(len(datalist)):
        try:
            cursor.execute(sql_line,datalist[i])
            conn.commit()
        except Exception as e:
            print(i,repr(e))

#封装执行函数1
def act_data1_to_db():
    urls = [prefix + getUrls(page)[k] for page in range(1,33) for k in range(10)] + [prefix + getUrls(33)[0]]
    full_data = []
    for url in urls:
        full_data.append(getData_cat_and_dog(url))
    insertData(full_data)

#封装执行函数2
def act_data2_to_db():
    urls = getUrls_2()
    full_data = []
    for url in urls:
        full_data.append(getData_others(url))
    insertData(full_data)

#调用执行函数，完成从爬取信息到写入数据库全过程
act_data1_to_db()
act_data2_to_db()

def accessData(name):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='pwz20011121',
        db='test',  
        charset='utf8')

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pet_data WHERE 中文名 like "%%%%%s%%%%"'% f'{name}')
    res = cursor.fetchall()
    print(len(res))
