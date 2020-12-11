# encoding: UTF-8

'''
les Traitement du fichier de l'Amplitude 
relative aux balances comptable

  - Enrichir le base des données avec le fichier généré par DIT
  
modification: le 30 janv. 2018
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
#rptDate = '20190228'

#Log configuration

#----------------------------------------------------------------------
DEBUG = False
if not DEBUG:
    logPyPath = '\\\\10.205.176.250\\share-dmf\\Working_Src\\batch\\log_py\\'+ today
    if not os.path.exists(logPyPath):
        os.makedirs(logPyPath)
    
    logging.basicConfig(filename=logPyPath+'\\'+'FEED_TB_' + rptDate + '_' + timestamp + '.log', level=logging.DEBUG)
    logging.info('Today Date is ' + today + ' Update Timestamp is ' + timestamp)
    logging.info('FEED_TB.py Starts')
    logging.info('Report Date is ' + rptDate)
########################################################################



#Read interface file
#----------------------------------------------------------------------
file = '\\\\10.205.176.250\\share-dit\\dmf\\' + rptDate + '_TB.txt'

logging.info('Reading File ' + file)


tb_src = pd.read_csv(file, sep='!', index_col=False)

#read interface files
#----------------------------------------------------------------------
old_names = [
    'DCO', 
    'DVA', 
    'CHA2',
    'CHA3',
    'CLI',
    'DEV',
    'NCP',
    'SHI',
    'MVTD',
    'MVTC',
    'SDE',
    'CTRL'
]


#replace interface file column with new name
new_names = [
    'DCO', 
    'DVA', 
    'CHA2',
    'CHA3',
    'CLI',
    'DEV',
    'NCP',
    'SHI',
    'MVTD',
    'MVTC',
    'SDE',
    'CTRL'
    ]

tb_src.rename(columns=dict(zip(old_names, new_names)), inplace=True)

#
#tb_src['CHA2'] = [line.decode('utf-8').strip() for line in tb_src['CHA2']]    
#tb_src['CHA3'] = [line.decode('utf-8').strip() for line in tb_src['CHA3']]
tb_src['CHA2'] = [line.strip() for line in tb_src['CHA2']]    
tb_src['CHA3'] = [line.strip() for line in tb_src['CHA3']]

#
tb_src = tb_src.dropna(subset=['DCO'])
tb_src = tb_src.dropna(subset=['DVA'])
tb_src = tb_src.dropna(subset=['DEV'])
tb_src = tb_src.dropna(subset=['NCP'])
#
tb_src['DEV'] = tb_src['DEV'].astype(str) 
tb_src['NCP'] = tb_src['NCP'].astype(str) 
tb_src['CLI'] = tb_src['CLI'].astype(str)
#
tb_src['CLI'] = tb_src['CLI'].map(lambda x: x.strip())
#
import numpy as np
tb_src['CLI'] = tb_src['CLI'].replace(r'\s+', np.NaN, regex=True)

#convert french number to float
#tb_src['SHI'] = tb_src['SHI'].map(lambda x: float(x.replace(',', '.')))
#tb_src['MVTD'] = tb_src['MVTD'].map(lambda x: float(x.replace(',', '.')))
#tb_src['MVTC'] = tb_src['MVTC'].map(lambda x: float(x.replace(',', '.')))
#tb_src['SDE'] = tb_src['SDE'].map(lambda x: float(x.replace(',', '.')))
tb_src['SHI'] = tb_src['SHI'].replace(',', '.', regex=True)
tb_src['MVTD'] = tb_src['MVTD'].replace(',', '.', regex=True)
tb_src['MVTC'] = tb_src['MVTC'].replace(',', '.', regex=True)
tb_src['SDE'] = tb_src['SDE'].replace(',', '.', regex=True)

#DROP DUPLICATES
tb_src.drop_duplicates(subset=['DCO','DVA','NCP','SDE'], keep='first', inplace=True)

out_path = '\\\\10.205.176.250\\share-dmf\\Working_Src\\batch\\outset\\TB_' + rptDate + '.csv'
tb_src.to_csv(out_path, sep=",", na_rep='', encoding='utf-8')


#ADD RPT DATE
from datetime import timedelta
def prev_weekday(date_in):
    date_in -= timedelta(days=1)
    while date_in.weekday() > 4: #Mon - Fri 0-4
        date_in -= timedelta(days=1)
    return date_in

rptDate =  pd.to_datetime(rptDate, format='%Y%m%d')

tb_src['DRT'] = prev_weekday(rptDate)
tb_src['DRT'] = tb_src['DRT'].map(lambda x: pd.to_datetime(str(x), format='%Y/%m/%d'))
tb_src['DCO'] = tb_src['DCO'].map(lambda x: pd.to_datetime(str(x), format='%d/%m/%Y'))
tb_src['DVA'] = tb_src['DVA'].map(lambda x: pd.to_datetime(str(x), format='%d/%m/%Y'))

tb_src = tb_src.where(pd.notnull(tb_src), None)



#Read interface file
#----------------------------------------------------------------------
#!/usr/bin/python
import MySQLdb
#Connection Database
con = MySQLdb.connect(host="10.108.1.10", user="proddba", passwd="dba@BSCA123", db="proddb")
cursor = con.cursor()
#target table
table_name = "ap_tb"

#1.query table, if record exists then drop line
query_date = prev_weekday(rptDate)
args = dict(table=table_name, arg_drt = query_date.strftime("%Y%m%d"))
sql = "SELECT * FROM {table} t WHERE DRT = STR_TO_DATE('{arg_drt}','%Y%m%d')".format(**args)
logging.info('DONNEE A LIRE ' + sql)
tb_query = pd.read_sql(sql, con)

tb_query.columns = [x.upper() for x in tb_query.columns]


#create insert dataset
if len(tb_query) != 0:
    
    tb_query['in_query']=1
    #print tb_query

    tb_src['DRT'] = tb_src['DRT'].map(lambda x: x.strftime('%Y%m%d'))
    tb_query['DRT'] = tb_query['DRT'].map(lambda x: x.strftime('%Y%m%d'))  

    tb_insert = pd.merge(tb_src, tb_query[['DRT','CHA3','DEV','NCP','in_query']], how='outer', on=['DRT','CHA3','DEV','NCP'])
    tb_insert = tb_insert[tb_insert['in_query'].isnull()]    
    del tb_insert['in_query']
    
    tb_insert['DRT'] = tb_insert['DRT'].map(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
    #print tb_insert
    
else:
    tb_insert = tb_src



#DO actions while new records presnt
#----------------------------------------------------------------------
if len(tb_insert) > 0 :

    table_name = "ap_tb"    
    args = dict(table=table_name) 
    
    #check insert key and add id into tb_insert
    #----------------------------------------------------------------------
    #sql = 'SELECT max(id)+1 FROM {table}'.format(**args)
    #cursor.execute(sql)
    #insert_key = cursor.fetchone()
    #tb_insert['ID'] = range(insert_key[0], insert_key[0] + len(tb_insert))    
    #tb_insert['ID'] = range(1, 1 + len(tb_insert))    
    
    col_vals=['%s','%s','%s','%s','%s',
              '%s','%s','%s','%s','%s',
              '%s','%s','%s','%s',]
    
    #replace interface file column with new name
    cols = [
        'DRT',         
        'DCO', 
        'DVA', 
        'CHA2',
        'CHA3',
        'CLI',
        'DEV',
        'NCP',
        'SHI',
        'MVTD',
        'MVTC',
        'SDE',
        'CTRL',
        'TIMESTAMP'
    ]
        
    args = dict(table=table_name, cols =', '.join(cols), col_vals=', '.join(col_vals))
    sql = "INSERT INTO {table} ({cols}) VALUES ({col_vals})".format(**args) 
    
    tb_insert['TIMESTAMP'] = timestamp  
    
    #get values
    tb_insert = tb_insert[cols]  
    
    params = [tuple(x) for x in tb_insert.values]
    
    try:
        #push log
        logging.info('Inserting ' + str(len(tb_insert)) + ' records ')        
        cursor.executemany(sql, params)
        con.commit()   
    except:
        e = sys.exc_info()[0]
        logging.error(e)
        sys.exit(0)          
    
    try:
        #check insert key and add id into tb_insert
        #----------------------------------------------------------------------
        sql = """
        INSERT INTO acc_tb
        (
          apTB_ptr_id
        )
        SELECT 
            id 		as aptb_ptr_id
        FROM ap_tb
        WHERE id not in (SELECT DISTINCT apTB_ptr_id FROM acc_tb) 
    
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
logging.info('FEED_TB.py Finished SUCCESSFULLY')