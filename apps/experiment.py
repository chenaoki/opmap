# -*- coding: utf-8 -*-

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

        cam_label = QLabel(u'カメラタイプ')
        image_label = QLabel(u'画像サイズ')
        start_label = QLabel(u'開始フレーム')
        end_label = QLabel(u'終了フレーム')
        diff_min_label = QLabel(u'要求変化幅')
        smooth_size_label = QLabel(u'ガウシアンフィルタのサイズ')
        interval_label = QLabel(u'動画のフレームスキップ間隔')
        plot_label = QLabel(u'膜電位の波形表示')
        imsave_label = QLabel(u'膜電位マップの画像保存')
        self.cam_type = 'max'
        self.image_size = 128
        self.frame_start = 0
        self.frame_end = 1900
        self.diff_min = 0
        self.smooth_size = 0
        self.interval = 1
        self.flg_plot = 0
        self.flg_imsave = 0

	self.path = str(QFileDialog.getExistingDirectory(None,
					  'Select a folder:',
					  'C:\\',
					  QFileDialog.ShowDirsOnly))

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
        self.combo1.addItem("max")
        self.combo1.addItem("max10")
        self.combo1.addItem("sa4")
        self.combo1.addItem("mini")
        def combochange1():
            self.cam_type = str(self.combo1.currentText())
        self.combo1.currentIndexChanged.connect(lambda: combochange1())
        layout1.addWidget(self.combo1)
        basicbox.addLayout(layout1)

        # image_size layout
        layout2= QHBoxLayout()
        layout2.addWidget(image_label)
        self.combo2 = QComboBox()
        self.combo2.addItem("128")
        self.combo2.addItem("256")
        self.combo2.addItem("512")
        def combochange2():
            self.image_size = str(self.combo2.currentText())
        self.combo2.currentIndexChanged.connect(lambda: combochange2())
        layout2.addWidget(self.combo2)
        basicbox.addLayout(layout2)

        # frame_start layout
        layout3 = QHBoxLayout()
        layout3.addWidget(start_label)
	slider1 = QSlider(Qt.Horizontal)
	slider1.setMinimum(0)
	slider1.setMaximum(1900)
	slider1.setValue(0)
	slider1.setTickPosition(QSlider.TicksBelow)
	slider1.setTickInterval(200)
	label1 = QLabel(str(self.frame_start))
	def valuechange1():
	    self.frame_start = slider1.value()
	    label1.setText(str(self.frame_start))
        slider1.valueChanged.connect(lambda: valuechange1())
	layout3.addWidget(slider1)
	layout3.addWidget(label1)
        basicbox.addLayout(layout3)

        # frame_end layout
        layout4 = QHBoxLayout()
        layout4.addWidget(end_label)
        slider2 = QSlider(Qt.Horizontal)
	slider2.setMinimum(0)
	slider2.setMaximum(1900)
	slider2.setValue(1900)
	slider2.setTickPosition(QSlider.TicksBelow)
	slider2.setTickInterval(200)
	label2 = QLabel(str(self.frame_end))
	def valuechange2():
	    self.frame_end = slider2.value()
	    label2.setText(str(self.frame_end))
        slider2.valueChanged.connect(lambda: valuechange2())
	layout4.addWidget(slider2)
	layout4.addWidget(label2)
        basicbox.addLayout(layout4)
        # basic layout
        self.groupBox1.setLayout(basicbox)
        grid.addWidget(self.groupBox1)

        # diff_min layout
        layout1 = QHBoxLayout()
        layout1.addWidget(diff_min_label)
        slider3 = QSlider(Qt.Horizontal)
	slider3.setMinimum(0)
	slider3.setMaximum(30)
	slider3.setValue(0)
	slider3.setTickPosition(QSlider.TicksBelow)
	slider3.setTickInterval(5)
	label3 = QLabel(str(self.diff_min))
	def valuechange3():
	    self.diff_min = slider3.value()
	    label3.setText(str(self.diff_min))
        slider3.valueChanged.connect(lambda: valuechange3())
	layout1.addWidget(slider3)
	layout1.addWidget(label3)
        optionbox.addLayout(layout1)

        # smooth_size layout
        layout2= QHBoxLayout()
        layout2.addWidget(smooth_size_label)
        slider4 = QSlider(Qt.Horizontal)
	slider4.setMinimum(0)
	slider4.setMaximum(20)
	slider4.setValue(0)
	slider4.setTickPosition(QSlider.TicksBelow)
	slider4.setTickInterval(5)
	label4 = QLabel(str(self.smooth_size))
	def valuechange4():
	    self.smooth_size = slider4.value()
	    label4.setText(str(self.smooth_size))
        slider4.valueChanged.connect(lambda: valuechange4())
	layout2.addWidget(slider4)
	layout2.addWidget(label4)
        optionbox.addLayout(layout2)

        # interval layout
        layout3 = QHBoxLayout()
        layout3.addWidget(interval_label)
        slider5 = QSlider(Qt.Horizontal)
	slider5.setMinimum(1)
	slider5.setMaximum(10)
	slider5.setValue(1)
	slider5.setTickPosition(QSlider.TicksBelow)
	slider5.setTickInterval(1)
	label5 = QLabel(str(self.interval))
	def valuechange5():
	    self.interval = slider5.value()
	    label5.setText(str(self.interval))
        slider5.valueChanged.connect(lambda: valuechange5())
	layout3.addWidget(slider5)
	layout3.addWidget(label5)
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
        layout5.addWidget(self.b3)
        layout5.addWidget(self.b4)
        optionbox.addLayout(layout5)

        # option layout
        self.groupBox2.setLayout(optionbox)
        grid.addWidget(self.groupBox2)

        # make quit button
        btn = QPushButton("OK", self)
        btn.clicked.connect(QCoreApplication.instance().quit)
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

param_vmem = {}
param_vmem["path"] = a.path
param_vmem["cam_type"] = a.cam_type
param_vmem["image_width"] = int(a.image_size)
param_vmem["image_height"] = int(a.image_size)
param_vmem["frame_start"] = int(a.frame_start)
param_vmem["frame_end"] = int(a.frame_end)


print param_vmem
print a.diff_min
print a.smooth_size
print a.interval
print a.flg_plot
print a.flg_imsave


saveDir = a.path + "/result/experiment/"
if not os.path.exists(saveDir+"img/"):
    os.makedirs(saveDir+"img/")

print "Loading camera data...",
cam = RawCam(**param_vmem)
print "done"

print "Making vmem data...",
vmem = VmemMap(cam)
vmem.setDiffRange(diff_min=int(a.diff_min))
if int(a.smooth_size) > 0 : vmem.smooth(size=int(a.smooth_size))
print "done"

import matplotlib
matplotlib.use('tkagg')

print "Saving movie...",
vmem.saveMovie(saveDir + "vmem.mp4", interval=int(a.interval))
print "done"

if int(a.flg_imsave):
    print "Saving images...",
    vmem.saveImage(saveDir + "img/", img_type = 'png')
    print "done"
if int(a.flg_plot):
    print "Plot start...",
    points = cam.selectPoints(saveDir+"selectPoints.png")
    vmem.plot(points, savepath = saveDir + "plot.png")
    print "done"

