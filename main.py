import conexion
import eventos
from VenPrincipal import *
import sys
import var
from VenPrincipal import Ui_venPrincipal
import styles
import clientes
from venAux import Calendar


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.uicalendar = Calendar()
        var.ui.setupUi(self)
        self.setStyleSheet(styles.load_stylesheet())
        conexion.Conexion.db_conexion(self)
        '''
        ZONA DE EVENTOS DEL MENUBAR
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        eventos.Eventos.cargarProv(self)

        '''
        EVENTOS DE BOTONES
        '''
        var.ui.btnGrabarCli.clicked.connect(clientes.Clientes.altaCliente)
        var.ui.btnAltaCli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0))
        '''
        EVENTOS DE CAJAS DE TEXTO
        '''
        var.ui.txtDniCli.editingFinished.connect(lambda:clientes.Clientes.checkDNI(var.ui.txtDniCli.text()))




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
