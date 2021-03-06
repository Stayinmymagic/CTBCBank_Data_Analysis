import pandas as pd
#%%
#使用chunksize原因在於資料筆數過多，一次存取會戰過多記憶體，所以分批匯入。
df_chunk = pd.read_csv('BNS_LOAN_1812.csv', encoding = 'cp437', chunksize = 500000, low_memory= False)
#amgPd = pd.DataFrame()
#for chunk in pd.read_csv('a.csv', encoding = 'cp950')
chunk_list = []
for chunk in df_chunk:
    chunk_list.append(chunk)
    print(chunk)
#concat合併
df_concat = pd.concat(chunk_list)
print('concat_done')

#%%%%%%%%%%%%%%%%%%%%%%
now = 'Education_Code'
ast = 'Asset_Bal'
element = loan[now].unique()
print(element)

#%%merge檔案中相同欄位的資料。
result = loan_data.merge(ast, on = 'Enc_Customer_ID', how = 'inner')
#%%
for i in result.columns:
    print(i)
#%%
now='Income_Code'
la=list(set(result['%s'%now]))
#%%
for p in range(len(result['%s'%now])):
    if result['%s'%now][p]!='N':
        result['%s'%now][p]=0

#%%
#計算資產的平均、標準差、次數
a=result.groupby(['%s'%now]).mean()
a=a[['Asset_Bal']].copy()
a1=round(a['Asset_Bal'][0],3)
a2=round(a['Asset_Bal'][1],3)
b=result.groupby(['%s'%now]).std()
b=b[['Asset_Bal']].copy()
b1=round(b['Asset_Bal'][0],3)
b2=round(b['Asset_Bal'][1],3)
c=result.groupby(['%s'%now]).count()
c1=c[['Asset_Bal']]
print(a1,b1)
print(a2,b2)
print(c1)

#%%
df1=result['Asset_Bal'][result['%s'%now]==la[0]]
df2=result['Asset_Bal'][result['%s'%now]==la[1]]
(sta,pvalue)=stats.ttest_ind(df1,df2,equal_var=False,nan_policy='omit')
print('%6.3f,%6.4f'%(sta,pvalue))


#%%%ANOVA
for i in range(1) :
    df_result = pd.DataFrame(index = element, columns = ['N','mean', 'std'])
    df_result['N'] = loan.groupby([now])[ast].count()
    df_result['mean'] = round(loan.groupby([now])[ast].mean())
    df_result['std'] = round(loan.groupby([now])[ast].std())
    print(df_result)

(f,pv) = stats.f_oneway(loan[ast][loan[now] == element[0]],loan[ast][loan[now] == element[1]],loan[ast][loan[now] == element[2]],loan[ast][loan[now] == element[4]],loan[ast][loan[now] == element[5]],loan[ast][loan[now] == element[6]],loan[ast][loan[now] == element[7]])
#,loan[ast][loan[now] == element[5]],loan[ast][loan[now] == element[6]],loan[ast][loan[now] == element[7]]
#],loan[ast][loan[now] == element[3]]
print('%6.3f,%6.4f'%(f,pv))
#%%
a=result.groupby(['%s'%now]).mean()
a=a[['Asset_Bal']].copy()
print(a['Asset_Bal'])
#%%ttest
result=loan
a=result.groupby(['%s'%now]).mean()
a=a[['Asset_Bal']].copy()
a1=round(a['Asset_Bal'][0],3)
a2=round(a['Asset_Bal'][5],3)
b=result.groupby(['%s'%now]).std()
b=b[['Asset_Bal']].copy()
b1=round(b['Asset_Bal'][0],3)
b2=round(b['Asset_Bal'][5],3)
c=result.groupby(['%s'%now]).count()
c1=c[['Asset_Bal']]
print(a1,b1)
print(a2,b2)
print(c1)
df1=result['Asset_Bal'][result['%s'%now]==element[0]]
df2=result['Asset_Bal'][result['%s'%now]==element[1]]
(sta,pvalue)=stats.ttest_ind(df1,df2,equal_var=False,nan_policy='omit')
print('%6.3f,%6.4f'%(sta,pvalue))
#%%re
import scipy.stats as ss
continual = ['Wm_Waive_Own_Cnt']
df_result = pd.DataFrame(columns = ['mean','std','corr', 'P value'], index = continual)
for i in range(len(continual)):
    temp = ss.pearsonr(loan[continual[i]], loan['Asset_Bal'])
    df_result.iat[i, 0] = loan[continual[i]].mean()
    df_result.iat[i, 1] = loan[continual[i]].std()
    df_result.iat[i, 2] = round(temp[0],3)
    df_result.iat[i, 3] = round(temp[1],4)
print(df_result)
