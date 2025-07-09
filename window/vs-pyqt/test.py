import sys
import os
import csv
import shutil
import time
from datetime import datetime
import pandas as pd
import pyqtgraph as pg
from PyQt5.QtGui import QPixmap,QFont,QTextCursor
from PyQt5.QtWidgets import QApplication,QTextEdit,QVBoxLayout, QMainWindow,QComboBox, QPushButton,QWidget,QFileDialog, QTableWidget, QTableWidgetItem,QMessageBox,QDialog
from 油色谱_ui import Ui_Mainwindow
from Form_ui import Ui_METHODCONFIGURE
from 登录_ui import Ui_denglu
from 密码错误_ui import Ui_mimacuowu
from dataset_ui import Ui_DATASETCONFIGURE
from communication_ui import Ui_txsz
from option_ui import Ui_option
from help_ui import Ui_sybz
from model_ui import Ui_mxjs
from predict_ui import Ui_ycmk
from warning_ui import Ui_bjjl
from methods.Key import Keyclass
from methods.Duval import Duvalclass
from methods.XGboost import XGboostclass
from methods.Rogers4 import Rogers4class
from methods.RF import RFclass
from methods.IEC60599 import IEC60599class
from PyQt5.QtCore import pyqtSignal, QTimer,QThread,QDateTime
import requests
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import matplotlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
import serial
import serial.tools.list_ports
from datetime import datetime
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="sip")


class SpecialWindow(QWidget, Ui_METHODCONFIGURE):
    my_signal = pyqtSignal(list)  # 创建一个信号
    
    listitems=["Duval","XGboost","RF","Rogers'4","IEC60599","Key"]
    lineEdit_2_text=["./methods/Duval.py","./methods/XGboost.py","./methods/RF.py","./methods/Rogers4.py","./methods/IEC60599.py","./methods/Key.py","","","","",""]
    
    A=''#方法
    B=''#路径
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.method_add)
        self.pushButton_2.clicked.connect(self.method_delete)
        #self.pushButton_4.clicked.connect(self.emit_signal)  # 按钮点击时发射信号
        self.pushButton_4.clicked.connect(self.method_save)
        
        self.pushButton_3.clicked.connect(self.method_browse)
        self.lineEdit.textEdited.connect(self.onTextChanged)
        self.filePath='1'

        for item_text in self.listitems:
            self.listWidget.addItem(item_text)
        #默认选中第一个
        item = self.listWidget.item(0)  # item(0) 是列表中的第一个项
        self.listWidget.setCurrentItem(item)
        selected_items = self.listWidget.selectedItems()
        selected_texts = [item.text() for item in selected_items]
        self.lineEdit.setText(', '.join(selected_texts))
        if selected_texts==['Duval']:
            self.lineEdit.setText(', '.join(selected_texts))
            relative_path = './methods/Duval.py'
            self.lineEdit_2.setText(relative_path)
            self.textEdit.append('1. Duval, M.: "A review of faults detectable by gas-in-oil analysis in transformers", IEEE Electr. Insul. Mag., 18, (3), pp. 8_17, 2002.')
            self.textEdit.append('2. Duval, M.: "Interpretation of gas-in-oil analysis using new IEC publication 60599 and IEC TC 10 databases", IEEE Electr. Insul. Mag., 17, (2), pp. 31_41, 2001.")')
        elif selected_texts==['XGboost']:
            self.lineEdit.setText(', '.join(selected_texts))
        elif selected_texts==['Clustering']:
            self.lineEdit.setText(', '.join(selected_texts))
        elif selected_texts==["Rogers'4"]:
            self.lineEdit.setText(', '.join(selected_texts))
        elif selected_texts==['IEC60599']:
            self.lineEdit.setText(', '.join(selected_texts))  
        elif selected_texts==['Key']:
            self.lineEdit.setText(', '.join(selected_texts))  
        else:
            self.lineEdit.setText('0 ')
        
        # 连接currentRowChanged信号到槽函数，当选项变化时更改标签内容
        self.listWidget.currentRowChanged.connect(self.RowChanged)
    
    # 当选择的条目变化时，更新标签的文本
    #def RowChanged(self, current, previous):
    def RowChanged(self,row):
        #self.lineEdit.setText(f"{current.text()}")
        currentitem = self.listWidget.currentItem()
        if currentitem is not None:
            
            currentitem = currentitem.text()
        self.lineEdit.setText(currentitem)
        if row==0:
        #if  current.text()=='Duval':
            #self.lineEdit.setText(f"{current.text()}")
            self.lineEdit.setReadOnly(True)
            relative_path = self.lineEdit_2_text[row]
            self.lineEdit_2.setText(relative_path)
            self.textEdit.setPlainText('1. Duval, M.: "A review of faults detectable by gas-in-oil analysis in transformers", IEEE Electr. Insul. Mag., 18, (3), pp. 8_17, 2002.')
            self.textEdit.append('2. Duval, M.: "Interpretation of gas-in-oil analysis using new IEC publication 60599 and IEC TC 10 databases", IEEE Electr. Insul. Mag., 17, (2), pp. 31_41, 2001.")')
        elif row==1:
            self.textEdit.setPlainText('1.王雨虹,王志中. 基于RFRFE与ISSA-XGBoost的变压器故障辨识方法 [J]. 电子测量与仪器学报, 2021, 35 (12): 142-150. DOI:10.13382/j.jemi.B2104384.')
            
            self.lineEdit.setReadOnly(True)
            relative_path = self.lineEdit_2_text[row]
            self.lineEdit_2.setText(relative_path)
        elif row==2:
            
            self.lineEdit.setReadOnly(True)
            relative_path = self.lineEdit_2_text[row]
            self.lineEdit_2.setText(relative_path)
            self.textEdit.setPlainText(' Sherif S. M. Ghoneim, and Ibrahim B. M. Taha,"A New Approach of DGA Interpretation Technique for Transformer Fault Diagnosis", International Journal of Electrical Power and Energy Systems, 81, Oct. 2016, pp. 265–274.')
        elif row==3:
           
            self.lineEdit.setReadOnly(True)
            relative_path = self.lineEdit_2_text[row]
            self.lineEdit_2.setText(relative_path)
            self.textEdit.setPlainText('1. IEEE Guide for the Interpretation of Gases Generated in Oil-Immersed Transformers, IEEE Standard C57.104-2008, Feb. 2009.')
            self.textEdit.append('2. Sherif S. M. Ghoneim, and I. B. M. Taha, and N. I. Elkalashy," Integrated ANN-Based Proactive Fault Diagnostic Scheme for Power Transformers Using Dissolved Gas Analysis", IEEE Transactions on Dielectric and Electrical Insulation, Vol. 23, No. 3, pp. 1838-1845, June 2016.')
            self.textEdit.append('3. J. L. Guardado, J. L. Nared, P. Moreno, and C. R. Fuerte, "A Comparative Study of Neural Network Efficiency in Power Transformers Diagnosis Using Dissolved Gas Analysis", IEEE Trans. Power Delivery, Vol. 16, No. 4, pp. 643 – 647, 2001.')
            self.textEdit.append('4. Ibrahim B. M. Taha, Sherif S. M. Ghoneim, and Hatim G. Zaini, "A Fuzzy Diagnostic System for Incipient Transformer Faults Based on DGA of the Insulating Transformer Oils", International Review of Electrical Engineering (I.R.E.E.), Vol. 11, n. 3, pp. 305-313, June 2016.')
        elif row==4:
           
            self.lineEdit.setReadOnly(True)
            relative_path = self.lineEdit_2_text[row]
            self.lineEdit_2.setText(relative_path)
            self.textEdit.setPlainText('1. IEC Publication 599, “Interpretation of the analysis of gases in transformers and other oil-filled electrical equipment in service,” First Edition 1978.')
            self.textEdit.append('2. Sherif S. M. Ghoneim, and I. B. M. Taha, and N. I. Elkalashy," Integrated ANN-Based Proactive Fault Diagnostic Scheme for Power Transformers Using Dissolved Gas Analysis", IEEE Transactions on Dielectric and Electrical Insulation, Vol. 23, No. 3, pp. 1838-1845, June 2016. ')
            self.textEdit.append('3. J. L. Guardado, J. L. Nared, P. Moreno, and C. R. Fuerte, "A Comparative Study of Neural Network Efficiency in Power Transformers Diagnosis Using Dissolved Gas Analysis", IEEE Trans. Power Delivery, Vol. 16, No. 4, pp. 643 – 647, 2001.')
            self.textEdit.append('4. Ibrahim B. M. Taha, Sherif S. M. Ghoneim, and Hatim G. Zaini, "A Fuzzy Diagnostic System for Incipient Transformer Faults Based on DGA of the Insulating Transformer Oils", International Review of Electrical Engineering (I.R.E.E.), Vol. 11, n. 3, pp. 305-313, June 2016.')
        elif row==5:
           
            self.lineEdit.setReadOnly(True)
            relative_path = self.lineEdit_2_text[row]
            self.lineEdit_2.setText(relative_path)
            self.textEdit.setPlainText('等待添加2')
        elif row==6:
            self.lineEdit_2.setText(self.lineEdit_2_text[row])
            self.textEdit.setPlainText('请添加...')
        elif row==7:
            self.lineEdit_2.setText(self.lineEdit_2_text[row])
            self.textEdit.setPlainText('请添加...')
        elif row==8:
            self.lineEdit_2.setText(self.lineEdit_2_text[row])
            self.textEdit.setPlainText('请添加...')
        elif row==9:
            self.lineEdit_2.setText(self.lineEdit_2_text[row])
            self.textEdit.setPlainText('请添加...')
        elif row==10:
            self.lineEdit_2.setText(self.lineEdit_2_text[row])
            self.textEdit.setPlainText('请添加...')
        else:
            self.lineEdit_2.setText('请选中...')
            self.textEdit.setPlainText('请选中...')
    
    def closeEvent(self, event):
        # 发射自定义信号，传递信息给窗口A
        self.my_signal.emit(self.listitems)
        #self.my_signal2.emit(self.B)
        super().closeEvent(event)

    def method_add(self):
        self.listWidget.clearSelection()
        items=['new method']
        self.listWidget.addItems(items)
        self.lineEdit.setReadOnly(False)
        self.lineEdit.setText('new method')
        self.lineEdit_2.setText('请添加路径')
        self.textEdit.setPlainText('请添加文章')
        #读取目前有多少项
        itemCount = self.listWidget.count()
        row=itemCount-1
        #self.listitems[row]='newmethod'
        #s#elf.lineEdit_2_text[row]='请添加路径'
        #刚添加的方法为选定项
        self.listWidget.setCurrentRow(row)
        current_item = self.listWidget.currentItem()
        self.selected_text2 = current_item.text()
        self.listitems.append(self.selected_text2)
        row_count = self.listWidget.count()
        self.lineEdit_2_text[row_count-1]=self.B
        self.lineEdit.setText((current_item.text()))

    def method_delete(self):
        row = self.listWidget.currentRow()
        #保证默认的6个方法不会被删除
        if row >5:
            del self.listitems[row]
            self.listWidget.takeItem(row)
            
            
            #self.lineEdit_2_text[row]=''
        else:
            self.listWidget.clearSelection()

    def method_save(self):
        # 给定的文件绝对路径
        source_file_path = self.filePath

        # 使用os.path.basename获取文件名
        file_name = os.path.basename(source_file_path)

        # 目标路径
        absolute_path = "C:\\Users\\wuhongchou\\Desktop\\vs-pyqt\\methods"

        # 使用os.path.join将绝对路径和文件名结合起来
        destination_file_path = os.path.join(absolute_path, file_name)

        # 确保目标目录存在，如果不存在则创建
        destination_dir = os.path.dirname(destination_file_path)
        if not os.path.exists(destination_dir):
         os.makedirs(destination_dir)

        # 复制文件
        try:
            shutil.copy(source_file_path, destination_file_path)
            print(f"文件已从 {source_file_path} 复制到 {destination_file_path}")
        except IOError as e:
            print(f"无法复制文件. {e}")
        except Exception as e:
            print(f"发生错误: {e}")
        
        row = self.listWidget.currentRow()
        #保证默认的6个方法不会再添加
        if row >5:
            self.A=self.lineEdit.text()
            self.B=self.lineEdit_2.text()
            self.lineEdit_2_text[row]=self.B
        else:
            self.A=0
            self.B=0
        
        #self.save_state()
        
        # 关闭窗口
        self.close()

    def save_state(self):
        # 保存状态
        # 当前项添加进listitems
        current_item = self.listWidget.currentItem()
        if current_item is not None:
            
            self.selected_text2 = current_item.text()
            self.listitems.append(self.selected_text2)
            #计算目前列表有几项，把数组该项替换为地址
            row_count = self.listWidget.count()
            self.lineEdit_2_text[row_count-1]=self.B
        else:
            items_list = []

            # 获取 QListWidget 中的条目数量
            for i in range(self.listWidget.count()):
             # 获取每个条目
             item = self.listWidget.item(i)
             # 获取条目的文本，并将其添加到列表中
             items_list.append(item.text())
            self.listitems=items_list.copy() 

    def method_browse(self):
        self.filePath, _ = QFileDialog.getOpenFileName(self, '选择文件', '/', 'All Files (*)')
        if self.filePath:
            # 将选中文件的绝对路径放入QLineEdit中
            self.lineEdit_2.setText(self.filePath)
        self.lineEdit_2.setReadOnly(True)

    def emit_signal(self):
        self.my_signal.emit('Hello from SignalEmitter!')  # 发射信号
        
    def onTextChanged(self):
        row = self.listWidget.currentRow()
        self.listWidget.item(row).setText(self.lineEdit.text())
        
class datasetWindow( QWidget, Ui_DATASETCONFIGURE):
    datasets=["dataset1(240)","dataset2(324)"]
    road=["./datasets/dataset1(240)","./datasets/dataset2(324)"]
    my_signal2 = pyqtSignal(list)  # 创建一个信号
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.dataset_save)
        self.pushButton_4.clicked.connect(self.dataset_browse)
        self.pushButton_3.clicked.connect(self.dataset_delete)
        self.pushButton_2.clicked.connect(self.dataset_add)
        self.lineEdit_2.textEdited.connect(self.onTextChanged)
        self.filePath='1'
        for item_text in self.datasets:
             self.listWidget.addItem(item_text)

        item = self.listWidget.item(0)  # item(0) 是列表中的第一个项
        self.listWidget.setCurrentItem(item)
        selected_items = self.listWidget.selectedItems()
        index = self.listWidget.currentRow()  # 获取当前选中项的索引
        text = self.listWidget.item(index).text()  # 获取该索引项的文本
        
        self.lineEdit_2.setText(text)

        # 连接currentRowChanged信号到槽函数，当选项变化时更改标签内容
        self.listWidget.currentRowChanged.connect(self.RowChanged)

    def RowChanged(self,row):
        #self.lineEdit.setText(f"{current.text()}")
        currentitem = self.listWidget.currentItem()
        if currentitem is not None:
            currentitem = currentitem.text()
        self.lineEdit_2.setText(currentitem)
        
        if row+1>len(self.road):
        #if  current.text()=='Duval':
            #self.lineEdit.setText(f"{current.text()}")
            self.lineEdit.setText("请添加路径")
         
        else :
            self.lineEdit.setReadOnly(True)
            relative_path = self.road[row]
            self.lineEdit.setText(relative_path)

    def onTextChanged(self):
        row = self.listWidget.currentRow()
        self.listWidget.item(row).setText(self.lineEdit_2.text())

    def dataset_add(self):
        self.listWidget.clearSelection()
        items=['dataset']
        self.listWidget.addItems(items)
        self.lineEdit.setReadOnly(False)
        self.lineEdit_2.setText('dataset')
        self.lineEdit.setText('请添加路径')
        
        #读取目前有多少项
        itemCount = self.listWidget.count()
        row=itemCount-1
        #self.listitems[row]='newmethod'
        #s#elf.lineEdit_2_text[row]='请添加路径'
        #刚添加的数据集为选定项
        self.listWidget.setCurrentRow(row)
        current_item = self.listWidget.currentItem()
        self.selected_text2 = current_item.text()
        self.datasets.append(self.selected_text2)
        self.lineEdit_2.setText((current_item.text()))

    def dataset_delete(self):
        row = self.listWidget.currentRow()
        #保证默认的2个数据集不会被删除
        if row >1:
            del self.datasets[row]
            self.listWidget.takeItem(row)
            del self.road[-1]
            #self.lineEdit_2_text[row]=''
        else:
            self.listWidget.clearSelection()

    def dataset_browse(self):
        self.filePath, _ = QFileDialog.getOpenFileName(self, '选择文件', '/', 'All Files (*)')
        if self.filePath:
            # 将选中文件的绝对路径放入QLineEdit中
            self.lineEdit.setText(self.filePath)
        self.lineEdit.setReadOnly(True)

    def dataset_save(self):
         # 给定的文件绝对路径
        source_file_path = self.filePath

        # 使用os.path.basename获取文件名
        file_name = os.path.basename(source_file_path)

        # 目标路径
        absolute_path = "C:\\Users\\wuhongchou\\Desktop\\vs-pyqt\\datasets"

        # 使用os.path.join将绝对路径和文件名结合起来
        destination_file_path = os.path.join(absolute_path, file_name)

        # 确保目标目录存在，如果不存在则创建
        destination_dir = os.path.dirname(destination_file_path)
        if not os.path.exists(destination_dir):
         os.makedirs(destination_dir)

        # 复制文件
        try:
            shutil.copy(source_file_path, destination_file_path)
            print(f"文件已从 {source_file_path} 复制到 {destination_file_path}")
        except IOError as e:
            print(f"无法复制文件. {e}")
        except Exception as e:
            print(f"发生错误: {e}")
        
       
        row = self.listWidget.currentRow()
        #保证默认的6个方法不会再添加
        if row >1:
            self.A=self.lineEdit.text()
            self.B=self.lineEdit_2.text()
        else:
            self.A=0
            self.B=0
        
        self.road.append(self.lineEdit.text())
        
        # 关闭窗口
        self.close()
    
    def closeEvent(self, event):

        # 发射自定义信号，传递信息给窗口A
        self.my_signal2.emit(self.datasets)
        super().closeEvent(event)

class MainWindow(QWidget, Ui_Mainwindow):
    listitems=["Duval","XGboost","RF","Rogers'4","IEC60599","Key","CNN"]
    datasets=["dataset1(240)","dataset2(324)"]
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.open_method_configure_window)
         #  self.pushButton_2.clicked.connect(self.open_special_window)
        self.pushButton.clicked.connect(self.on_click_run)
        self.pushButton_3.clicked.connect(self.open_dataset_configure_window) 
        self.pushButton_4.clicked.connect(self.save_result) 
        self.pushButton_5.clicked.connect(self.delete_result) 

        for item_text in self.listitems:
             self.listWidget.addItem(item_text)
        for item_text in self.datasets:
             self.listWidget_2.addItem(item_text)
        
        for index in range(self.listWidget.count()):
          item = self.listWidget.item(index)
          item.setSelected(False) 
        for index in range(self.listWidget_2.count()):
          item = self.listWidget_2.item(index)
          item.setSelected(False)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time_weather)
        self.timer.start(1000)  # 每秒更新一次
        self.listWidget.setCurrentRow(-1)
        self.listWidget_2.setCurrentRow(-1)

    #更新时间天气
    def update_time_weather(self):
         # 获取网络时间
        #response = requests.get("https://worldtimeapi.org/api/timezone/Asia/Shanghai")
        #if response.status_code == 200:
        #    data = response.json()
        #    time_string = data['datetime']
        #    self.label_10.setText(f"当前时间: {time_string}")
 
        # 获取和风天气https://console.qweather.com/#/statistics
        #response = requests.get("https://devapi.qweather.com/v7/weather/now?location=101010100&key=9a864c94d98c4633a2fdca88015a64bc")
        #if response.status_code == 200:
            #data = response.json()
            #print(data)
            #weather_string = f"{data['now']['obsTime']}, {data['now']['temp']}°C"
            #self.label_11.setText(f"天气信息: {weather_string}")
            #self.label_10.setText(f" {data['now']['text']}")
     pass

    #接收方法窗口信号        
    def receive_signal(self, message):
        
        self.listWidget.clear()
        self.listitems=message.copy()
        for item_text in self.listitems:
             self.listWidget.addItem(item_text)
    
    #接收数据窗口信号
    def receive_signal2(self, message):
        
        self.listWidget_2.clear()
        self.datasets=message.copy()
        for item_text in self.datasets:
             self.listWidget_2.addItem(item_text)
        
    #打开方法设置窗口
    def open_method_configure_window(self):
        self.special_window = SpecialWindow()
         #  self.pushButton_2.clicked.connect(self.open_special_window)
        self.special_window.my_signal.connect(self.receive_signal)  # 连接信号和槽
       
        self.special_window.show()

    def open_dataset_configure_window(self):
        self.special_window = datasetWindow()
        self.special_window.my_signal2.connect(self.receive_signal2)  # 连接信号和槽
        self.special_window.show()   

    #可视化
    def visual(self,act,result):
         # 计算混淆矩阵
        self.act=act
        self.result=result
        labels = [1, 2, 3, 4, 5, 6]
        cm = confusion_matrix(self.act, self.result, labels=labels)
        # 创建一个新的图形，并设置图形尺寸（以英寸为单位）
        fig, ax = plt.subplots(figsize=(290/100, 290/100))  # 这里假设DPI为100

        # 使用seaborn的heatmap函数绘制混淆矩阵
        sns.heatmap(cm, annot=True, fmt='d', cmap='Reds',xticklabels=labels, yticklabels=labels)
        ax.set_xlabel('预测')
        ax.set_ylabel('真实')
        # 方法1: 全局设置中文字体
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题
        # 设置图形的DPI和保存图片的尺寸
        plt.savefig('confusion_matrix.png', dpi=100, bbox_inches='tight')
        
        # 计算每个类别的准确率
        class_accuracies = np.diag(cm) / np.sum(cm, axis=1)
        class_accuracies = class_accuracies * 100  # 转换为百分比

        # 计算总体准确率
        overall_accuracy = np.sum(np.diag(cm)) / np.sum(cm) * 100  # 转换为百分比

        # 类别的名称（如果有）
        class_names = ['1', '2','3','4','5','6']

        # 计算图形的尺寸（以英寸为单位）
        fig_width = 551 / 100
        fig_height = 241 / 100

        # 创建一个指定尺寸的图形
        plt.figure(figsize=(fig_width, fig_height))
        # 绘制柱状图
        plt.bar(class_names, class_accuracies, color='skyblue', label='Class Accuracy')

        # 添加总体准确率
        plt.bar('Overall', overall_accuracy, color='green', label='Overall Accuracy')

        # 添加标签和标题
        plt.xlabel('Classes')
        plt.ylabel('Accuracy (%)')
        plt.title('准确率表')
        plt.ylim(0, 100)  # 设置y轴的范围为0到100
        plt.savefig('accurate', dpi=100, bbox_inches='tight')
        # 添加图例
        plt.legend()

    def save_result(self):
        # PNG文件的源路径
        source_file_path = 'accurate.png'
        source_file_path2 = 'confusion_matrix.png'
        selected_item = self.listWidget.currentItem()
        name=selected_item.text()
        # 目标文件夹路径
        target_folder_path = 'result/'

        # 检查目标文件夹是否存在，如果不存在则创建它
        if not os.path.exists(target_folder_path):
         os.makedirs(target_folder_path)

        # 获取当前时间，并格式化为字符串
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 构建目标文件的完整路径，包括时间戳和文件扩展名
        target_file_name1 = f"{name}_准确率_{current_time}.png"
        target_file_name2 = f"{name}_混淆矩阵_{current_time}.png"
        target_file_path = os.path.join(target_folder_path, target_file_name1)
        target_file_path2 = os.path.join(target_folder_path, target_file_name2)

        # 复制文件
        try:
            shutil.copy(source_file_path, target_file_path)
            shutil.copy(source_file_path2, target_file_path2)
            print(f"File copied successfully to {target_file_path}")
            print(f"File copied successfully to {target_file_path2}")
    
            # 删除原文件
            os.remove(source_file_path)
            os.remove(source_file_path2)
            print(f"Original file {source_file_path} has been deleted.")
            print(f"Original file {source_file_path2} has been deleted.")
        except IOError as e:
            print(f"Unable to copy or delete file. {e}")
        
        
        tableData = []
        for row in range(self.tableWidget.rowCount()):
            row_data = []
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, column)
                row_data.append(item.text() if item else "")
            tableData.append(row_data)
        
        df = pd.DataFrame(tableData, columns=['h2', 'ch4', 'c2h6','c2h4','c2h2','act','Duval'])
        # 目标文件夹路径
        
        target_file_name3 = f"{name}_table_{current_time}.xlsx"
        target_file_path3 = os.path.join(target_folder_path, target_file_name3)
        df.to_excel(target_file_path3, index=True)

    def delete_result(self):
        self.tableWidget.clearContents()  # 清除所有单元格内容
        self.tableWidget.setRowCount(0)  # 删除所有行
        self.tableWidget.setColumnCount(0)  # 删除所有列
        self.label_8.setPixmap(QPixmap())
        self.label_9.setPixmap(QPixmap())
        # PNG文件的路径
        file_path = 'accurate.png'
        # 检查文件是否存在
        if os.path.exists(file_path):
            # 删除文件
            os.remove(file_path)
            print(f"The file {file_path} has been deleted.")
        else:
            print(f"The file {file_path} does not exist.")
        file_path2 = 'confusion_matrix.png'
        if os.path.exists(file_path2):
            # 删除文件
            os.remove(file_path2)
            print(f"The file {file_path2} has been deleted.")
        else:
            print(f"The file {file_path2} does not exist.")
    
    def on_click_run(self):
       methodrow=self.listWidget.currentRow()
       datasetrow=self.listWidget_2.currentRow()

       if methodrow==0:
            if datasetrow==0:
                file_path ='C:\\Users\\wuhongchou\\Desktop\\vs-pyqt\\datasets\\dataset1(240).xlsx'
                # 使用pandas读取.xlsx文件
                df = pd.read_excel(file_path, engine='openpyxl')
                h2=df['h2']
                ch4=df['ch4']
                c2h6=df['c2h6']
                c2h4=df['c2h4']
                c2h2=df['c2h2']
                act=df['act']
                duval=Duvalclass(h2,ch4,c2h6,c2h4,c2h2)
                result=duval.Duvalrun()
                df['Duval']=result
                self.visual(act,result)
                self.set_tableWidget(df)

                # 创建一个QPixmap对象并加载图片
                pixmap1 = QPixmap('confusion_matrix.png')  # 替换为你的图片路径
                pixmap2 = QPixmap('accurate.png')  # 替换为你的图片路径
                 # 将加载的图片设置给标签
                self.label_8.setPixmap(pixmap1)
                self.label_9.setPixmap(pixmap2)
                 # 可选：让图片自适应标签大小
                #self.label.setScaledContents(True)
                
            else :
                file_path ='C:\\Users\\wuhongchou\\Desktop\\vs-pyqt\\datasets\\dataset2(324).xlsx'
                # 使用pandas读取.xlsx文件
                df = pd.read_excel(file_path, engine='openpyxl')
                h2=df['h2']
                ch4=df['ch4']
                c2h6=df['c2h6']
                c2h4=df['c2h4']
                c2h2=df['c2h2']
                act=df['act']
                duval=Duvalclass(h2,ch4,c2h6,c2h4,c2h2)
                result=duval.Duvalrun()
                df['Duval']=result
                self.visual(act,result)
                self.set_tableWidget(df)

                # 创建一个QPixmap对象并加载图片
                pixmap1 = QPixmap('confusion_matrix.png')  # 替换为你的图片路径
                pixmap2 = QPixmap('accurate.png')  # 替换为你的图片路径
                 # 将加载的图片设置给标签
                self.label_8.setPixmap(pixmap1)
                self.label_9.setPixmap(pixmap2)
                 # 可选：让图片自适应标签大小
                #self.label.setScaledContents(True)
       elif methodrow==1:
            if datasetrow==0:
                file_path ='C:\\Users\\wuhongchou\\Desktop\\vs-pyqt\\datasets\\dataset1(240).xlsx'
                # 使用pandas读取.xlsx文件
                df = pd.read_excel(file_path, engine='openpyxl')
                XGboost=XGboostclass(df)
                df=XGboost.XGboostrun()
                act=df['act']
                result=df['XGboost']
                self.visual(act,result)
                self.set_tableWidget(df)

                # 创建一个QPixmap对象并加载图片
                pixmap1 = QPixmap('confusion_matrix.png')  # 替换为你的图片路径
                pixmap2 = QPixmap('accurate.png')  # 替换为你的图片路径
                 # 将加载的图片设置给标签
                self.label_8.setPixmap(pixmap1)
                self.label_9.setPixmap(pixmap2)
            else:
                file_path ='C:\\Users\\wuhongchou\\Desktop\\vs-pyqt\\datasets\\dataset2(324).xlsx'
                # 使用pandas读取.xlsx文件
                df = pd.read_excel(file_path, engine='openpyxl')
                XGboost=XGboostclass(df)
                df=XGboost.XGboostrun()
                act=df['act']
                result=df['XGboost']
                self.visual(act,result)
                self.set_tableWidget(df)

                # 创建一个QPixmap对象并加载图片
                pixmap1 = QPixmap('confusion_matrix.png')  # 替换为你的图片路径
                pixmap2 = QPixmap('accurate.png')  # 替换为你的图片路径
                 # 将加载的图片设置给标签
                self.label_8.setPixmap(pixmap1)
                self.label_9.setPixmap(pixmap2)
       elif methodrow==2:
            if datasetrow==0:
                file_path ='C:\\Users\\wuhongchou\\Desktop\\vs-pyqt\\datasets\\dataset1(240).xlsx'
                # 使用pandas读取.xlsx文件
                df = pd.read_excel(file_path, engine='openpyxl')
                h2=df['h2']
                ch4=df['ch4']
                c2h6=df['c2h6']
                c2h4=df['c2h4']
                c2h2=df['c2h2']
                act=df['act']
                R=RFclass(df)
                df=R.RFrun()
                act=df['act']
                result=df['RF']
                
                self.visual(act,result)
                self.set_tableWidget(df)

                # 创建一个QPixmap对象并加载图片
                pixmap1 = QPixmap('confusion_matrix.png')  # 替换为你的图片路径
                pixmap2 = QPixmap('accurate.png')  # 替换为你的图片路径
                 # 将加载的图片设置给标签
                self.label_8.setPixmap(pixmap1)
                self.label_9.setPixmap(pixmap2)
                 # 可选：让图片自适应标签大小
                #self.label.setScaledContents(True)
            else:
                file_path ='C:\\Users\\wuhongchou\\Desktop\\vs-pyqt\\datasets\\dataset2(324).xlsx'
                # 使用pandas读取.xlsx文件
                df = pd.read_excel(file_path, engine='openpyxl')
                h2=df['h2']
                ch4=df['ch4']
                c2h6=df['c2h6']
                c2h4=df['c2h4']
                c2h2=df['c2h2']
                act=df['act']
                R=RFclass(df)
                df=R.RFrun()
                act=df['act']
                result=df['RF']
                self.visual(act,result)
                self.set_tableWidget(df)

                # 创建一个QPixmap对象并加载图片
                pixmap1 = QPixmap('confusion_matrix.png')  # 替换为你的图片路径
                pixmap2 = QPixmap('accurate.png')  # 替换为你的图片路径
                 # 将加载的图片设置给标签
                self.label_8.setPixmap(pixmap1)
                self.label_9.setPixmap(pixmap2)
                 # 可选：让图片自适应标签大小
                #self.label.setScaledContents(True)
           
       elif methodrow==3:
            if datasetrow==0:
                file_path ='C:\\Users\\wuhongchou\\Desktop\\vs-pyqt\\datasets\\dataset1(240).xlsx'
                # 使用pandas读取.xlsx文件
                df = pd.read_excel(file_path, engine='openpyxl')
                h2=df['h2']
                ch4=df['ch4']
                c2h6=df['c2h6']
                c2h4=df['c2h4']
                c2h2=df['c2h2']
                act=df['act']
                R=Rogers4class(h2,ch4,c2h6,c2h4,c2h2)
                result=R.Rogers4run()
                df['Roger']=result
                self.visual(act,result)
                self.set_tableWidget(df)

                # 创建一个QPixmap对象并加载图片
                pixmap1 = QPixmap('confusion_matrix.png')  # 替换为你的图片路径
                pixmap2 = QPixmap('accurate.png')  # 替换为你的图片路径
                 # 将加载的图片设置给标签
                self.label_8.setPixmap(pixmap1)
                self.label_9.setPixmap(pixmap2)
                 # 可选：让图片自适应标签大小
                #self.label.setScaledContents(True)
            else:
                file_path ='C:\\Users\\wuhongchou\\Desktop\\vs-pyqt\\datasets\\dataset2(324).xlsx'
                # 使用pandas读取.xlsx文件
                df = pd.read_excel(file_path, engine='openpyxl')
                h2=df['h2']
                ch4=df['ch4']
                c2h6=df['c2h6']
                c2h4=df['c2h4']
                c2h2=df['c2h2']
                act=df['act']
                R=Rogers4class(h2,ch4,c2h6,c2h4,c2h2)
                result=R.Rogers4run()
                df['Roger']=result
                self.visual(act,result)
                self.set_tableWidget(df)

                # 创建一个QPixmap对象并加载图片
                pixmap1 = QPixmap('confusion_matrix.png')  # 替换为你的图片路径
                pixmap2 = QPixmap('accurate.png')  # 替换为你的图片路径
                 # 将加载的图片设置给标签
                self.label_8.setPixmap(pixmap1)
                self.label_9.setPixmap(pixmap2)
                 # 可选：让图片自适应标签大小
                #self.label.setScaledContents(True)
       elif methodrow==4:
            if datasetrow==0:
                file_path ='C:\\Users\\wuhongchou\\Desktop\\vs-pyqt\\datasets\\dataset1(240).xlsx'
                # 使用pandas读取.xlsx文件
                df = pd.read_excel(file_path, engine='openpyxl')
                h2=df['h2']
                ch4=df['ch4']
                c2h6=df['c2h6']
                c2h4=df['c2h4']
                c2h2=df['c2h2']
                act=df['act']
                IEC=IEC60599class(h2,ch4,c2h6,c2h4,c2h2)
                result=IEC.IEC60599run()
                df['IEC']=result
                self.visual(act,result)
                self.set_tableWidget(df)

                # 创建一个QPixmap对象并加载图片
                pixmap1 = QPixmap('confusion_matrix.png')  # 替换为你的图片路径
                pixmap2 = QPixmap('accurate.png')  # 替换为你的图片路径
                 # 将加载的图片设置给标签
                self.label_8.setPixmap(pixmap1)
                self.label_9.setPixmap(pixmap2)
                 # 可选：让图片自适应标签大小
                #self.label.setScaledContents(True)
            else:
                file_path ='C:\\Users\\wuhongchou\\Desktop\\vs-pyqt\\datasets\\dataset2(324).xlsx'
                 # 使用pandas读取.xlsx文件
                df = pd.read_excel(file_path, engine='openpyxl')
                h2=df['h2']
                ch4=df['ch4']
                c2h6=df['c2h6']
                c2h4=df['c2h4']
                c2h2=df['c2h2']
                act=df['act']
                IEC=IEC60599class(h2,ch4,c2h6,c2h4,c2h2)
                result=IEC.IEC60599run()
                df['IEC']=result
                self.visual(act,result)
                self.set_tableWidget(df)

                # 创建一个QPixmap对象并加载图片
                pixmap1 = QPixmap('confusion_matrix.png')  # 替换为你的图片路径
                pixmap2 = QPixmap('accurate.png')  # 替换为你的图片路径
                 # 将加载的图片设置给标签
                self.label_8.setPixmap(pixmap1)
                self.label_9.setPixmap(pixmap2)
                 # 可选：让图片自适应标签大小
                #self.label.setScaledContents(True)
       elif methodrow==5:
            if datasetrow==0:
                file_path ='C:\\Users\\wuhongchou\\Desktop\\vs-pyqt\\datasets\\dataset1(240).xlsx'
                # 使用pandas读取.xlsx文件
                df = pd.read_excel(file_path, engine='openpyxl')
                h2=df['h2']
                ch4=df['ch4']
                c2h6=df['c2h6']
                c2h4=df['c2h4']
                c2h2=df['c2h2']
                act=df['act']
                key=Keyclass(h2,ch4,c2h6,c2h4,c2h2)
                result=key.Keyrun()
                df['Key']=result
                self.visual(act,result)
                self.set_tableWidget(df)

                # 创建一个QPixmap对象并加载图片
                pixmap1 = QPixmap('confusion_matrix.png')  # 替换为你的图片路径
                pixmap2 = QPixmap('accurate.png')  # 替换为你的图片路径
                 # 将加载的图片设置给标签
                self.label_8.setPixmap(pixmap1)
                self.label_9.setPixmap(pixmap2)
                 # 可选：让图片自适应标签大小
                #self.label.setScaledContents(True)
            else :
                file_path ='C:\\Users\\wuhongchou\\Desktop\\vs-pyqt\\datasets\\dataset2(324).xlsx'
                # 使用pandas读取.xlsx文件
                df = pd.read_excel(file_path, engine='openpyxl')
                h2=df['h2']
                ch4=df['ch4']
                c2h6=df['c2h6']
                c2h4=df['c2h4']
                c2h2=df['c2h2']
                act=df['act']
                key=Keyclass(h2,ch4,c2h6,c2h4,c2h2)
                result=key.Keyrun()
                df['Key']=result
                self.visual(act,result)
                self.set_tableWidget(df)
                

                # 创建一个QPixmap对象并加载图片
                pixmap1 = QPixmap('confusion_matrix.png')  # 替换为你的图片路径
                pixmap2 = QPixmap('accurate.png')  # 替换为你的图片路径
                 # 将加载的图片设置给标签
                self.label_8.setPixmap(pixmap1)
                self.label_9.setPixmap(pixmap2)
                 # 可选：让图片自适应标签大小
                #self.label.setScaledContents(True)
    
    def set_tableWidget (self,df) :  
        self.setWindowTitle("Table Example")
                 # 设置表格的行数和列数
        self.tableWidget.setRowCount(len(df))
        self.tableWidget.setColumnCount(len(df.columns))

                # 设置表头标签
        self.tableWidget.setHorizontalHeaderLabels(df.columns.tolist())

                # 填充表格数据
        for row_idx in range(len(df)):
            for col_idx in range(len(df.columns)):
              item = QTableWidgetItem(str(df.iloc[row_idx, col_idx]))
              self.tableWidget.setItem(row_idx, col_idx, item)

                    # 调整列宽以适应内容（可选）
        self.tableWidget.resizeColumnsToContents()

                #设置表格只读
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

                  # 显示窗口
        self.show()

class dengluwindow(QDialog,Ui_denglu) :
    zhanghu=['13565668888','13365668888','13165668888']
    mima=['135','133','131']
    def __init__(self):
        super().__init__()
        #self.initUI()
        self.setupUi(self)
        for item_text in self.zhanghu: 
             self.comboBox.addItem(item_text)
        self.pushButton.clicked.connect(self.chuangjian)
        self.pushButton_2.clicked.connect(self.denglu)

    def initUI(self):
        self.setObjectName("denglu")
        self.resize(467, 460)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(130, 20, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(120, 130, 72, 41))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(120, 190, 72, 21))
        self.label_3.setObjectName("label_3")
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(170, 140, 121, 22))
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(170, 190, 121, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(120, 250, 93, 28))
        self.pushButton.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(230, 250, 93, 28))
        self.pushButton_2.setStyleSheet("background-color: rgb(170, 255, 0);")
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    

    def chuangjian(self):
        currentText = self.comboBox.currentText()  # 获取索引
        password=self.lineEdit.text()  # 获取密码
        if len(password) > 0:
          self.zhanghu.append(currentText)
          self.mima.append(password)
          self.comboBox.addItem(currentText)
          QMessageBox.information(self, '提示', '账户创建成功！')
          self.lineEdit.clear()
        else:
           QMessageBox.information(self, '提示', '密码忘了输入！')
           print("密码为空")
    
    def denglu(self):
        currentIndex = self.comboBox.currentIndex()  # 获取索引
        password=self.lineEdit.text()  # 获取密码
        
        if password==self.mima[currentIndex]:
                 self.hide() 
                 self.accept()  
                                       
        else:
                QMessageBox.warning(self, "Error", "Incorrect username or password")
                  
class mimacuowuwindow(QWidget,Ui_mimacuowu) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.to_dengluwindow)
    def to_dengluwindow(self):
        self.hide() 
        self.D=dengluwindow() 
        self.D.show()
        
class ycmkwindow(QWidget,Ui_ycmk) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # 创建 PlotWidget 实例
        self.plotWidget = pg.PlotWidget(title="不同气体含量预测")
        self.plotWidget.setFixedSize(750, 400)  # 设置固定大小为 500x400 像素

        # 使用 setGeometry 设置 PlotWidget 的位置和大小
        self.plotWidget.setGeometry(QtCore.QRect(100, 100, 500, 400)) # x, y, width, height

        # 创建一个按钮
        self.button = QPushButton('开始预测', self)
        self.button.setFixedSize(750, 50)  # 设置按钮固定大小
        self.button.setGeometry(QtCore.QRect(100, 550, 750, 50))
        self.button.clicked.connect(self.onButtonClicked)  # 连接按钮点击信号到槽函数

        # 设置 PlotWidget 的背景颜色（可选）
        self.plotWidget.setBackground('w')

        # 绘制图形
        x = np.linspace(-5 * np.pi, 5 * np.pi, 500)
        y1 = 0.5 * np.sin(x)
        y2 = 0.5 * np.cos(x)
        self.curve1=self.plotWidget.plot(x, y1, pen='r')  # 绘制红色正弦波
        self.curve2=self.plotWidget.plot(x, y2, pen='blue')
        # 创建一个垂直布局
        layout = QVBoxLayout()
        layout.addWidget(self.plotWidget)
        layout.addWidget(self.button)
        # 创建 PlotItem
        self.plotItem = self.plotWidget.getPlotItem()
         # 创建图例
        self.legend = pg.LegendItem(offset=(70, 30))
        self.legend.setParentItem(self.plotItem)
        self.legend.addItem(self.curve1, 'sin(x)')
        self.legend.addItem(self.curve2, 'cos(x)')

        # 设置布局
        self.setLayout(layout)
    def onButtonClicked(self):
        pass
        
class SerialWorker(QThread):
    data_received = pyqtSignal(str)  # 发送原始数据或HEX格式数据
    error_occurred = pyqtSignal(str)  # 发送错误信息

    def __init__(self, port, baud_rate, data_bits, parity, stop_bits, is_hex_mode=True):
        super().__init__()
        self.port = port
        self.baud_rate = baud_rate
        self.data_bits = data_bits
        self.parity = parity
        self.stop_bits = stop_bits
        self.running = True
        self.is_hex_mode = is_hex_mode  # 是否启用HEX模式
        self.serial_port = None
        self.byte_buffer = bytes()  # 用于存储接收到的字节数据
        self.last_receive_time = time.time()  # 记录最后一次接收数据的时间
        self.packet_timeout = 0.1  # 数据包超时时间（100ms）

    def run(self):
        try:
            self.serial_port = serial.Serial(
                self.port,
                self.baud_rate,
                bytesize=self.data_bits,
                parity=self.parity,
                stopbits=self.stop_bits,
                timeout=0.1  # 设置超时避免阻塞
            )
            # 清空输入缓冲区
            self.serial_port.reset_input_buffer()
            
            while self.running:
                current_time = time.time()
                try:
                    if self.serial_port and self.serial_port.is_open:
                        # 检查是否有数据可读
                        if self.serial_port.in_waiting > 0:
                            # 读取串口数据（原始字节）
                            data = self.serial_port.read(self.serial_port.in_waiting)
                            
                            if self.is_hex_mode:
                                # HEX模式：添加到缓冲区
                                self.byte_buffer += data
                                self.last_receive_time = current_time
                            else:
                                # 文本模式：直接处理数据
                                self.handle_text_data(data)
                        else:
                            # 无论是否有数据，都检查HEX缓冲区是否超时
                            if self.is_hex_mode and self.byte_buffer:
                                self.check_hex_timeout(current_time)
                            
                            # 短暂休眠，减少CPU占用
                            self.msleep(10)
                    else:
                        # 串口未打开时检查并处理HEX缓冲区
                        if self.is_hex_mode and self.byte_buffer:
                            self.check_hex_timeout(current_time)
                        
                        # 延长休眠时间
                        self.msleep(100)
                except serial.SerialException as e:
                    self.error_occurred.emit(f"串口读取错误: {str(e)}")
                    self.msleep(500)
                except Exception as e:
                    self.error_occurred.emit(f"运行时错误: {str(e)}")
                    self.msleep(500)
        
        except Exception as e:
            self.error_occurred.emit(f"串口初始化错误: {str(e)}")
        finally:
            # 确保处理所有剩余数据
            self.process_hex_buffer()
            self._close_serial_port()

    def handle_text_data(self, data):
        """处理文本模式下的数据"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            decoded_data = data.decode('utf-8')
        except UnicodeDecodeError:
            try:
                decoded_data = data.decode('gbk', errors='replace')
            except:
                decoded_data = data.decode('latin1', errors='replace')
        
        self.data_received.emit(f"[{timestamp}] {decoded_data}")

    def check_hex_timeout(self, current_time):
        """检查HEX缓冲区是否超时"""
        if self.is_hex_mode and self.byte_buffer:
            # 如果缓冲区有数据且超时时间已到
            if current_time - self.last_receive_time > self.packet_timeout:
                self.process_hex_buffer()

    def process_hex_buffer(self):
        """处理HEX模式下的缓冲区数据"""
        if not self.byte_buffer:
            return
            
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # HEX模式：将字节转换为HEX字符串（如："48 65 6C 6C 6F"）
        try:
            hex_data = ' '.join([f"{byte:02X}" for byte in self.byte_buffer])
            self.data_received.emit(f"[{timestamp}] {hex_data}")
            print(self.data_received)

        except Exception as e:
            self.error_occurred.emit(f"HEX转换错误: {str(e)}")
        finally:
            # 清空缓冲区
            self.byte_buffer = bytes()

    def stop(self):
        self.running = False
        # 停止前刷新缓冲区
        self.process_hex_buffer()
        self._close_serial_port()
        self.wait()  # 等待线程结束

    def set_hex_mode(self, is_hex_mode):
        """设置是否以HEX模式显示数据"""
        # 切换模式时刷新缓冲区
        if self.is_hex_mode != is_hex_mode:
            self.process_hex_buffer()
        self.is_hex_mode = is_hex_mode

    def _close_serial_port(self):
        """安全关闭串口"""
        try:
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()
        except Exception as e:
            self.error_occurred.emit(f"关闭串口错误: {str(e)}")
        finally:
            self.serial_port = None





class txszwindow(QWidget,Ui_txsz) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.worker = None
        
        self.isOriginalStyle = True  # 标志，用于跟踪当前样式状态
        self.pushButton_open.clicked.connect(self.openSerialPort)
        self.pushButton_save.clicked.connect(self.saveSerialPort)
        self.pushButton_clear.clicked.connect(self.clearSerialPort)
        self.comboBox.clear()
        available_ports = QSerialPortInfo.availablePorts()
        for port in available_ports:
            self.comboBox.addItem(port.portName())
    def openSerialPort(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker = None
            
        else:
            try:
                port = self.comboBox.currentText()
                baud_rate = self.comboBox_2.currentText()
                data_bits = int(self.comboBox_5.currentText())
                parity = self.comboBox_4.currentText().upper()
                stop_bits = int(self.comboBox_3.currentText())
                self.worker = SerialWorker(port, baud_rate, data_bits, parity, stop_bits)
                self.worker.data_received.connect(self.append_data)
                self.worker.start()
                
            except Exception as e:
                self.textEdit.append(f"Error opening port: {e}")

        if self.isOriginalStyle:
            # 更改样式
            self.pushButton_open.setStyleSheet("background-color: red; color: white;")
            self.pushButton_open.setText('关闭串口')
            self.isOriginalStyle = False
        else:
            # 还原样式
            self.pushButton_open.setStyleSheet("background-color: white; color: black;")
            self.pushButton_open.setText('打开串口')
            self.isOriginalStyle = True
    def saveSerialPort(self):
         QMessageBox.warning(self, "你好", "串口设置已保存！")

    def append_data(self, data):
        self.textEdit.append(data)
        self.textEdit.moveCursor(QTextCursor.End)  # Ensure the latest data is always visible

    def clearSerialPort(self):
         self.textEdit.clear()
         QMessageBox.warning(self, "你好", "接收的数据已清空！")

class bjjlwindow(QWidget,Ui_bjjl) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.clearTable)
        self.pushButton_2.clicked.connect(self.saveTableToCSV)
        self.pushButton_3.clicked.connect(self.addAlarmRecord)
        self.timer=QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.onTimeout)
    
    def clearTable(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

    def saveTableToCSV(self):
        # 保存表格内容到 CSV 文件
        filename = "告警记录.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # 写入表头
            headers = [self.tableWidget.horizontalHeaderItem(i).text() for i in range(self.tableWidget.columnCount())]
            writer.writerow(headers)
            # 写入表格数据
            for row in range(self.tableWidget.rowCount()):
                row_data = [self.tableWidget.item(row, column).text() if self.tableWidget.item(row, column) else '' for column in range(self.tableWidget.columnCount())]
                writer.writerow(row_data)
            #self.statusBar().showMessage(f'数据已保存到 {filename}')
            print(f'数据已保存到 {filename}')

    def onTimeout(self):
        current_time = QDateTime.currentDateTime().toString('yyyy-MM-dd HH:mm:ss')
        self.label_2.setText(current_time)

    def addAlarmRecord(self):
        # 获取当前时间
        current_time = QDateTime.currentDateTime().toString('yyyy-MM-dd HH:mm:ss')

        # 创建新的告警记录行
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)

        # 设置告警时间
        time_item = QTableWidgetItem(current_time)
        self.tableWidget.setItem(row_position, 0, time_item)

        # 设置告警类型（这里只是一个示例，您可以让用户输入或从其他方式获取）
        alert_type = "温度告警"
        type_item = QTableWidgetItem(alert_type)
        self.tableWidget.setItem(row_position, 1, type_item)

        # 设置告警描述（这里只是一个示例，您可以让用户输入或从其他方式获取）
        description = "温度超过阈值"
        description_item = QTableWidgetItem(description)
        self.tableWidget.setItem(row_position, 2, description_item)

class RFChildWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText("随机森林（Random Forest）是一种集成学习算法，主要用于解决分类和回归问题。它通过构建多个决策树并将它们的预测结果进行整合，以提高模型的准确性和鲁棒性。")
        self.text_edit.append(" ")
        self.text_edit.append("  1.集成学习：随机森林是一种集成学习方法，它结合多个弱学习器（决策树）的预测结果，以提高整体模型的性能。")
        self.text_edit.append("  2.构建多个决策树：随机森林通过构建多个决策树来工作，每棵树都是独立构建的，并且在构建过程中引入随机性。")
        self.text_edit.append("  3.特征随机选择：在构建每棵决策树时，随机森林从原始特征集中随机选择一部分特征。这个过程称为“特征袋抽样”（feature bagging），有助于增加树之间的多样性。")
        self.text_edit.append("  4.自助采样（Bootstrap Sampling）：每棵决策树的训练数据集是通过从原始数据集中进行有放回抽样得到的，这种方法称为自助采样。这意味着同一数据点可能被多次使用，而某些数据点可能一次也不被使用。")
        self.text_edit.append("  5.投票机制：在分类问题中，随机森林通过多数投票的方式来确定最终的预测结果。每棵树给出一个类别预测，得票最多的类别被选为最终预测结果。")
        self.text_edit.append("  6.平均预测：在回归问题中，随机森林通过平均所有决策树的预测结果来得到最终预测。")
        self.text_edit.append("  7.特征重要性评估：随机森林可以评估各个特征对模型预测的贡献度，即特征重要性。这是通过观察在构建树时，各个特征在随机选择的特征子集中出现的次数来确定的。")
        self.text_edit.append("  8.防止过拟合：由于随机森林集成了多个决策树，它可以有效地减少过拟合的风险，特别是在特征空间很大时。")
        self.text_edit.append("  9.适用性广：随机森林可以处理数值型和类别型特征，不需要特征标准化，并且可以处理高维数据。")
        self.text_edit.append("  10.模型解释性：虽然随机森林本身是一个黑盒模型，但是通过特征重要性评估，我们可以对模型的预测有一定的解释。")
        # 设置字体大小为12
        font = QFont("Arial", 12)
        self.text_edit.setFont(font)
        layout.addWidget(self.text_edit)
        self.setGeometry(300, 300, 900, 900)  # 设置子窗口的位置和大小

class LSTMChildWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText("LSTM（Long Short-Term Memory）是一种特殊的循环神经网络（RNN）架构，专门设计用来解决传统RNN在处理长序列数据时遇到的梯度消失和梯度爆炸问题。LSTM由Hochreiter和Schmidhuber在1997年提出，它通过引入门控机制来保持长期依赖关系，使其在序列预测、时间序列分析、自然语言处理等领域表现出色。")
        self.text_edit.append(" ")
        self.text_edit.append("LSTM的关键特性:")
        self.text_edit.append("  门控机制：LSTM引入了三个门控来控制信息的流动，分别是输入门（Input Gate）、遗忘门（Forget Gate）和输出门（Output Gate）。")
        self.text_edit.append("  单元状态（Cell State）：LSTM有一个特殊的单元状态，它贯穿整个序列，携带有关序列的信息。这个状态被门控机制保护，可以保持或修改信息，而不是像传统RNN那样简单地被替换。")
        self.text_edit.append("  长期记忆：由于单元状态的存在，LSTM能够捕捉和保持长期的依赖关系，这使得它在处理长序列数据时更加有效。")
        self.text_edit.append(" ")
        self.text_edit.append("LSTM的工作流程:")
        self.text_edit.append("  LSTM在每个时间步长中执行以下操作：")
        self.text_edit.append("    遗忘门（Forget Gate）：决定哪些信息应该从单元状态中丢弃。它基于当前输入和前一个时间步的隐藏状态来计算。")
        self.text_edit.append("    输入门（Input Gate）：决定哪些新信息应该被存储在单元状态中。它还计算一个新的候选值，这个值将被用来更新单元状态。")
        self.text_edit.append("    单元状态更新：结合遗忘门的输出和输入门的输出来更新单元状态。")
        self.text_edit.append("    输出门（Output Gate）：决定隐藏状态应该包含哪些信息。隐藏状态是基于单元状态和输出门的输出计算的，它决定了网络的输出。")
        self.text_edit.append(" ")
        self.text_edit.append("LSTM的设计使其在处理具有复杂长期依赖的序列数据时非常有效，这使得它成为许多深度学习应用的首选模型之一。")
        # 设置字体大小为12
        font = QFont("Arial", 12)
        self.text_edit.setFont(font)
        layout.addWidget(self.text_edit)
        self.setGeometry(300, 300, 900, 900)  # 设置子窗口的位置和大小

class CNNChildWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText("CNN，全称为卷积神经网络（Convolutional Neural Network），是一种深度学习模型，主要用于处理具有网格结构的数据，如图像。CNN通过模拟生物视觉皮层对图像的处理方式，能够自动和逐层地提取特征，因此在图像识别、分类、分割等领域表现出色。以下是CNN的一些关键特点:")
        self.text_edit.append(" ")
        self.text_edit.append("  1.局部感受野：CNN中的卷积层（Convolutional Layer）由一系列可学习的滤波器（或称为卷积核）组成，这些滤波器在输入数据上滑动，捕捉局部特征。这种局部连接模式使得网络能够捕捉到图像中的局部模式，如边缘、纹理等。")
        self.text_edit.append("  2.参数共享：在卷积层中，同一个滤波器在整个输入图像上使用相同的权重，这种参数共享减少了模型的复杂度，并允许网络在不同位置检测相同的特征。")
        self.text_edit.append("  3.稀疏连接：由于滤波器的局部感受野，CNN具有稀疏连接性，这意味着每个神经元只与输入数据的一个子集相连，这有助于减少计算量。")
        self.text_edit.append("  4.平移不变性：由于参数共享和局部感受野的特性，CNN具有一定程度的平移不变性，即网络能够在图像的不同位置识别相同的特征。")
        self.text_edit.append("  5.激活函数：CNN中的非线性激活函数（如ReLU）被应用于卷积层和池化层之后，增加了网络的非线性表达能力。")
        self.text_edit.append("  6.全连接层：在多个卷积和池化层之后，CNN通常包含一个或多个全连接层（Fully Connected Layer），用于将特征映射到最终的输出，如类别标签。")
        self.text_edit.append("  7.反向传播和梯度下降：CNN的训练过程通常使用反向传播算法来计算梯度，并使用梯度下降或其变体（如Adam、RMSprop）来更新网络权重。")
        self.text_edit.append("  8.适用于多种任务：CNN不仅可以用于图像分类，还可以扩展到其他任务，如目标检测、语义分割、图像生成等。")
        self.text_edit.append("  ")
        self.text_edit.append("CNN的成功在于其能够自动学习数据的层次化特征表示，无需手动设计特征提取器。这种能力使得CNN在计算机视觉领域成为最受欢迎的模型之一，并在许多实际应用中取得了突破性成果。")
        # 设置字体大小为12
        font = QFont("Arial", 12)
        self.text_edit.setFont(font)
        layout.addWidget(self.text_edit)
        self.setGeometry(300, 300, 900, 900)  # 设置子窗口的位置和大小

class GRUChildWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText("GRU（Gated Recurrent Unit）是一种循环神经网络（RNN）的变体，由Kyunghyun Cho等人在2014年提出。GRU旨在解决传统RNN在处理长序列数据时的梯度消失和梯度爆炸问题，这些问题限制了RNN在处理长依赖问题上的能力。GRU通过引入门控机制来改进这一点，使其在某些任务中比传统的LSTM（Long Short-Term Memory）单元更简单、更易于训练，同时保持了类似的性能。")
        self.text_edit.append(" ")
        self.text_edit.append("GRU的核心是两个门控机制：更新门（Update Gate）和重置门（Reset Gate）。这两个门控都是学习到的参数，它们决定了在每个时间步长中，单元状态应该如何更新。")
        self.text_edit.append("  更新门（Update Gate）：这个门控决定了多少之前的隐藏状态应该被保留，以及多少新信息应该被加入到当前的隐藏状态中。它帮助模型决定在每一步中保留多少过去的信息。")
        self.text_edit.append("  重置门（Reset Gate）：这个门控决定了多少过去的信息应该被用来更新当前状态。它允许模型“忘记”不再重要的信息，从而更好地关注当前的任务。")
        self.text_edit.append(" ")
        self.text_edit.append("GRU的计算过程包括以下几个步骤：")
        self.text_edit.append("  计算更新门和重置门的值。")
        self.text_edit.append("  根据重置门的值调整之前的隐藏状态。")
        self.text_edit.append("  计算一个新的候选隐藏状态。")
        self.text_edit.append("  根据更新门的值混合旧的隐藏状态和新的候选隐藏状态，得到最终的隐藏状态。")
        self.text_edit.append(" ")
        self.text_edit.append("GRU的这种设计使其在处理序列数据时更加灵活，特别是在自然语言处理（NLP）和时间序列预测等领域。GRU的一个关键优势是参数更少，这使得它在某些情况下比LSTM训练得更快，同时仍然能够捕捉长期依赖关系。")
        self.text_edit.append("GRU因其在处理序列数据时的有效性和效率而在深度学习社区中受到欢迎。")
        # 设置字体大小为12
        font = QFont("Arial", 12)
        self.text_edit.setFont(font)
        layout.addWidget(self.text_edit)
        self.setGeometry(300, 300, 900, 900)  # 设置子窗口的位置和大小

class mxjswindow(QWidget,Ui_mxjs):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.openRFChildWindow)
        self.pushButton_2.clicked.connect(self.openLSTMChildWindow)
        self.pushButton_3.clicked.connect(self.openCNNChildWindow)
        self.pushButton_4.clicked.connect(self.openGRUChildWindow)

    def openRFChildWindow(self):
        self.child = RFChildWindow()  # 创建子窗口实例
        self.child.show()  # 显示子窗口
    def openLSTMChildWindow(self):
        self.child = LSTMChildWindow()  # 创建子窗口实例
        self.child.show()  # 显示子窗口
    def openCNNChildWindow(self):
        self.child = CNNChildWindow()  # 创建子窗口实例
        self.child.show()  # 显示子窗口
    def openGRUChildWindow(self):
        self.child = GRUChildWindow()  # 创建子窗口实例
        self.child.show()  # 显示子窗口

class sybzwindow(QWidget,Ui_sybz) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class optionwindow(QMainWindow,Ui_option) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.to_mainwindow)
        self.pushButton_2.clicked.connect(self.to_ycwindow)
        self.pushButton_3.clicked.connect(self.to_txwindow)
        self.pushButton_4.clicked.connect(self.to_gjwindow)
        self.pushButton_6.clicked.connect(self.to_mxwindow)
        self.pushButton_5.clicked.connect(self.to_bzwindow)

    def to_mainwindow(self):
        self.M=MainWindow()
        self.M.show()

    def to_ycwindow(self):
        self.M=ycmkwindow()
        self.M.show()  

    def to_txwindow(self):
        self.M=txszwindow()
        self.M.show() 

    def to_gjwindow(self):
        self.M=bjjlwindow()
        self.M.show()

    def to_mxwindow(self):
        self.M=mxjswindow()
        self.M.show()

    def to_bzwindow(self):
        self.M=sybzwindow()
        self.M.show()



# 串口接收线程类
class SerialThread(QThread):
    data_received = pyqtSignal(str)
    
    def __init__(self, serial_port):
        super().__init__()
        self.serial_port = serial_port
        self.running = False
        
    def run(self):
        self.running = True
        while self.running:
            try:
                if self.serial_port.in_waiting:
                    data = self.serial_port.read(self.serial_port.in_waiting).decode('utf-8', errors='replace')
                    self.data_received.emit(data)
            except Exception as e:
                print(f"串口读取错误: {e}")
                self.running = False
            self.msleep(10)  # 短暂休眠避免CPU占用过高
            
    def stop(self):
        self.running = False
        self.wait()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 初始化串口
    try:
        ser = serial.Serial(
            port='COM12',
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            parity=serial.PARITY_NONE,
            timeout=0.1
        )
        print("串口COM12已连接")
        
        # 创建串口接收线程
        serial_thread = SerialThread(ser)
        
        # 创建登录窗口
        D = dengluwindow()
        
        # 定义数据接收槽函数
        def show_data_popup(data):
            #QMessageBox.information(None, "串口数据", f"接收到数据: {data}")
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)  # 设置警告图标
            msg_box.setWindowTitle("警告")
            msg_box.setText(f"发生故障")
            
            # 设置红色样式表（修正语法错误）
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #FF6666;
                }
                QLabel {
                    color: white;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #FF3333;
                    color: white;
                    border-radius: 5px;
                    padding: 5px 15px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #FF0000;
                }
            """)
             
            msg_box.exec_()  # 显示消息框
        # 连接信号和槽
        serial_thread.data_received.connect(show_data_popup)
        
        # 启动串口线程
        serial_thread.start()
        
        # 窗口关闭时停止线程和关闭串口
        app.aboutToQuit.connect(serial_thread.stop)
        app.aboutToQuit.connect(ser.close)
        
        D.show()
        
        if D.exec_() == QDialog.Accepted:
            o = optionwindow()
            o.show()
            sys.exit(app.exec_())
            
    except serial.SerialException as e:
        print(f"串口连接错误: {e}")
        QMessageBox.critical(None, "错误", f"无法连接到COM12串口: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {e}")
        QMessageBox.critical(None, "错误", f"发生未知错误: {str(e)}")
        sys.exit(1)
