from multiprocessing.connection import Client
from PyQt6 import QtWidgets , QtCore
from PyQt6.QtGui import QIcon

import conexion
import eventos
import var


class Clientes:
    @staticmethod
    def altaCliente(self):
        try:
            nuevoCli = [var.ui.txtDniCli.text(), var.ui.txtAltaCli.text(), var.ui.txtApelCli.text(),
                        var.ui.txtNomCli.text(), var.ui.txtEmailCli.text(), var.ui.txtMovilCli.text(),
                        var.ui.txtDirCli.text(), var.ui.cmbProvCli.currentText(),
                        var.ui.cmbMuniCli.currentText()]
            if (var.ui.txtDniCli.text() != ''):
                if conexion.Conexion.altaCliente(nuevoCli):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowTitle('Aviso')
                    mbox.setWindowIcon(QIcon('./img/logo.ico'))
                    mbox.setText('Cliente Alta en Base de Datos')
                    mbox.setStandardButtons(
                        QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()
                    Clientes.cargaTablaClientes(self)
                    print("Cliente dado de alta")
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('./img/logo.ico'))
                mbox.setText("Error al dar de alta el cliente")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()
        except Exception as e:
            print("error altaCliente", e)


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
            listado = conexion.Conexion.listadoClientes(self)
            #listado = conexionserver.ConexionServer.listadoClientes(self)
            print(listado)
            index = 0
            for registro in listado:
                var.ui.tabClientes.setRowCount(index + 1)
                var.ui.tabClientes.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[2])))
                var.ui.tabClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[3])))
                var.ui.tabClientes.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[5])))
                var.ui.tabClientes.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[7])))
                var.ui.tabClientes.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[8])))
                var.ui.tabClientes.setItem(index, 5, QtWidgets.QTableWidgetItem(str(registro[9])))


                var.ui.tabClientes.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabClientes.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabClientes.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabClientes.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabClientes.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                index += 1





        except Exception as e:
            print("error cargaTablaClientes", e)

