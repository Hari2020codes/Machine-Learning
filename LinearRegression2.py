from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import datasets,linear_model
from sklearn import metrics
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error,r2_score
df=pd.read_excel('aptitude.xlsx')

X=df[['x1']]
y=df[['y1']]
x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=0.3)
clf=LinearRegression()
clf.fit(x_train,y_train)
y_pred=clf.predict(x_test)
print(y_pred)
print("y=",clf.intercept_,"+",clf.coef_,"* x")
newvalue=float(input("enter the score:"))
y_pred=clf.intercept_+clf.coef_*newvalue
print(y_pred)

output
===========
x1	y1
95	85
85	95
80	70
70	65
60	70

[[101.84210526]
 [ 85.65789474]]
y= [-0.65789474] + [[1.07894737]] * x
enter the score:80
[[85.65789474]]

