import conexion
import eventos
import informes
import vendedores
from VenPrincipal import *
import sys
import var
from VenPrincipal import Ui_venPrincipal
import styles
import clientes
from dlgGestionProp import *
from venAux import Calendar, FileDialogAbrir, dlgGestionProp, dlgAbout
import propiedades



class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.uicalendar = Calendar()
        var.dlgabrir = FileDialogAbrir()
        var.current_page_prop = 0
        var.current_page_cli = 0
        var.items_per_page_prop = 17
        var.items_per_page_cli = 7

        var.historico = 1
        var.dlgGestion = dlgGestionProp()
        var.dlgAbout = dlgAbout()
        self.setStyleSheet(styles.load_stylesheet())
        conexion.Conexion.db_conexion(self)
        #conexionserver.ConexionServer.crear_conexion(self)
        eventos.Eventos.cargaMuniCli(self)
        propiedades.Propiedades.controlDeCheckbox(self)
        propiedades.Propiedades.controlDeRadioButtons(self)

        clientes.Clientes.cargaTablaClientes(self)
        propiedades.Propiedades.cargaTablaPropiedades(self,0)
        '''
        EVENTOS DE TABLAS
        '''
        eventos.Eventos.resizeTableClientes(self)
        var.ui.tabClientes.clicked.connect(clientes.Clientes.cargaCliente)
        eventos.Eventos.resizeTablaPropiedades(self)
        var.ui.tablaPropiedades.clicked.connect(propiedades.Propiedades.cargaPropiedad)


        '''
        ZONA DE EVENTOS DEL MENUBAR
        '''
        var.ui.actionSalir_2.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionCrear_Backup.triggered.connect(eventos.Eventos.crearBackup)
        var.ui.actionRestaurar_Backup.triggered.connect(eventos.Eventos.restaurarBackup)
        var.ui.actionTipoProp.triggered.connect(eventos.Eventos.abrirTipoProp)
        var.ui.actionExportar_Propiedades_CSV.triggered.connect(eventos.Eventos.exportCSVProp)
        var.ui.actionExportar_Propiedades_JSON.triggered.connect(eventos.Eventos.exportJSONprop)
        var.ui.actionAbout.triggered.connect(eventos.Eventos.abrirAbout)
        var.ui.actionListado_Clientes.triggered.connect(informes.Informes.reportClientes)
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
        var.ui.btnDelprop.clicked.connect(propiedades.Propiedades.bajaPropiedad)
        var.ui.btnModifprop.clicked.connect(propiedades.Propiedades.modifPropiedad)
        var.ui.btnTipoProp.clicked.connect(lambda: propiedades.Propiedades.cargaTablaPropiedades(self,1))
        var.ui.btnBajaVend.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1))

        var.ui.btnSiguientecli.clicked.connect(clientes.Clientes.siguientePaginaClientes)
        var.ui.btnAnteriorcli.clicked.connect(clientes.Clientes.anteriorPaginaClientes)
        propiedades_instance = propiedades.Propiedades()
        var.ui.btnSiguienteProp.clicked.connect(propiedades_instance.siguientePaginaProp)
        var.ui.btnAnteriorProp.clicked.connect(propiedades_instance.anteriorPaginaProp)


        '''
        ---------Examen----------
        '''
        var.ui.btnCrearVend.clicked.connect(vendedores.Vendedores.altaVendedor)
        var.ui.btnFechaVend.clicked.connect(lambda: eventos.Eventos.abrirCalendar(4))
        var.ui.btnBajaVend.clicked.connect(lambda: eventos.Eventos.abrirCalendar(5))



        '''
        EVENTOS DE CAJAS DE TEXTO
        '''
        var.ui.txtDniCli.editingFinished.connect(lambda:clientes.Clientes.checkDNI(var.ui.txtDniCli.text()))
        var.ui.txtEmailCli.editingFinished.connect(lambda:clientes.Clientes.checkEmail(var.ui.txtEmailCli.text()))
        var.ui.txtMovilCli.editingFinished.connect(lambda: clientes.Clientes.checkTelefono(var.ui.txtMovilCli.text()))
        var.ui.txtPrecioAlquilerprop.textChanged.connect(lambda: propiedades.Propiedades.controlDeCheckbox(self))
        var.ui.txtPrecioVentaprop.textChanged.connect(lambda: propiedades.Propiedades.controlDeCheckbox(self))
        var.ui.txtFechaprop.textChanged.connect(lambda: propiedades.Propiedades.controlDeRadioButtons(self))
        var.ui.txtBajaprop.textChanged.connect(lambda: propiedades.Propiedades.controlDeRadioButtons(self))
        #var.ui.txtDniVend.editingFinished.connect(lambda: vendedores.Vendedores.checkDNI(var.ui.txtDniVend.text()))





        '''
        EVENTOS COMOBOX 
        '''
        eventos.Eventos.cargarProv(self)
        var.ui.cmbProvCli.currentIndexChanged.connect(eventos.Eventos.cargaMuniCli)
        var.ui.cmbProvprop.currentIndexChanged.connect(eventos.Eventos.cargaMuniProp)
        var.ui.cmbProvVend.currentIndexChanged.connect(eventos.Eventos.cargarProv)
        eventos.Eventos.cargarTipoprop(self)

        '''
        EVENTOS DEL TOOLBAR
        '''
        var.ui.actionbarSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionbarLimpiar.triggered.connect(eventos.Eventos.limpiarPanel)
        var.ui.actionCrear_tipo_Propiedad.triggered.connect(eventos.Eventos.abrirTipoProp)
        var.ui.actionFiltrarTipoProp.triggered.connect(lambda: eventos.Eventos.controlarBtnBuscar(self))

        '''
        EVENTOS CHECKBOX
        '''
        var.ui.chkHistoriaCli.stateChanged.connect(clientes.Clientes.historicoCli)
        var.ui.chkHistoriaprop.stateChanged.connect(propiedades.Propiedades.historicoProp)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
