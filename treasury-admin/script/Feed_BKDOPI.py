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
#rptDate = '20180302'

#Log configuration
#----------------------------------------------------------------------
DEBUG = False
if not DEBUG:
    logPyPath = '\\\\10.205.176.250\\share-dmf\\Working_Src\\batch\\log_py\\'+ today
    if not os.path.exists(logPyPath):
        os.makedirs(logPyPath)
    
    logging.basicConfig(filename=logPyPath+'\\'+'FEED_BKDOPI_' + rptDate + '_' + timestamp + '.log', level=logging.DEBUG)
    logging.info('Today Date is ' + today + ' Update Timestamp is ' + timestamp)
    logging.info('FEED_BKDOPI.py Starts')
    logging.info('Report Date is ' + rptDate)
########################################################################


#Read interface file
#----------------------------------------------------------------------
file = '\\\\10.205.176.250\\share-dit\\dmf\\' + rptDate + '_BKDOPI.txt'

logging.info('Reading File ' + file)
tb_bkdopi = pd.read_csv(file, sep='|', index_col=False)

#read interface files
#----------------------------------------------------------------------
old_names = [
    'NAT', 	  #01.Nature  
    'AGE', 	  #02.Branch_ID
    'NDOS',   #03.Ref_ID*/
    'ETA',	  #04.Status
    'DEV',	  #05.Ccy
    'OTRF',	  #06.OrderType	
    'NOMDO',  #07.Client
    'NCPDO',  #08.CAcc
    'NOMBF',  #09.Bene
    'NCPBF',  #10.BeneAcc
    'MDEV',   #11.FCcyAmt
    'MNET',	  #12.LCcyAmt
    'MBAN',	  #13.Net Amount to the Bank
    'TXCP',   #14.FxRate replaced TDEV 201707
    'DVA', 	  #15.Value Date*/
    'DEXEC',  #16.Exec Date*/
    'FCORR',  #17.CorrespChgType
    'MOTIF1', #18.Reason1
    'MOTIF2', #19.Reason2
    'MOTIF3', #20.Reason3
    'UTI'
]

#replace interface file column with new name
new_names = [
    'NATURE', 	      #NAT  
    'AGENCE_ID',      #AGE
    'REF_ID',         #NDOS*/
    'STATUT_SYS',     #ETA
    'CCY_CODE',	      #DEV
    'OTRF',	          #OrderType	
    'DONNEUR',        #NOMDO
    'NCPDO',          #CAcc
    'BENEF',          #NOMBF
    'NCPBF',          #BeneAcc
    'MONTANT',        #MDEV
    'MONTANT_XAF',	  #MNET
    'MONTANT_XAF_NET',#Net Amount to the Bank
    'FX_RATE',	      #TXCP
    'DATE_VAL',       #DVA
    'DATE_EXEC',      #DEXEC
    'FEE_TYPE',       #FCORR
    'MOTIF1',         #Reason1
    'MOTIF2',         #Reason2
    'MOTIF3',         #Reason3
    'UTI'
    ]
    
tb_bkdopi.rename(columns=dict(zip(old_names, new_names)), inplace=True)
tb_bkdopi['REF_ID'].drop_duplicates()

tb_bkdopi = tb_bkdopi.where(pd.notnull(tb_bkdopi), None)
#
tb_bkdopi['NCPDO'] = tb_bkdopi['NCPDO'].astype(str)
tb_bkdopi['NCPBF'] = tb_bkdopi['NCPBF'].astype(str)
tb_bkdopi['NCPDO'] = tb_bkdopi['NCPDO'].map(lambda x: x.replace('.0', ''))
tb_bkdopi['NCPBF'] = tb_bkdopi['NCPBF'].map(lambda x: x.replace('.0', ''))

#add nature
tb_bkdopi['NATURE'] = tb_bkdopi['REF_ID'].str.extract("(\w{3})")

#convert french number to float
tb_bkdopi['FX_RATE'] = tb_bkdopi['FX_RATE'].map(lambda x: float(x.replace(',', '.')))

tb_bkdopi['MONTANT'] = tb_bkdopi['MONTANT'].map(lambda x: float(x.replace(',', '.')))
tb_bkdopi['MONTANT_XAF'] = tb_bkdopi['MONTANT_XAF'].map(lambda x: float(x.replace(',', '.')))

#concatenate MOTIF
tb_bkdopi['MOTIF'] = tb_bkdopi['MOTIF1'] + tb_bkdopi['MOTIF2'] + tb_bkdopi['MOTIF3']

tb_bkdopi['INV'] = tb_bkdopi['MOTIF'].str.extract("(/INV/\S*\w+\s+\w+ \d{2,4}/?\d{2}/?\d{2,4})")

#convert date to yyyymmdd
tb_bkdopi = tb_bkdopi.where(pd.notnull(tb_bkdopi), None)
tb_bkdopi[['DATE_VAL','DATE_EXEC']] = tb_bkdopi[['DATE_VAL','DATE_EXEC']].fillna("01/01/1970")

tb_bkdopi['DATE_VAL'] = tb_bkdopi['DATE_VAL'].map(lambda x: pd.to_datetime(str(x), format='%d/%m/%Y'))
tb_bkdopi['DATE_VAL'] = tb_bkdopi['DATE_VAL'].map(lambda x: x.strftime('%Y%m%d'))
idx = tb_bkdopi[tb_bkdopi['DATE_VAL'] == '19700101'].index
tb_bkdopi.loc[idx,'DATE_VAL'] = ""

tb_bkdopi['DATE_EXEC'] = tb_bkdopi['DATE_EXEC'].map(lambda x: pd.to_datetime(str(x), format='%d/%m/%Y'))
tb_bkdopi['DATE_EXEC'] = tb_bkdopi['DATE_EXEC'].map(lambda x: x.strftime('%Y%m%d'))
idx = tb_bkdopi[tb_bkdopi['DATE_EXEC'] == '19700101'].index
tb_bkdopi.loc[idx,'DATE_EXEC'] = ""




#Read interface file
#----------------------------------------------------------------------

#!/usr/bin/python
import MySQLdb

#Connection Database
con = MySQLdb.connect(host="10.108.1.10", user="proddba", passwd="dba@BSCA123", db="proddb")
cursor = con.cursor()


#target table
table_name = "ap_bkdopi"

arg_idx = tb_bkdopi['REF_ID']
#1.query table, if record exists then drop line
args = dict(table=table_name, args_idx=', '.join("'"+arg_idx+"'"))
#sql = 'SELECT * FROM {table} t WHERE CONVERT(varchar(8),t.DATE_DEPOT, 112)= {arg_date}'.format(**args)
sql = 'SELECT * FROM {table} t WHERE t.REF_ID IN ({args_idx})'.format(**args)
logging.info('DONNEE A LIRE ' + sql)
tb_query = pd.read_sql(sql,con)


#create insert dataset
if len(tb_query) != 0:
    tb_query['in_query']=1
    #print tb_query
    #new record to insert
    tb_insert = pd.merge(tb_bkdopi,tb_query[['id','REF_ID','STATUT_SYS','in_query',]], how='outer', on=['REF_ID','STATUT_SYS'])
    tb_insert = tb_insert[tb_insert['in_query'] !=1]
    del tb_insert['in_query']
    #print tb_insert
else:
    tb_insert = tb_bkdopi


#DO actions while new records presnt
#----------------------------------------------------------------------
if len(tb_insert) > 0 :
    #target table
    table_name = "ap_bkdopi" 
    
    #check insert key and add id into tb_insert
    #----------------------------------------------------------------------
    sql = 'SELECT max(id)+1 FROM {table}'.format(**args)
    cursor.execute(sql)
    insert_key = cursor.fetchone()
    tb_insert['ID'] = range(insert_key[0], insert_key[0] + len(tb_insert))    

    col_vals=['%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',
              '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',
              '%s','%s','%s','%s',
              ]
 
    cols= [
        'NATURE', 	      #NAT  
        'AGENCE_ID',      #AGE
        'REF_ID',         #NDOS*/
        'STATUT_SYS',     #ETA
        'CCY_CODE',	      #DEV
        'OTRF',	          #OrderType	
        'DONNEUR',        #NOMDO
        'NCPDO',          #CAcc
        'BENEF',          #NOMBF
        'NCPBF',          #BeneAcc
        'MONTANT',        #MDEV
        'MONTANT_XAF',	  #MNET
        'FX_RATE',	      #TDEV
        'DATE_VAL',       #DVA
        'DATE_EXEC',      #DEXEC
        'INV',            #DEXEC
        'FEE_TYPE',       #FCORR
        'MOTIF',          #Reason1
        'UTI',
        'ID',
        'statut_id',
        'dossierCtrl_id',    
        'dossierCouvr_id',     
        'TIMESTAMP'
    ]
    
    args = dict(table=table_name, cols =', '.join(cols), col_vals=', '.join(col_vals))
    sql = "INSERT INTO {table} ({cols}) VALUES ({col_vals})".format(**args) 

    tb_insert['statut_id'] = None  
    tb_insert['dossierCtrl_id'] = None  
    tb_insert['dossierCouvr_id'] = None 
    tb_insert['CTRL'] = False 
    tb_insert['TIMESTAMP'] = timestamp     

    #handle missing: NaN,NaT
    tb_insert = tb_insert.where(pd.notnull(tb_insert), None)
    
    #tb_insert[['DATE_VAL','DATE_EXEC']] = tb_insert[['DATE_VAL','DATE_EXEC']].fillna(0)
    
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
        
        #check insert key and add id into tb_insert
        #----------------------------------------------------------------------
        sql = """
        INSERT INTO trf_dossier_exec
        (
                apbkdopi_ptr_id
                ,trfDossierCouvr_id
                ,trfDossier_id
                ,statut_id
                ,date_val_d
                ,date_exec_d
                ,ctrl
        )
        SELECT 
                id 		as apbkdopi_ptr_id
                ,Null 	as dossierCouvr_id
                ,Null  	as dossierCtrl_id 
                ,Null 	as statut_id
                ,STR_TO_DATE(DATE_VAL,'%Y%m%d') as date_val_d
                ,STR_TO_DATE(DATE_EXEC,'%Y%m%d') as date_exec_d
                ,False  as ctrl 
        FROM ap_bkdopi
        WHERE id NOT IN (SELECT DISTINCT apbkdopi_ptr_id FROM trf_dossier_exec)
        """
        cursor.execute(sql)    
        con.commit()
            
    except:
        e = sys.exc_info()[0]
        logging.error(e)
        sys.exit(0)
 
        #update
  
con.close()
#========================================McPreva===========================
#Standard ending code
#----------------------------------------------
logging.info('FEED_BKDOPI.py Finished SUCCESSFULLY')