# -*- coding: utf-8 -*-

"""
Created on Mon Sep 04 10:07:30 2017

Run Enviroment: 
    python packages : numpy , pyomo  ( just pip install )
    extra supports : ipopt (need ipopt source and extention source to compliled)
    install guide: https://www.coin-or.org/Ipopt/documentation/node10.html

@author: kanon
"""

import numpy as np

from pyomo.environ import ConcreteModel ,Set,Param,Var,Constraint,Objective,PositiveReals,PercentFraction,maximize

class MarkowitzModel(object):
    """
    A model of Markowitz 
    Get the best weight vector of securities with a expected return
    if expected return Ra is not given, will use mean to replace
    """
    def __init__(self,R,Ra=[] ,Er = 0.0 ):
        self.__model = ConcreteModel('Markowitz MODEL')
        model = self.__model
        if not Ra:
            Ra = list([np.mean(x) for x in R])    
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
            sf = SolverFactory('ipopt' , fee= True)
            sf.solve(self.__model)    
        except Exception as e:
            print(e)
            return False , e , self.__Ra , 0 ,0 
        weight = [self.__model.w[item].value for item in self.__model.w] 
        weight = np.array(weight)
        w = np.ndarray((len(weight) , 1) , buffer =weight)
        wt = np.ndarray((1 , len(weight)) , buffer = weight)
        return True , weight , self.__Ra , np.sum(weight * self.__Ra) , np.sum( np.dot(w,wt) * self.__covR )
            
        
def example():
    values = [
        [0.2 , 1.3 , 3 ,12 ,32. ,1.2 ,0.4],
        [0.1 , 0.2 , 3 ,0  ,0.5 ,0.5 ,0.5]
    ]

    model =  MarkowitzModel(values,Er = 0.3)
    flag , w ,ra , er , risk  = model.solve()
    if flag:
        print("Er:{} , Risk:{} , Er/Risk:{}".format( er , risk , er/risk))
        print(ra)
        print(w)

example()