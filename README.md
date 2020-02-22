# Pandas-practice


使用內政部不動產時價登錄網中，位於【臺北市/新北市/桃園市/臺中市/高雄市】的 【不動產買賣】資料，嘗試將資料以pandas整合，並篩選所需資訊，最後匯出成CSV檔

## import 套件

```python
import pandas as pd
import numpy as np
```

## 讀取csv檔
```python
df_a = pd.read_csv('a_lvr_land_a.csv',encoding ='utf-8') 
#將第0行的英文欄位名稱去除
df_a = df_a.drop([0,0])
```

## 合併所有dataframe
```python
df_all = pd.concat([df_a,df_b,df_e,df_f,df_h],axis = 0)
```

## 處理總樓層數中中文數字轉英文數字
```python
def trans(s):
    digit = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
    num = 0
    if type(s) == str:
        idx_b, idx_s =  s.find('百'), s.find('十')
        
        if idx_b != -1:
            num += digit[s[idx_b - 1:idx_b]] * 100
        if idx_s != -1:
            # 十前忽略一的處理
            num += digit.get(s[idx_s - 1:idx_s], 1) * 10
        if s[-1] in digit:
            num += digit[s[-1]]

        return num      
```

## 總樓層數處理
```python
#去除'層'字
df_all['總樓層數'] = df_all['總樓層數'].str.replace("層","")
#套入國字轉數字func
df_all['總樓層數'] = df_all['總樓層數'].apply(trans)
```

## 條件：filter_a,篩選並輸出csv檔
條件為取出 主要用途為住家用、建物型態為住宅大樓、總樓層數大於等於13的物件，並輸出CSV檔
```python
condition_1 = df_all['主要用途']=='住家用'
condition_2 = df_all['建物型態'].str.contains('住宅大樓')
condition_3 = df_all['總樓層數']>=13
filter_a = df_all[(condition_1 & condition_2 & condition_3)]
#轉出csv檔
filter_a.to_csv('filter_a.csv',encoding ='big5')
```

## 條件：filter_b,篩選並輸出csv檔
取出 總件數、總車位數、平均總價元、平均車位總價元，並輸出CSV檔
```python
#總件數
total_mount = len(df_all)
#交易筆棟數格式為：土地1建物1車位2，從'車位'一詞分割出車位數，再進行加總
total_berth_mount = df_all['交易筆棟數'].str.split('車位',expand=True)[1].astype('int64').sum()
#平均總價元
avg_price = df_all['總價元'].astype('int64').mean()
#平均車位總價元
avg_berth_price = df_all['車位總價元'].astype('int64').mean()

info_dict ={
    '總件數':total_mount,
    '總車位數':total_berth_mount,
    '平均總價元':avg_price,
    '平均車位總價元':avg_berth_price
}

pd.Series(info_dict).to_csv('filter_b.csv',encoding ='big5')
```