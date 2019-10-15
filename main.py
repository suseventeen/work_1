# -*- coding: utf-8 -*-

import pandas as pd
import jieba
import nltk


def word_split(filename):
    read_data = pd.read_csv(filename, nrows=1000)
    title_word_split = []
    headline_words_split = []
    for i in range(len(read_data)):
        row_data = read_data.iloc[i, 1]  # 读取title描述文本
        list_row_data = list(jieba.cut(row_data))  # 进行分词
        list_row_data = [x for x in list_row_data if x != ' ']  # 去除列表中的空格字符
        title_word_split.append(list_row_data)

        row_data_2 = read_data.iloc[i, 2]  # 读取headline描述文本
        list_row_data = list(jieba.cut(row_data_2))  # 进行分词
        list_row_data = [x for x in list_row_data if x != ' ']  # 去除列表中的空格字符
        headline_words_split.append(list_row_data)

    return title_word_split, headline_words_split


def word_clean(list_words):#词法分析
    list_words_clean = []
    for words in list_words:
        words_new = []
        for word in words:
            if 'a' <= word[0] <= 'z' or 'A' <= word[0] <= 'Z':
                words_new.append(word.lower())
        if words_new!=[]:
            list_words_clean.append(words_new)
    return list_words_clean




def stopwords_filter(filename, list_words_lemmatizer):
    list_filter_stopwords = []  # 声明一个停用词过滤后的词列表
    with open(filename, 'r') as fr:
        stop_words = list(fr.read().split('\n'))  # 将停用词读取到列表里
        for i in range(len(list_words_lemmatizer)):
            word_list = []
            for j in list_words_lemmatizer[i]:
                if j not in stop_words:
                    word_list.append(j.lower())
            list_filter_stopwords.append(word_list)
        return list_filter_stopwords


def word_lemmatizer(list_words):  #词干化
    porter = nltk.PorterStemmer()
    list_words_lemmatizer = []
    for words in list_words:
        list_new = []
        for word in words:
            word_new = porter.stem(word)
            list_new.append(word_new)
        list_words_lemmatizer.append(list_new)
    return list_words_lemmatizer



def words_dictionary(list_word):
    list=[]
    list1=[]
    dict=[]
    spe=[]
    words=[]
    nums=[]
    for obj in list_word:
        for word in obj:
            if word not in words:
                nums.append(1)
                words.append(word)
                list.append(word)
            else:
                a=words.index(word)
                nums[a]=nums[a]+1
    i=1
    for num in nums:
        list1.append(num)
        i=i+1
    list2=[]
    list3=[]
    i=0
    for num in list1:
        if num>3:
            list2.append(list[i])
            list3.append(list1[i])
        i=i+1
    i=1
    for obj in list2:
        dict.append(str(i)+':'+obj)
        i=i+1
    i = 1
    for obj in list3:
        spe.append(str(i) + ':' + str(obj))
        i = i + 1
    return dict,spe,list2,list3


def tf_df_list(list_word, df_list, dic_list):
    ans=[]
    ans1=[]
    for list in list_word:
        cmp=[]
        cmp1=[]
        anscp=[]
        tmp=[]
        tmp1=[]
        for word in list:
            if word in dic_list:
                if word not in cmp:
                    cmp.append(word)
                    cmp1.append(df_list[dic_list.index(word)])
                    anscp.append(1)
                else:
                    a=cmp.index(word)
                    anscp[a]=anscp[a]+1
        i=0
        cmp2=cmp1[:]
        for num in cmp2:
            cmp1[i]=anscp[i]/num
            i=i+1
        i=1
        for obj in anscp:
            tmp.append(str(dic_list.index(cmp[i-1])+1)+':'+str(obj))
            tmp1.append(str(dic_list.index(cmp[i-1])+1)+':'+str(cmp1[i-1]))
            i=i+1
        ans.append(tmp)
        ans1.append(tmp1)
    return ans,ans1


if __name__ == '__main__':
    title_word_split, headline_word_split = word_split('News_Final.csv')  # 获得每条文本的分词列表和标签列表
    ##print(title_word_split)
    print(headline_word_split)
    print('分词成功')
    ##title_word_split=word_clean(title_word_split)
    headline_word_split = word_clean(headline_word_split)       # 词性分析
    ##print(title_word_split)
    print(headline_word_split)
    print('词性分析成功')
    ##title_filter_stopwords = stopwords_filter('stopwords.txt', title_word_split)
    headline_filter_stopwords = stopwords_filter('stopwords.txt', headline_word_split)  # 获得停用词过滤后的列表
    ##print(title_filter_stopwords)
    print(headline_filter_stopwords)
    print('停用词过滤成功')
    ##title_words_lemmatizer = word_lemmatizer(title_filter_stopwords)
    headline_words_lemmatizer = word_lemmatizer(headline_filter_stopwords)  # 词性还原
    ##print(title_words_lemmatizer)
    print(headline_words_lemmatizer)
    print('词干化成功')
    ##title_words_dictionary,title_specify,title_list,title_numlist=words_dictionary(title_words_lemmatizer)
    headline_words_dictionary,headline_specify ,headline_list,headline_numlist= words_dictionary(headline_words_lemmatizer)
    ##print(title_words_dictionary)
    print(headline_words_dictionary)
    print('词典化成功')
    ##print(title_specify)
    print(headline_specify)
    print('df计算成功')
    ##dictionary_title = pd.DataFrame(data=title_words_dictionary)
    dictionary_headline = pd.DataFrame(data=headline_words_dictionary)
    ##feature_title = pd.DataFrame(data=title_specify)
    feature_headline = pd.DataFrame(data=headline_specify)
    ##dictionary_title.to_csv('Output/dictionary_title.csv', index=0, header=0)
    dictionary_headline.to_csv('Output/dictionary_headline.csv', index=0, header=0)
    ##feature_title.to_csv('Output/feature_title.csv', index=0, header=0)
    feature_headline.to_csv('Output/feature_headline.csv', index=0, header=0)
    deadline_ans ,deadline_tf_df= tf_df_list(headline_words_lemmatizer, headline_numlist, headline_list)
    ans_headline=pd.DataFrame(data=deadline_ans)
    ans_headline.to_csv('Output/ans_headline.csv', index=0, header=0)
    tf_df_headline = pd.DataFrame(data=deadline_tf_df)
    tf_df_headline.to_csv('Output/tf_df_headline.csv', index=0, header=0)
    f=open('tf_df_headline.txt','w')
    for i in deadline_tf_df:
        k=''.join([str(j+' ') for j in i])
        f.write(k+'\n')
    f.close()
    print('文件输出成功，以保存到Output文件夹中')