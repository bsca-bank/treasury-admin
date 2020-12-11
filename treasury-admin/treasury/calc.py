# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

def calc(startDate, tb_trf_normal, tb_trf_large):

    #clean trf table
    date_start = startDate

    #get statut
    columns = ['ccy', 'donneur', 'time_approv.date()','montant','chk_approv','chk_exec','chk_pay'] #'date_recu',
    tb_trf_large = tb_trf_large[columns].sort_values(by=['ccy'], ascending=[False])      
    tb_trf_normal = tb_trf_normal[columns].sort_values(by=['ccy'], ascending=[False])

    #tb_trf_large['nature_size'] = 'large'   
    #tb_trf_normal['nature_size'] = 'normal'

    tb_trf_ctrl = tb_trf_normal.append(tb_trf_large)


    #tb_trf_ctrl['nature_depot'] = 'Nouveaux'      
    #idx = tb_trf_ctrl[tb_trf_ctrl['date_recu'] < date_start].index
    #tb_trf_ctrl.loc[idx,'nature_depot'] = 'Anciens'

    columns = ['ccy', 'donneur', 'time_approv.date()','montant','nature_depot','nature_size','chk_approv','chk_exec','chk_pay']  #'date_recu',
    tb_trf_ctrl = tb_trf_ctrl[columns].sort_values(by=['ccy'], ascending=[False])    

    #update status
    tb_trf_ctrl['status'] = 'En_Attente'

    idx = tb_trf_ctrl[tb_trf_ctrl['chk_approv']].index
    tb_trf_ctrl.loc[idx,'status'] = 'Tranféré' 

    #calc sum dossier montant

    pt_trf_sum = pd.pivot_table(tb_trf_ctrl, values='montant', index=['ccy'], columns=['nature_depot','nature_size','status'], aggfunc=np.sum)
    #if not 'En_Attente' in pt_trf_sum: 
        #pt_trf_sum['En_Attente'] = 0
    #if not 'Tranféré' in pt_trf_sum: 
        #pt_trf_sum['Tranféré'] = 0    
    #if not 'Executé' in pt_trf_sum: 
        #pt_trf_sum['Executé'] = 0    
    #if not 'Payé' in pt_trf_sum: 
        #pt_trf_sum['Payé'] = 0      


    ##calc dossier nbr 
    #pt_trf_len = pd.pivot_table(tb_trf_ctrl, values='montant', index=['ccy'], columns=['status'], aggfunc=len)
    #if not 'En_Attente' in pt_trf_len: 
        #pt_trf_len['En_Attente'] = 0
    #if not 'Tranféré' in pt_trf_len: 
        #pt_trf_len['Tranféré'] = 0    
    #if not 'Executé' in pt_trf_len: 
        #pt_trf_len['Executé'] = 0    
    #if not 'Payé' in pt_trf_len: 
        #pt_trf_len['Payé'] = 0   

    #pt_trf_len = pt_trf_len.add_suffix('_cnt')

    ##make pivot table trf 
    pt_trf_sum.fillna(0, inplace=True)
    pt_trf_sum.reset_index(inplace=True)

    #pt_trf_len.fillna(0, inplace=True) 
    #pt_trf_len.reset_index(inplace=True)

    #pt_trf = pd.merge(pt_trf_sum, pt_trf_len, how='left', on=['ccy'])

    #if 'En_Attente_cnt' in pt_trf:       
        #pt_trf['En_Attente_cnt'] = pt_trf['En_Attente_cnt'].astype(int)
    #if 'Tranféré_cnt' in pt_trf:     
        #pt_trf['Tranféré_cnt'] = pt_trf['Tranféré_cnt'].astype(int)
    #if 'Executé_cnt' in pt_trf:     
        #pt_trf['Executé_cnt'] = pt_trf['Executé_cnt'].astype(int) 
    #if 'Payé_cnt' in pt_trf:    
        #pt_trf['Payé_cnt'] = pt_trf['Payé_cnt'].astype(int)

    #columns = ['ccy', 'En_Attente','Tranféré','Executé','En_Attente_cnt','Tranféré_cnt','Executé_cnt']  
    outset = pt_trf_sum.sort_values(by=['ccy'], ascending=[False]) 

    num_format = lambda x:'{0:,}'.format(x)

    def build_formatters(df, format):
        return {column:format
                for (column,dtype) in df.dtypes.iteritems()
                if dtype in [np.dtype('int64'), np.dtype('float64')]}

    formatters = build_formatters(outset, num_format)


    outset = outset.to_html(formatters=formatters, index=True, classes='table table-hover').replace('border="1"','border="0"')

    outset = outset.replace(',',' ')
    outset = outset.replace('.',',')

    return outset



def calcLoroCtrl(tb_acc, tb_loro, tb_trf):

    del tb_acc['account']
    old_names = ['id'] 
    new_names = ['account']

    tb_acc.rename(columns=dict(zip(old_names, new_names)), inplace=True)
    old_names = ['montant'] 
    new_names = ['loro']
    tb_loro.rename(columns=dict(zip(old_names, new_names)), inplace=True)

    tb_loro = pd.merge(tb_loro, tb_acc, how='left', on=['corresp', 'account'])

    tb_loro = tb_loro.sort_values(by=['account','date_val'], ascending=[False, False]) 
    tb_loro.drop_duplicates(subset=['account'], keep='first', inplace=True)

    #clean trf table
    #adjust actual payment amount
    #idx = tb_trf[tb_trf['montant_pay'] > 0 ].index
    #tb_trf.loc[idx, 'montant'] = tb_trf['montant_pay']
   
    #get statut
        
    idx = tb_trf[~tb_trf['chk_exec']].index
    tb_trf.loc[idx,'status'] = 'pending_verify'

    idx = tb_trf[tb_trf['chk_verify']].index
    tb_trf.loc[idx,'status'] = 'pending_go'   

    idx = tb_trf[tb_trf['chk_verify'] & tb_trf['chk_approv']].index
    tb_trf.loc[idx,'status'] = 'pending_exec'

    idx = tb_trf[tb_trf['chk_verify'] & tb_trf['chk_approv'] & tb_trf['chk_exec']].index
    tb_trf.loc[idx,'status'] = 'pending_pay'

    idx = tb_trf[tb_trf['chk_verify'] & tb_trf['chk_approv'] & tb_trf['chk_exec'] & tb_trf['chk_pay']].index
    tb_trf.loc[idx,'status'] = 'paid'   


    #calc sum dossier montant
    pt_trf_sum = pd.pivot_table(tb_trf, values='montant', index=['corresp', 'account'], columns=['status'], aggfunc=np.sum)
    if not 'pending_verify' in pt_trf_sum: 
        pt_trf_sum['pending_verify'] = 0
    if not 'pending_go' in pt_trf_sum: 
        pt_trf_sum['pending_go'] = 0    
    if not 'pending_exec' in pt_trf_sum: 
        pt_trf_sum['pending_exec'] = 0    
    if not 'pending_pay' in pt_trf_sum: 
        pt_trf_sum['pending_pay'] = 0   

    #calc dossier nbr 
    pt_trf_len = pd.pivot_table(tb_trf, values='montant', index=['corresp', 'account'], columns=['status'], aggfunc=len)
    if not 'pending_verify' in pt_trf_len: 
        pt_trf_len['pending_verify'] = 0
    if not 'pending_go' in pt_trf_len: 
        pt_trf_len['pending_go'] = 0    
    if not 'pending_exec' in pt_trf_len: 
        pt_trf_len['pending_exec'] = 0    
    if not 'pending_pay' in pt_trf_len: 
        pt_trf_len['pending_pay'] = 0 
    pt_trf_len = pt_trf_len.add_suffix('_cnt')

    #make pivot table trf 
    pt_trf_sum.fillna(0, inplace=True) 
    pt_trf_len.fillna(0, inplace=True) 
    pt_trf_sum.reset_index(inplace=True)
    pt_trf_len.reset_index(inplace=True)
    pt_trf = pd.merge(pt_trf_sum, pt_trf_len, how='left', on=['corresp', 'account'])

    #merge pivot tables
    tb_loro.fillna(0, inplace=True)
    tb_loro.reset_index(inplace=True)
    pt_trf.fillna(0, inplace=True)
    pt_trf.reset_index(inplace=True)   

    pt_loro_trf = pd.merge(tb_loro, pt_trf, how='inner', on=['corresp', 'account'])

    if not 'pending_exec' in pt_loro_trf:
        pt_loro_trf['pending_exec'] = 0
    if not 'pending_pay' in pt_loro_trf:
        pt_loro_trf['pending_pay'] = 0

    pt_loro_trf.fillna(0, inplace=True)

    pt_loro_trf['loro_act'] = pt_loro_trf['loro'] - pt_loro_trf['pending_exec'] - pt_loro_trf['pending_pay'] 

    pt_loro_trf['pending_exec_cnt'] = pt_loro_trf['pending_exec_cnt'].astype(int)
    pt_loro_trf['pending_pay_cnt'] = pt_loro_trf['pending_pay_cnt'].astype(int)    

    #columns = ['ccy','corresp','loro_t-1','pending_exec','pending_pay','loro_t','pending_verify','pending_go','pending_verify_cnt','pending_go_cnt','pending_exec_cnt','pending_pay_cnt']
    columns = ['corresp','alias','date_val','loro','loro_act','pending_exec','pending_exec_cnt','pending_pay','pending_pay_cnt']      
    outset = pt_loro_trf[columns].sort_values(by=['corresp','alias'], ascending=[False, False]) 

    num_format = lambda x:'{0:,}'.format(x)

    def build_formatters(df, format):
        return {column:format
                for (column,dtype) in df.dtypes.iteritems()
                if dtype in [np.dtype('int64'), np.dtype('float64')]}

    formatters = build_formatters(outset, num_format)

    outset = outset.to_html(formatters=formatters, index=False, classes='table table-hover').replace('border="1"','border="0"')

    outset = outset.replace(',',' ')
    outset = outset.replace('.',',')

    return outset
