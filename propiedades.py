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
                         var.ui.cmbProvprop.currentText(), var.ui.cmbMuniprop.currentText(),
                         var.ui.cmbTipoprop.currentText(), var.ui.spinHabprop.text(),
                         var.ui.spinBanosprop.text(), var.ui.txtSuperprop.text(),
                         var.ui.txtPrecioAlquilerprop.text(), var.ui.txtPrecioVentaprop.text(),
                         var.ui.txtCPprop.text(), var.ui.txtDescriprop.toPlainText()]
            tipooper = []
            if var.ui.chkAlquilerprop.isChecked():
                tipooper.append(var.ui.chkAlquilerprop.text())
            if var.ui.chkVentaprop.isChecked():
                tipooper.append(var.ui.chkVentaprop.text())
            if var.ui.chkIntercambioprop.isChecked():
                tipooper.append(var.ui.chkIntercambioprop.text())
            propiedad.append("-".join(tipooper))
            if var.ui.rbDisponibleprop.isChecked():
                propiedad.append(var.ui.rbDisponibleprop.text())
            if var.ui.rbAlquilerprop.isChecked():
                propiedad.append(var.ui.rbAlquilerprop.text())
            if var.ui.rbVentaprop.isChecked():
                propiedad.append(var.ui.rbVentaprop.text())
            propiedad.append(var.ui.txtNomeprop.text())
            propiedad.append(var.ui.txtMovilprop.text())
            conexion.Conexion.altaPropiedad(propiedad)
            Propiedades.cargaTablaPropiedades(self)
        except Exception as error:
            print("Error en alta propiedad: ", error)
        print(propiedad)

    @staticmethod
    def cargaTablaPropiedades(self):
        try:
            listado = conexion.Conexion.listadoPropiedades(self)
            if listado is None:
                listado = []
            index = 0
            for registro in listado:
                var.ui.tablaPropiedades.setRowCount(index + 1)
                var.ui.tablaPropiedades.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaPropiedades.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[5])))
                var.ui.tablaPropiedades.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[6])))
                var.ui.tablaPropiedades.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[7])))
                var.ui.tablaPropiedades.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[8])))
                var.ui.tablaPropiedades.setItem(index, 5, QtWidgets.QTableWidgetItem(
                    str(registro[10]) + " €" if registro[10] else "- €"))
                var.ui.tablaPropiedades.setItem(index, 6, QtWidgets.QTableWidgetItem(
                    str(registro[11]) + " €" if registro[11] else "- €"))
                var.ui.tablaPropiedades.setItem(index, 7, QtWidgets.QTableWidgetItem(str(registro[14])))

                var.ui.tablaPropiedades.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 7).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                index += 1
        except Exception as e:
            print("error cargaTablaPropiedades", e)

    def cargaPropiedad(self):
        try:
            fila = var.ui.tablaPropiedades.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = conexion.Conexion.datosOnePropiedad(str(datos[0]))

            listado = [var.ui.lblprop, var.ui.txtFechaprop,
                       var.ui.txtBajaprop, var.ui.txtDirprop,
                       var.ui.cmbProvprop, var.ui.cmbMuniprop,
                       var.ui.cmbTipoprop, var.ui.spinHabprop, var.ui.spinBanosprop,
                       var.ui.txtSuperprop, var.ui.txtPrecioAlquilerprop, var.ui.txtPrecioVentaprop,
                       var.ui.txtCPprop, var.ui.txtDescriprop, var.ui.chkAlquilerprop,
                       var.ui.rbDisponibleprop, var.ui.txtNomeprop, var.ui.txtMovilprop
                       ]

            for i, casilla in enumerate(listado):
                if isinstance(casilla, QtWidgets.QComboBox):
                    casilla.setCurrentText(str(registro[i]))
                elif isinstance(casilla, QtWidgets.QCheckBox):
                    if ("Alquiler") in registro[i]:
                        var.ui.chkAlquilerprop.setChecked(True)
                    else:
                        var.ui.chkAlquilerprop.setChecked(False)
                    if ("Venta") in registro[i]:
                        var.ui.chkVentaprop.setChecked(True)
                    else:
                        var.ui.chkVentaprop.setChecked(False)
                    if ("Intercambio") in registro[i]:
                        var.ui.chkIntercambioprop.setChecked(True)
                    else:
                        var.ui.chkIntercambioprop.setChecked(False)
                elif isinstance(casilla, QtWidgets.QRadioButton):
                    if registro[i] == "Vendido":
                        var.ui.rbVentaprop.setChecked(True)
                    elif registro[i] == "Disponible":
                        var.ui.rbDisponibleprop.setChecked(True)
                    else:
                        var.ui.rbAlquilerprop.setChecked(True)
                elif isinstance(casilla, QtWidgets.QSpinBox):
                    casilla.setValue(int(registro[i]))
                elif isinstance(casilla, QtWidgets.QTextEdit):
                    casilla.setPlainText(str(registro[i]))
                else:
                    casilla.setText(str(registro[i]))
        except Exception as error:
            print("Error cargar propiedad: ", error)

    def bajaPropiedad(self):
        try:
            codigo = var.ui.lblprop.text()
            fecha = var.ui.txtBajaprop.text()
            if conexion.Conexion.bajaPropiedad(codigo,fecha):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('./img/logo.ico'))
                mbox.setText('Propiedad dada de baja')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()

            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('./img/logo.ico'))
                mbox.setText("Error al dar de baja la propiedad")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()
            Propiedades.cargaTablaPropiedades(self)
        except Exception as e:
            print("error bajaPropiedad en propiedades", e)





