# encoding: UTF-8

'''
SYGMA daily batch 

modification: le 12 sept. 2016
auteurs: Cheng.ZHANG@bscabank.com, mcpreva.badiba@bscabank.com

'''
import xdrlib,sys
import xlrd
import datetime 
import time 
import pandas as pd
import logging
import os


#SAVE XL files into Sql Server 
today = datetime.date.today().strftime("%Y%m%d") 
timestamp = datetime.date.today().strftime("%Y%m%d") + time.strftime("%H%M", time.localtime())

rptDate = today
#rptDate = '20190301'


#Log settings
#____________________________________________________________________________________________________________
DEBUG = False
if not DEBUG:

    logPyPath = '\\\\10.205.176.250\\share-dmf\\Working_Src\\batch\\log_py\\'+ today
    if not os.path.exists(logPyPath):
        os.makedirs(logPyPath)

    logging.basicConfig(filename=logPyPath+'\\'+'FEED_SYGMA_' + rptDate + '_' + timestamp + '.log', level=logging.DEBUG)
    logging.info('Today Date is ' + today + ' Update Timestamp is ' + timestamp)

logging.info('Today Date is ' + today + ' Update Timestamp is ' + timestamp)
logging.info('FEED_TRF_DEPOT_BEAC.py Starts') 

logging.info('Report Date is ' + rptDate)


#read .csv file
#____________________________________________________________________________________________________________
file = '\\\\10.205.176.250\\share-dit\dmf\\' + rptDate + '_SYGMA.csv'
logging.info('Reading File ' + file)


try:
    tb_sygma = pd.read_csv(file, sep=',', index_col=False)

    out_path = '\\\\10.205.176.250\\share-dmf\\Working_Src\\Test\\' + rptDate + '.csv'
    tb_sygma.to_csv(out_path, sep=",", na_rep='', encoding='utf-8')

    columns = ['STATUS'
                ,'F20' #Référence émetteur
                ,'F2_1' #Msg type
                ,'F32A_1','F32A_2','F32A_3' #1.DateVal/2.Devise/3.Montant
                ,'F50K_2','F59_2' #Donneur, BENEF
                ,'F1','F2_2' #EXPD','DEST'
                ,'F53A_2','F53A_3' #Correspondant de l’expéditeur
                ,'F57A_2','F57A_3' #Compte de l’établissement
                ,'F70','F71A','F72' #Code Type de Transaction
            ]    
    tb_sygma = pd.DataFrame(tb_sygma, columns = columns)
except:
    e = sys.exc_info()[0]
    logging.error(e)
    sys.exit(0)
    
#replace column ID
#____________________________________________________________________________________________________________
new_names = ['STATUT_MSG'
             ,'REF_ID'
             ,'TYPE_MSG'
             ,'DATE_VAL','CCY', 'MONTANT' 
             ,'DONNEUR','BENEF'
             ,'EXPD','DEST'
             ,'CMPT_EXPD','CORR_EXPD'
             ,'CMPT_DEST','CORR_DEST'
             ,'INFO','CHARGE_TYPE','TRANS_TYPE'
             ]

tb_sygma.rename(columns=dict(zip(columns, new_names)), inplace=True)
#tb_sygma['REF_ID'].drop_duplicates()

tb_sygma['DATE_VAL'] = tb_sygma['DATE_VAL'].map(lambda x: pd.to_datetime(str(x), format='%d/%m/%Y'))
#tb_sygma['DATE_VAL'] = tb_sygma['DATE_VAL'].map(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))


#distinguish CF_IN/CF_OUT
#---------------------------------------------
tb_sygma['CF'] = 1 #'CF_IN'
idx = tb_sygma[tb_sygma['CORR_EXPD'] == 'SCAQCGCG'].index
tb_sygma.loc[idx,'CF'] = 2 #"CF_OUT"

#seperate CODTYPE
#---------------------------------------------
tb_sygma['CODTYPE'] = ''
idx = tb_sygma[pd.notnull(tb_sygma['TRANS_TYPE'].str.extract("(/CODTYPTR/\d{3})")) == True].index
tb_sygma.loc[idx,'CODTYPE'] = tb_sygma['TRANS_TYPE'].str.extract("(/CODTYPTR/\d{3})")
#
#---------------------------------------------
tb_sygma['OBS'] = tb_sygma['TRANS_TYPE']
#
#---------------------------------------------
tb_sygma['LINK_ID'] = None


#____________________________________________________________________________________________________________
tb_sygma = tb_sygma.where(pd.notnull(tb_sygma), None)

#Correct donneur and BENEF for 103
#____________________________________________________________________________________________________________
#tb_sygma['DONNEUR'] = tb_sygma['DONNEUR'].astype(str)
tb_sygma.loc[:,'DONNEUR'] = tb_sygma['DONNEUR'].str.extract("(\w+.+\n*)")
tb_sygma.loc[:,'DONNEUR'] = tb_sygma['DONNEUR'].str.replace('\n', '')

#tb_sygma['BENEF'] = tb_sygma['BENEF'].astype(str)
tb_sygma.loc[:,'BENEF'] = tb_sygma['BENEF'].str.extract("(\w+.+\n*)")
tb_sygma.loc[:,'BENEF'] = tb_sygma['BENEF'].str.replace('\n', '')


#Correct donneur and BENEF for 202
#____________________________________________________________________________________________________________

#/CODTYPTR/004 couverture
#---------------------------------------------
idx1 = tb_sygma[pd.notnull(tb_sygma['TRANS_TYPE'].str.extract("(/CODTYPTR/004)"))==True].index                 
idx2 = tb_sygma[pd.notnull(tb_sygma['TRANS_TYPE'].str.extract("(C[a-zA-Z]+TURE)"))==True].index               
idx = idx1 & idx2

tb_sygma.loc[idx,'LINK_ID'] = tb_sygma['TRANS_TYPE'].str.extract("(/REF\s+\d{0,4})")
tb_sygma.loc[idx,'LINK_ID'] = tb_sygma['LINK_ID'].str.replace('/REF\s+', '')
tb_sygma.loc[idx,'LINK_ID'] = tb_sygma['LINK_ID'].str.zfill(4)


#/CODTYPTR/018 commission
#---------------------------------------------
idx = tb_sygma[pd.notnull(tb_sygma['TRANS_TYPE'].str.extract("(^/CODTYPTR/018)"))==True].index
tb_sygma.loc[idx,'LINK_ID'] = tb_sygma['TRANS_TYPE'].str.extract("(ORDRE\s+(?:8414\s+)?\d{0,4})")
tb_sygma.loc[idx,'LINK_ID'] = tb_sygma['LINK_ID'].str.replace('(ORDRE(?:8414\s+)?\s+(8414\s+))?', '')
tb_sygma.loc[idx,'LINK_ID'] = tb_sygma['LINK_ID'].str.zfill(4)


#!/usr/bin/python

import MySQLdb

#Connection Database
con = MySQLdb.connect(host="10.108.1.10", user="proddba", passwd="dba@BSCA123", db="proddb")
cursor = con.cursor()

#
#____________________________________________________________________________________________________________

#tb_insert_bk
table_name = "sygma"
#
arg_idx = tb_sygma['REF_ID']
#___________________________________________________________________
args = dict(table=table_name, args_idx=', '.join("'"+arg_idx+"'"))
#args = dict(table=table_name, args_idx=', '.join(""+arg_idx+""))
sql = 'SELECT * FROM {table} t WHERE t.REF_ID IN ({args_idx})'.format(**args)
tb_query = pd.read_sql(sql,con)
tb_query.columns = [x.upper() for x in tb_query.columns]


#Insert/Update
#---------------------------------------------
if len(tb_query) != 0:
    tb_query['in_query']=1
    #new record to insert
    
    tb_sygma['DATE_VAL'] = tb_sygma['DATE_VAL'].astype(str)    
    tb_query['DATE_VAL'] = tb_query['DATE_VAL'].astype(str)       
    
    tb_insert = pd.merge(tb_sygma, tb_query[['DATE_VAL','REF_ID','in_query']], how='outer', on=['DATE_VAL','REF_ID',])
    
    tb_insert = tb_insert[tb_insert['in_query'] !=1]
    del tb_insert['in_query']
else:
    tb_insert = tb_sygma


if len(tb_insert) > 0:    
    table_name = "sygma"
    args = dict(table=table_name)
    
    #check insert key and add id into tb_insert
    sql = 'SELECT max(id)+1 FROM {table}'.format(**args)
    cursor.execute(sql)
    insert_key = cursor.fetchone()
    tb_insert['id'] = range(insert_key[0], insert_key[0] + len(tb_insert))    
    #tb_insert['id'] = range(1, 1 + len(tb_insert))    
    
    #push log
    logging.info('Inserting ' + str(len(tb_insert)) + ' records ')	

    #x20 args
    col_vals=['%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s']
    
    cols = ['DATE_VAL'
            ,'REF_ID'
            ,'TYPE_MSG'
            ,'STATUT_MSG'
            ,'CODTYPE'
            ,'CCY'
            ,'MONTANT'
            ,'EXPD'
            ,'DEST'
            ,'INFO'
            ,'CF'
            ,'LINK_ID'
            ,'DONNEUR'
            ,'BENEF'
            ,'CMPT_EXPD'
            ,'CORR_EXPD'
            ,'CMPT_DEST'
            ,'CORR_DEST'
            ,'CHARGE_TYPE'
            ,'OBS'
            ,'CHK_VERIFY'
            ,'TIMESTAMP'
            ]

    args = dict(table=table_name, cols =', '.join(cols), col_vals=', '.join(col_vals))
    sql = "INSERT INTO {table} ({cols}) VALUES ({col_vals})".format(**args) 

    
    #handle missing: NaN,NaT
    tb_insert = tb_insert.where(pd.notnull(tb_insert), None)
    tb_insert['DATE_VAL'] = tb_insert['DATE_VAL'].fillna(0)
    tb_insert['CHK_VERIFY'] = 0
    tb_insert['TIMESTAMP'] = timestamp 

    #handle missing: NaN,NaT
    tb_insert = tb_insert.where(pd.notnull(tb_insert), None)
    logging.info(tb_insert)

    #get values
    tb_insert = pd.DataFrame(tb_insert, columns=cols)
    params = [tuple(x) for x in tb_insert.values]
    
    out_path = '\\\\10.205.176.250\\share-dmf\\AA_Report\\Rpt_Sygma\\' + rptDate + '.csv'
    tb_insert.to_csv(out_path, sep=",", na_rep='', encoding='utf-8')
    
    try:

        logging.info('Inserting ' + str(len(tb_insert)) + ' records ')        
        cursor.executemany(sql, params)
        con.commit()
        
        #check insert key and add id into tb_insert
        #----------------------------------------------------------------------
        sql = """
        INSERT INTO tresor_sygma_ctrl
        (
                sygma_ptr_id,
                ctrl
        )
        SELECT 
                id 		as sygma_ptr_id,
                0		as ctrl
        FROM sygma
        WHERE id not in (SELECT DISTINCT sygma_ptr_id FROM tresor_sygma_ctrl) 
        """
        cursor.execute(sql)    
        con.commit()                
        
    except:
        e = sys.exc_info()[0]
        logging.error(e)
        sys.exit(0)  
        
else:
    logging.info('No record to insert')

con.close()

#Standard ending code
#----------------------------------------------
logging.info('Script terminated SUCCESSFULLY with no exception')
