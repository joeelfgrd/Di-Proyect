from multiprocessing.connection import Client
from PyQt6 import QtWidgets

import eventos
import var
from eventos import Eventos


class Clientes:
    def altaCliente(self):
        dni=var.ui.txtDniCli.text()
        print(dni)

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
