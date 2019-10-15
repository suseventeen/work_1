# -*- coding: utf-8 -*-

import work_function as wf
import pandas as pd

if __name__ == '__main__':
    headline_words_split = wf.words_split('News_Final.csv')  # 获得分词后的列表
    print(headline_words_split)
    print('分词成功')
    headline_words_clean = wf.words_clean(headline_words_split)  # 词性分析
    print(headline_words_clean)
    print('词性分析成功')
    headline_filter_stopwords = wf.stopwords_filter('stopwords.txt', headline_words_clean)  # 获得停用词过滤后的列表
    print(headline_filter_stopwords)
    print('停用词过滤成功')
    headline_words_stemming = wf.words_stemming(headline_filter_stopwords)  # 词性还原
    print(headline_words_stemming)
    print('词干化成功')
    dictionary, df, dic_list, df_list = wf.words_dict(headline_words_stemming)
    print(dictionary)
    print('词典化成功')
    print(df)
    print('df计算成功')
    dictionary_headline = pd.DataFrame(data=dictionary)
    df_headline = pd.DataFrame(data=df)
    dictionary_headline.to_csv('Output/dictionary_headline.csv', index=0, header=0)
    df_headline.to_csv('Output/df_headline.csv', index=0, header=0)
    deadline_tf, deadline_fw = wf.words_fw(headline_words_stemming, df_list, dic_list)
    tf_headline = pd.DataFrame(data=deadline_tf)
    tf_headline.to_csv('Output/tf_headline.csv', index=0, header=0)
    fw_headline = pd.DataFrame(data=deadline_fw)
    fw_headline.to_csv('Output/fw_headline.csv', index=0, header=0)
    print('文件输出成功，已保存到Output文件夹中')
