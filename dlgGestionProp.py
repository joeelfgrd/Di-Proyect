# Form implementation generated from reading ui file '.\\templates\\dlgGestionProp.ui'
#
# Created by: PyQt6 UI code generator 6.9.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_dlg_Tipoprop(object):
    def setupUi(self, dlg_Tipoprop):
        dlg_Tipoprop.setObjectName("dlg_Tipoprop")
        dlg_Tipoprop.resize(380, 289)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dlg_Tipoprop.sizePolicy().hasHeightForWidth())
        dlg_Tipoprop.setSizePolicy(sizePolicy)
        dlg_Tipoprop.setMinimumSize(QtCore.QSize(380, 289))
        dlg_Tipoprop.setMaximumSize(QtCore.QSize(380, 289))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\\\templates\\../img/icono.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlg_Tipoprop.setWindowIcon(icon)
        dlg_Tipoprop.setModal(True)
        self.frame = QtWidgets.QFrame(parent=dlg_Tipoprop)
        self.frame.setGeometry(QtCore.QRect(20, 18, 341, 201))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(parent=self.frame)
        self.label.setGeometry(QtCore.QRect(0, 100, 341, 31))
        self.label.setMinimumSize(QtCore.QSize(0, 31))
        self.label.setMaximumSize(QtCore.QSize(700, 16777215))
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.txtGestipoprop = QtWidgets.QLineEdit(parent=self.frame)
        self.txtGestipoprop.setGeometry(QtCore.QRect(120, 140, 111, 20))
        self.txtGestipoprop.setObjectName("txtGestipoprop")
        self.label_2 = QtWidgets.QLabel(parent=self.frame)
        self.label_2.setGeometry(QtCore.QRect(140, 30, 60, 60))
        self.label_2.setMinimumSize(QtCore.QSize(60, 60))
        self.label_2.setMaximumSize(QtCore.QSize(60, 60))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(".\\\\templates\\../img/icono.ico"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.layoutWidget = QtWidgets.QWidget(parent=dlg_Tipoprop)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 230, 298, 27))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnAnadirtipoprop = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.btnAnadirtipoprop.setObjectName("btnAnadirtipoprop")
        self.horizontalLayout.addWidget(self.btnAnadirtipoprop, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnDeltipoprop = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.btnDeltipoprop.setObjectName("btnDeltipoprop")
        self.horizontalLayout.addWidget(self.btnDeltipoprop)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)

        self.retranslateUi(dlg_Tipoprop)
        QtCore.QMetaObject.connectSlotsByName(dlg_Tipoprop)

    def retranslateUi(self, dlg_Tipoprop):
        _translate = QtCore.QCoreApplication.translate
        dlg_Tipoprop.setWindowTitle(_translate("dlg_Tipoprop", "Dialog"))
        self.label.setText(_translate("dlg_Tipoprop", "Introduzca el tipo de propiedad a añadir o a eliminar"))
        self.btnAnadirtipoprop.setText(_translate("dlg_Tipoprop", "Añadir"))
        self.btnDeltipoprop.setText(_translate("dlg_Tipoprop", "Eliminar"))
