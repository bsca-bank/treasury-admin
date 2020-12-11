# encoding: UTF-8

'''
les Traitement du fichier de l'Amplitude 
relative aux Transferts/Rapatriements en devise

  - Enrichir le base des données avec le fichier généré par DIT
  
modification: le 12 sept. 2016
auteurs: Cheng.ZHANG@bscabank.com, mcpreva.badiba@bscabank.com

'''

import xdrlib,sys
import xlrd
import datetime 
import time 
import pandas as pd
#
import logging
import os


#SAVE XL files into Sql Server 
today = datetime.date.today().strftime("%Y%m%d") 
timestamp = datetime.date.today().strftime("%Y%m%d") + time.strftime("%H%M", time.localtime())

rptDate = today
#rptDate = '20181218'

#Log configuration
#----------------------------------------------------------------------
DEBUG = False
if not DEBUG:
    logPyPath = '\\\\10.205.176.250\\share-dmf\\Working_Src\\batch\\log_py\\'+ today
    if not os.path.exists(logPyPath):
        os.makedirs(logPyPath)
    
    logging.basicConfig(filename=logPyPath+'\\'+'FEED_BKCLI_' + rptDate + '_' + timestamp + '.log', level=logging.DEBUG)
    logging.info('Today Date is ' + today + ' Update Timestamp is ' + timestamp)
    logging.info('FEED_BKCLI.py Starts')
logging.info('Report Date is ' + rptDate)
########################################################################



#Read interface file
#----------------------------------------------------------------------
file = '\\\\10.205.176.250\\share-dit\dmf\\' + rptDate + '_BKCLI.txt'
#file = '\\\\10.208.41.250\\share-dit\\dmf\\'  + 'BKCLI.txt'


logging.info('Reading File ' + file)
tb_bkcli = pd.read_csv(file, sep='|', index_col=False)

#read interface files
#----------------------------------------------------------------------
old_names = [
    'CLI', 	 #01.Ref_ID
    'NOMREST',  #03.ALIAS*/
    'DOU',	 #04.DATE_PROFIL
    'DMO',	 #05.DATE_VAL
]

#replace interface file column with new name
new_names = [
    'REF_ID', 	      #CLI  
    'FULLNAME',       #ALIAS
    'DATE_PROFIL',    #DATE_PROFIL
    'DATE_VAL',	      #DATE_VAL
    ]

    
tb_bkcli.rename(columns=dict(zip(old_names, new_names)), inplace=True)
tb_bkcli['REF_ID'] = tb_bkcli['REF_ID'].astype(str).drop_duplicates()

tb_bkcli['REF_ID'] = tb_bkcli['REF_ID'].apply(lambda x: x.zfill(6))

tb_bkcli = tb_bkcli.where(pd.notnull(tb_bkcli), None)

tb_bkcli = tb_bkcli[pd.notnull(tb_bkcli['FULLNAME'])]


tb_bkcli[['DATE_VAL','DATE_PROFIL']] = tb_bkcli[['DATE_VAL','DATE_PROFIL']].fillna("01/01/1970")
tb_bkcli['DATE_PROFIL'] = tb_bkcli['DATE_PROFIL'].map(lambda x: pd.to_datetime(str(x), format='%d/%m/%Y'))
idx = tb_bkcli[tb_bkcli['DATE_PROFIL'] == '1970-01-01'].index
#if len(idx) > 0:
    #tb_bkcli.loc[idx,'DATE_PROFIL'] = ""

tb_bkcli['DATE_VAL'] = tb_bkcli['DATE_VAL'].map(lambda x: pd.to_datetime(str(x), format='%d/%m/%Y'))
idx = tb_bkcli[tb_bkcli['DATE_VAL'] == '1970-01-01'].index

#if len(idx) > 0:
    #tb_bkcli.loc[idx,'DATE_VAL'] = None


#Read interface file
#----------------------------------------------------------------------

#!/usr/bin/python
import MySQLdb

#Connection Database
con = MySQLdb.connect(host="10.108.1.10", user="proddba", passwd="dba@BSCA123", db="proddb")
cursor = con.cursor()


#target table
table_name = "ap_bkcli"

arg_idx = tb_bkcli['REF_ID']
#1.query table, if record exists then drop line
args = dict(table=table_name, args_idx=', '.join("'"+arg_idx+"'"))
#sql = 'SELECT * FROM {table} t WHERE CONVERT(varchar(8),t.DATE_DEPOT, 112)= {arg_date}'.format(**args)
sql = 'SELECT * FROM {table} t WHERE t.REF_ID IN ({args_idx})'.format(**args)
logging.info('DONNEE A LIRE ' + sql)
tb_query = pd.read_sql(sql,con)

tb_query.columns = [x.upper() for x in tb_query.columns]

#create insert dataset
if len(tb_query) != 0:
    tb_query['in_query']=1
    #print tb_query
    #new record to insert
    tb_insert = pd.merge(tb_bkcli,tb_query[['REF_ID','in_query',]], how='outer', on=['REF_ID',])
    tb_insert = tb_insert[tb_insert['in_query'] !=1]
    del tb_insert['in_query']
    #print tb_insert
else:
    tb_insert = tb_bkcli


#DO actions while new records presnt
#----------------------------------------------------------------------
if len(tb_insert) > 0 :
    
    #check insert key and add id into tb_insert
    #----------------------------------------------------------------------
    sql = 'SELECT max(id)+1 FROM {table}'.format(**args)
    cursor.execute(sql)
    insert_key = cursor.fetchone()
    tb_insert['id'] = range(insert_key[0], insert_key[0] + len(tb_insert))    
    #tb_insert['id'] = range(1, 1 + len(tb_insert))    
    
    tb_insert['CHK_ACTIF'] =  True         
    
    tb_insert['CHK_BLOQUE'] =  False
    
    #old tb_insert['FULLNAME'] = [line.decode('utf-8').strip() for line in tb_insert['FULLNAME']]    
    tb_insert['FULLNAME'] = [line.strip() for line in tb_insert['FULLNAME']] 

    col_vals=['%s','%s','%s','%s','%s','%s','%s']
    
    #replace interface file column with new name
    cols = [
        'REF_ID', 	      #CLI  
        'FULLNAME',       #ALIAS
        'DATE_PROFIL',    #DATE_PROFIL
        'DATE_VAL',	      #DATE_VAL
        'CHK_ACTIF',
        'CHK_BLOQUE',
        'id',
    ]
        
    args = dict(table=table_name, cols =', '.join(cols), col_vals=', '.join(col_vals))
    sql = "INSERT INTO {table} ({cols}) VALUES ({col_vals})".format(**args) 
    
    #handle missing: NaN,NaT
    tb_insert = tb_insert.where(pd.notnull(tb_insert), None)
    #tb_insert[['DATE_VAL','DATE_EXEC']] = tb_insert[['DATE_VAL','DATE_EXEC']].fillna(0)

    #print tb_insert
    logging.info(tb_insert)
    
    #get values
    tb_insert = tb_insert[cols]
    tb_insert['REF_ID'].drop_duplicates()   
    
    params = [tuple(x) for x in tb_insert.values]
    

    try:
        #push log
        logging.info('Inserting ' + str(len(tb_insert)) + ' records ')        
        
        cursor.executemany(sql, params)
        con.commit()
        
        #check insert key and add id into tb_insert
        #----------------------------------------------------------------------
        sql = """
        INSERT INTO third_client_ctrl
        (
            apbkcli_ptr_id,
            type_client_id,
            chk_corresp,
            chk_cpty,
            chk_depo
        )
        SELECT 
            id 	as apbkcli_ptr_id,
            7   as type_client_id,
            0   as chk_corresp,
            0   as chk_cpty,
            0   as chk_depo
        FROM ap_bkcli
        WHERE id not in (SELECT DISTINCT apbkcli_ptr_id FROM third_client_ctrl) 
    
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
#========================================McPreva===========================
#Standard ending code
#----------------------------------------------
logging.info('FEED_BKCLI.py Finished SUCCESSFULLY')