'''archivo de propiedades'''
from PyQt6.QtGui import QIcon

import var
from dlgGestionProp import *
import conexion
import venAux

class Propiedades():
    def altaTipopropiedad(self):
        try:
            tipo = var.dlgGestion.ui.txtGestTipoProp.text().title()
            registro = conexion.Conexion.altaTipoProp(tipo)
            if registro:
                var.ui.cmbTipoprop.clear()
                var.ui.cmbTipoprop.addItems(registro)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('./img/logo.ico'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText("Error: Tipo de propiedad ya existe")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()
        except Exception as error:
            print("Error en alta tipo propiedad: ", error)
    def bajaTipopropiedad(self):
        try:
            tipo = var.dlgGestion.ui.txtGestTipoProp.text().title()
            conexion.Conexion.bajaTipoProp(tipo)
            print(tipo + "eliminado tipo propiedad")
        except Exception as error:
            print("Error en baja tipo propiedad: ", error)

    def altaPropiedad(self):
        try:
            propiedad = [var.ui.txtFechaprop.text(),var.ui.txtBajaprop.text(), var.ui.txtDirprop.text(),
                         var.ui.cmbProvprop.currentText(),var.ui.cmbMuniprop.currentText(),
                         var.ui.cmbTipoprop.currentText(),var.ui.spinHabprop.text(),
                         var.ui.spinBanosprop.text(),var.ui.txtSuperprop.text(),
                         var.ui.txtPrecioAlquilerprop.text(),var.ui.txtPrecioVentaprop.text(),
                         var.ui.txtCPprop.text(),var.ui.txtDescriprop.toPlainText(),var.ui.txtNomeprop.text(),
                         var.ui.txtMovilprop.text()]
            print(propiedad)
        except Exception as error:
            print("Error en alta propiedad: ", error)
