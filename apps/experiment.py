# -*- coding: utf-8 -*-
      
import matplotlib

import sys
import os

from opmap.opmap import VmemMap, RawCam
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class setParam(QWidget):
  
  def __init__(self):

    super(setParam, self).__init__()

    self.setGeometry(300, 300, 350, 300)
    self.setWindowTitle(u'パラメータ設定')

    cam_label         = QLabel(u'カメラタイプ　　　　　　　')
    image_label       = QLabel(u'画像サイズ　　　　　　　　')
    start_label       = QLabel(u'開始フレーム　　　　　　　')
    end_label         = QLabel(u'終了フレーム　　　　　　　')
    diff_min_label    = QLabel(u'要求変化幅　　　　　　　　')
    smooth_size_label = QLabel(u'平滑化サイズ　　　　　　　')
    interval_label    = QLabel(u'保存フレーム間隔　　　　　')
    plot_label        = QLabel(u'膜電位波形　　　　　　　　')
    imsave_label      = QLabel(u'膜電位マップ　　　　　　　')
    self.cam_type = 'sa4'
    self.image_size = 256
    self.frame_start = 0
    self.frame_end = 1900
    self.diff_min = 0
    self.smooth_size = 0
    self.interval = 1
    self.flg_plot = 0


    grid = QVBoxLayout()

    self.groupBox1 = QGroupBox("basic")
    basicbox = QVBoxLayout()
    self.groupBox2 = QGroupBox("option")
    optionbox = QVBoxLayout()
    self.groupBox3 = QGroupBox("")
    exitbox = QVBoxLayout()

    # cam_type layout
    layout1 = QHBoxLayout()
    layout1.addWidget(cam_label)
    self.combo1 = QComboBox()
    self.combo1.addItem("sa4")
    self.combo1.addItem("max")
    self.combo1.addItem("max10")
    self.combo1.addItem("mini")
    self.combo1.setCurrentIndex(0)
    layout1.addWidget(self.combo1)
    basicbox.addLayout(layout1)

    # image_size layout
    layout2= QHBoxLayout()
    layout2.addWidget(image_label)
    self.combo2 = QComboBox()
    self.combo2.addItem("128")
    self.combo2.addItem("256")
    self.combo2.addItem("512")
    self.combo2.setCurrentIndex(1)
    layout2.addWidget(self.combo2)
    basicbox.addLayout(layout2)

    # frame_start layout
    layout3 = QHBoxLayout()
    layout3.addWidget(start_label)
    self.edit1 = QLineEdit()
    self.edit1.setText(str(0))
    layout3.addWidget(self.edit1)
    basicbox.addLayout(layout3)

    # frame_end layout
    layout4 = QHBoxLayout()
    layout4.addWidget(end_label)
    self.edit2 = QLineEdit()
    self.edit2.setText(str(400))
    layout4.addWidget(self.edit2)
    basicbox.addLayout(layout4)
    
    # basic layout
    self.groupBox1.setLayout(basicbox)
    grid.addWidget(self.groupBox1)

    # diff_min layout
    layout1 = QHBoxLayout()
    layout1.addWidget(diff_min_label)
    self.edit3 = QLineEdit()
    self.edit3.setText(str(10))
    layout1.addWidget(self.edit3)
    optionbox.addLayout(layout1)

    # smooth_size layout
    layout2= QHBoxLayout()
    layout2.addWidget(smooth_size_label)
    self.edit4 = QLineEdit()
    self.edit4.setText(str(0))
    layout2.addWidget(self.edit4)
    optionbox.addLayout(layout2)

    # interval layout
    layout3 = QHBoxLayout()
    layout3.addWidget(interval_label)
    self.edit5 = QLineEdit()
    self.edit5.setText(str(1))
    layout3.addWidget(self.edit5)
    optionbox.addLayout(layout3)

    # flg_plot layout
    layout4 = QHBoxLayout()
    layout4.addWidget(plot_label)
    self.b1 = QRadioButton(u"表示しない")
    self.b2 = QRadioButton(u"表示する")
    self.group1 = QButtonGroup()
    self.group1.addButton(self.b1, 1)
    self.group1.addButton(self.b2, 2)
    def off_plot():
        self.flg_plot = 0
    def on_plot():
        self.flg_plot = 1
    self.b1.clicked.connect(lambda: off_plot())
    self.b2.clicked.connect(lambda: on_plot())
    layout4.addWidget(self.b1)
    layout4.addWidget(self.b2)
    self.b1.setChecked(True)
    optionbox.addLayout(layout4)

    # flg_imsave layout
    layout5 = QHBoxLayout()
    layout5.addWidget(imsave_label)
    self.b3 = QRadioButton(u"保存しない")
    self.b4 = QRadioButton(u"保存する")
    self.group2 = QButtonGroup()
    self.group2.addButton(self.b3, 1)
    self.group2.addButton(self.b4, 2)
    def off_imsave():
        self.flg_imsave = 0
    def on_imsave():
        self.flg_imsave = 1
    self.b3.clicked.connect(lambda: off_imsave())
    self.b4.clicked.connect(lambda: on_imsave())
    self.b4.setChecked(True)
    on_imsave()
    layout5.addWidget(self.b3)
    layout5.addWidget(self.b4)
    optionbox.addLayout(layout5)

    # option layout
    self.groupBox2.setLayout(optionbox)
    grid.addWidget(self.groupBox2)

    def execute():
    
      self.path = str(QFileDialog.getExistingDirectory(None,
          u'セッションフォルダを選択',
          '',
          QFileDialog.ShowDirsOnly))
      print self.path

      try:
        assert self.path is not ''
        saveDir = self.path + "/result/experiment/"
        self.frame_start = int(str(self.edit1.text()))
        self.frame_end   = int(str(self.edit2.text()))
        self.diff_min    = int(str(self.edit3.text()))
        self.smooth_size = int(str(self.edit4.text()))
        self.interval    = int(str(self.edit5.text()))
        
        cam = RawCam(
            path = self.path,
            cam_type = self.cam_type,
            image_width=self.image_size,
            image_height=self.image_size,
            frame_start = self.frame_start,
            frame_end = self.frame_end
        )
        vmem = VmemMap(cam)
        vmem.setDiffRange(diff_min=self.diff_min)
        if self.smooth_size > 0 : vmem.smooth(size=self.smooth_size)
        #vmem.saveMovie(saveDir + "vmem.mp4", interval=self.interval)

        if int(self.flg_imsave):
          vmem.saveImage(saveDir + "vmem", skip=self.interval, img_type = 'png')
          os.system("ffmpeg -r 15 -y -i {0}/%06d.png -c:v libx264 -pix_fmt yuv420p -qscale 0 {0}.mp4".format(saveDir+"vmem"))

        if int(self.flg_plot):
          points = cam.selectPoints(saveDir+"selectPoints.png")
          vmem.plot(points, savepath = saveDir + "plot.png")

        QMessageBox.information(None,"",u"処理完了！　保存フォルダ:\n"+saveDir)

      except ValueError:
        err = QErrorMessage()
        err.showMessage("Invalid value")
        err.exec_()
        return
      except:
        err = QErrorMessage()
        err.showMessage("Unexpected error:{0}".format(sys.exc_info()))
        err.exec_()
        return

    #btn = QPushButton("終了", self)
    #btn.clicked.connect(QCoreApplication.instance().quit)
    btn = QPushButton(u'セッションフォルダを選んで実行', self)
    btn.clicked.connect(lambda: execute())
    layout1 = QHBoxLayout()
    layout1.addWidget(btn)
    exitbox.addLayout(layout1)

    self.groupBox3.setLayout(exitbox)
    grid.addWidget(self.groupBox3)
    self.setLayout(grid)

    self.show()

app = QApplication(sys.argv)
a = setParam()
sys.exit(app.exec_())

