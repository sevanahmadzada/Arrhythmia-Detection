import pandas as pd
import os
import wfdb
import sys

# importing Qt widgets 
from PyQt5.QtWidgets import * 
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
# importing pyqtgraph as pg 
import pyqtgraph as pg 

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QDialog,QLabel,
                            QFileDialog,QMainWindow,QGridLayout,QLineEdit)
#from mplwidget import MplWidget

from PyQt5.uic import loadUi


import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.metrics import mean_squared_error, accuracy_score, explained_variance_score
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()
        loadUi("/Users/leylaghazada/Desktop/ECG_QTDes-1/gui.ui",self)

        self.setWindowTitle('Arrhytmia detection')
        
        # self.txt_dir.setCursorPosition(0)
        self.noisyData()
        
        #self.process_button.clicked.connect(self.noisyData)
        #self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))


    def noisyData(self):
        canvas = Canvas(self)
        canvas.move(10,60)

        self.file = os.path.dirname(os.path.realpath(__file__))  #folder path

         # to use in get_work_dir function
        
        self.txt_dir.setPlaceholderText("File Path") #make it empty  text line
        
        self.bt_dir.clicked.connect(self.getFile) #get file when clicked
        self.process_button.clicked.connect(self.__init__)

        self.filename = self.getFile()
        self.surname= self.file[12:4]
        self.name = self.file[12:17]
        self.patName.setPlaceholderText(self.name)
        self.patName.setReadOnly(True)
        
        self.patSurname.setPlaceholderText(self.surname)
        self.patSurname.setReadOnly(True)

        
        #self.aaa.setPlaceholderText()
        #self.aaa.setReadOnly(True)

        time = QTime.currentTime()
        timeData = (time.toString(Qt.DefaultLocaleLongDate))
        self.Time.setPlaceholderText(timeData)
        self.Time.setReadOnly(True)

        date = QDate.currentDate()
        dateData = (date.toString(Qt.DefaultLocaleLongDate))
        self.Date.setPlaceholderText(dateData)
        self.Date.setReadOnly(True)
		# setting this layout to the widget 
       # widget.setLayout(layout) 


    def getFile(self):
        self.file = str(QFileDialog.getOpenFileName(self, 'Select Excel File')[0]) 
        #create a file-open dialog
        self.file = self.file[:-4]
        self.txt_dir.setText(self.file) #send that text to file

class Canvas(FigureCanvas):
    def __init__(self, parent = None):
         #fig = Figure(figsize=(width, height), dpi=dpi)
         fig, self.axs = plt.subplots(2)
         FigureCanvas.__init__(self, fig)
         self.setParent(parent)
         self.plot()

    def plot(self):


        # data must be downloaded and path provided
        data_path = '/Users/leylaghazada/Desktop/ADA/SDP/mit-bih-arrhythmia-database-1.0.0/' ##'/' olmali   
        # list of patients
        pts = ['Elman Karimli','Leyla Aghazada','Sevana Ahmadzada','Safura Mayilli','Mammadgulu Novruzov','105','106','107',
                    '108','109','111','112','113','114','115','116',
                    '117','118','119','121','122','123','124','200',
                    '201','202','203','205','207','208','209','210',
                    '212','213','214','215','217','219','220','221',
                    '222','223','228','230','231','232','233','234']
        df = pd.DataFrame() ##list of vectors

        for pt in pts:
            file = data_path + pt
        # load the ecg
        # example file: 'mit-bih-arrhythmia-database-1.0.0/101'
        
         # load the ecg
        record = wfdb.rdrecord(file)
         # load the annotation
        annotation = wfdb.rdann(file, 'atr')

         # extract the signal
        p_signal = record.p_signal
    
          # verify frequency is 360
        assert record.fs == 360, 'sample freq is not 360'
    
          # extract symbols and annotation index
        atr_sym = annotation.symbol
        atr_sample = annotation.sample
        t = p_signal[0:1000]
        noise = np.random.normal(0, .1, t.shape)
        new_signal = t + noise
        
    
       # return p_signal, atr_sym, atr_sample
        font_sizes = [15, 25]
        
        self.axs[0].set_title('Noisy Data')
        self.axs[0].grid(True, linewidth=0.5, color='#ccc8c8', linestyle='-') #creating grid
        self.axs[0].plot(new_signal)

        self.axs[1].set_title('Filtered Data')
        self.axs[1].grid(True, linewidth=0.5, color='#ccc8c8', linestyle='-') #creating grid
        self.axs[1].plot(t)
        
        plt.show()
        
        

app = QApplication(sys.argv)
MainWindow = MainWindow()
MainWindow.show()
#widget = QtWidgets.QStackedWidget()
#widget.addWidget(MainWindow)
#widget.setFixedWidth(1200)
#widget.setFixedHeight(1000)
#widget.show()
sys.exit(app.exec_())
