import pandas as pd
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np

class XGboostclass:
    def __init__(self,dataset):
        self.dataset=dataset
    
    def XGboostrun(self):
        # 划分数据矩阵和标签
        X = self.dataset.iloc[:, :-1]
        y = self.dataset.iloc[:, -1]
        
        
        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,stratify=y,random_state=0)
        
        model=GradientBoostingClassifier(random_state=12)

        #生成实例model后用fit()方法进行估计
        model.fit(X_train, y_train)

        y_pre = model.predict(X_test)

        #使用score()方法计算测试集的预测准确率
        accurate=model.score(X_test,y_test)
        
        X_test = pd.DataFrame(X_test)  
        y_test=y_test.to_frame()
        X_test['act']=y_test
        df=X_test.reset_index(drop=True)
        y_pre=pd.DataFrame(y_pre, columns=['XGboost'])
        df['XGboost']=y_pre
        
        return df

