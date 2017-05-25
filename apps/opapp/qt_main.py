# -*- coding: utf-8 -*-

import matplotlib

import sys
import os
import json

import opmap
from opmap.RawCam import RawCam
from opmap.VmemMap import VmemMap
from opmap.PhaseMap import PhaseMap
from opmap.PhaseVarianceMap import PhaseVarianceMap
from opmap.CoreMap import CoreMap
from opmap.util import makeMovie, phase_add
from opmap.cmap import bipolar

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from opapp import run_opapp

class ParamWidget(QWidget):
  cam_types = ["sa4", "max", "max10", "mini"]
  image_sizes = [128, 256, 512]
  menus = [u"停止", u"実行のみ", u"静止画保存", u"動画作成"]

  def saveParam(self):
        params={'camera':{}, 'vmem':{}, 'pvmap':{}, 'menu':{}, 'roi_rect':{}, 'core':{}, 'integ':{}}
        params['camera']['path']           = self.path
        params['camera']['cam_type']       = str(self.combo1.currentText())
        params['camera']['image_width']    = int(self.combo2.currentText())
        params['camera']['image_height']   = int(self.combo2.currentText())
        params['camera']['frame_start']    = int(self.edit1.text())
        params['camera']['frame_end']      = int(self.edit2.text())
        params['vmem']['diff_min']         = int(self.edit3.text())
        params['vmem']['intensity_min']    = int(self.edit4.text())
        params['vmem']['smooth_size']      = int(self.edit5.text())
        params['pvmap']['pv_win']          = int(self.edit6.text())
        params['menu']['save_int']         = int(self.edit7.text())
        params['menu']['cam']             = int(self.combo3.currentIndex())
        params['menu']['vmem']            = int(self.combo4.currentIndex())
        params['menu']['pmap']            = int(self.combo5.currentIndex())
        params['menu']['pvmap']           = int(self.combo6.currentIndex())
        params['menu']['core']            = int(self.combo7.currentIndex())
        params['menu']['core_log']        = int(self.cb_1.isChecked())
        params['menu']['integrate']       = int(self.combo8.currentIndex())
        params['roi_rect']['top']         = int(self.edit8.text())
        params['roi_rect']['bottom']      = int(self.edit9.text())
        params['roi_rect']['left']        = int(self.edit10.text())
        params['roi_rect']['right']       = int(self.edit11.text())
        params['core']['pv_thre']         = float(self.edit12.text())
        params['integ']['phase_wf']       = float(self.edit13.text())
        params['integ']['phase_wt']       = float(self.edit14.text())
        params['integ']['phase_dwf']      = float(self.edit15.text())
        params['integ']['phase_dwt']      = float(self.edit16.text())

        with open('./param.json', 'w') as json_file:
          json.dump(params, json_file, ensure_ascii=False, indent=4)

  def loadParam(self):
        with open('./param.json', 'r') as json_file:
            params = json.load(json_file)
        self.path=params['camera']['path']
        self.combo1.setCurrentIndex(self.cam_types.index(params['camera']['cam_type']))
        self.combo2.setCurrentIndex(self.image_sizes.index(int(params['camera']['image_width'])))
        self.combo3.setCurrentIndex(int(params['menu']['cam']))
        self.combo4.setCurrentIndex(int(params['menu']['vmem']))
        self.combo5.setCurrentIndex(int(params['menu']['pmap']))
        self.combo6.setCurrentIndex(int(params['menu']['pvmap']))
        self.combo7.setCurrentIndex(int(params['menu']['core']))
        self.combo8.setCurrentIndex(int(params['menu']['integrate']))
        self.edit1.setText(str(params['camera']['frame_start']))
        self.edit2.setText(str(params['camera']['frame_end']))
        self.edit3.setText(str(params['vmem']['diff_min']))
        self.edit4.setText(str(params['vmem']['intensity_min']))
        self.edit5.setText(str(params['vmem']['smooth_size']))
        self.edit6.setText(str(params['pvmap']['pv_win']))
        self.edit7.setText(str(params['menu']['save_int']))
        self.edit8.setText(str(params['roi_rect']['top']))
        self.edit9.setText(str(params['roi_rect']['bottom']))
        self.edit10.setText(str(params['roi_rect']['left']))
        self.edit11.setText(str(params['roi_rect']['right']))
        self.edit12.setText(str(params['core']['pv_thre']))
        self.edit13.setText(str(params['integ']['phase_wf']))
        self.edit14.setText(str(params['integ']['phase_wt']))
        self.edit15.setText(str(params['integ']['phase_dwf']))
        self.edit16.setText(str(params['integ']['phase_dwt']))
        self.cb_1.setCheckState(Qt.Checked if params['menu']['core_log'] == 1 else Qt.Unchecked)



  def __init__(self):

    self.path=""

    super(ParamWidget, self).__init__()
    self.setWindowTitle(u'opapp')


    #----------
    # Control
    #----------

    self.combo1 = QComboBox()
    for cam_type in self.cam_types: self.combo1.addItem(cam_type)

    self.combo2 = QComboBox()
    for image_size in self.image_sizes: self.combo2.addItem(str(image_size))

    self.combo3 = QComboBox()
    for menu in self.menus: self.combo3.addItem(menu)
    self.combo4 = QComboBox()
    for menu in self.menus: self.combo4.addItem(menu)
    self.combo5 = QComboBox()
    for menu in self.menus: self.combo5.addItem(menu)
    self.combo6 = QComboBox()
    for menu in self.menus: self.combo6.addItem(menu)
    self.combo7 = QComboBox()
    for menu in self.menus: self.combo7.addItem(menu)
    self.combo8 = QComboBox()
    for menu in self.menus: self.combo8.addItem(menu)

    self.edit1 = QLineEdit()
    self.edit2 = QLineEdit()
    self.edit3 = QLineEdit()
    self.edit4 = QLineEdit()
    self.edit5 = QLineEdit()
    self.edit6 = QLineEdit()
    self.edit7 = QLineEdit()
    self.edit8 = QLineEdit()
    self.edit9 = QLineEdit()
    self.edit10 = QLineEdit()
    self.edit11 = QLineEdit()
    self.edit12 = QLineEdit()
    self.edit13 = QLineEdit()
    self.edit14 = QLineEdit()
    self.edit15 = QLineEdit()
    self.edit16 = QLineEdit()
    self.cb_1 = QCheckBox(u"保存する", self)
    self.cb_1.setTristate(False)


    #----------
    # Model
    #----------

    def execute():

        path = str(QFileDialog.getExistingDirectory(None,
            u'セッションフォルダを選択',
            self.path,
            QFileDialog.ShowDirsOnly))
        saveDir = path + "/result/opapp/"
        print path

        try:
            assert path is not ""
            self.path = path
            self.saveParam()
            run_opapp(raw_path=self.path, result_path=saveDir)
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
    cont_roi = QVBoxLayout()
    cont_core = QVBoxLayout()
    cont_integ = QVBoxLayout()
    cont_menu = QVBoxLayout()
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

    #----- cont_menu

    layout = QHBoxLayout()
    label_ = QLabel(u'保存フレーム間隔　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.edit7)
    cont_menu.addLayout(layout)

    layout= QHBoxLayout()
    label_ = QLabel(u'カメラ画像　　　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.combo3)
    cont_menu.addLayout(layout)

    layout= QHBoxLayout()
    label_ = QLabel(u'膜電位マップ　　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.combo4)
    cont_menu.addLayout(layout)

    layout= QHBoxLayout()
    label_ = QLabel(u'位相マップ　　　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.combo5)
    cont_menu.addLayout(layout)

    layout= QHBoxLayout()
    label_ = QLabel(u'位相分散マップ　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.combo6)
    cont_menu.addLayout(layout)

    layout= QHBoxLayout()
    label_ = QLabel(u'コアマップ　　　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.combo7)
    cont_menu.addLayout(layout)

    layout= QHBoxLayout()
    label_ = QLabel(u'コアのログ出力　　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.cb_1)
    cont_menu.addLayout(layout)

    layout= QHBoxLayout()
    label_ = QLabel(u'統合マップ　　　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.combo8)
    cont_menu.addLayout(layout)


    #----- cont_roi

    layout = QHBoxLayout()
    label_ = QLabel(u'上')
    layout.addWidget(label_)
    layout.addWidget(self.edit8)
    label_ = QLabel(u'下')
    layout.addWidget(label_)
    layout.addWidget(self.edit9)
    cont_roi.addLayout(layout)

    layout = QHBoxLayout()
    label_ = QLabel(u'左')
    layout.addWidget(label_)
    layout.addWidget(self.edit10)
    label_ = QLabel(u'右')
    layout.addWidget(label_)
    layout.addWidget(self.edit11)
    cont_roi.addLayout(layout)

    #----- cont_core

    layout = QHBoxLayout()
    label_ = QLabel(u'位相分散　閾値')
    layout.addWidget(label_)
    layout.addWidget(self.edit12)
    cont_core.addLayout(layout)

    #----- cont_integ

    layout = QHBoxLayout()
    label_ = QLabel(u'興奮前面 位相値')
    layout.addWidget(label_)
    layout.addWidget(self.edit13)
    label_ = QLabel(u'興奮後面 位相値')
    layout.addWidget(label_)
    layout.addWidget(self.edit14)
    cont_integ.addLayout(layout)

    layout = QHBoxLayout()
    label_ = QLabel(u'前面幅')
    layout.addWidget(label_)
    layout.addWidget(self.edit15)
    label_ = QLabel(u'後面幅')
    layout.addWidget(label_)
    layout.addWidget(self.edit16)
    cont_integ.addLayout(layout)

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

    gb_roi = QGroupBox(u"ROI設定")
    gb_roi.setLayout(cont_roi)

    gb_core = QGroupBox(u"コア検出")
    gb_core.setLayout(cont_core)

    gb_integ = QGroupBox(u"統合マップ")
    gb_integ.setLayout(cont_integ)

    gb_save = QGroupBox(u"実行メニュー")
    gb_save.setLayout(cont_menu)

    gb_exec = QGroupBox(u"")
    gb_exec.setLayout(cont_exec)

    cont_left.addWidget(gb_cam)
    cont_left.addWidget(gb_save)
    cont_left.addWidget(gb_exec)

    cont_right.addWidget(gb_roi)
    cont_right.addWidget(gb_vmem)
    cont_right.addWidget(gb_pvmap)
    cont_right.addWidget(gb_core)
    cont_right.addWidget(gb_integ)

    cont_all.addLayout(cont_left)
    cont_all.addLayout(cont_right)

    self.setLayout(cont_all)

    self.loadParam()
    self.show()

app = QApplication(sys.argv)
a = ParamWidget()
sys.exit(app.exec_())
