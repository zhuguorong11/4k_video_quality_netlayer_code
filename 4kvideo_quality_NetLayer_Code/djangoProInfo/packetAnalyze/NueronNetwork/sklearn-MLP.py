# coding:utf-8
# -*- coding: utf-8 -*-
from sklearn.neural_network import MLPClassifier

X = [[0., 0.], [1., 1.]]
y = [0, 1]

clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(5, 4,3), random_state=1)

clf.fit(X, y)
print 'predict\t', clf.predict([[2., 2.], [-1., -2.]])
print 'predict\t', clf.predict_proba([[2., 2.], [1., 2.]])
print 'clf.coefs_ contains the weight matrices that constitute the model parameters:\t', [coef.shape for coef in
                                                                                          clf.coefs_]
print clf
c = 0
for i in clf.coefs_:
    c += 1
    print c, len(i), i