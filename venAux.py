from datetime import datetime
from dlgCalendar import *
import var
import eventos
from dlgGestionProp import *
import propiedades
class Calendar(QtWidgets.QDialog):
    def __init__(self):
        super(Calendar, self).__init__()
        var.uicalendar = Ui_dlgCalendar()
        var.uicalendar.setupUi(self)
        dia = datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year

        var.uicalendar.calendar.setSelectedDate(QtCore.QDate(ano, mes, dia))
        var.uicalendar.calendar.clicked.connect(eventos.Eventos.cargaFecha)
class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir,self).__init__()
class dlgGestionProp(QtWidgets.QDialog):
    def __init__(self):
        super(dlgGestionProp,self).__init__()
        self.ui = Ui_dlg_TipoProp()
        self.ui.setupUi(self)
        self.ui.btnAltaTipoProp.clicked.connect(propiedades.Propiedades.altaTipopropiedad)
        self.ui.btnDelTipoProp.clicked.connect(propiedades.Propiedades.bajaTipopropiedad)