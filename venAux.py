from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QCompleter

import conexion
import informes
import propiedades
from dlgAbout import Ui_dlgAbout
from dlgBuscarProp import Ui_dlgInformeProp
from dlgCalendar import *
import var
import eventos
from dlgGestionProp import *


class Calendar(QtWidgets.QDialog):
    def __init__(self):
        super(Calendar, self).__init__()
        var.uicalendar = Ui_dlgCalendar()
        var.uicalendar.setupUi(self)
        dia = datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year

        var.uicalendar.Calendar.setSelectedDate((QtCore.QDate(ano,mes,dia)))
        var.uicalendar.Calendar.clicked.connect(eventos.Eventos.cargaFecha)

class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir, self).__init__()

class dlgGestionProp(QtWidgets.QDialog):
    def __init__(self):
        super(dlgGestionProp, self).__init__()
        self.ui = Ui_dlg_Tipoprop()
        self.ui.setupUi(self)
        self.ui.btnAnadirtipoprop.clicked.connect(propiedades.Propiedades.altaTipoPropiedad)
        self.ui.btnDeltipoprop.clicked.connect(propiedades.Propiedades.bajaTipoPropiedad)

class dlgAbout(QtWidgets.QDialog):
    def __init__(self):
        super(dlgAbout, self).__init__()
        self.ui = Ui_dlgAbout()
        self.ui.setupUi(self)
        self.ui.btnSalir.clicked.connect(self.close)

class dlgBuscarProp(QtWidgets.QDialog):
    def __init__(self, propiedades):
        super(dlgBuscarProp, self).__init__()
        self.ui = Ui_dlgInformeProp()
        self.ui.setupUi(self)
        self.ui.cmbInformeMuniProp.addItem("")
        self.ui.cmbInformeMuniProp.addItems(propiedades)

        completer = QCompleter(propiedades, self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self.ui.cmbInformeMuniProp.setCompleter(completer)
        self.ui.btnInformeProp.clicked.connect(self.on_btnBuscarProp_clicked)

    def on_btnBuscarProp_clicked(self):
        localidad = self.ui.cmbInformeMuniProp.currentText()
        informes.Informes.reportPropiedades(localidad)
        self.accept()