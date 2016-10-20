# -*- coding: utf-8 -*-

import matplotlib

import sys
import os
import json

from opmap.opmap import RawCam, VmemMap, PhaseMap, PhaseVarianceMap, makeMovie
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from opapp import run_opapp

class ParamWidget(QWidget):

  def __init__(self):

    super(ParamWidget, self).__init__()
    self.setWindowTitle(u'opapp')

    with open('./param.json', 'r') as json_data:
      params = json.load(json_data)

    cam_types = ["sa4", "max", "max10", "mini"]
    image_sizes = [128, 256, 512]
    menus = [u"停止", u"実行のみ", u"静止画保存", u"動画作成", u"numpy保存"]

    #----------
    # Control
    #----------

    # cam_type
    self.combo1 = QComboBox()
    for cam_type in cam_types: self.combo1.addItem(cam_type)
    self.combo1.setCurrentIndex(cam_types.index(params['basic']['cam_type']))

    # image_size
    self.combo2 = QComboBox()
    for image_size in image_sizes: self.combo2.addItem(str(image_size))
    self.combo2.setCurrentIndex(image_sizes.index(int(params['basic']['image_width'])))

    # cam_data
    self.combo3 = QComboBox()
    for menu in menus: self.combo3.addItem(menu)
    self.combo3.setCurrentIndex(int(params['menu']['cam']))

    # vmemmap
    self.combo4 = QComboBox()
    for menu in menus: self.combo4.addItem(menu)
    self.combo4.setCurrentIndex(int(params['menu']['vmem']))

    # pmap
    self.combo5 = QComboBox()
    for menu in menus: self.combo5.addItem(menu)
    self.combo5.setCurrentIndex(int(params['menu']['pmap']))

    # pvmap
    self.combo6 = QComboBox()
    for menu in menus: self.combo6.addItem(menu)
    self.combo6.setCurrentIndex(int(params['menu']['pvmap']))

    # coremap
    self.combo7 = QComboBox()
    for menu in menus: self.combo7.addItem(menu)
    self.combo7.setCurrentIndex(int(params['menu']['core']))

    # integratemap
    self.combo8 = QComboBox()
    for i in range(len(menus) - 1): self.combo8.addItem(menus[i])
    self.combo8.setCurrentIndex(int(params['menu']['integrate']))

    # frame_start
    self.edit1 = QLineEdit()
    self.edit1.setText(str(params['basic']['frame_start']))

    # frame_end
    self.edit2 = QLineEdit()
    self.edit2.setText(str(params['basic']['frame_end']))

    # diff_min
    self.edit3 = QLineEdit()
    self.edit3.setText(str(params['option']['diff_min']))

    # int_min
    self.edit4 = QLineEdit()
    self.edit4.setText(str(params['option']['intensity_min']))

    # smooth_size
    self.edit5 = QLineEdit()
    self.edit5.setText(str(params['option']['smooth_size']))

    # pv_win
    self.edit6 = QLineEdit()
    self.edit6.setText(str(params['option']['pv_win']))

    """
    # pv_erode
    self.edit7 = QLineEdit()
    self.edit7.setText(str(params['option']['pv_erode']))
    """

    # save_int
    self.edit8 = QLineEdit()
    self.edit8.setText(str(params['option']['save_int']))

    # core_log
    self.cb_1 = QCheckBox(u"保存する", self)
    self.cb_1.setTristate(False)
    if params['menu']['core_log'] == 1:
      self.cb_1.setCheckState(Qt.Checked)
    else:
      self.cb_1.setCheckState(Qt.Unchecked)


    #----------
    # Model
    #----------

    def execute():

      path = str(QFileDialog.getExistingDirectory(None,
          u'セッションフォルダを選択',
          params['basic']['path'],
          QFileDialog.ShowDirsOnly))
      print path

      try:
        assert path is not ''
        saveDir                           = path + "/result/opapp/"
        params['basic']['path']           = path
        params['basic']['cam_type']       = str(self.combo1.currentText())
        params['basic']['image_width']    = int(self.combo2.currentText())
        params['basic']['image_height']   = int(self.combo2.currentText())
        params['basic']['frame_start']    = int(self.edit1.text())
        params['basic']['frame_end']      = int(self.edit2.text())
        params['option']['diff_min']      = int(self.edit3.text())
        params['option']['intensity_min'] = int(self.edit4.text())
        params['option']['smooth_size']   = int(self.edit5.text())
        params['option']['pv_win']        = int(self.edit6.text())
        #pv_erode                         = str(self.edit7.text())
        params['option']['save_int']      = int(self.edit8.text())
        params['menu']['cam']             = int(self.combo3.currentIndex())
        params['menu']['vmem']            = int(self.combo4.currentIndex())
        params['menu']['pmap']            = int(self.combo5.currentIndex())
        params['menu']['pvmap']           = int(self.combo6.currentIndex())
        params['menu']['core']            = int(self.combo7.currentIndex())
        params['menu']['core_log']        = int(self.cb_1.isChecked())
        params['menu']['integrate']       = int(self.combo8.currentIndex())

        with open('./param.json', 'w') as json_file:
          json.dump(params, json_file, ensure_ascii=False, indent=4)

        run_opapp(raw_path=path, result_path=saveDir)

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

    """
    layout = QHBoxLayout()
    label_ = QLabel(u'ROI 縮小サイズ　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.edit7)
    cont_pvmap.addLayout(layout)
    """

    #----- cont_save

    layout = QHBoxLayout()
    label_ = QLabel(u'保存フレーム間隔　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.edit8)
    cont_save.addLayout(layout)

    layout= QHBoxLayout()
    label_ = QLabel(u'カメラ画像　　　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.combo3)
    cont_save.addLayout(layout)

    layout= QHBoxLayout()
    label_ = QLabel(u'膜電位マップ　　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.combo4)
    cont_save.addLayout(layout)

    layout= QHBoxLayout()
    label_ = QLabel(u'位相マップ　　　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.combo5)
    cont_save.addLayout(layout)

    layout= QHBoxLayout()
    label_ = QLabel(u'位相分散マップ　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.combo6)
    cont_save.addLayout(layout)

    layout= QHBoxLayout()
    label_ = QLabel(u'コアマップ　　　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.combo7)
    cont_save.addLayout(layout)

    layout= QHBoxLayout()
    label_ = QLabel(u'コアのログ出力　　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.cb_1)
    cont_save.addLayout(layout)

    layout= QHBoxLayout()
    label_ = QLabel(u'統合マップ　　　　　　　　')
    layout.addWidget(label_)
    layout.addWidget(self.combo8)
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

