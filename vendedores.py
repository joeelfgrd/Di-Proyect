from multiprocessing.connection import Client
from PyQt6 import QtWidgets , QtCore
from PyQt6.QtGui import QIcon
from PyQt6.uic.Compiler.qtproxies import QtGui

import clientes
import conexion
import eventos
import var


class Vendedores:
    @staticmethod
    def altaVendedor(self):
        try:
            nuevovend = [var.ui.txtDniVend.text(), var.ui.txtAltaVend.text(),
                        var.ui.txtNombreVend.text(), var.ui.txtMailVend.text(), var.ui.txtMovilVend.text(),
                        var.ui.cmbProvVend.currentText()]
            if all(nuevovend[i] for i in [0, 1, 2, 3, 4, 5]):
                if conexion.Conexion.altaCliente(nuevovend):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowTitle('Aviso')
                    mbox.setWindowIcon(QIcon('./img/logo.ico'))
                    mbox.setText('Cliente dado de alta en la Base de Datos')
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()
                    #Clientes.cargaTablaClientes(self)
                    print("Vendedor dado de alta")
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('./img/logo.ico'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText("Error: Faltan campos obligatorios")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()

        except Exception as e:
            print("Error en altaVendedor:", e)

    def checkDNI(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDniVend.setText(str(dni))
            check = eventos.Eventos.validarDNIcli(dni)
            if check:
                var.ui.txtDniVend.setStyleSheet('background-color:rgb(255,255,220)')
            else:
                var.ui.txtDniVend.setStyleSheet('background-color:#FFC0CB;')
                var.ui.txtDniVend.setText(None)
                var.ui.txtDniVend.setFocus()

        except Exception as e:
            print("error check vendedor ", e)