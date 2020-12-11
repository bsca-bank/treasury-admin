# encoding: UTF-8
'''

les Traitement du fichier de l'Amplitude 
relative aux BKMVT

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
#rptDate = '20180604'

#Log configuration
#----------------------------------------------------------------------
DEBUG = False
#DEBUG = True

if not DEBUG:
    logPyPath = '\\\\10.205.176.250\\share-dmf\\Working_Src\\batch\\log_py\\'+ rptDate
    if not os.path.exists(logPyPath):
        os.makedirs(logPyPath)
    
    logging.basicConfig(filename=logPyPath+'\\'+'FEED_BKMVT_' + rptDate + '_' + timestamp + '.log', level=logging.DEBUG)
    logging.info('Today Date is ' + today + ' Update Timestamp is ' + timestamp)
    logging.info('FEED_BKMVT.py Starts')
    logging.info('Report Date is ' + rptDate)
########################################################################


#Read interface file
#----------------------------------------------------------------------
file = '\\\\10.205.176.250\\share-dit\\dmf\\' + rptDate + '_BKMVT.txt'

logging.info('Reading File ' + file)
tb_bkmvt = pd.read_csv(file, sep='|', index_col=False)

#read interface files
#----------------------------------------------------------------------
old_names = [
    'AGEE',   #01.ENTITY
    'DVA', 	  #02.DATA_TRD
    'DSAI',   #03.DATE_VAL
    'HSAI',	  #04.TIME_VAL
    'DEVA',	  #05.CCY1
    'DEVC',	  #06.CCY2	
    'CLI',    #07.Client
    'NAT',    #08.NATURE
    'NOMP',   #09.CLIENT_NAME
    'NCP',    #10.CLIENT_ACC
    'SEN',    #11.DIRECTION
    'MNAT',	  #12.AMT1
    'MHTT',	  #13.AMT2
    'TCAI2',  #14.FX_RATE
    'ETA' 	  #15.STATUS
]

#replace interface file column with new name
new_names = [
    'AGE',    #01.ENTITY (DEL AN E)
    'DVA', 	  #02.DATA_TRD
    'DSAI',   #03.DATE_VAL
    'HSAI',	  #04.TIME_VAL
    'DEVA',	  #05.CCY1
    'DEVC',	  #06.CCY2	
    'CLI',    #07.Client
    'NAT',    #08.NATURE
    'NOMP',   #09.CLIENT_NAME
    'NCP',    #10.CLIENT_ACC
    'SEN',    #11.DIRECTION
    'MNAT',	  #12.AMT1
    'MHTT',	  #13.AMT2
    'TCAI2',  #14.FX_RATE
    'ETA' 	  #15.STATUS
    ]
    
tb_bkmvt.rename(columns=dict(zip(old_names, new_names)), inplace=True)
tb_bkmvt = tb_bkmvt.where(pd.notnull(tb_bkmvt), None)

#
tb_bkmvt['NCP'] = tb_bkmvt['NCP'].astype(str)
tb_bkmvt['NCP'] = tb_bkmvt['NCP'].map(lambda x: x.replace('.0', ''))

#convert french number to float
tb_bkmvt['TCAI2'] = tb_bkmvt['TCAI2'].map(lambda x: float(x.replace(',', '.')))
#tb_bkmvt['MNAT'] = tb_bkmvt['MNAT'].map(lambda x: float(x.replace(',', '.')))
#tb_bkmvt['MHTT'] = tb_bkmvt['MHTT'].map(lambda x: float(x.replace(',', '.')))


#convert date to yyyymmdd
#correct missing date
tb_bkmvt['DVA'] = tb_bkmvt['DVA'].map(lambda x: pd.to_datetime(str(x), format='%d/%m/%Y'))
tb_bkmvt['DSAI'] = tb_bkmvt['DSAI'].map(lambda x: pd.to_datetime(str(x), format='%d/%m/%Y'))

#
import numpy as np
tb_bkmvt['CLI'] = tb_bkmvt['CLI'].replace(r'\s+', np.nan, regex=True)
#handle missing: NaN,NaT
tb_bkmvt = tb_bkmvt.dropna(subset=['CLI'])

idx = tb_bkmvt[tb_bkmvt['CLI'] > 0].index
tb_bkmvt.loc[idx,'CLI'] = tb_bkmvt.loc[idx,'CLI'].astype(str).apply(lambda x: x.zfill(6))

#handle missing: NaN,NaT
tb_bkmvt = tb_bkmvt.astype(object).where(tb_bkmvt.notnull(), None)



#Read interface file
#----------------------------------------------------------------------
#!/usr/bin/python
import MySQLdb

#Connection Database
con = MySQLdb.connect(host="10.108.1.10", user="proddba", passwd="dba@BSCA123", db="proddb")
cursor = con.cursor()
#target table
table_name = "ap_bkmvt"

arg_idx = tb_bkmvt['CLI'].drop_duplicates()

#1.query table, if record exists then drop line
args = dict(table=table_name, args_idx=', '.join("'"+arg_idx+"'"))

#sql = 'SELECT * FROM {table} t WHERE CONVERT(varchar(8),t.DATE_DEPOT, 112)= {arg_date}'.format(**args)
sql = 'SELECT * FROM {table} t WHERE t.CLI IN ({args_idx})'.format(**args)
logging.info('DONNEE A LIRE ' + sql)
tb_query = pd.read_sql(sql,con)

tb_query.columns = [x.upper() for x in tb_query.columns]


#create insert dataset
if len(tb_query) != 0:
    tb_query['in_query']=1
    #print tb_query
    #new record to insert

    tb_bkmvt['DVA'] = tb_bkmvt['DVA'].map(lambda x: x.strftime('%Y%m%d'))
    tb_bkmvt['DSAI'] = tb_bkmvt['DSAI'].map(lambda x: x.strftime('%Y%m%d'))
    
    tb_query['DVA'] = tb_query['DVA'].map(lambda x: x.strftime('%Y%m%d'))  
    tb_query['DSAI'] = tb_query['DSAI'].map(lambda x: x.strftime('%Y%m%d'))
        

    #non '999999'
    tb_insert = pd.merge(tb_bkmvt, tb_query[['DVA','DSAI','AGE','CLI','NAT','MHTT','DEVC','ETA','TCAI2','in_query']], how='outer', on=['DVA','DSAI','AGE','CLI','NAT','MHTT','DEVC','ETA','TCAI2',])
    tb_insert = tb_insert[tb_insert['in_query'].isnull()]    
    del tb_insert['in_query']
    
    tb_insert['DVA'] = tb_insert['DVA'].map(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
    tb_insert['DSAI'] = tb_insert['DSAI'].map(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
    #print tb_insert
else:
    tb_insert = tb_bkmvt


#DO actions while new records presnt
#----------------------------------------------------------------------
if len(tb_insert) > 0 :
    
    #check insert key and add id into tb_insert
    #----------------------------------------------------------------------
    sql = 'SELECT max(id)+1 FROM {table}'.format(**args)
    cursor.execute(sql)
    insert_key = cursor.fetchone()
    tb_insert['ID'] = range(insert_key[0], insert_key[0] + len(tb_insert))    
    #tb_insert['ID'] = range(1, 1 + len(tb_insert))  
    
    
    col_vals=['%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',
              '%s','%s','%s','%s','%s',
              '%s','%s','%s',
              ]
 
    cols= [
        'AGE',    #01.ENTITY (DEL AN E)
        'DVA', 	  #02.DATA_TRD
        'DSAI',   #03.DATE_VAL
        'HSAI',	  #04.TIME_VAL
        'DEVA',	  #05.CCY1
        'DEVC',	  #06.CCY2	
        'CLI',    #07.Client
        'NAT',    #08.NATURE
        'NOMP',   #09.CLIENT_NAME
        'NCP',    #10.CLIENT_ACC
        'SEN',    #11.DIRECTION
        'MNAT',	  #12.AMT1
        'MHTT',	  #13.AMT2
        'TCAI2',  #14.FX_RATE
        'ETA', 	  #15.STATUS
        'ID', 
        'TIMESTAMP',
        'CTRL',
    ]
    
    args = dict(table=table_name, cols =', '.join(cols), col_vals=', '.join(col_vals))
    sql = "INSERT INTO {table} ({cols}) VALUES ({col_vals})".format(**args) 

    tb_insert['TIMESTAMP'] = timestamp  
    tb_insert['CTRL'] = 0      

    #handle missing: NaN,NaT
    tb_insert = tb_insert.where(pd.notnull(tb_insert), None)
    
    #print tb_insert
    logging.info(tb_insert)
    
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
else:
    logging.info('No record to insert')


con.close()
#========================================McPreva===========================
#Standard ending code
#----------------------------------------------
logging.info('FEED_BKMVT.py Finished SUCCESSFULLY')