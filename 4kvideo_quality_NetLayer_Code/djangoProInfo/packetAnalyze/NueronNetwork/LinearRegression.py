# coding:utf-8
# -*- coding: utf-8 -*-
from sklearn import linear_model
clf1 = linear_model.LinearRegression(copy_X=True,fit_intercept=True,n_jobs=1,normalize=False)

clf1.fit([[0,0],[1,1],[2,2],[2,3]],[0,1,2,3])
print clf1.coef_



#Ridge󰀃将数组X和y作fit方法的参数，将线性模型的系数存在成员变量coef_

clf2 = linear_model.Ridge(alpha=.5)
clf2.fit([[0,0],[0,0],[1,1]],[0,.1,1])
print clf2.coef_
print clf2.predict([1,1])
