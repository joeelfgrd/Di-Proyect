'''archivo de propiedades'''
from PyQt6.QtGui import QIcon

import eventos
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
                eventos.Eventos.cargarTipoprop(self)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('./img/logo.ico'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText("Error: Tipo de propiedad ya existe")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()
            var.dlgGestion.ui.txtGestTipoProp.setText('')
        except Exception as error:
            print("Error en alta tipo propiedad: ", error)
    def bajaTipopropiedad(self):
        try:
            tipo = var.dlgGestion.ui.txtGestTipoProp.text().title()
            registro = conexion.Conexion.bajaTipoProp(tipo)

            if registro:
                eventos.Eventos.cargarTipoprop(self)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('./img/logo.ico'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText("Error: Tipo de propiedad no existe")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()
            var.dlgGestion.ui.txtGestTipoProp.setText('')
        except Exception as error:
            print("Error en baja tipo propiedad: ", error)

    def altaPropiedad(self):
        try:
            propiedad = [var.ui.txtFechaprop.text(), var.ui.txtDirprop.text(),
                         var.ui.cmbProvprop.currentText(),var.ui.cmbMuniprop.currentText(),
                         var.ui.cmbTipoprop.currentText(),var.ui.spinHabprop.text(),
                         var.ui.spinBanosprop.text(),var.ui.txtSuperprop.text(),
                         var.ui.txtPrecioAlquilerprop.text(),var.ui.txtPrecioVentaprop.text(),
                         var.ui.txtCPprop.text(),var.ui.txtDescriprop.toPlainText(),var.ui.txtNomeprop.text(),
                         var.ui.txtMovilprop.text()]
            tipooper = []
            if var.ui.chkAlquilerprop.isChecked():
                tipooper.append(var.ui.chkAlquilerprop.text())
            if var.ui.chkVentaprop.isChecked():
                tipooper.append(var.ui.chkVentaprop.text())
            if var.ui.chkIntercambioprop.isChecked():
                tipooper.append(var.ui.chkIntercambioprop.text())
            propiedad.append(tipooper)
            if var.ui.rbDisponibleprop.isChecked():
                tipooper.append(var.ui.rbDisponibleprop.text())
            if var.ui.rbAlquilerprop.isChecked():
                tipooper.append(var.ui.rbAlquilerprop.text())
            if var.ui.rbVentaprop.isChecked():
                tipooper.append(var.ui.rbVentaprop.text())
            propiedad.append(var.ui.txtNomeprop.text())
            propiedad.append(var.ui.txtMovilprop.text())
            conexion.Conexion.altaPropiedad(propiedad)
        except Exception as error:
            print("Error en alta propiedad: ", error)
        print(propiedad)

