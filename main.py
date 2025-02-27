from ctypes.wintypes import VARIANT_BOOL

import alquileres
import clientes
import eventos
import facturas
import styles
import vendedores
from venAux import *
from venPrincipal import *
import sys
import var

class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.uicalendar = Calendar()
        var.dlgabrir = FileDialogAbrir()
        var.dlggestion = dlgGestionProp()
        var.dlgAbout = dlgAbout()
        conexion.Conexion.db_conexion()
        listado = conexion.Conexion.listaTodosMunicipios()
        var.dlgLocalidad = dlgBuscarProp(listado)
        self.setStyleSheet(styles.load_stylesheet())
        var.historicoCli = 0
        var.historicoProp = 0
        var.historicoVend = 0
        var.lupaState = 0
        var.rowsClientes = 15
        var.rowsPropiedades = 11
        var.rowsVendedores = 10
        #conexionserver.ConexionServer.crear_conexion(self)
        propiedades.Propiedades.manageCheckbox()
        propiedades.Propiedades.manageRadioButtons()
        facturas.Facturas.checkDatosFacturas()

        '''
        EVENTOS DE TABLAS
        '''

        clientes.Clientes.cargaTablaClientes()
        propiedades.Propiedades.cargarTablaPropiedades(0)
        vendedores.Vendedores.cargarTablaVendedores()
        facturas.Facturas.cargarTablaFacturas()
        alquileres.Alquileres.cargarTablaAlquileres()
        eventos.Eventos.resizeTablaClientes()
        eventos.Eventos.resizeTablaPropiedades()
        eventos.Eventos.resizeTablaVendedores()
        eventos.Eventos.resizeTablaFacturas()
        eventos.Eventos.resizeTablaMensualidades()
        eventos.Eventos.resizeTablaVentas()
        eventos.Eventos.resizeTablaContratos()
        var.ui.tablaClientes.clicked.connect(clientes.Clientes.cargaOneCliente)
        var.ui.tablaPropiedades.clicked.connect(propiedades.Propiedades.cargaOnePropiedad)
        var.ui.tablaVendedores.clicked.connect(vendedores.Vendedores.cargarOneVendedor)
        var.ui.tablaFacturas.clicked.connect(facturas.Facturas.cargaOneFactura)
        var.ui.tablaContratos.clicked.connect(alquileres.Alquileres.cargarOneContrato)
        var.ui.tablaContratos.clicked.connect(alquileres.Alquileres.cargarTablaMensualidades)

        '''
        EVENTOS DEL MENUBAR
        '''

        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionCrear_Backup.triggered.connect(eventos.Eventos.crearBackup)
        var.ui.actionCargar_Backup.triggered.connect(eventos.Eventos.restaurarBackup)
        var.ui.actionTipo_Propiedades.triggered.connect(eventos.Eventos.abrirTipoProp)
        var.ui.action_exportCSVprop.triggered.connect(eventos.Eventos.exportCSVprop)
        var.ui.action_exportJSONprop.triggered.connect(eventos.Eventos.exportJSONprop)
        var.ui.actionAbout.triggered.connect(eventos.Eventos.abrirAbout)
        var.ui.actionExportar_Vendedores_JSON.triggered.connect(eventos.Eventos.exportJSONvendedores)
        var.ui.actionListado_Clientes.triggered.connect(informes.Informes.reportClientes)
        var.ui.actionListado_Propiedades.triggered.connect(eventos.Eventos.abrirBuscarLocalidad)
        var.ui.actionListado_Vendedores.triggered.connect(eventos.Eventos.checkFactura)

        '''
        EVENTOS DE BOTONES
        '''

        var.ui.btnGrabarcli.clicked.connect(clientes.Clientes.altaCliente)
        var.ui.btnAltacli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0))
        var.ui.btnBajacli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1))
        var.ui.btnPublicacionPro.clicked.connect(lambda: eventos.Eventos.abrirCalendar(2))
        var.ui.btnBajaPro.clicked.connect(lambda: eventos.Eventos.abrirCalendar(3))
        var.ui.btnModifcli.clicked.connect(clientes.Clientes.modifCliente)
        var.ui.btnDelcli.clicked.connect(clientes.Clientes.bajaCliente)
        var.ui.btnGrabarPro.clicked.connect(propiedades.Propiedades.altaPropiedad)
        var.ui.btnModificarPro.clicked.connect(propiedades.Propiedades.modifPropiedad)
        var.ui.btnEliminarPro.clicked.connect(propiedades.Propiedades.bajaPropiedad)
        var.ui.btnFiltrar.clicked.connect(lambda: clientes.Clientes.cargaClienteDni())
        var.ui.btnAnteriorCli.clicked.connect(lambda: eventos.Eventos.movimientoPaginas(0, "Clientes"))
        var.ui.btnSiguienteCli.clicked.connect(lambda: eventos.Eventos.movimientoPaginas(1, "Clientes"))
        var.ui.btnAnteriorPro.clicked.connect(lambda: eventos.Eventos.movimientoPaginas(0, "Propiedades"))
        var.ui.btnSiguientePro.clicked.connect(lambda: eventos.Eventos.movimientoPaginas(1, "Propiedades"))
        var.ui.btnGrabarVend.clicked.connect(vendedores.Vendedores.altaVendedor)
        var.ui.btnModificarVend.clicked.connect(vendedores.Vendedores.modificarVendedor)
        var.ui.btnBajaVend.clicked.connect(vendedores.Vendedores.bajaVendedor)
        var.ui.btnAltaCalVend.clicked.connect(lambda: eventos.Eventos.abrirCalendar(5))
        var.ui.btnBajaCalVend.clicked.connect(lambda: eventos.Eventos.abrirCalendar(4))
        var.ui.btnFiltrarVend.clicked.connect(vendedores.Vendedores.filtrarPorTelefono)
        var.ui.btnCalendarVentas.clicked.connect(lambda: eventos.Eventos.abrirCalendar(6))
        var.ui.btnFechaInicioMensualidad.clicked.connect(lambda: eventos.Eventos.abrirCalendar(7))
        var.ui.btnFechaFinMensualidad.clicked.connect(lambda: eventos.Eventos.abrirCalendar(8))
        var.ui.btnGrabarFactura.clicked.connect(facturas.Facturas.altaFactura)
        var.ui.btnGrabarVenta.clicked.connect(facturas.Facturas.altaVenta)
        var.ui.btnInformeVentas.clicked.connect(eventos.Eventos.checkFactura)
        var.ui.btnAltaContrato.clicked.connect(alquileres.Alquileres.altaContrato)
        #var.ui.btnAnteriorVend.clicked.connect(lambda: eventos.Eventos.movimientoPaginas(0, "Vendedores"))
        #var.ui.btnSiguienteVend.clicked.connect(lambda: eventos.Eventos.movimientoPaginas(1, "Vendedores"))


        '''
        EVENTOS DE CAJAS DE TEXTO
        '''

        var.ui.txtDnicli.editingFinished.connect(lambda : clientes.Clientes.checkDNI(var.ui.txtDnicli.text()))
        var.ui.txtEmailcli.editingFinished.connect(lambda : clientes.Clientes.checkEmail(var.ui.txtEmailcli.text()))
        var.ui.txtMovilcli.editingFinished.connect(lambda : clientes.Clientes.checkTelefono(var.ui.txtMovilcli.text()))
        var.ui.txtMovilPro.editingFinished.connect(lambda : propiedades.Propiedades.checkTelefono(var.ui.txtMovilPro.text()))
        var.ui.txtPrecioAlquilerPro.textChanged.connect(lambda : propiedades.Propiedades.manageCheckbox())
        var.ui.txtPrecioVentaPro.textChanged.connect(lambda : propiedades.Propiedades.manageCheckbox())
        var.ui.txtFechabajaPro.textChanged.connect(lambda : propiedades.Propiedades.manageRadioButtons())

        '''
        EVENTOS COMBOBOX
        '''

        eventos.Eventos.cargarProv()
        var.ui.cmbProvinciacli.currentIndexChanged.connect(eventos.Eventos.cargarMunicipiosCli)
        var.ui.cmbProvinciaPro.currentIndexChanged.connect(eventos.Eventos.cargarMunicipiosPro)
        eventos.Eventos.cargarTipoPropiedad()

        '''
        EVENTOS TOOLBAR
        '''

        var.ui.actionbarSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionbarLimpiar.triggered.connect(eventos.Eventos.limpiarPanel)
        var.ui.actionTipoPropiedad.triggered.connect(eventos.Eventos.abrirTipoProp)
        var.ui.actionBuscar.triggered.connect(propiedades.Propiedades.filtrarPropiedades)

        '''
        EVENTOS DE CHECKBOX
        '''

        var.ui.chkHistoriacli.stateChanged.connect(clientes.Clientes.historicoCli)
        var.ui.chkHistoricoPro.stateChanged.connect(propiedades.Propiedades.historicoProp)
        var.ui.chkHistoricoVend.stateChanged.connect(vendedores.Vendedores.historicoVend)
        var.ui.chkHistoricoMensualidades.stateChanged.connect(alquileres.Alquileres.cargarTablaMensualidades)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())