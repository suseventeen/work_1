import pandas as pd
import jieba
import nltk


def words_split(filename):
    """分词"""
    read_data = pd.read_csv(filename, nrows=1000)
    words_split = []
    for i in range(len(read_data)):
        row_data_2 = read_data.iloc[i, 2]  # 读取headline描述文本
        list_row_data = list(jieba.cut(row_data_2))  # 进行分词
        list_row_data = [x for x in list_row_data if x != ' ']  # 去除列表中的空格字符
        words_split.append(list_row_data)
    return words_split


def words_clean(list_words):
    """词法分析"""
    words_clean = []
    for words in list_words:
        words_new = []
        for word in words:
            if 'a' <= word[0] <= 'z' or 'A' <= word[0] <= 'Z':
                words_new.append(word.lower())
        if words_new:
            words_clean.append(words_new)
    return words_clean


def stopwords_filter(filename, list_words):
    """停用词过滤"""
    list_filter_stopwords = []  # 声明一个停用词过滤后的词列表
    with open(filename, 'r') as fr:
        stop_words = list(fr.read().split('\n'))  # 将停用词读取到列表里
        for i in range(len(list_words)):
            word_list = []
            for j in list_words[i]:
                if j not in stop_words:
                    word_list.append(j.lower())
            list_filter_stopwords.append(word_list)
    return list_filter_stopwords


def words_stemming(list_words):
    """词干化"""
    porter = nltk.PorterStemmer()
    list_stemming = []
    for words in list_words:
        list_new = []
        for word in words:
            word_new = porter.stem(word)
            list_new.append(word_new)
        list_stemming.append(list_new)
    return list_stemming


def words_dict(list_words):
    """词典化"""
    # 建立初始词典并统计df
    list_tmp = []
    df_tmp = []
    for words in list_words:
        for word in words:
            if word not in list_tmp:
                list_tmp.append(word)
                df_tmp.append(1)
            else:
                i = list_tmp.index(word)
                df_tmp[i] += 1
    # 过滤掉df小于3的词
    list_dic = []
    list_df = []
    for i in range(len(list_tmp)):
        if df_tmp[i] > 3:
            list_dic.append(list_tmp[i])
            list_df.append(df_tmp[i])
    # 给每个词添加序列
    dict = []
    df = []
    i = 1
    for word in list_dic:
        dict.append(str(i) + ':' + word)
        df.append(str(i) + ':' + str(list_df[i - 1]))
        i += 1
    return dict, df, list_dic, list_df


def words_fw(list_words, df_list, dic_list):
    """特征权重计算"""
    list_tf = []
    list_fw = []
    for words in list_words:
        part_dic = []
        part_tf_tmp = []
        part_tf = []
        part_fw = []
        for word in words:
            if word in dic_list:
                if word not in part_dic:
                    part_dic.append(word)
                    part_tf_tmp.append(1)
                else:
                    part_tf_tmp[part_dic.index(word)] += 1
        for i in range(len(part_dic)):
            index_word = dic_list.index(part_dic[i]) + 1
            fw_word = round(part_tf_tmp[i] / df_list[index_word - 1], 5)  # 特征权重保留到小数点后五位
            part_tf.append(str(index_word) + ':' + str(part_tf_tmp[i]))
            part_fw.append(str(index_word) + ':' + str(fw_word))
        list_tf.append(part_tf)
        list_fw.append(part_fw)
    return list_tf,list_fw
