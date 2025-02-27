import calendar
from calendar import Month
from datetime import datetime
from PyQt6 import QtWidgets, QtCore, QtGui

import conexion
import eventos
import propiedades
import var
from informes import Informes


class Alquileres:

    chkPagado = []
    botonesdel = []
    botonesInforme = []
    idAlquiler = 0

    @staticmethod
    def altaContrato():
        """
        Función que graba un contrato en la base de datos y devuelve un mensaje de éxito o error
        """
        try:
            if not Alquileres.checkCampos():
                return
            infoContrato = [var.ui.txtPropiedadContrato.text(),
                            var.ui.txtDniClienteContrato.text(),
                            var.ui.txtVendedorContrato.text(),
                            var.ui.txtFechaInicioMensualidad.text(),
                            var.ui.txtFechaFinMensualidad.text()]
            if conexion.Conexion.grabarContrato(infoContrato):
                eventos.Eventos.crearMensajeInfo("Informacion", "El contrato se ha grabado exitosamente")
            else:
                eventos.Eventos.crearMensajeError("Error", "El contrato no se ha podido grabar")
            conexion.Conexion.cambiarEstadoPropiedad(var.ui.txtPropiedadContrato.text(), 2)
            Alquileres.cargarTablaAlquileres()
            propiedades.Propiedades.cargarTablaPropiedades(0)
            idContrato = conexion.Conexion.obtenerUltimoContrato()
            Alquileres.crearMensualidades(var.ui.txtFechaInicioMensualidad.text(), var.ui.txtFechaFinMensualidad.text(), idContrato)
        except Exception as error:
            print('Error altaContrato: %s' % str(error))

    @staticmethod
    def cargarTablaAlquileres():
        """
        Función que recupera la lista de alquileres mediante Conexion.listadoAlquileres
        y muestra dicha información en la tabla de alquileres
        """
        try:
            listado = conexion.Conexion.listadoAlquileres()
            var.ui.tablaContratos.setRowCount(len(listado))
            index = 0

            Alquileres.botonesdel = []

            for registro in listado:
                container = QtWidgets.QWidget()
                layout = QtWidgets.QVBoxLayout()

                Alquileres.botonesdel.append(QtWidgets.QPushButton())
                Alquileres.botonesdel[-1].setFixedSize(30, 20)
                Alquileres.botonesdel[-1].setIcon(QtGui.QIcon("./img/papelera.ico"))
                Alquileres.botonesdel[-1].setStyleSheet("background-color: #efefef;")
                Alquileres.botonesdel[-1].clicked.connect(
                    lambda checked, idFactura=str(registro[0]): Alquileres.borrarContratoAlquiler(idFactura))
                layout.addWidget(Alquileres.botonesdel[-1])

                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)
                container.setLayout(layout)
                var.ui.tablaContratos.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaContratos.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
                var.ui.tablaContratos.setCellWidget(index, 2, container)

                var.ui.tablaContratos.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaContratos.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index += 1
        except Exception as e:
            print("Error al cargar la tabla de facturas", e)

    @staticmethod
    def checkCampos():
        """
        :return: los campos están rellenos
        :rtype: boolean

        Función que comprueba si los campos del formulario de contrato están rellenos
        """

        try:
            campos = [var.ui.txtDniClienteContrato.text(),
                            var.ui.txtPropiedadContrato.text(),
                            var.ui.txtVendedorContrato.text(),
                            var.ui.txtFechaInicioMensualidad.text(),
                            var.ui.txtFechaFinMensualidad.text()]

            for campo in campos:
                if campo == '':
                    eventos.Eventos.crearMensajeError("Error", "Todos los campos son obligatorios")
                    return False

            propiedad = conexion.Conexion.datosOnePropiedad(var.ui.txtPropiedadContrato.text())

            if propiedad[10] == "":
                eventos.Eventos.crearMensajeError("Error", "La propiedad debe de tener un precio de alquiler")
                return False
            elif propiedad[15] != "Disponible":
                eventos.Eventos.crearMensajeError("Error", "La propiedad no está disponible")
                return False

            fechaInicio = datetime.strptime(var.ui.txtFechaInicioMensualidad.text(), '%d/%m/%Y')
            fechaFin = datetime.strptime(var.ui.txtFechaFinMensualidad.text(), '%d/%m/%Y')
            if fechaInicio > fechaFin:
                eventos.Eventos.crearMensajeError("Error", "La fecha de inicio no puede ser mayor que la fecha de fin")
                return False

            return True
        except Exception as error:
            print('Error checkCamposRellenados: %s' % str(error))

    @staticmethod
    def borrarContratoAlquiler(idFactura):
        """
        :param idFactura: id de la factura a borrar
        :type idFactura: int

        Función que borra un contrato de la base de datos y actualiza la tabla de contratos
        """
        try:
            idPropiedad = conexion.Conexion.datosOneContrato(idFactura)[1]
            if conexion.Conexion.borrarContrato(idFactura) and conexion.Conexion.borrarMensualidadesContrato(idFactura):
                eventos.Eventos.crearMensajeInfo("Informacion", "El contrato se ha eliminado exitosamente")
                Alquileres.cargarTablaAlquileres()
                conexion.Conexion.cambiarEstadoPropiedad(idPropiedad, 0)
                propiedades.Propiedades.cargarTablaPropiedades(0)
            else:
                eventos.Eventos.crearMensajeError("Error", "El contrato no se ha podido eliminar")
        except Exception as error:
            print('Error borrarContratoAlquiler: %s' % str(error))

    @staticmethod
    def cargarOneContrato():
        """
        Función que carga la información de un contrato en el formulario de contratos
        """
        try:
            fila = var.ui.tablaContratos.selectedItems()
            if conexion.Conexion.datosOneContrato(fila[0].text()):
                fila = [dato.text() for dato in fila]
                contrato = conexion.Conexion.datosOneContrato(fila[0])
                var.ui.lblNumContrato.setText(str(contrato[0]))
                var.ui.txtPropiedadContrato.setText(str(contrato[1]))
                var.ui.txtDniClienteContrato.setText(str(contrato[2]))
                var.ui.txtVendedorContrato.setText(str(contrato[3]))
                var.ui.txtFechaInicioMensualidad.setText(str(contrato[4]))
                var.ui.txtFechaFinMensualidad.setText(str(contrato[5]))
        except Exception as error:
            print('Error cargarOneContrato: %s' % str(error))

    @staticmethod
    def crearMensualidades(fechainicio, fechafin, idContrato):
        """
        :param fechainicio: fecha de inicio del contrato
        :type fechainicio: str
        :param fechafin: ficha final del contrato
        :type fechafin: str
        :param idContrato: id del contrato
        :type idContrato: int
        :return: None
        :rtype: none

        Función que crea las mensualidades de un contrato
        """
        try:

            listaMeses = []
            fecha_inicio = datetime.strptime(fechainicio, '%d/%m/%Y')
            fecha_fin = datetime.strptime(fechafin, '%d/%m/%Y')

            while fecha_inicio <= fecha_fin:
                listaMeses.append(fecha_inicio.strftime('%m-%Y'))
                if fecha_inicio.month == 12:
                    fecha_inicio = fecha_inicio.replace(year=fecha_inicio.year + 1, month=1)
                else:
                    fecha_inicio = fecha_inicio.replace(month=fecha_inicio.month + 1)

            for mes in listaMeses:
                if conexion.Conexion.grabarMensualidadesContrato(mes, idContrato):
                    pass
                else:
                    eventos.Eventos.crearMensajeError("Error", "No se han podido grabar las mensualidades")
                    return
            return

        except Exception as error:
            print('Error crearMensualidades: %s' % str(error))

    @staticmethod
    def cargarTablaMensualidades():
        """
        Función que carga la tabla de mensualidades de un alquiler
        """
        try:
            selected_items = var.ui.tablaContratos.selectedItems()
            if not selected_items or len(selected_items) < 1:
                print("No hay elementos seleccionados en la tabla de contratos.")
                return

            idAlquiler = selected_items[0]
            if not var.ui.chkHistoricoMensualidades.isChecked():
                listado = conexion.Conexion.listadoMensualidadesSinPagar(idAlquiler.text())
            else:
                listado = conexion.Conexion.listadoMensualidadesAlquiler(idAlquiler.text())

            if not listado:
                print("No hay mensualidades para mostrar.")
                return

            propiedad = conexion.Conexion.datosOnePropiedad(
                conexion.Conexion.datosOneContrato(idAlquiler.text())[1])

            var.ui.tablaMensualidades.setRowCount(len(listado))
            index = 0
            Alquileres.chkPagado = []
            Alquileres.botonesInforme = []
            for registro in listado:
                if len(registro) < 4:
                    print(f"Registro incompleto: {registro}")
                    continue

                chkbox = QtWidgets.QCheckBox()
                chkbox.setChecked(registro[3] == 1)
                chkbox.stateChanged.connect(
                    lambda checked, idMensualidad=str(registro[0]): Alquileres.pagarMensualidad(idMensualidad, checked))
                Alquileres.chkPagado.append(chkbox)

                chkbox_container = QtWidgets.QWidget()
                chkbox_layout = QtWidgets.QHBoxLayout()
                chkbox_layout.addWidget(chkbox)
                chkbox_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                chkbox_layout.setContentsMargins(0, 0, 0, 0)
                chkbox_container.setLayout(chkbox_layout)

                btnInforme = QtWidgets.QPushButton()
                btnInforme.setFixedSize(30, 20)
                btnInforme.setIcon(QtGui.QIcon("./img/file.png"))
                btnInforme.setStyleSheet("background-color: #efefef;")
                btnInforme.clicked.connect(
                    lambda checked, idFactura=str(registro[0]): Alquileres.crearInformeMensualidades(idFactura))
                Alquileres.botonesInforme.append(btnInforme)

                btnInforme_container = QtWidgets.QWidget()
                btnInforme_layout = QtWidgets.QHBoxLayout()
                btnInforme_layout.addWidget(btnInforme)
                btnInforme_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                btnInforme_layout.setContentsMargins(0, 0, 0, 0)
                btnInforme_container.setLayout(btnInforme_layout)

                var.ui.tablaMensualidades.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaMensualidades.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
                mes = registro[2]
                var.ui.tablaMensualidades.setItem(index, 2, QtWidgets.QTableWidgetItem(mes))
                var.ui.tablaMensualidades.setItem(index, 3, QtWidgets.QTableWidgetItem(propiedad[10] + " €"))
                var.ui.tablaMensualidades.setCellWidget(index, 4, chkbox_container)
                var.ui.tablaMensualidades.setCellWidget(index, 5, btnInforme_container)

                var.ui.tablaMensualidades.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaMensualidades.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaMensualidades.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaMensualidades.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index += 1
            eventos.Eventos.resizeTablaMensualidades()

        except Exception as e:
            print("Error al cargar la tabla de mensualidades:", e)

    @staticmethod
    def pagarMensualidad(idMensualidad, pagada):
        """
        :param idMensualidad: id de la mensualidad
        :type idMensualidad: int
        :param pagada: si está pagada o no
        :type pagada: boolean

        Función que cambia el estado de pago de una mensualidad
        """
        if pagada:
            if conexion.Conexion.setMensualidadPagada(idMensualidad, pagada):
                eventos.Eventos.crearMensajeInfo("Todo bien","Se ha registrado el nuevo estado de pago")
            else:
                eventos.Eventos.crearMensajeError("Error", "No se ha podido registrar el estado de pago")
        else:
            eventos.Eventos.crearMensajeError("Error", "No se puede eliminar un pago")
            for row in range(var.ui.tablaMensualidades.rowCount()):
                item = var.ui.tablaMensualidades.item(row, 0)
                if item and item.text() == str(idMensualidad):
                    checkbox = var.ui.tablaMensualidades.cellWidget(row, 4).layout().itemAt(0).widget()
                    checkbox.setChecked(not pagada)
                    break
        Alquileres.cargarTablaMensualidades()

    @staticmethod
    def crearInformeMensualidades(idMensualidad):
        """
        :param idMensualidad: id de la mensualidad
        :type idMensualidad: str

        Función que crea un informe de una mensualidad
        """
        try:
            mensualidad = conexion.Conexion.datosOneMensualidad(idMensualidad)
            mensualidadInforme = [mensualidad[0], mensualidad[1]]
            mes, ano = mensualidad[2].split("-")
            nombre_mes = calendar.month_name[int(mes)]
            mensualidadInforme.append(nombre_mes.capitalize())
            mensualidadInforme.append(ano)
            mensualidadInforme.append(mensualidad[3])
            Informes.reportMensualidad(mensualidadInforme)
        except Exception as e:
            print("Error al crear el informe de mensualidades:", e)