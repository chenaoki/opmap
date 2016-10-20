# -*- coding: utf-8 -*-

import matplotlib

import sys
import os

from opmap.opmap import RawCam, VmemMap, PhaseMap, PhaseVarianceMap, makeMovie
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class ParamWidget(QWidget):

  def __init__(self):

    super(ParamWidget, self).__init__()
    self.setWindowTitle(u'opapp')

    #----------  
    # Control
    #----------  
    
    # cam_type 
    self.combo1 = QComboBox()
    self.combo1.addItem("sa4")
    self.combo1.addItem("max")
    self.combo1.addItem("max10")
    self.combo1.addItem("mini")
    self.combo1.setCurrentIndex(0)

    # image_size 
    self.combo2 = QComboBox()
    self.combo2.addItem("128")
    self.combo2.addItem("256")
    self.combo2.addItem("512")
    self.combo2.setCurrentIndex(1)

    # frame_start 
    self.edit1 = QLineEdit()
    self.edit1.setText(str(0))

    # frame_end 
    self.edit2 = QLineEdit()
    self.edit2.setText(str(400))

    # diff_min 
    self.edit3 = QLineEdit()
    self.edit3.setText(str(10))

    # int_min
    self.edit4 = QLineEdit()
    self.edit4.setText(str(100))

    # smooth_size
    self.edit5 = QLineEdit()
    self.edit5.setText(str(5))

    # pv_win
    self.edit6 = QLineEdit()
    self.edit6.setText(str(9))

    # pv_erode
    self.edit7 = QLineEdit()
    self.edit7.setText(str(9))
    
    # save_int
    self.edit8 = QLineEdit()
    self.edit8.setText(str(5))

    # flg_vmem_save
    self.cb_1 = QCheckBox(u"マップ", self)
    self.cb_1.setTristate(False)
    self.cb_1.setCheckState(Qt.Checked)

    # flg_vmem_plot
    self.cb_2 = QCheckBox(u"プロット", self)
    self.cb_2.setTristate(False)
    self.cb_2.setCheckState(Qt.Unchecked)

    # flg_pmap_save
    self.cb_3 = QCheckBox(u"マップ", self)
    self.cb_3.setTristate(False)
    self.cb_3.setCheckState(Qt.Checked)

    # flg_pmap_plot
    self.cb_4 = QCheckBox(u"プロット", self)
    self.cb_4.setTristate(False)
    self.cb_4.setCheckState(Qt.Unchecked)

    # flg_pvmap_save
    self.cb_5 = QCheckBox(u"マップ", self)
    self.cb_5.setTristate(False)
    self.cb_5.setCheckState(Qt.Checked)

    # flg_pvmap_plot
    self.cb_6 = QCheckBox(u"プロット", self)
    self.cb_6.setTristate(False)
    self.cb_6.setCheckState(Qt.Unchecked)

    #----------  
    # Model
    #----------  
    
    def execute():

      path = str(QFileDialog.getExistingDirectory(None,
          u'セッションフォルダを選択',
          '',
          QFileDialog.ShowDirsOnly))
      print path

      try:
        assert path is not ''
        saveDir        = path + "/result/opapp/"
        cam_type       = str(self.combo1.currentText())
        image_size     = int(str(self.combo2.currentText()))
        frame_start    = int(str(self.edit1.text()))
        frame_end      = int(str(self.edit2.text()))
        diff_min       = int(str(self.edit3.text()))
        int_min        = int(str(self.edit4.text()))
        smooth_size    = int(str(self.edit5.text()))
        pv_win         = int(str(self.edit6.text()))
        pv_erode       = int(str(self.edit7.text()))
        save_int       = int(str(self.edit8.text()))
        flg_vmem_save  = self.cb_1.isChecked()
        flg_vmem_plot  = self.cb_2.isChecked()
        flg_pmap_save  = self.cb_3.isChecked()
        flg_pmap_plot  = self.cb_4.isChecked()
        flg_pvmap_save = self.cb_5.isChecked()
        flg_pvmap_plot = self.cb_6.isChecked()

        points = []

        cam = RawCam(
            path = path,
            cam_type = cam_type,
            image_width=image_size,
            image_height=image_size,
            frame_start = frame_start,
            frame_end = frame_end
        )

        vmem = VmemMap(cam)
        if diff_min > 0: vmem.setDiffRange(diff_min=diff_min)
        if smooth_size > 0 : vmem.smooth(size=smooth_size)
        if flg_vmem_save:
          vmem.saveImage(saveDir + "vmem", skip=save_int, img_type = 'png')
          makeMovie(saveDir+"vmem", img_type="png")
        if flg_vmem_plot:
          if len(points) == 0:
            points = cam.selectPoints(saveDir+"selectPoints.png")
          vmem.plot(points, savepath = saveDir + "plot_vmem.png")

        pmap = PhaseMap(vmem, shrink=image_size/128)
        if flg_pmap_save:
          pmap.saveImage(saveDir+'pmap', skip=save_int, img_type = 'png')	
          makeMovie(saveDir+"pmap", img_type="png")
        if flg_pmap_plot:
          if len(points) == 0:
            points = cam.selectPoints(saveDir+"selectPoints.png")
          pmap.plot(points, savepath = saveDir + "plot_pmap.png")

        pvmap = PhaseVarianceMap(pmap, size=pv_win)
        if pv_erode > 0:
          pvmap.morphROI(erosion=pv_erode) 
        if flg_pvmap_save:
          pvmap.saveImage(saveDir+'pvmap', skip=save_int, img_type = 'png')	
          makeMovie(saveDir+"pvmap", img_type="png")
        if flg_pvmap_plot:
          if len(points) == 0:
            points = cam.selectPoints(saveDir+"selectPoints.png")
          pvmap.plot(points, savepath = saveDir + "plot_pvmap.png")

        QMessageBox.information(None,"",u"処理完了！　保存フォルダ:\n"+saveDir)

      except:
        err = QErrorMessage()
        err.showMessage("Unexpected error:{0}".format(sys.exc_info()))
        err.exec_()
        return

    btn = QPushButton(u'セッションフォルダを選んで実行', self)
    btn.clicked.connect(lambda: execute())

    #----------  
    # View
    #----------  

    cont_cam = QVBoxLayout()
    cont_vmem = QVBoxLayout()
    cont_pvmap = QVBoxLayout()
    cont_save = QVBoxLayout()
    cont_exec = QVBoxLayout()
    cont_right = QVBoxLayout()
    cont_left = QVBoxLayout()
    cont_all = QHBoxLayout()

    #----- cont_cam

    layout = QHBoxLayout()
    label_ = QLabel(u'カメラタイプ　　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.combo1)
    cont_cam.addLayout(layout)

    layout= QHBoxLayout()
    label_ = QLabel(u'画像サイズ　　　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.combo2)
    cont_cam.addLayout(layout)

    layout = QHBoxLayout()
    label_ = QLabel(u'開始フレーム　　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.edit1)
    cont_cam.addLayout(layout)

    layout = QHBoxLayout()
    label_ = QLabel(u'終了フレーム　　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.edit2)
    cont_cam.addLayout(layout)

    #----- cont_vmem

    layout= QHBoxLayout()
    label_ = QLabel(u'ROI 要求輝度値　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.edit4)
    cont_vmem.addLayout(layout)

    layout = QHBoxLayout()
    label_ = QLabel(u'ROI 要求変化幅　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.edit3)
    cont_vmem.addLayout(layout)

    layout = QHBoxLayout()
    label_ = QLabel(u'平滑化サイズ　　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.edit5)
    cont_vmem.addLayout(layout)

    #----- cont_pvmap

    layout = QHBoxLayout()
    label_ = QLabel(u'窓サイズ　　　　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.edit6)
    cont_pvmap.addLayout(layout)

    layout = QHBoxLayout()
    label_ = QLabel(u'ROI 縮小サイズ　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.edit7)
    cont_pvmap.addLayout(layout)
    
    #----- cont_save

    layout = QHBoxLayout()
    label_ = QLabel(u'保存フレーム間隔　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.edit8)
    cont_save.addLayout(layout)

    layout = QHBoxLayout()
    label_ = QLabel(u'膜電位　')
    layout.addWidget(label_)
    layout.addWidget(self.cb_1)
    layout.addWidget(self.cb_2)
    cont_save.addLayout(layout)

    layout = QHBoxLayout()
    label_ = QLabel(u'位相　　')
    layout.addWidget(label_)
    layout.addWidget(self.cb_3)
    layout.addWidget(self.cb_4)
    cont_save.addLayout(layout)

    layout = QHBoxLayout()
    label_ = QLabel(u'位相分散')
    layout.addWidget(label_)
    layout.addWidget(self.cb_5)
    layout.addWidget(self.cb_6)
    cont_save.addLayout(layout)

    #----- cont_exec

    layout = QHBoxLayout()
    layout.addWidget(btn)
    cont_exec.addLayout(layout)

    #----- build up 

    gb_cam = QGroupBox(u"カメラ入力")
    gb_cam.setLayout(cont_cam)

    gb_vmem = QGroupBox(u"膜電位マップ")
    gb_vmem.setLayout(cont_vmem)

    gb_pvmap = QGroupBox(u"位相分散マップ")
    gb_pvmap.setLayout(cont_pvmap)

    gb_save = QGroupBox(u"保存設定")
    gb_save.setLayout(cont_save)

    gb_exec = QGroupBox(u"")
    gb_exec.setLayout(cont_exec)

    cont_left.addWidget(gb_cam)
    cont_left.addWidget(gb_save)

    cont_right.addWidget(gb_vmem)
    cont_right.addWidget(gb_pvmap)
    cont_right.addWidget(gb_exec)

    cont_all.addLayout(cont_left)
    cont_all.addLayout(cont_right)

    self.setLayout(cont_all)

    self.show()

app = QApplication(sys.argv)
a = ParamWidget()
sys.exit(app.exec_())

