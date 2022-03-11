# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/sound_recording_frame.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(551, 447)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/resources/icon/语音.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Frame.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(Frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = MatplotlibWidget(Frame)
        self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.widget)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.sound_recording_save_path_pushButton = QtWidgets.QPushButton(Frame)
        self.sound_recording_save_path_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sound_recording_save_path_pushButton.setObjectName("sound_recording_save_path_pushButton")
        self.gridLayout.addWidget(self.sound_recording_save_path_pushButton, 0, 2, 1, 1)
        self.sound_recording_save_path_lineEdit = QtWidgets.QLineEdit(Frame)
        self.sound_recording_save_path_lineEdit.setObjectName("sound_recording_save_path_lineEdit")
        self.gridLayout.addWidget(self.sound_recording_save_path_lineEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Frame)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.save_name_pushButton = QtWidgets.QPushButton(Frame)
        self.save_name_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save_name_pushButton.setObjectName("save_name_pushButton")
        self.gridLayout.addWidget(self.save_name_pushButton, 1, 2, 1, 1)
        self.save_name_lineEdit = QtWidgets.QLineEdit(Frame)
        self.save_name_lineEdit.setObjectName("save_name_lineEdit")
        self.gridLayout.addWidget(self.save_name_lineEdit, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(Frame)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.show_save_path_label = QtWidgets.QLabel(Frame)
        self.show_save_path_label.setObjectName("show_save_path_label")
        self.gridLayout.addWidget(self.show_save_path_label, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.sound_recording_save_path_start_pushButton = QtWidgets.QPushButton(Frame)
        self.sound_recording_save_path_start_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/resources/icon/运行.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sound_recording_save_path_start_pushButton.setIcon(icon1)
        self.sound_recording_save_path_start_pushButton.setObjectName("sound_recording_save_path_start_pushButton")
        self.horizontalLayout_3.addWidget(self.sound_recording_save_path_start_pushButton)
        self.sound_recording_save_path_end_pushButton = QtWidgets.QPushButton(Frame)
        self.sound_recording_save_path_end_pushButton.setEnabled(False)
        self.sound_recording_save_path_end_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/resources/icon/结束.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sound_recording_save_path_end_pushButton.setIcon(icon2)
        self.sound_recording_save_path_end_pushButton.setCheckable(False)
        self.sound_recording_save_path_end_pushButton.setObjectName("sound_recording_save_path_end_pushButton")
        self.horizontalLayout_3.addWidget(self.sound_recording_save_path_end_pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "录音窗口"))
        self.sound_recording_save_path_pushButton.setToolTip(_translate("Frame", "选择语音文件保存的路径"))
        self.sound_recording_save_path_pushButton.setText(_translate("Frame", "打开"))
        self.label_2.setText(_translate("Frame", "文件名"))
        self.save_name_pushButton.setToolTip(_translate("Frame", "确定文件名称"))
        self.save_name_pushButton.setText(_translate("Frame", "确定"))
        self.label.setText(_translate("Frame", "<html><head/><body><p>语音保存路径</p></body></html>"))
        self.show_save_path_label.setToolTip(_translate("Frame", "最后文件保存的路径以及文件名显示"))
        self.show_save_path_label.setText(_translate("Frame", "请输入文件名，否则以默认文件名保存文件"))
        self.sound_recording_save_path_start_pushButton.setToolTip(_translate("Frame", "开始录音"))
        self.sound_recording_save_path_start_pushButton.setText(_translate("Frame", "开始"))
        self.sound_recording_save_path_end_pushButton.setToolTip(_translate("Frame", "结束录音，并按照路径保存文件"))
        self.sound_recording_save_path_end_pushButton.setText(_translate("Frame", "结束并保存文件"))
from core.MatplotlibWidget import MatplotlibWidget
import apprcc_rc
