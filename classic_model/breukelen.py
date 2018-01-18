# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 12:14:38 2017

@author: kanon
"""
import pandas as pd
import numpy as np

from WindPy import *
w.start()

def breukelen(classification , p , b ):
    def calWD(matrix): 
        return reduce(lambda x,y : x + y , map(lambda x : x[0] * x[1]  , matrix) , 0)
    def calWR(matrix) : 
        return reduce(lambda x,y : x + y , map(lambda x : x[0] * x[1] * x[2], matrix) , 0)
    Dp = calWD(p)
    Db = calWD(b)
    Rp = calWR(p)
    Rb = calWR(b)    
    Ds = map(lambda x : (Dp / Db - 1) * x[0] * x[1] * x[2] , b )
    Ws = map(lambda x ,y : (x[0] * x[1] - (Dp / Db) * y[0] * y[1])*(y[2] - Rb) , p , b)
    Ps = map(lambda x, y : (x[0] * x[1]) * (x[2] - y[2]) , p , b)
    return pd.DataFrame([Ds , Ws , Ps] ,index = ['duration' , 'allocation' , 'select'] , columns = classification ).T

def AdditionData(symbol , tradedate):
    symbols = ",".join(symbol)
    rs = w.wss("{}".format(symbols), "ytm_b,ptmyear,modifiedduration","tradeDate={};returnType=1;credibility=1".format(tradedate))
    
    df =  pd.DataFrame(rs.Data , index = rs.Fields )
    df = df.T
    df['CODES'] = rs.Codes
    return df

def ProductTimeMatrix(df):
    total = df['amount'].sum()
    
    conditions = [ (df['PTMYEAR'] > 0) & (df['PTMYEAR'] <= 1),
                   (df['PTMYEAR'] > 1) & (df['PTMYEAR'] <= 3),
                   (df['PTMYEAR'] > 3) & (df['PTMYEAR'] <= 6),
                   (df['PTMYEAR'] > 6) & (df['PTMYEAR'] <= 10),
                   df['PTMYEAR'] > 10]
    Ws = []
    Ds = []
    Rs = []
    for condition in conditions:
        cond = df[condition]
        W = cond['amount'].sum() / total
        D = 0
        R = 0
        if W > 0 :
            D = (cond['amount'] * cond['MODIFIEDDURATION']).sum() / cond['amount'].sum()
            R = (cond['amount'] * cond['YTM_B']).sum() / cond['amount'].sum() / 100
        Ws.append(W)
        Ds.append(D)
        Rs.append(R)
    return np.transpose([Ws, Ds , Rs])
   
def governmentLoanBase(tradedate):
    
    from sqlalchemy import create_engine
    sourceDBconnStr =  'postgresql://trms:trms@trms-ppas-outter.ppas.rds.aliyuncs.com:3432/trms'
    engine = create_engine(sourceDBconnStr)
    
    
    sql = """  SELECT  
        	DISTINCT(s_info_windcode)
        FROM
        	wind_cbonddescription
        WHERE
        	b_info_issuercode = '2000850'
        AND b_info_maturitydate > '20170901'
        AND s_info_exchmarket = 'NIB'
        AND b_info_carrydate > '20170101'
        AND is_incbonds = '0'
    """
    df = pd.read_sql_query(sql , con = engine)

    symbols = ",".join(df['s_info_windcode'])
    rs = w.wss("{}".format(symbols), "ytm_b,ptmyear,modifiedduration,bondsettle_transaction","tradeDate={};returnType=1;credibility=1".format(tradedate))

    df =  pd.DataFrame(rs.Data , index = rs.Fields )
    df = df.T
    df['CODES'] = rs.Codes
    #df.rename(columns = {'BONDSETTLE_TRANSACTION':'amount'}, inplace = True)
    df['amount'] = pd.Series([1.] * df['CODES'].size) 
    df = df.dropna()   
    print df
    return ProductTimeMatrix(df)
     
    
    
def preTRMSPosition(tradedate):
    from sqlalchemy import create_engine
    sourceDBconnStr =  'postgresql://trms:trms@trms-ppas-outter.ppas.rds.aliyuncs.com:3432/trms'
    engine = create_engine(sourceDBconnStr)
    
    sql = "SELECT productid, symbol, px, vol, px * vol * 100 AS amount FROM position_detail WHERE tradedate = '{}' AND symboltype = '债券' AND SOURCE = '普通' AND vol > 0 AND productid NOT IN( SELECT productid FROM trm_product_name WHERE invest_type IN ('5'))".format(tradedate)
    poDf = pd.read_sql_query(sql , con = engine)
    
    seces = poDf['symbol'].unique()
    productids = poDf['productid'].unique()
    addDf = AdditionData(seces , tradedate)
    
    df = pd.merge(poDf , addDf , how = 'left' , left_on = 'symbol' , right_on = 'CODES')
    
    productData = {}
    for productid in productids:
        temp = df[df['productid'] == productid]
        productData[productid] = ProductTimeMatrix(temp)
    return productData
    
    

if __name__ == "__main__":
    c = ['(0,1]', '(1,3]' , '(3,6]' , '(6,10]' , '(10, )']
    analysisdate = '20170901'
    
    productData = preTRMSPosition(analysisdate)
    base = governmentLoanBase(analysisdate)
    print 'base:'
    print base
    print 'end'
    for key in productData:
        print "\n" , key 
        rst = breukelen(c,productData[key],base)
        print rst
        print rst['duration'].sum(),rst['allocation'].sum() , rst['select'].sum()
        print np.sum([ rst['duration'].sum(),rst['allocation'].sum() , rst['select'].sum()])
    print base