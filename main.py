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
        var.ui.setupUi(self)
        var.uicalendar = Calendar()
        self.setStyleSheet(styles.load_stylesheet())
        conexion.Conexion.db_conexion(self)
        eventos.Eventos.cargarProv(self)
        eventos.Eventos.cargaMuniCli(self)


        '''
        ZONA DE EVENTOS DEL MENUBAR
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)


        '''
        EVENTOS DE BOTONES
        '''
        var.ui.btnGrabarCli.clicked.connect(clientes.Clientes.altaCliente)
        var.ui.btnAltaCli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0))

        '''
        EVENTOS DE CAJAS DE TEXTO
        '''
        var.ui.txtDniCli.editingFinished.connect(lambda:clientes.Clientes.checkDNI(var.ui.txtDniCli.text()))
        var.ui.txtEmailCli.editingFinished.connect(lambda:clientes.Clientes.checkEmail(var.ui.txtEmailCli.text()))

        '''
        EVENTOS COMOBOX 
        '''
        var.ui.cmbProvCli.currentIndexChanged.connect(eventos.Eventos.cargaMuniCli)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
