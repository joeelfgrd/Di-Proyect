import conexion
import eventos
from VenPrincipal import *
import sys
import var
from VenPrincipal import Ui_venPrincipal
import styles
import clientes
from dlgGestionProp import *
from venAux import Calendar, FileDialogAbrir, dlgGestionProp
import propiedades


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.uicalendar = Calendar()
        var.dlgabrir = FileDialogAbrir()
        var.historico = 1
        var.dlgGestion = dlgGestionProp()
        self.setStyleSheet(styles.load_stylesheet())
        conexion.Conexion.db_conexion(self)
        #conexionserver.ConexionServer.crear_conexion(self)
        eventos.Eventos.cargaMuniCli(self)




        clientes.Clientes.cargaTablaClientes(self)
        '''
        EVENTOS DE TABLAS
        '''
        eventos.Eventos.resizeTableClientes(self)
        var.ui.tabClientes.clicked.connect(clientes.Clientes.cargaCliente)

        '''
        ZONA DE EVENTOS DEL MENUBAR
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionCrear_Backup.triggered.connect(eventos.Eventos.crearBackup)
        var.ui.actionRestaurar_Backup.triggered.connect(eventos.Eventos.restaurarBackup)
        var.ui.actionTipoProp.triggered.connect(eventos.Eventos.abrirTipoProp)




        '''
        EVENTOS DE BOTONES
        '''
        var.ui.btnGrabarCli.clicked.connect(clientes.Clientes.altaCliente)
        var.ui.btnAltaCli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0))
        var.ui.btnBajaCli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1))
        var.ui.btnModifCli.clicked.connect(clientes.Clientes.modifCliente)
        var.ui.btnDelCli.clicked.connect(clientes.Clientes.bajaCliente)
        var.ui.btnFechaProp.clicked.connect(lambda: eventos.Eventos.abrirCalendar(2))
        var.ui.btnBajaprop.clicked.connect(lambda: eventos.Eventos.abrirCalendar(3))
        var.ui.btnGrabarprop.clicked.connect(propiedades.Propiedades.altaPropiedad)


        '''
        EVENTOS DE CAJAS DE TEXTO
        '''
        var.ui.txtDniCli.editingFinished.connect(lambda:clientes.Clientes.checkDNI(var.ui.txtDniCli.text()))
        var.ui.txtEmailCli.editingFinished.connect(lambda:clientes.Clientes.checkEmail(var.ui.txtEmailCli.text()))
        var.ui.txtMovilCli.editingFinished.connect(lambda: clientes.Clientes.checkTelefono(var.ui.txtMovilCli.text()))

        '''
        EVENTOS COMOBOX 
        '''
        eventos.Eventos.cargarProv(self)
        var.ui.cmbProvCli.currentIndexChanged.connect(eventos.Eventos.cargaMuniCli)

        '''
        EVENTOS DEL TOOLBAR
        '''
        var.ui.actionbarSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionbarLimpiar.triggered.connect(eventos.Eventos.limpiarPanel)

        '''
        EVENTOS CHECKBOX
        '''
        var.ui.chkHistoriaCli.stateChanged.connect(clientes.Clientes.historicoCli)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
