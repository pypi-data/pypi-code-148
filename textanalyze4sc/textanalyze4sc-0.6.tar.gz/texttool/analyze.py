import jieba
import numpy as np
import pandas as pd
from pprint import pprint
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim import corpora, models, similarities
import networkx as nx

import wordcloud
import time
from matplotlib.pylab import datestr2num


import numpy as np
# Plotting tools
import pyLDAvis
import pyLDAvis.gensim
import matplotlib.pyplot as plt

import jieba.analyse as analyse
from pandas import Series, DataFrame
import pandas as pd
import seaborn as sns
import hanlp
from cnsenti import Sentiment
from cnsenti import Emotion


# Enable logging for gensim - optional
# import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)


def time_tran(number):
    StyleTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(number))
    return StyleTime

#/home/bqw/gradual
def load_data(text_path):
    with open(text_path+'/body.txt', 'r', encoding='utf-8') as f:
        body_text = [i for i in list(f.readlines())]
    with open(text_path+'/title.txt', 'r', encoding='utf-8') as f:
        title_text = [i for i in list(f.readlines())]
    with open(text_path+'/time.txt', 'r', encoding='utf-8') as f:
        time_text = [i for i in list(f.readlines())]
    
    body_text=[meta.replace('\n','') for meta in body_text]
    title_text=[meta.replace('\n','') for meta in title_text]
    time_text=[int(eval(meta.replace('\n',''))) for meta in time_text]

    data_pd = {'title_text':title_text,
            'body_text':body_text,
            'time_text':time_text}
    df_data = DataFrame(data_pd)
    df_data.time_text=df_data.time_text.apply(time_tran)

    df_data=df_data.drop(df_data[(df_data['body_text'].eq('') | df_data['title_text'].eq(''))].index)
    def month_cut(text):
        return text[:7]
    def hour_cut(text):
        return text[11:13]
    df_data['month']=df_data.time_text.apply(month_cut)
    df_data['hour']=df_data.time_text.apply(hour_cut)
    
    return df_data


def trend_plot(df_data,work_dir='/home/bqw/gradual/analyzetext/'):
    group1 = df_data.groupby('month')
    group1_data=group1.size()
    
    
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']

    # x = range(len(data))
    x_date = [datestr2num(i) for i in list(group1_data.index)]
    plt.figure(figsize=(10,5))
    plt.title("三联生活周刊发布量变化图")
    plt.xlabel("时间")
    plt.xticks(rotation=45)
    plt.ylabel("发布量")
    plt.plot_date(list(group1_data.index),group1_data.values,'-',label="收盘价")
    # plt.plot_date(x_date,data['high'],'-',color='r',label="最高价")
    # plt.legend()
    plt.grid()
    plt.savefig(work_dir+'./amount.jpg')
    return

def hot_plot(df_data,work_dir='/home/bqw/gradual/analyzetext/'):
    group1 = df_data.groupby('month')
    group1_data=group1.size()
    
    group2 = df_data.groupby(['month', 'hour'])
    hot_matrix=np.zeros((12, 24))
    group2_data=group2.size()
    
    # month_map_dic=dict(zip(list(group2_data.index), range(12)))
    month_map_dic=dict(zip(sorted(list(set([meta[0] for meta in list(group2_data.index)]))), range(12)))
    for cur_index, cur_count in zip(list(group2_data.index), group2_data.values):
        cur_x=month_map_dic[cur_index[0]]
        cur_y=int(cur_index[1])
        hot_matrix[cur_x][cur_y]+=cur_count
        
    plot_data=pd.DataFrame(np.transpose(hot_matrix), index=list(range(24)), columns=list(group1_data.index))

    
    plt.figure(figsize=(8, 5))
    sns.heatmap(plot_data, cmap='Reds')
    plt.savefig(work_dir+'./month_hour.jpg')
    plt.show()
    return

def get_keyword(df_data,work_dir='/home/bqw/gradual/analyzetext/'):
    text=list(df_data.body_text)
    # 创建停用词列表
    def stopwordslist(stop_path=work_dir+'/stopwords-master/baidu_stopwords.txt'):
        stopwords = [line.strip() for line in open(stop_path, 'r', encoding='UTF-8').readlines()]
        return stopwords

    # 定义停词函数 对句子进行中文分词
    def seg_depart(sentence):
        # 对文档中的每一行进行中文分词
        sentence_depart = jieba.cut(sentence.strip())
        # 创建一个停用词列表
        stopwords = stopwordslist()
        # 输出结果为outstr
        outstr = ''
        # 去停用词
        for word in sentence_depart:
            if word not in stopwords:
                if word != '\t':
                    outstr += word
                    outstr += " "
        return outstr
    # 分词后的结果
    result_fenci = []
    for i in text:
        # print(i)
        if seg_depart(i) != '':
            # print(seg_depart(i))
            result_fenci.append([i, seg_depart(i)])
    # # pd.DataFrame(result_fenci,columns=['rawtext','fencitext']).to_excel(path+'result.xlsx',index=False)
    result_fenci = [i[1].split(' ')[:-1] for i in result_fenci]
    
    def filter(text):
        return [w for w in text if len(w)>1]

    result_fenci_2gram = list(map(filter, result_fenci))
    df_data['fenci_2gram']=result_fenci_2gram
    
    keywords = analyse.textrank(''.join(result_fenci[0]), topK=50, allowPOS=('n','nz','v','vd','vn','l','a','d'))
    def extract(text):
        keywords=analyse.textrank(''.join(text), topK=50, allowPOS=('n','nz','v','vd','vn','l','a','d'))
        return keywords

    df_data['keyword_2gram']=df_data.fenci_2gram.apply(extract)
    group_key = df_data.groupby('month')

    return df_data
    
    
def word_cloud(df_data,work_dir='/home/bqw/gradual/analyzetext/'):
    group1 = df_data.groupby('month')
    group1_data=group1.size()
    
    month_keyword=dict()
    for month in list(group1_data.index):
        cur_df_data=df_data[df_data['month']==month]
        #### 
        keyword_dic=dict()
        for meta in list(cur_df_data['keyword_2gram']):
            for word in meta:
                if word not in keyword_dic:
                    keyword_dic[word]=1
                else:
                    keyword_dic[word]=keyword_dic[word]+1
        cur_top=sorted(keyword_dic.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)[:10]
        month_keyword[month]=cur_top

    #### 所有时间
    keyword_dic=dict()
    for meta in list(df_data['keyword_2gram']):
        for word in meta:
            if word not in keyword_dic:
                keyword_dic[word]=1
            else:
                keyword_dic[word]=keyword_dic[word]+1
    
    top50_all = sorted(keyword_dic.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)[:50]

    print(top50_all)


    txt=[meta[0] for meta in top50_all]
    txt=' '.join(txt)
    # 构建词云对象w，设置词云图片宽、高、字体、背景颜色等参数
    w = wordcloud.WordCloud(width=1000,
                            height=700,
                            background_color='white',
                            font_path='msyh.ttc')

    # 将txt变量传入w的generate()方法，给词云输入文字
    w.generate(txt)
    # 将词云图片导出到当前文件夹
    w.to_file(work_dir+'key_cloud.png')
    

## 返回df_data语料库前100个实体
def entity_cloud(df_data,work_dir='/home/bqw/gradual/analyzetext/'):
    tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
    # hanlp.pretrained.ner.ALL # 语种见名称最后一个字段或相应语料库
    ner = hanlp.load(hanlp.pretrained.ner.MSRA_NER_ELECTRA_SMALL_ZH)
    
    
    def extract_ner(text):
        ner_list=ner(text, tasks='ner*')
        ner_list_=[meta[0] for meta in ner_list]
        ner_dict=dict()
        for cur_ner in ner_list_:
            if cur_ner not in ner_dict:
                ner_dict[cur_ner]=1
            else:
                ner_dict[cur_ner]+=1
        ner_ = sorted(ner_dict.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)[:10]
        ner_ = [meta[0] for meta in ner_]
        return ner_
    df_data['ner_2gram']=df_data.fenci_2gram.apply(extract_ner)


    #### 所有时间
    keyword_dic=dict()
    for meta in list(df_data['ner_2gram']):
        for word in meta:
            if word not in keyword_dic:
                keyword_dic[word]=1
            else:
                keyword_dic[word]=keyword_dic[word]+1

    top50_all = sorted(keyword_dic.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)[:100]
    top50_all=[meta[0] for meta in top50_all]
    print([meta[0] for meta in top50_all])

    ##指定单词输出wordcloud
    ##过滤一部分
    ner_list_=['中国', '北京', '美国',   '三联',   '一年',   '英国',   '上海',   '晚上', '2021', '日本', '2022',    '第一个', '周末', '年代',  '欧洲', '夏天', '2020', '早上',   '世纪', '春天', '法国', '一个月', '三联生活周刊',   '云南',   '下午', '深夜', '德国', '冬天', '韩国',  '香港', '成都', '太阳', '俄罗斯', '鲁迅', '半年',   '第一人称', '春节', '地球',  '纽约', '白天', '深圳', '王海燕', '万元', '重庆', '意大利', '广东',  '第一步', '杭州', '巴黎', '四川',   '2019', '阿田', '苏州', '百年', '江南', '广州', '小贝', '一周',  '长沙',  '河南']
    ## all
    # ner_list=top50_all

    txt=' '.join(ner_list_)
    # 构建词云对象w，设置词云图片宽、高、字体、背景颜色等参数
    w = wordcloud.WordCloud(width=1000,
                            height=700,
                            background_color='white',
                            font_path='msyh.ttc')

    w.generate(txt)
    w.to_file(work_dir+'ner_cloud.png')
    return top50_all


##共现语义图，语料库：df_data，指定单词top50_all
def get_cosemantic(df_data, top50_all, work_dir='/home/bqw/gradual/analyzetext/'):
    
    keywords = [meta[0] for meta in top50_all]
    matrix = np.zeros((len(keywords)+1)*(len(keywords)+1)).reshape(len(keywords)+1, len(keywords)+1).astype(str)
    matrix[0][0] = np.NaN
    matrix[1:, 0] = matrix[0, 1:] = keywords



    # cont_list = sum(test_list, [])
    # cont_list = result_fenci
    cont_list = list(df_data.fenci_2gram)

    for i, w1 in enumerate(keywords[:50]):
        for j, w2 in enumerate(keywords[:50]):
            count = 0
            for cont in cont_list:
                if w1 in cont and w2 in cont:
    #                 if abs(cont.index(w1)-cont.index(w2)) == 0 or abs(cont.index(w1)-cont.index(w2)) == 1:
                    if abs(cont.index(w1)-cont.index(w2)) <= 3:
                        count += 1
            matrix[i+1][j+1] = count
    df = pd.DataFrame(data=matrix)
    ## 必须，去掉表头
    df.to_csv(work_dir+'con_key.csv', index=False, header=None, encoding='utf-8-sig')
    df = pd.read_csv(work_dir+'con_key.csv')

    df.index = df.iloc[:, 0].tolist()
    df_ = df.iloc[:20, 1:21]
    df_.astype(int)


    plt.figure(figsize=(10, 10))
    graph1 = nx.from_pandas_adjacency(df_)
    nx.draw(graph1, with_labels=True, node_color='yellow', font_size=15, edge_color='blue')
    plt.savefig(work_dir+'con_key.jpg')


##情感分析，text：给定文本
def get_emotion(text):
    emotion = Emotion()
    test_text = text
    ## dict
    result = emotion.emotion_count(test_text)
    return result


## 话题分析，df_data：给定语料
def get_topic(df_data):
    result_fenci = df_data.fenci_2gram
    id2word = corpora.Dictionary(result_fenci)
    id2word.filter_extremes(no_below=5, no_above=0.5)

    # 将字典转换为词袋,为文档中的每一个单词创建唯一的ID
    corpus = [id2word.doc2bow(doc) for doc in result_fenci]


    tfidf = gensim.models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    #多核并行lda模型
    tf_idf_lda_model = gensim.models.LdaMulticore(corpus_tfidf, num_topics=12, id2word=id2word, passes=2, workers=4)


    pprint(tf_idf_lda_model.print_topics(num_words=10))


    def get_topic(text):
        tmp=tf_idf_lda_model.get_document_topics(id2word.doc2bow(text))
        tmp=sorted(tmp, key=lambda x: x[1], reverse=True)
        return tmp[0][0]

    df_data['topic']=df_data.fenci_2gram.apply(get_topic)
    return df_data




