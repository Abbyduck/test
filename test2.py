from bs4 import BeautifulSoup
import re
import csv

def getDocument(page):
    page = str(page)
    # path_name = '10' + '\\content.txt'
    path_name = '10' + '\\words.txt'

    # file = open(path_name, 'w+',encoding='utf-8') #创建文件
    # file2 = open(path_name2, 'w+',encoding='utf-8') #创建文件

    #由于要搜索的关键词是中文，所以需要进行转码，这里调用了urllib.pathname2url函数
    #print(response.read())
    htmlf=open('page/'+page+'.html','r',encoding="utf-8")
    document=htmlf.read()
    #将网页源码用UTF-8解码
    soup = BeautifulSoup(document, 'html.parser')
    items_name = re.findall(r'data-hippo-type="shop"\stitle="([^"]+)"', document, re.S)  #正则匹配出商家名
    items_address = re.findall(r'<span\sclass="addr">([^\s]+)</span>', document, re.S)   #正则匹配出地址
    items_star = re.findall(r'<span\sclass="sml-rank-stars sml-str([^\s]+)"', document, re.S)   #正则匹配出星级
    tmp_price = soup.find_all('a', attrs = {'class': 'mean-price'})
    items_price=re.findall(r'<a\s.*?>.*?([￥(\d+)|-]+)(?:</b>)*.*?</a>',str(tmp_price),re.S)#正则匹配出价钱
    tmp_review = soup.find_all('a', attrs = {'class': 'review-num'})
    items_review=re.findall(r'<a\s.*?>[\s\S]*?<b>(.*?)</b>',str(tmp_review),re.S) #正则匹配出评论数目
    datas = [items_name,items_address,items_star,items_price,items_review]
    result = ''
    # for index in range(len(items_name)):
    #     result += items_name[index] + '  ' + items_address[index] + '  ' + items_star[index] +'  ' + items_price[index] +'  ' + items_review[index] + '\n'
    # file.write(result)                                                                   #将结果存入文件
    # file.close()
    result_csv = []
    for index in range(len(items_name)):
        tmp=[]
        for i in range(0,5):
            tmp.append(datas[i][index])
        result_csv.append(tmp)
    return result_csv



def start_crawl2():
    path_name2 = '10' + '\\content.csv'

    result_csv=[]
    for index in range(0, 2):
        result_csv +=getDocument(index)


    with open(path_name2, "w+", newline='',encoding='utf-8') as f:
         # with open(birth_weight_file, "w") as f:
        writer = csv.writer(f)
        writer.writerows([['店名','地址','星星','人均','评论数']])
        writer.writerows(result_csv)
        f.close()
    print (result_csv)

def is_the_only_string_within_a_tag(s):
    """Return True if this string is the only child of its parent tag."""
    return (s == s.parent.string)
def crawl_words():

    htmlf=open('page/words.html','r',encoding="utf-8")
    document=htmlf.read()
    #将网页源码用UTF-8解码
    soup = BeautifulSoup(document, 'html.parser')
    #中文翻译
    cn_definition = soup.find_all('div', attrs = {'class': 'cndf'})
    cn_defs=re.findall(r'<span\s.*?>(.*?)</span>',str(cn_definition),re.S)
    cn_def=''
    for index in range(len(cn_defs)):
        cn_def += cn_defs[index] +' '
    #英文解释
    en_definition = soup.find_all('div', attrs = {'id': 'review-definitions'})
    en_def_soup=BeautifulSoup(str(en_definition), 'html.parser')
    en_defs_speech = en_def_soup.find_all('span', attrs = {'class': 'part-of-speech'})
    en_defs = en_def_soup.find_all('span', attrs = {'class': 'content'})
    en_defs_speech=re.findall(r'<span\s.*?>(.*?)</span>',str(en_defs_speech),re.S) #英文词性
    en_defs=re.findall(r'<span\s.*?>(.*?)</span>',str(en_defs),re.S) #英文翻译
    en_def=''
    for index in range(len(en_defs)):
        en_def += en_defs_speech[index]+'. '+ en_defs[index] +'\n '
    #例子
    example = soup.find_all('div', attrs = {'id': 'ex-sys-box'})
    example_soup=BeautifulSoup(str(example), 'html.parser')
    example=example_soup.get_text().replace('  ','').replace('喜欢（0） 不喜欢（0） 更多','').replace('\n','')

    detail={}
    detail['cndf']=cn_def.replace('\n',' ')
    detail['endf']=en_def
    detail['example']=example
    print(detail)
    # return detail



def test_for_dict():
    dic= {"objects": [
            {
                "pronunciations": {
                    "uk": "'embriəʊ",
                    "us": "'embrioʊ"
                },
                "en_definitions": {
                    "n": [
                        "(botany) a minute rudimentary plant contained within a seed or an archegonium",
                        "an animal organism in the early stages of growth and differentiation that in higher forms merge into fetal stages but in lower forms terminate in commencement of larval life"
                    ]
                },
                "audio_addresses": {
                    "uk": [
                        "https://media-audio1.baydn.com/uk%2Fe%2Fem%2Fembryo_v3.mp3",
                        "http://media-audio1.qiniu.baydn.com/uk/e/em/embryo_v3.mp3"
                    ],
                    "us": [
                        "https://media-audio1.baydn.com/us%2Fe%2Fem%2Fembryo_v3.mp3",
                        "http://media-audio1.qiniu.baydn.com/us/e/em/embryo_v3.mp3"
                    ]
                },
                "uk_audio": "http://media.shanbay.com/audio/uk/embryo.mp3",
                "conent_id": 5,
                "audio_name": "embryo_v3",
                "cn_definition": {
                    "pos": "",
                    "defn": "n. 胚胎,萌芽"
                },
                "num_sense": 1,
                "content_id": 5,
                "content_type": "vocabulary",
                "sense_id": 0,
                "id": 5,
                "definition": " n. 胚胎,萌芽",
                "url": "https://www.shanbay.com/bdc/mobile/preview/word?word=embryo",
                "en_definition": {
                    "pos": "n",
                    "defn": "(botany) a minute rudimentary plant contained within a seed or an archegonium; an animal organism in the early stages of growth and differentiation that in higher forms merge into fetal stages but in lower forms terminate in commencement of larval life"
                },
                "object_id": 5,
                "learning_id": 901153662503184,
                "content": "embryo",
                "pron": "'embrioʊ",
                "pronunciation": "'embrioʊ",
                "id_str": "giwnn",
                "audio": "http://media.shanbay.com/audio/us/embryo.mp3",
                "us_audio": "http://media.shanbay.com/audio/us/embryo.mp3"
            },
            {
                "pronunciations": {
                    "uk": "ɑːtʃ",
                    "us": "ɑːrtʃ"
                },
                "en_definitions": {
                    "n": [
                        "a curved shape in the vertical plane that spans an opening",
                        "a curved bony structure supporting or enclosing organs (especially the inner sides of the feet)",
                        "a passageway under a curved masonry construction"
                    ],
                    "adj": [
                        "(used of behavior or attitude) characteristic of those who treat others with condescension",
                        "expert in skulduggery",
                        "naughtily or annoyingly playful"
                    ],
                    "v": [
                        "form an arch or curve"
                    ]
                },
                "audio_addresses": {
                    "uk": [
                        "https://media-audio1.baydn.com/uk%2Fa%2Far%2Farch_v3.mp3",
                        "http://media-audio1.qiniu.baydn.com/uk/a/ar/arch_v3.mp3"
                    ],
                    "us": [
                        "https://media-audio1.baydn.com/us%2Fa%2Far%2Farch_v3.mp3",
                        "http://media-audio1.qiniu.baydn.com/us/a/ar/arch_v3.mp3"
                    ]
                },
                "uk_audio": "http://media.shanbay.com/audio/uk/arch.mp3",
                "conent_id": 215,
                "audio_name": "arch_v3",
                "cn_definition": {
                    "pos": "",
                    "defn": "n. 拱门,弓形\nvt. 使成弓形弯曲, 拱起\nvi. 成弓形, 用拱连接\nadj. 主要的,调皮的"
                },
                "num_sense": 1,
                "content_id": 215,
                "content_type": "vocabulary",
                "sense_id": 0,
                "id": 215,
                "definition": " n. 拱门,弓形\nvt. 使成弓形弯曲, 拱起\nvi. 成弓形, 用拱连接\nadj. 主要的,调皮的",
                "url": "https://www.shanbay.com/bdc/mobile/preview/word?word=arch",
                "en_definition": {
                    "pos": "n",
                    "defn": "a curved shape in the vertical plane that spans an opening; a curved bony structure supporting or enclosing organs (especially the inner sides of the feet); a passageway under a curved masonry construction"
                },
                "object_id": 215,
                "learning_id": 901153662667031,
                "content": "arch",
                "pron": "ɑːrtʃ",
                "pronunciation": "ɑːrtʃ",
                "id_str": "bvzunx",
                "audio": "http://media.shanbay.com/audio/us/arch.mp3",
                "us_audio": "http://media.shanbay.com/audio/us/arch.mp3"
            }]}
    for word in dic['objects']:
        temp={}
        temp['content']=word['content']
        temp['us_audio']=word['us_audio']
        temp['pronunciation']=word['pronunciation']
        temp['cn_definition']=word['cn_definition']['defn']
        temp['en_definition']=word['en_definition']['defn']

        print(temp)
# test_for_dict()   #开始爬数据！

import time
def test_write_txt(new_context):
    txtName = "txt/"+time.strftime('%Y%m%d',time.localtime(time.time()))+".txt"
    f=open(txtName, "w")

    f.write(new_context)

    f.close()

def test_range():
    total_page=43//10

    page=1
    words_list={'objects':['dd',page]}
    for page in range(1,total_page+2):

        for word in words_list['objects']:
            print(word)

        words_list = {'objects':['dd',page+1]}

def test_string():
    sql=''
    a=1
    b='ss'
    sql+= '("'+b+'",'+str(a)+')'
    # sql ='("sdsf",sdf,2)'
    print(sql)
# crawl_words()


import pymysql
def link_db():
    db = pymysql.connect(host='localhost',user='root',passwd='mysql',db='vocabulary',port=3306,charset='utf8')
    cursor=db.cursor()
    words=cursor.execute('select content from words limit 10')

    words=cursor.fetchall()
    words_list=[]
    for word in words:
        words_list.append(word[0])

    if 'embryoo' not in words_list:
        words_list.append('embryoo')
    print(words_list)
    cursor.close()
    db.close()

link_db()
