# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np

from datetime import date, timedelta



'''

  This program sucks !

'''
def calc_cash_position(tb_ts, tb_cf):

    #file = 'F:\\share-dmf\\Working_Src\\batch\\outset\\20190402\\' + 'tb_ts.csv'
    #tb_ts = pd.read_csv(file, sep='|', index_col=0)

    #file = 'F:\\share-dmf\\Working_Src\\batch\\outset\\20190402\\' + 'tb_cf.csv'
    #tb_cf = pd.read_csv(file, sep='|', index_col=0) 

    #declarations and dates
    #------------------------------------------------------- 
    today = date.today()   

    #output history
    rptDate = today.strftime("%Y%m%d")
    
    str_path = '\\\\10.205.176.250\\share-dmf\\Working_Src\\batch\\outset\\' + rptDate
    #str_path = 'C:\\GitHub\\treasury-admin\\' + rptDate

    if not os.path.exists(str_path):
        os.makedirs(str_path)
    #str_path = 'C:\\github\\temp\\'    
    #
    out_path = str_path + "\\" + rptDate + '_tb_ts.csv'
    tb_ts.to_csv(out_path, sep=",", na_rep='', encoding='utf-8')
    #
    out_path = str_path + "\\" + rptDate + '_tb_cf.csv'
    tb_cf.to_csv(out_path, sep=",", na_rep='', encoding='utf-8')
    #
    #récupération des données
    #-------------------------------------------------------
    tb_ts = tb_ts.sort_values(by=['corresp','account','date_val'], ascending=[True,False,False]) 
    tb_ts.drop_duplicates(subset=['corresp','account'], keep='first', inplace=True)
    
    #temp = tb_ts
    #tb_ts.loc[:] = temp[temp['nature']=='Correspondant'] 
   
    tb_ts.fillna(0, inplace=True)
    tb_ts.reset_index(inplace=True)

    tb_cf = tb_cf[tb_cf['chk_pay'] == False]

    #convert to date
    tb_cf['date_val'] = pd.to_datetime(tb_cf['date_val']).dt.date

    tb_cf['delta'] = tb_cf['date_val'] - today
    tb_cf['delta'].fillna(0, inplace=True)
    tb_cf['delta'] = (tb_cf['delta'] / np.timedelta64(1, 'D')).astype(int)

    tb_cf['time_delta'] = None

    idx = tb_cf[tb_cf['delta'] <= 1 ].index    
    tb_cf.loc[idx, 'time_delta'] = "ON"

    idx = tb_cf[(tb_cf['delta'] > 1) & (tb_cf['delta'] <= 3)].index  
    tb_cf.loc[idx, 'time_delta'] = "3D"        

    idx = tb_cf[(tb_cf['delta'] > 3) & (tb_cf['delta'] <= 7)].index   
    tb_cf.loc[idx, 'time_delta'] = "7D"           

    idx = tb_cf[(tb_cf['delta'] > 7) & (tb_cf['delta'] <= 30)].index   
    tb_cf.loc[idx, 'time_delta'] = "1M"    

    tb_cf_on = tb_cf[(tb_cf['delta'] <= 1) & (tb_cf['chk_verify'] == True)]
    tb_cf_3d = tb_cf[(tb_cf['delta'] <= 3)  & (tb_cf['chk_verify'] == True)]
    tb_cf_7d = tb_cf[(tb_cf['delta'] <= 7)  & (tb_cf['chk_verify'] == True)]
    tb_cf_1m = tb_cf[(tb_cf['delta'] <= 30)  & (tb_cf['chk_verify'] == True)]

    def calcCashflow(loro, cashflow, suffix):

        #loro = tb_ts
        #cashflow = tb_cf_on
        #suffix = 'ON'

        if len(cashflow) > 0:

            pt_cf_sum = pd.pivot_table(cashflow, values='montant', \
                index=['corresp','account',], columns=['nature'], aggfunc=np.sum)
            
            pt_cf_sum = pt_cf_sum.add_suffix(suffix)
            
            #calc dossier nbr 
            pt_cf_len = pd.pivot_table(cashflow, values='montant', \
                index=['corresp','account',], columns=['nature'], aggfunc=len)
            
            pt_cf_len = pt_cf_len.add_suffix('_cnt'+ suffix)

            #make pivot table trf 
            pt_cf_sum.fillna(0, inplace=True) 
            pt_cf_len.fillna(0, inplace=True)

            pt_cf_sum.reset_index(inplace=True)
            pt_cf_len.reset_index(inplace=True)    

            #récupération des données
            #-------------------------------------------------------    
            pt_cf = pd.merge(pt_cf_sum, pt_cf_len, \
                how='inner', on=['corresp', 'account'])
            
            pt_cf.fillna(0, inplace=True)
            pt_cf.reset_index(inplace=True)   

            pt_cf.sort_values(by=['corresp','account'], ascending=[False, False]) 

        else:
            pt_cf = pd.DataFrame(columns=[['corresp','account',
                                           'CF_InFlow' + suffix,
                                           'CF_InFlow_cnt' + suffix,
                                           'CF_OutFlow' + suffix,
                                           'CF_OutFlow_cnt' + suffix
                                           ]])     

        _loro = loro[['nature','corresp','account','montant']]
        pt_loro_cf = pd.merge(_loro, pt_cf, how='left', on=['corresp', 'account'])
        
        pt_loro_cf.fillna(0, inplace=True)  
        pt_loro_cf = pt_loro_cf[pt_loro_cf['corresp']!=0]
        

        if 'CF_InFlow' + suffix not in pt_loro_cf.columns: pt_loro_cf['CF_InFlow' + suffix] = 0
        if 'CF_InFlow_cnt' + suffix not in pt_loro_cf.columns:pt_loro_cf['CF_InFlow_cnt' + suffix] = 0
        
        if 'CF_OutFlow' + suffix not in pt_loro_cf.columns: pt_loro_cf['CF_OutFlow' + suffix] = 0    
        if 'CF_OutFlow_cnt' + suffix not in pt_loro_cf.columns:pt_loro_cf['CF_OutFlow_cnt' + suffix] = 0    
            
        pt_loro_cf['CF_InFlow_cnt' + suffix] = pt_loro_cf['CF_InFlow_cnt' + suffix].astype(int)
        pt_loro_cf['CF_OutFlow_cnt' + suffix] = pt_loro_cf['CF_OutFlow_cnt' + suffix].astype(int)          
        #
        pt_loro_cf.loc[:, 'CF_OutFlow' + suffix] = -1*pt_loro_cf['CF_OutFlow' + suffix]
        pt_loro_cf['CF'+suffix] = pt_loro_cf['CF_InFlow' + suffix] + pt_loro_cf.loc[:, 'CF_OutFlow' + suffix] 
        pt_loro_cf['ACT'+suffix] = pt_loro_cf['montant'] + pt_loro_cf.loc[:, 'CF'+suffix] 

        outset = pt_loro_cf[['nature','corresp','account',
                             'ACT' + suffix,
                             'CF' + suffix,
                             'CF_InFlow' + suffix,
                             'CF_InFlow_cnt' + suffix,
                             'CF_OutFlow' + suffix,
                             'CF_OutFlow_cnt' + suffix
                             ]]
        return outset
    
    outset_on = calcCashflow(tb_ts, tb_cf_on, "_ON") 
    outset_3d = calcCashflow(tb_ts, tb_cf_3d, "_3D")
    outset_7d = calcCashflow(tb_ts, tb_cf_7d, "_7D")
    outset_1m = calcCashflow(tb_ts, tb_cf_1m, "_1M")

    #columns = ['nature','corresp','account','date_val','montant',\
    # 'ACT_ON','CF_ON','ACT_3D','CF_3D','ACT_7D','CF_7D','ACT_1M','CF_1M',]
    
    outset = tb_ts[['nature','account','corresp','date_val','montant']]
    outset = pd.merge(outset, outset_on, how='left', on=['corresp', 'account',])
    outset = pd.merge(outset, outset_3d, how='left', on=['corresp', 'account',])
    outset = pd.merge(outset, outset_7d, how='left', on=['corresp', 'account',])
    outset = pd.merge(outset, outset_1m, how='left', on=['corresp', 'account',])    

    outset.fillna(0, inplace=True)  
    outset = outset[outset['corresp']!=0]
    
    old_names = ['nature','account','corresp','date_val','montant',\
                 'ACT_ON','CF_ON','ACT_3D','CF_3D','ACT_7D','CF_7D','ACT_1M','CF_1M',
                 ] #
    new_names = ['nature','account','corresp','date_val','LORO',\
                 'ACT_ON','CF_ON','ACT_3D','CF_3D','ACT_7D','CF_7D','ACT_1M','CF_1M',
                 ] #
    
    outset.rename(columns=dict(zip(old_names, new_names)), inplace=True)          
    
    outset = outset[new_names].sort_values(by=['nature','account','corresp',], ascending=[False, False, True]) 
    
    out_path = str_path + "\\" + rptDate + '_ts_outset.csv'
    outset.to_csv(out_path, sep=",", na_rep='', encoding='utf-8')

    #output html
    num_format = lambda x:'{0:,.0f}'.format(x)

    def build_formatters(df, format):
        return {column:format
                for (column,dtype) in df.dtypes.iteritems()
                if dtype in [np.dtype('int64'), np.dtype('float64')]}

    formatters = build_formatters(outset, num_format)
    outset = outset.to_html(formatters=formatters, index=False, classes='table table-bordered')\
        #.replace('border="1"','border="0"')

    #outset = outset.replace(',',' ')
    #outset = outset.replace('.',',')

    return outset

'''
  This program sucks !
'''
def calc_cash_position_detail(tb_ts, tb_cf):

    #file = 'F://share-dmf//Working_Src//Test//' + 'tb_ts.csv'
    #tb_ts = pd.read_csv(file, sep='|', index_col=0)

    #file = 'F://share-dmf//Working_Src//Test//' + 'tb_cf.csv'
    #tb_cf = pd.read_csv(file, sep='|', index_col=0)  

    #declarations and dates
    #------------------------------------------------------- 
    today = date.today()  

    #récupération des données
    #-------------------------------------------------------
    tb_ts = tb_ts.sort_values(by=['corresp','account','date_val'], \
        ascending=[True,False,False]) 
    
    tb_ts.drop_duplicates(subset=['corresp','account'], \
        keep='first', inplace=True)
   
    tb_ts.fillna(0, inplace=True)
    tb_ts.reset_index(inplace=True)

    tb_cf = tb_cf[tb_cf['chk_pay'] == False]

    #convert to date
    tb_cf['date_val'] = pd.to_datetime(tb_cf['date_val']).dt.date

    tb_cf['delta'] = tb_cf['date_val'] - today
    tb_cf['delta'].fillna(0, inplace=True)
    tb_cf['delta'] = (tb_cf['delta'] / np.timedelta64(1, 'D')).astype(int)

    tb_cf['time_delta'] = None

    idx = tb_cf[tb_cf['delta'] <= 1 ].index    
    tb_cf.loc[idx, 'time_delta'] = "ON"

    idx = tb_cf[(tb_cf['delta'] > 1) & (tb_cf['delta'] <= 3)].index  
    tb_cf.loc[idx, 'time_delta'] = "3D"        

    idx = tb_cf[(tb_cf['delta'] > 3) & (tb_cf['delta'] <= 7)].index   
    tb_cf.loc[idx, 'time_delta'] = "7D"           

    idx = tb_cf[(tb_cf['delta'] > 7) & (tb_cf['delta'] <= 30)].index   
    tb_cf.loc[idx, 'time_delta'] = "1M"    
    
    #original data has put all chk_verify = True
    tb_cf_on = tb_cf[(tb_cf['delta'] <= 1) & (tb_cf['chk_verify'] == True)]
    if len(tb_cf_on) == 0: tb_cf_on = pd.DataFrame()  
        
    tb_cf_3d = tb_cf[(tb_cf['delta'] > 1) & (tb_cf['delta'] <= 3)  & (tb_cf['chk_verify'] == True)]
    if len(tb_cf_3d) == 0: tb_cf_3d = pd.DataFrame()   
    
    tb_cf_7d = tb_cf[(tb_cf['delta'] > 3) & (tb_cf['delta'] <= 7)  & (tb_cf['chk_verify'] == True)]
    if len(tb_cf_7d) == 0: tb_cf_7d = pd.DataFrame()  
    
    tb_cf_1m = tb_cf[(tb_cf['delta'] > 7) & (tb_cf['delta'] <= 30)  & (tb_cf['chk_verify'] == True)]
    if len(tb_cf_1m) == 0: tb_cf_1m = pd.DataFrame()  

    def calc_cashflow_detail(loro, cashflow, suffix):
    
        #loro = tb_ts
        #cashflow = tb_cf_7d
        #suffix = '_7D'
        
        columns=['corresp','account','content_type',
                 'CF_InFlow' + suffix,
                 'CF_InFlow_cnt' + suffix,
                 'CF_OutFlow' + suffix,
                 'CF_OutFlow_cnt' + suffix
                 ]    
    
        #combine loro information
        _loro = loro[['corresp','account','montant']]
        _loro.loc[:,'content_type'] = '0 - Total'     
    
        if len(cashflow) > 0:
    
            pt_cf_sum = pd.pivot_table(cashflow, \
                values='montant', index=['corresp','account',], columns=['nature'], aggfunc=np.sum)
            
            pt_cf_sum = pt_cf_sum.add_suffix(suffix)
            pt_cf_sum['content_type'] = '0 - Total' 
            pt_cf_sum.fillna(0, inplace=True) 
            pt_cf_sum.reset_index(inplace=True)
            
            #calc dossier nbr 
            pt_cf_len = pd.pivot_table(cashflow, \
                values='montant', index=['corresp','account',], columns=['nature'], aggfunc=len)
            
            pt_cf_len = pt_cf_len.add_suffix('_cnt'+ suffix)
            pt_cf_len['content_type'] = '0 - Total'
            pt_cf_len.fillna(0, inplace=True)
            pt_cf_len.reset_index(inplace=True)    
            
            #make pivot table trf 
            pt_cf_sum_d = pd.pivot_table(cashflow, \
                values='montant', index=['corresp','account','content_type'], columns=['nature'], aggfunc=np.sum) 
            
            pt_cf_sum_d = pt_cf_sum_d.add_suffix(suffix)            
            pt_cf_sum_d.fillna(0, inplace=True) 
            pt_cf_sum_d.reset_index(inplace=True)
            
            pt_cf_len_d = pd.pivot_table(cashflow, \
                values='montant', index=['corresp', 'account','content_type'], columns=['nature'], aggfunc=len)
            
            pt_cf_len_d = pt_cf_len_d.add_suffix('_cnt'+ suffix)
            pt_cf_len_d.fillna(0, inplace=True)   
            pt_cf_len_d.reset_index(inplace=True)

            #récupération des données
            #-------------------------------------------------------   
            pt_cf_sum_detail = pt_cf_sum.append(pt_cf_sum_d) 
            pt_cf_len_detail = pt_cf_len.append(pt_cf_len_d)            
        
            pt_cf_sum_detail.reset_index(inplace=True)            
            pt_cf_len_detail.reset_index(inplace=True)  

            pt_cf = pd.merge(pt_cf_sum_detail, pt_cf_len_detail, \
                how='inner', on=['corresp', 'account','content_type'])
            
            pt_cf.fillna(0, inplace=True)

            #handle missing
            if 'CF_InFlow' + suffix not in pt_cf.columns: pt_cf['CF_InFlow' + suffix] = 0
            if 'CF_InFlow_cnt' + suffix not in pt_cf.columns: pt_cf['CF_InFlow_cnt' + suffix] = 0
        
            if 'CF_OutFlow' + suffix not in pt_cf.columns: pt_cf['CF_OutFlow' + suffix] = 0    
            if 'CF_OutFlow_cnt' + suffix not in pt_cf.columns: pt_cf['CF_OutFlow_cnt' + suffix] = 0        
        
            pt_cf= pt_cf[columns]
            pt_cf.sort_values(by=['corresp','account','content_type'], ascending=[False, False, True])     
        
            pt_loro_cf = pd.merge(_loro, pt_cf, \
                how='right', on=['corresp', 'account','content_type'])
        
            pt_loro_cf.fillna(0, inplace=True)  
            pt_loro_cf = pt_loro_cf[pt_loro_cf['corresp']!=0]
        
            pt_loro_cf['CF_InFlow_cnt' + suffix] = pt_loro_cf['CF_InFlow_cnt' + suffix].astype(int)
            pt_loro_cf['CF_OutFlow_cnt' + suffix] = pt_loro_cf['CF_OutFlow_cnt' + suffix].astype(int)          
        
            pt_loro_cf.loc[:, 'CF_OutFlow' + suffix] = -1*pt_loro_cf['CF_OutFlow' + suffix]
            pt_loro_cf['CF'+suffix] = pt_loro_cf['CF_InFlow' + suffix] + pt_loro_cf['CF_OutFlow' + suffix] 
            pt_loro_cf['ACT'+suffix] = pt_loro_cf['montant'] + pt_loro_cf.loc[:, 'CF'+suffix] 
        
            outset = pt_loro_cf[columns]
        else:
            pt_loro_cf = _loro
            pt_loro_cf.loc[:,'ACT' + suffix] =  pt_loro_cf.loc[:,'montant']
            pt_loro_cf.loc[:,'CF' + suffix] = 0
            pt_loro_cf.loc[:,'CF_InFlow' + suffix] = 0
            pt_loro_cf.loc[:,'CF_InFlow_cnt' + suffix] = 0
            pt_loro_cf.loc[:,'CF_OutFlow' + suffix] = 0
            pt_loro_cf.loc[:,'CF_OutFlow_cnt' + suffix] = 0
            
            outset = pt_loro_cf[columns]

        return outset

    outset_on = calc_cashflow_detail(tb_ts, tb_cf_on, "_ON")
    outset_3d = calc_cashflow_detail(tb_ts, tb_cf_3d, "_3D")
    outset_7d = calc_cashflow_detail(tb_ts, tb_cf_7d, "_7D")
    outset_1m = calc_cashflow_detail(tb_ts, tb_cf_1m, "_1M")
 
    tb_ts['content_type'] = '0 - Total'  

    outset = tb_ts[['account','corresp','date_val','content_type','montant']]
    outset = pd.merge(outset, outset_on, how='outer', on=['account','corresp','content_type',])
    outset = pd.merge(outset, outset_3d, how='outer', on=['account','corresp','content_type',])
    outset = pd.merge(outset, outset_7d, how='outer', on=['account','corresp','content_type',])
    outset = pd.merge(outset, outset_1m, how='outer', on=['account','corresp','content_type',])
    
    outset.fillna(0, inplace=True)  
    #outset = outset[outset['corresp']!=0]
    
    old_names = ['account','corresp','date_val','content_type','montant',
                 'CF_InFlow_ON','CF_InFlow_cnt_ON','CF_OutFlow_ON','CF_OutFlow_cnt_ON',
                 'CF_InFlow_3D','CF_InFlow_cnt_3D','CF_OutFlow_3D','CF_OutFlow_cnt_3D',
                 'CF_InFlow_7D','CF_OutFlow_7D',
                 'CF_InFlow_1M','CF_OutFlow_1M',
                 ]
    new_names = ['account','corresp','date_val','content_type','LORO',
                 'CFI_ON','NBI_ON','CFO_ON','NBO_ON',
                 'CFI_3D','NBI_3D','CFO_3D','NBO_3D',
                 'CFI_7D','CFO_7D',
                 'CFI_1M','CFO_1M',
                 ]    
    
    outset.rename(columns=dict(zip(old_names, new_names)), inplace=True)       
    #
    #outset['CFI_ON'] = outset['CFI_ON'].astype(int)
    #outset['CFI_3D'] = outset['CFI_3D'].astype(int)
    #outset['CFI_7D'] = outset['CFI_7D'].astype(int)   
    #outset['CFI_1M'] = outset['CFI_1M'].astype(int)  
    #
    #outset['CFO_ON'] = outset['CFO_ON'].astype(int)
    #outset['CFO_3D'] = outset['CFO_3D'].astype(int)
    #outset['CFO_7D'] = outset['CFO_7D'].astype(int)   
    #outset['CFO_1M'] = outset['CFO_1M'].astype(int)
    #
    outset['NBI_ON'] = outset['NBI_ON'].astype(int)
    outset['NBI_3D'] = outset['NBI_3D'].astype(int)   
    outset['NBO_ON'] = outset['NBO_ON'].astype(int)
    outset['NBO_3D'] = outset['NBO_3D'].astype(int)   

    outset = outset[new_names].sort_values(by=['account','corresp','content_type',], ascending=[True, False, True]) 
    
    num_format = lambda x:'{0:,.0f}'.format(x)

    def build_formatters(df, format):
        return {column:format
                for (column,dtype) in df.dtypes.iteritems()
                if dtype in [np.dtype('int64'), np.dtype('float64')]}

    formatters = build_formatters(outset, num_format)
    
    outset = outset.to_html(formatters=formatters, index=False, classes='table table-bordered')


    str_path = '\\\\10.205.176.250\\share-dmf\\Working_Src\\batch\\outset\\' + rptDate
    #str_path = 'C:\\GitHub\\treasury-admin\\' + rptDate

    if not os.path.exists(str_path):
        os.makedirs(str_path)
    #str_path = 'C:\\github\\temp\\' 

    out_path = str_path + "\\" + rptDate + '_ts_detail_outset.csv'
    outset.to_csv(out_path, sep=",", na_rep='', encoding='utf-8')

    #.replace('border="1"','border="0"')

    #html = (
        #df.style
        #.format(percent)
        #.applymap(color_negative_red, subset=['col1', 'col2'])
        #.set_properties(**{'font-size': '9pt', 'font-family': 'Calibri'})
        #.bar(subset=['col4', 'col5'], color='lightblue')
        #.render()
    #)
    
    #outset = outset.replace(',',' ')
    #outset = outset.replace('.',',')

    return outset

##if __name__ == 'main':
        ##print calc_loroCtrl(qs_loro, qs_dossier)

