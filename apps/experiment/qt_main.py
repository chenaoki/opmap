# -*- coding: utf-8 -*-
      
import matplotlib

import sys
import os
import json
from experiment import experiment

from opmap.opmap import VmemMap, RawCam, makeMovie
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class ExperimentWidget(QWidget):
  cam_types = ["sa4", "max"]
  image_sizes = ["128", "256", "512"]

  def loadParam(self):
      with open("param.json","r") as f: 
          params = json.load(f)
          self.path = params["basic"]["path"]
          self.combo1.setCurrentIndex(
                  self.cam_types.index(str(params["basic"]["cam_type"]))) 
          self.combo2.setCurrentIndex(
                  self.image_sizes.index(str(params["basic"]["image_width"])))
          self.edit1.setText( str(params["basic"]["frame_start"]  ))
          self.edit2.setText( str(params["basic"]["frame_end"]    ))
          self.edit3.setText( str(params["option"]["diff_min"]    ))
          self.edit4.setText( str(params["option"]["smooth_size"] ))
          self.edit5.setText( str(params["option"]["interval"]    ))
          self.cb_1.setCheckState( Qt.Checked if params["option"]["map"]  != 0 else Qt.Unchecked)
          self.cb_2.setCheckState( Qt.Checked if params["option"]["plot"] != 0 else Qt.Unchecked)
  
  def saveParam(self):
      params = {"basic":{}, "option":{}} 
      params["basic"]["path"]         = self.path
      params["basic"]["cam_type"]     = str(self.combo1.currentText())
      params["basic"]["image_width"]  = int(self.combo2.currentText())
      params["basic"]["image_height"] = int(self.combo2.currentText())
      params["basic"]["frame_start"]  = int(str(self.edit1.text()))
      params["basic"]["frame_end"]    = int(str(self.edit2.text()))
      params["option"]["diff_min"]    = int(str(self.edit3.text()))
      params["option"]["smooth_size"] = int(str(self.edit4.text()))
      params["option"]["interval"]    = int(str(self.edit5.text()))
      params["option"]["map"]         = 1 if self.cb_1.isChecked() else 0  
      params["option"]["plot"]        = 1 if self.cb_2.isChecked() else 0 
      with open("param.json","w") as f: json.dump( params, f, indent=4)
  
  def __init__(self):
    self.path = ""

    super(ExperimentWidget, self).__init__()

    self.setGeometry(300, 300, 350, 300)
    self.setWindowTitle(u'パラメータ設定')

    grid = QVBoxLayout()

    self.groupBox1 = QGroupBox("basic")
    basicbox = QVBoxLayout()
    self.groupBox2 = QGroupBox("option")
    optionbox = QVBoxLayout()
    self.groupBox3 = QGroupBox("")
    exitbox = QVBoxLayout()

    # cam_type layout
    layout1 = QHBoxLayout()
    layout1.addWidget(QLabel(u'カメラタイプ　　　　　　　'))
    self.combo1 = QComboBox()
    for cam_type in self.cam_types: self.combo1.addItem(cam_type)
    layout1.addWidget(self.combo1)
    basicbox.addLayout(layout1)

    # image_size layout
    layout2= QHBoxLayout()
    layout2.addWidget(QLabel(u'画像サイズ　　　　　　　　'))
    self.combo2 = QComboBox()
    for image_size in self.image_sizes: self.combo2.addItem(image_size)
    layout2.addWidget(self.combo2)
    basicbox.addLayout(layout2)

    # frame_start layout
    layout3 = QHBoxLayout()
    layout3.addWidget(QLabel(u'開始フレーム　　　　　　　'))
    self.edit1 = QLineEdit()
    layout3.addWidget(self.edit1)
    basicbox.addLayout(layout3)

    # frame_end layout
    layout4 = QHBoxLayout()
    layout4.addWidget(QLabel(u'終了フレーム　　　　　　　'))
    self.edit2 = QLineEdit()
    layout4.addWidget(self.edit2)
    basicbox.addLayout(layout4)

    # basic layout
    self.groupBox1.setLayout(basicbox)
    grid.addWidget(self.groupBox1)

    # diff_min layout
    layout1 = QHBoxLayout()
    layout1.addWidget(QLabel(u'要求変化幅　　　　　　　　'))
    self.edit3 = QLineEdit()
    layout1.addWidget(self.edit3)
    optionbox.addLayout(layout1)

    # smooth_size layout
    layout2= QHBoxLayout()
    layout2.addWidget(QLabel(u'平滑化サイズ　　　　　　　'))
    self.edit4 = QLineEdit()
    layout2.addWidget(self.edit4)
    optionbox.addLayout(layout2)

    # interval layout
    layout3 = QHBoxLayout()
    layout3.addWidget(QLabel(u'保存フレーム間隔　　　　　'))
    self.edit5 = QLineEdit()
    layout3.addWidget(self.edit5)
    optionbox.addLayout(layout3)

    # flg_map / flg_plot
    layout = QHBoxLayout()
    self.cb_1 = QCheckBox(u"膜電位マップ保存", self)
    self.cb_1.setTristate(False)
    layout.addWidget(self.cb_1)
    self.cb_2 = QCheckBox(u"膜電位波形保存", self)
    self.cb_2.setTristate(False)
    layout.addWidget(self.cb_2)
    optionbox.addLayout(layout)
    
    # option layout
    self.groupBox2.setLayout(optionbox)
    grid.addWidget(self.groupBox2)

    def execute():
    
      self.path = str(QFileDialog.getExistingDirectory(None,
          u'セッションフォルダを選択',
          self.path,
          QFileDialog.ShowDirsOnly))
      saveDir = self.path + "/result/experiment/"
      print self.path

      try:

        self.saveParam()
        experiment(path=self.path, saveDir=saveDir, param_file="./param.json")

        QMessageBox.information(None,"",u"処理完了！　保存フォルダ:\n"+saveDir)

      except:
        err = QErrorMessage()
        err.showMessage("Unexpected error:{0}".format(sys.exc_info()))
        err.exec_()
        return

    btn = QPushButton(u'セッションフォルダを選んで実行', self)
    btn.clicked.connect(lambda: execute())
    layout1 = QHBoxLayout()
    layout1.addWidget(btn)
    exitbox.addLayout(layout1)

    self.groupBox3.setLayout(exitbox)
    grid.addWidget(self.groupBox3)
    self.setLayout(grid)

    self.loadParam()
    self.show()

app = QApplication(sys.argv)
w = ExperimentWidget()
sys.exit(app.exec_())

