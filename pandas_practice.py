#coding:utf-8 

import pandas as pd
import numpy as np



#讀取csv檔
df_a = pd.read_csv('a_lvr_land_a.csv',encoding ='utf-8')
df_a = df_a.drop([0,0])
df_b = pd.read_csv('b_lvr_land_a.csv',encoding ='utf-8')
df_b = df_b.drop([0,0])
df_e = pd.read_csv('e_lvr_land_a.csv',encoding ='utf-8')
df_e = df_e.drop([0,0])
df_f = pd.read_csv('f_lvr_land_a.csv',encoding ='utf-8')
df_f = df_f.drop([0,0])
df_h = pd.read_csv('h_lvr_land_a.csv',encoding ='utf-8')
df_h = df_h.drop([0,0])




#將五個csv檔讀入後產生的dataframe合併
df_all = pd.concat([df_a,df_b,df_e,df_f,df_h],axis = 0)



#處理總樓層數中中文數字轉英文數字
digit = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
def trans(s):
    num = 0
    if type(s) == str:
        idx_q, idx_b, idx_s = s.find('千'), s.find('百'), s.find('十')
        if idx_q != -1:
            num += digit[s[idx_q - 1:idx_q]] * 1000
        if idx_b != -1:
            num += digit[s[idx_b - 1:idx_b]] * 100
        if idx_s != -1:
            # 十前忽略一的處理
            num += digit.get(s[idx_s - 1:idx_s], 1) * 10
        if s[-1] in digit:
            num += digit[s[-1]]

        return num       




df_all['總樓層數'] = df_all['總樓層數'].str.replace("層","")
df_all['總樓層數'] = df_all['總樓層數'].apply(trans)
pd.set_option('display.max_column', None)



#條件：filter_a,篩選並輸出csv檔
condition_1 = df_all['主要用途']=='住家用'
condition_2 = df_all['建物型態'].str.contains('住宅大樓')
condition_3 = df_all['總樓層數']>=13
filter_a = df_all[(condition_1 & condition_2 & condition_3)]
filter_a.to_csv('filter_a.csv',encoding ='big5')



#條件：filter_b,篩選並輸出csv檔
total_mount = len(df_all)
total_berth_mount = len(df_all[df_all['車位類別'].isnull().values==False])
avg_price = df_all['總價元'].astype('int64').mean()
avg_berth_price = df_all['車位總價元'].astype('int64').mean()
info_dict ={
    '總件數':total_mount,
    '總車位數':total_berth_mount,
    '平均總價元':avg_price,
    '平均車位總價元':avg_berth_price
}
pd.Series(info_dict).to_csv('filter_b.csv',encoding ='big5')






