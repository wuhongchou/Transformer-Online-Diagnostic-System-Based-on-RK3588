import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

class RFclass:
    def __init__(self,dataset):
        self.dataset=dataset

    def RFrun(self):
        # 划分数据矩阵和标签
        X = self.dataset.iloc[:, :-1]
        y = self.dataset.iloc[:, -1]
        # 处理缺失值
        X.fillna(X.mean(), inplace=True)

        # 特征缩放
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # 训练测试集分割
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        # 模型训练
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # 模型评估
        y_pred = model.predict(X_test)
        X_test=scaler.inverse_transform(X_test)
        X_test = pd.DataFrame(X_test)  
        y_test=y_test.to_numpy()
        #y_test=y_test.to_frame()
        X_test['act']=pd.DataFrame(y_test, columns=['act'])
        df=X_test.reset_index(drop=True)
        y_pred=pd.DataFrame(y_pred, columns=['RF'])
        df['RF']=y_pred
        df.columns=['h2','ch2','c2h6','c2h4','c2h2','act','RF']
        df=df.round(3)
        return df



