# -*- coding: utf-8 -*-
from __future__ import division

"""
Created on Mon Sep 04 10:07:30 2017

Run Enviroment: 
    python packages : numpy , pyomo  ( just pip install )
    extra supports : ipopt (need ipopt source and extention source to compliled)
@author: kanon
"""

import numpy as np

from pyomo.environ import ConcreteModel ,Set,Param,Var,Constraint,Objective,PositiveReals,PercentFraction,maximize

class MarkowitzModel(object):
    """
    A model of Markowitz 
    Get the best weight vector of securities with a expected return
    """
    def __init__(self,R,Ra=[] ,Er = 0.0 ):
        self.__model = ConcreteModel('Markowitz MODEL')
        model = self.__model
        if not Ra:
            Ra = list(map(lambda x : np.mean(x) , R))    
        n = len(Ra)
        #Create the inc with length n
        model.inc = Set(initialize=list(range(n)))
        self.__Ra = Ra
        temp0 = {}
        for i in range(n):
            temp0[i] = Ra[i]
                    
        #Create the parameter Ra
        model.ra = Param(model.inc , initialize = temp0)
        
        #Create the parameter Cov(R)
        covR = np.cov(R)
        self.__covR = covR
        temp1 = {}
        for i in range(len(covR)):
            for j in range(len(covR[i])):
              temp1[i,j] = covR[i][j]  
        model.covr = Param(model.inc , model.inc , initialize =temp1)
        
        temp2 = {}
        for i in range(n):
            temp2[i] = 1. / n
        #Create thr Var of weights
        model.w = Var(model.inc , domain=PositiveReals ,initialize = temp2 , bounds = (0.0 , 1.0))

        #def Cons_WeightLimit(self.model):
        #    return sum( [self.model.w[i] for i in self.model.inc] ) == 1
        model.cons_weight = Constraint(expr=sum( [model.w[i] for i in model.inc] ) == 1)

        model.cons_er = Constraint(expr=sum( [ model.w[i] * model.ra[i] for i in model.inc] ) >= (Er))
        
        #Object: Use the transfer equation to cal the Er and Risk
        model.obj = Objective(expr=sum( [ model.w[i] * model.ra[i] for i in model.inc] )/sum([ model.w[inc[0]] * model.w[inc[1]] * model.covr[inc] for inc in model.covr ]) , sense=maximize)        
    
    def solve(self):
        try:
            from pyomo.opt import SolverFactory
            sf = SolverFactory('ipopt.exe' , fee= True)
            sf.solve(self.__model)    
        except Exception as e:
            print '[ERROR]' , e
            return False , e , self.__Ra , 0 ,0 
        weight = [self.__model.w[item].value for item in self.__model.w] 
        weight = np.array(weight)
        w = np.ndarray((len(weight) , 1) , buffer =weight)
        wt = np.ndarray((1 , len(weight)) , buffer = weight)
        return True , weight , self.__Ra , np.sum(weight * self.__Ra) , np.sum( np.dot(w,wt) * self.__covR )
            
        
if __name__ == '__main__':
    from WindPy import w
    w.start()
    zh50 = 'a00103010b000000'
    hs300 = '1000002396000000'
    qA='a001010100000000'
    res0 = w.wset("sectorconstituent","date=2006-01-01;sectorid={}".format(qA))
    print res0
    codes = ",".join( res0.Data[1])
    res1 = w.wsd(codes, "pct_chg", "ED-1M", "2006-01-01", "Period=W;Fill=Previous;PriceAdj=B")
    #R = res1.Data
    import pandas as pd
    df = pd.DataFrame(res1.Data , index = res1.Codes , columns = res1.Times)
    df = df.fillna(0)
    model =  MarkowitzModel(df.values,Er = 0.3)
    flag , w ,ra , er , risk  = model.solve()
    if flag:
        print "Er:{} , Risk:{} , Er/Risk:{}".format( er , risk , er/risk)
        weight = pd.Series(  w  , index = res1.Codes )
        ra = pd.Series(ra , index = res1.Codes)
        result = pd.DataFrame()
        result.insert(0 , 'weight' , weight)
        result.insert(1 , 'ra' , ra)
        result = result.sort_values('weight', ascending = False)
        print result

