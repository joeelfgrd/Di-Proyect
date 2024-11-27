from multiprocessing.connection import Client
from PyQt6 import QtWidgets , QtCore
from PyQt6.QtGui import QIcon
from PyQt6.uic.Compiler.qtproxies import QtGui

import clientes
import conexion
import conexionserver
import eventos
import var


class Clientes:
    @staticmethod
    def altaCliente(self):
        try:
            nuevoCli = [var.ui.txtDniCli.text(), var.ui.txtAltaCli.text(), var.ui.txtApelCli.text(),
                        var.ui.txtNomCli.text(), var.ui.txtDirCli.text(), var.ui.txtEmailCli.text(), var.ui.txtMovilCli.text(),
                        var.ui.cmbProvCli.currentText(),
                        var.ui.cmbMuniCli.currentText()]
            if all(nuevoCli[i] for i in [0, 2, 3, 5, 6, 7, 8]):
            #if conexion.Conexion.altaCliente(nuevoCli):
                if conexionserver.ConexionServer.altaCliente(nuevoCli):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowTitle('Aviso')
                    mbox.setWindowIcon(QIcon('./img/logo.ico'))
                    mbox.setText('Cliente dado de alta en la Base de Datos')
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()
                    Clientes.cargaTablaClientes(self)
                    print("Cliente dado de alta")
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('./img/logo.ico'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText("Error: Faltan campos obligatorios")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()

        except Exception as e:
            print("Error en altaCliente:", e)



    def checkDNI(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDniCli.setText(str(dni))
            check = eventos.Eventos.validarDNIcli(dni)
            if check:
               var.ui.txtDniCli.setStyleSheet('background-color:rgb(255,255,220)')
            else:
                var.ui.txtDniCli.setStyleSheet('background-color:#FFC0CB;')
                var.ui.txtDniCli.setText(None)
                var.ui.txtDniCli.setFocus()

        except Exception as e:
            print("error check cliente ", e)

    def checkEmail(mail):
        try:
           mail = str(var.ui.txtEmailCli.text())
           if eventos.Eventos.validarMail(mail):
                var.ui.txtEmailCli.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtEmailCli.setText(mail.lower())

           else:
                var.ui.txtEmailCli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtEmailCli.setText(None)
                var.ui.txtEmailCli.setText("correo no válido")
                var.ui.txtEmailCli.setFocus()

        except Exception as error:
            print("error check cliente", error)

    def cargaTablaClientes(self):
        try:
            #listado = conexion.Conexion.listadoClientes(self)
            listado = conexionserver.ConexionServer.listadoClientes(self)
            for i, registro in enumerate(listado):
                var.ui.tabClientes.setRowCount(i + 1)

                for j, value in enumerate(
                        [registro[0], registro[2], registro[3], registro[5], registro[7], registro[8], registro[9]]):
                    item = QtWidgets.QTableWidgetItem(value)
                    var.ui.tabClientes.setItem(i, j, item)

                for j in range(7):
                    item = var.ui.tabClientes.item(i, j)
                    if item is not None:
                        if j in [0, 3, 6]:
                            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        else:
                            item.setTextAlignment(
                                QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

        except Exception as e:
            print("Error cargar Clientes", e)

    def cargaCliente(self):
        try:
            fila = var.ui.tabClientes.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = conexionserver.ConexionServer.datosOneCliente(str(datos[0]))
            #listado = [var.ui.txtDniCli, var.ui.txtAltaCli, var.ui.txtApelCli,
             #           var.ui.txtNomCli, var.ui.txtEmailCli, var.ui.txtMovilCli,
              #          var.ui.txtDirCli, var.ui.cmbProvCli,
               #         var.ui.cmbMuniCli, var.ui.txtBajaCli]
            listado = [var.ui.txtDniCli, var.ui.txtAltaCli, var.ui.txtApelCli,
                       var.ui.txtNomCli, var.ui.txtDirCli, var.ui.txtEmailCli, var.ui.txtMovilCli,
                        var.ui.cmbProvCli,
                       var.ui.cmbMuniCli, var.ui.txtBajaCli]
            for i in range(len(listado)):
                if i in (7, 8):
                    listado[i].setCurrentText(registro[i])
                else:
                    listado[i].setText(registro[i])
        except Exception as e:
            print("error cargaOneCliente en clientes", e)

    def modifCliente(self):
        try:
            modifcli = [var.ui.txtDniCli.text(), var.ui.txtAltaCli.text(), var.ui.txtApelCli.text(),
                        var.ui.txtNomCli.text(), var.ui.txtEmailCli.text(), var.ui.txtMovilCli.text(),
                        var.ui.txtDirCli.text(), var.ui.cmbProvCli.currentText(),
                        var.ui.cmbMuniCli.currentText(),var.ui.txtBajaCli.text()]
            if conexionserver.ConexionServer.modifCliente(modifcli):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('./img/logo.ico'))
                mbox.setText('Datos del Cliente Modificados')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Clientes.cargaTablaClientes(self)
                print("Cliente modificado")
                clientes.Clientes.cargaTablaClientes(self)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('./img/logo.ico'))
                mbox.setText("Error al dar de alta el cliente")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()


        except Exception as e:
            print("error modifCliente", e)

    @staticmethod
    def checkTelefono(telefono):
        try:
            telefono = str(var.ui.txtMovilCli.text())
            if eventos.Eventos.validarTelefono(telefono):
                var.ui.txtMovilCli.setStyleSheet('background-color: rgb(255, 255, 255);')
            else:
                var.ui.txtMovilCli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtMovilCli.setText(None)
                var.ui.txtMovilCli.setFocus()
        except Exception as error:
            print("error check cliente", error)
    @staticmethod
    def bajaCliente(self):
        try:
            if var.ui.txtBajaCli is not None and var.ui.txtDniCli is not None:
                datos = [var.ui.txtBajaCli.text(), var.ui.txtDniCli.text()]
                if conexionserver.ConexionServer.bajaCliente(datos):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowTitle('Aviso')
                    mbox.setWindowIcon(QIcon('./img/logo.ico'))
                    mbox.setText('Cliente dado de Baja')
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle('Aviso')
                    mbox.setWindowIcon(QIcon('./img/logo.ico'))
                    mbox.setText("Error al dar de baja el cliente")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                    mbox.exec()
                Clientes.cargaTablaClientes(self)
        except Exception as e:
            print("error bajaCliente en clientes", e)

    @staticmethod
    def historicoCli(self):
        try:
            if var.ui.chkHistoriaCli.isChecked():
                var.historico = 0
            else:
                var.historico = 1
            Clientes.cargaTablaClientes(self)
        except Exception as e:
            print("error en historicoCli", e)

    def cargaClienteDni(self):
        try:
            dni = var.ui.txtDniCli.text()
            #registro = conexion.Conexion.datosOneCliente(dni)
            registro = conexionserver.ConexionServer.datosOneCliente(dni)
            if not registro:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Aviso")
                mbox.setText("No se ha encontrado el cliente")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                return

            listado = [var.ui.txtDniCli, var.ui.txtAltaCli,
                       var.ui.txtApelCli, var.ui.txtNomCli,
                       var.ui.txtEmailCli, var.ui.txtMovilCli,
                       var.ui.txtDirCli, var.ui.cmbProvCli,
                       var.ui.cmbMuniCli, var.ui.txtBajaCli]

            for i, casilla in enumerate(listado):
                if isinstance(casilla, QtWidgets.QComboBox):
                    casilla.setCurrentText(registro[i])
                else:
                    casilla.setText(registro[i])

        except Exception as e:
            print("Error cargar Clientes por dni", e)



