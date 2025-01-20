from multiprocessing.connection import Client
from PyQt6 import QtWidgets , QtCore
from PyQt6.QtGui import QIcon
from PyQt6.uic.Compiler.qtproxies import QtGui
from datetime import datetime

import clientes
import conexion
import eventos
import var


class Vendedores:

    @staticmethod
    def comprobarCamposObligatorios():
        campos = [var.ui.txtDniVend, var.ui.txtNombreVend, var.ui.txtTelefonoVend, var.ui.cmbDelegacionVend]

        for i, dato in enumerate(campos):
            if i in (0, 1, 2):
                if dato.text() == "":
                    eventos.Eventos.crearMensajeError("Comprueba los campos",
                                                      "Campo vacío, compruebe que los campos amarillos estén rellenados")
                    return False
            if i == 2:
                if not eventos.Eventos.validarTelefono(var.ui.txtTelefonoVend.text()):
                    eventos.Eventos.crearMensajeError("Teléfono mal", "Escriba un telefono válido")
                    return False
            if i == 0:
                if not eventos.Eventos.validarDNIcli(var.ui.txtDniVend.text()):
                    eventos.Eventos.crearMensajeError("Dni mal",
                                                      "Escriba un dni válido (Creo que la expresion regular la tengo mal)")
                    return False
        if var.ui.txtEmailVend.text() != "":
            eventos.Eventos.validarMail(var.ui.txtEmailVend.text())
            eventos.Eventos.crearMensajeError("Email mal", "Escriba un email válido")
            return False
        return True

    @staticmethod
    def cargarTablaVendedores(self):
        try:
            listado = conexion.Conexion.listadoVendedores(self)
            if listado is None:
                listado = []
            index = 0
            for registro in listado:
                var.ui.tablaVendedores.setRowCount(index + 1)
                var.ui.tablaVendedores.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaVendedores.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
                var.ui.tablaVendedores.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[2])))
                var.ui.tablaVendedores.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[3])))
                var.ui.tablaVendedores.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaVendedores.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaVendedores.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaVendedores.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                index += 1

        except Exception as e:
            print("error cargaTablaClientes", e)

    @staticmethod
    def altaVendedor(self):
        try:
            if vendedores.Vendedores.comprobarCamposObligatorios():
                nuevoVendedor = [var.ui.txtDniVend.text(), var.ui.txtNombreVend.text(), var.ui.txtAltaVend.text(),
                                 var.ui.txtTelefonoVend.text(), var.ui.txtEmailVend.text(),
                                 var.ui.cmbDelegacionVend.currentText()]
                if conexion.Conexion.altaVendedor(nuevoVendedor):
                    eventos.Eventos.crearMensajeInfo("Operacion exitosa",
                                                     "El vendedor se ha dado de alta correctamente")
                else:
                    eventos.Eventos.crearMensajeError("Error",
                                                      "Error al dar de alta al vendedor, comprueba si ya existe uno con tu mismo dni")
                Vendedores.cargarTablaVendedores(self)
        except Exception as e:
            print(e)

    @staticmethod
    def cargarOneVendedor(self):
        try:
            fila = var.ui.tablaVendedores.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = conexion.Conexion.datosOneVendedor(self, str(datos[0]))
            listado = [var.ui.txtIdVend, var.ui.txtDniVend, var.ui.txtNombreVend, var.ui.txtAltaVend,
                       var.ui.txtBajaVend, var.ui.txtTelefonoVend, var.ui.txtEmailVend,
                       var.ui.cmbDelegacionVend]
            for i in range(len(listado)):
                if i == 7:
                    listado[i].setCurrentText(str(registro[i]))
                else:
                    listado[i].setText(registro[i])
        except Exception as e:
            print("error cargarOneVendedor en vendedores", e)

    @staticmethod
    def modificarVendedor(self):
        try:
            if vendedores.Vendedores.comprobarCamposObligatorios():
                datosModificar = [var.ui.txtIdVend.text(), var.ui.txtNombreVend.text(), var.ui.txtAltaVend.text(),
                                  var.ui.txtTelefonoVend.text(), var.ui.txtEmailVend.text(),
                                  var.ui.cmbDelegacionVend.currentText(),
                                  var.ui.txtBajaVend.text()]
                if conexion.Conexion.modifVendedor(datosModificar):
                    eventos.Eventos.crearMensajeInfo("Operacion exitosa", "El vendedor se ha modificado correctamente")
                else:
                    eventos.Eventos.crearMensajeError("Error",
                                                      "Error al modificado al vendedor, comprueba si ya existe uno con tu mismo dni")
                Vendedores.cargarTablaVendedores(self)
            Vendedores.cargarTablaVendedores(self)
        except Exception as e:
            print(e)

    @staticmethod
    def bajaVendedor(self):
        try:
            if var.ui.txtBajaVend.text() != '':
                eventos.Eventos.crearMensajeError("Error", "Error el vendedor ya está de baja")
                return
            now = datetime.now()
            formatted_date = now.strftime("%d/%m/%Y")
            var.ui.txtBajacli.setText(formatted_date)
            if conexion.Conexion.bajaVendedor(var.ui.txtIdVend.text(), formatted_date):
                eventos.Eventos.crearMensajeInfo("Bien", "Vendedor dato de baja correctamente")
            else:
                eventos.Eventos.crearMensajeError("Mal", "Error al dar de baja")
            Vendedores.cargarTablaVendedores(self)
        except Exception as e:
            print("error bajaCliente en clientes", e)

    @staticmethod
    def filtrarPorTelefono(self):
        try:
            if var.ui.txtTelefonoVend.text() == "":
                eventos.Eventos.crearMensajeError("Faltan datos", "Debes ingresar un telefono valido")
                return

            listado = conexion.Conexion.datosVendedoresByTelefono(self, var.ui.txtTelefonoVend.text())
            if len(listado) == 0:
                eventos.Eventos.crearMensajeError("Error", "No se han encontrado datos con ese numero de telefono")
                return
            index = 0
            var.ui.tablaVendedores.setRowCount(index + 1)
            var.ui.tablaVendedores.setItem(0, 0, QtWidgets.QTableWidgetItem(str(listado[0])))
            var.ui.tablaVendedores.setItem(0, 1, QtWidgets.QTableWidgetItem(str(listado[1])))
            var.ui.tablaVendedores.setItem(0, 2, QtWidgets.QTableWidgetItem(str(listado[2])))
            var.ui.tablaVendedores.setItem(0, 3, QtWidgets.QTableWidgetItem(str(listado[3])))
            var.ui.tablaVendedores.item(0, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            var.ui.tablaVendedores.item(0, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
            var.ui.tablaVendedores.item(0, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
            var.ui.tablaVendedores.item(0, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        except Exception as e:
            print("error cargaTablaClientes", e)

    @staticmethod
    def historicoVend(self):
        try:
            if var.ui.chkHistoricoVend.isChecked():
                var.historicoVend = 1
            else:
                var.historicoVend = 0
            Vendedores.cargarTablaVendedores(self)
        except Exception as e:
            print("checkbox historico error ", e)