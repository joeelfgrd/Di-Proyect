from datetime import datetime
from dlgCalendar import *
import var
import eventos

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
