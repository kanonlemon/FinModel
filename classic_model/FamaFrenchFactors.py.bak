# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 13:32:41 2017

@author: kanon
"""

"""
Three Factors
Ri = a + bx(Rm-Rf) + cxSMB + dxHML + e'

Five Factors
Ri = a + bx(Rm-Rf) + cxSMB + dxHML + exRMW + fxCMA + e'

Rm = rm - rf (the return of index - risk-free interest rate)
SMB = E(rs) - E(rb) : small mv return - big mv return
HML = E(rh) - E(rl) : high bv/mv - low bv/mv
RMW = E(rh) - E(rl) : high roe - low roe
CMA = E(rh) - E(rl) : low yoy_asset - high yoy_asset
"""
import pandas as pd
import numpy as np

class FamaFrenchFactors():
    
    def __init__(self):
        pass
    
    def GenerateFiveFactors(self ,rf , data ):
        """
        data template:
        Rm = 0.15   (0.15% return of day)
        rf = 0.12   (0.12% return of cash)  
        data = 
        [
        [ mv_1 , bps_1 , roe_1 , yoy_asset_1 , return_1]
        [ mv_2 , bps_2 , roe_2 , yoy_asset_2 , return_2],
                        ...
        [ mv_n , bps_n , roe_n , yoy_asset_n , return_n]
        ]
        where n is the number of portfolio’s underlyings
        
        Return : (rm-rf , SMB , HML , RMW , CMA , rf)
        """
        df = pd.DataFrame(data , columns = ['mv', 'bps' , 'roe' , 'yoy_asset' , 'return'])
        
        rm = (df['mv'] * df['return']).sum() / df['mv'].sum()
        rmMrf = rm - rf
        df['return'] = df['return'] - rf 
        #Asc
        #Small Minus Big, The Small may have more rM-rF
        SMB_ASC = df.sort_values('mv')['return'].tolist()
        #Des
        #High Bps maybe underestimated
        HML_DES = df.sort_values('bps' , ascending = False)['return'].tolist()
        #Des
        #High return may have more rM-rF
        RMW_DES = df.sort_values('roe'  , ascending = False)['return'].tolist()
        #Asc
        #Low reinvestment may have more rM-rF 
        CMA_ASC = df.sort_values('yoy_asset' )['return'].tolist()
        
        getEr = lambda x : np.mean(x[0:len(x)/3]) - np.mean(x[len(x)/3*2:])
        
        result = map(getEr , [SMB_ASC,HML_DES,RMW_DES,CMA_ASC])    
        return (rmMrf , result[0], result[1], result[2], result[3], rf)
   
    def GenerateThreeFactors(self ,rf , data ):
        """
        data template:
        Rm = 0.15   (0.15% return of day)
        rf = 0.12   (0.12% return of no-risk)  
        data = 
        [
        [ mv_1 , bps_1 ,  return_1]
        [ mv_2 , bps_2 ,  return_2],
                    ...
        [ mv_n , bps_n ,  return_n]
        ]
        where n is the number of portfolio’s underlyings
        
        Return : [rm-rf , SMB , HML , rf]
        """
        df = pd.DataFrame(data , columns = ['mv', 'bps' , 'return'])
        
        rm = (df['mv'] * df['return']).sum() / df['mv'].sum()
        rmMrf = rm - rf
        df['return'] = df['return'] - rf 
        #Asc
        #Small Minus Big, The Small may have more rM-rF
        SMB_ASC = df.sort_values('mv')['return'].tolist()
        #Des
        #High Bps maybe underestimated
        HML_DES = df.sort_values('bps' , ascending = False)['return'].tolist()
        
        getEr = lambda x : np.mean(x[0:len(x)/3]) - np.mean(x[len(x)/3*2:])
        
        result = map(getEr , [SMB_ASC,HML_DES])    
        return (rmMrf , result[0], result[1], rf)
    