'''archivo de propiedades'''
from datetime import datetime

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox

import VenPrincipal
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
            direccion = var.ui.txtDirprop.text()
            propietario = var.ui.txtNomeprop.text()
            movil = var.ui.txtMovilprop.text()
            fecha = var.ui.txtFechaprop.text()
            provincia = var.ui.cmbProvprop.currentText()
            municipio = var.ui.cmbMuniprop.currentText()
            cp = var.ui.txtCPprop.text()
            superf = var.ui.txtSuperprop.text()

            if not direccion or not propietario or not movil or fecha == "" or provincia == "" or municipio == "" or cp == "" or superf == "":
                mbox = QMessageBox()
                mbox.setIcon(QMessageBox.Icon.Warning)
                mbox.setWindowTitle('Aviso')
                mbox.setText(
                    "Por favor, complete los campos obligatorios.")
                mbox.setStandardButtons(QMessageBox.StandardButton.Ok)
                mbox.exec()
                var.ui.txtDirprop.setStyleSheet('background-color:rgb(255,255,220);')
                return

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
            Propiedades.cargaTablaPropiedades(self, 0)
        except Exception as error:
            print("Error en alta propiedad: ", error)
        print(propiedad)

    def cargaTablaPropiedades(self, contexto):
        try:
            # Restablecer la tabla
            var.ui.tablaPropiedades.setRowCount(0)

            # Obtener listado completo
            listado = conexion.Conexion.listadoPropiedades(self)
            total_items = len(listado)

            # Cálculo de paginación
            start_index = var.current_page_prop * var.items_per_page_prop
            end_index = start_index + var.items_per_page_prop
            paginated_list = listado[start_index:end_index]

            # Rellenar la tabla
            for i, registro in enumerate(paginated_list):
                # Filtrar por tipo y municipio si corresponde
                if var.ui.btnTipoProp.isChecked() and contexto == 1:
                    tipo = var.ui.cmbTipoprop.currentText()
                    muni = var.ui.cmbMuniprop.currentText()
                    if registro[6] != tipo or registro[5] != muni:
                        continue

                # Añadir fila a la tabla
                var.ui.tablaPropiedades.setRowCount(i + 1)
                var.ui.tablaPropiedades.setItem(i, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaPropiedades.setItem(i, 1, QtWidgets.QTableWidgetItem(registro[5]))
                var.ui.tablaPropiedades.setItem(i, 2, QtWidgets.QTableWidgetItem(registro[6]))
                var.ui.tablaPropiedades.setItem(i, 3, QtWidgets.QTableWidgetItem(str(registro[7])))
                var.ui.tablaPropiedades.setItem(i, 4, QtWidgets.QTableWidgetItem(str(registro[8])))

            # Mostrar mensaje si no hay resultados
            if var.ui.tablaPropiedades.rowCount() == 0:
                var.ui.tablaPropiedades.setRowCount(1)
                var.ui.tablaPropiedades.setItem(0, 2, QtWidgets.QTableWidgetItem("No Hay Propiedades"))

            # Habilitar/deshabilitar botones de paginación
            var.ui.btnSiguienteProp.setEnabled(end_index < total_items)
            var.ui.btnAnteriorProp.setEnabled(var.current_page_prop > 0)

        except Exception as e:
            print("Error al cargar propiedades:", e)

    def siguientePaginaProp(self):
        try:
            total_items = len(conexion.Conexion.listadoPropiedades(self))
            total_pages = (total_items + var.items_per_page_prop - 1) // var.items_per_page_prop
            print("pulsado boton siguiente")
            if var.current_page_prop < total_pages - 1:
                var.current_page_prop += 1
                self.cargaTablaPropiedades(contexto=0)
            else:
                print("No hay más páginas.")
        except Exception as e:
            print("Error al pasar a la siguiente página:", e)

    def anteriorPaginaProp(self):
        try:
            if var.current_page_prop > 0:
                var.current_page_prop -= 1
                self.cargaTablaPropiedades(contexto=1)
            else:
                print("No hay páginas anteriores.")
        except Exception as e:
            print("Error al retroceder a la página anterior:", e)


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
            fechabaja = var.ui.txtBajaprop.text()
            if not fechabaja:
                fechabaja = datetime.today().strftime('%Y-%m-%d')
            if fechabaja < var.ui.txtFechaprop.text():
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('./img/logo.ico'))
                mbox.setText("Error, la fecha de baja no puede ser anterior a la fecha de alta")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()
                return
            if var.ui.rbDisponibleprop.isChecked():
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('./img/logo.ico'))
                mbox.setText("Error,no se puede dar de baja una propiedad disponible")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()
                return

            if conexion.Conexion.bajaPropiedad(codigo, fechabaja):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('./img/logo.ico'))
                mbox.setText('Propiedad dada de baja')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
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
            Propiedades.cargaTablaPropiedades(self, 0)

        except Exception as e:
            print("Error bajaPropiedad en propiedades:", e)

    def modifPropiedad(self):
        try:

            registro = [
                var.ui.lblprop.text(),
                var.ui.txtFechaprop.text(),
                var.ui.txtDirprop.text(),
                var.ui.cmbProvprop.currentText(),
                var.ui.cmbMuniprop.currentText(),
                var.ui.cmbTipoprop.currentText(),
                var.ui.spinHabprop.text(),
                var.ui.spinBanosprop.text(),
                var.ui.txtSuperprop.text(),
                var.ui.txtPrecioAlquilerprop.text(),
                var.ui.txtPrecioVentaprop.text(),  # Validación de precios
                var.ui.txtCPprop.text(),
                var.ui.txtDescriprop.toPlainText()
            ]

            tipooper = []
            if var.ui.chkAlquilerprop.isChecked():
                tipooper.append(var.ui.chkAlquilerprop.text())
            if var.ui.chkVentaprop.isChecked():
                tipooper.append(var.ui.chkVentaprop.text())
            if var.ui.chkIntercambioprop.isChecked():
                tipooper.append(var.ui.chkIntercambioprop.text())
            registro.append("-".join(tipooper))

            if var.ui.rbDisponibleprop.isChecked():
                registro.append(var.ui.rbDisponibleprop.text())
            if var.ui.rbAlquilerprop.isChecked():
                registro.append(var.ui.rbAlquilerprop.text())
            if var.ui.rbVentaprop.isChecked():
                registro.append(var.ui.rbVentaprop.text())
            registro.append(var.ui.txtNomeprop.text())
            registro.append(var.ui.txtMovilprop.text())
            if var.ui.txtBajaprop.text() == "":
                registro.append("")
            else:
                fecha_alta = datetime.strptime(var.ui.txtFechaprop.text(), '%d/%m/%Y')
                fecha_baja = datetime.strptime(var.ui.txtBajaprop.text(), '%d/%m/%Y')
                if fecha_baja > fecha_alta:
                    registro.append(var.ui.txtBajaprop.text())
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle('Aviso')
                    mbox.setWindowIcon(QIcon('./img/logo.ico'))
                    mbox.setText("Error, la fecha de baja no puede ser anterior a la fecha de alta")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                    mbox.exec()
                    return

            if conexion.Conexion.modifPropiedad(registro):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText('Propiedad modificada correctamente')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Propiedades.cargaTablaPropiedades(self, 0)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setText("Error al modificar la propiedad")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()
                Propiedades.cargaTablaPropiedades(self, 0)

        except Exception as error:
            print("error modificar propiedad", error)

    def historicoProp(self):
        try:
            if var.ui.chkHistoriaprop.isChecked():
                var.historico = 0
            else:
                var.historico = 1
            Propiedades.cargaTablaPropiedades(self, 0)

        except Exception as error:
            print("Error en historico propiedades: ", error)

    def filtroPorTipoPropiedad(self):

        if var.ui.btnTipoProp.isChecked():
            try:
                tipoSeleccionado = var.ui.cmbTipoprop.currentText()
                if tipoSeleccionado:
                    listado = conexion.Conexion.propiedadesPorTipo(tipoSeleccionado)
                else:
                    listado = conexion.Conexion.listadoPropiedades(self)

                var.ui.tablaPropiedades.setRowCount(0)
                i = 0
                for registro in listado:
                    var.ui.tablaPropiedades.setRowCount(i + 1)

                    var.ui.tablaPropiedades.setItem(i, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                    var.ui.tablaPropiedades.setItem(i, 1, QtWidgets.QTableWidgetItem(registro[5]))
                    var.ui.tablaPropiedades.setItem(i, 2, QtWidgets.QTableWidgetItem(registro[6]))
                    var.ui.tablaPropiedades.setItem(i, 3, QtWidgets.QTableWidgetItem(str(registro[7])))
                    var.ui.tablaPropiedades.setItem(i, 4, QtWidgets.QTableWidgetItem(str(registro[8])))
                    if registro[10] == "":
                        registro[10] = "-"
                    if registro[11] == "":
                        registro[11] = "-"
                    var.ui.tablaPropiedades.setItem(i, 5, QtWidgets.QTableWidgetItem(str(registro[10]) + " €"))
                    var.ui.tablaPropiedades.setItem(i, 6, QtWidgets.QTableWidgetItem(str(registro[11]) + " €"))
                    var.ui.tablaPropiedades.setItem(i, 7, QtWidgets.QTableWidgetItem(registro[14]))
                    var.ui.tablaPropiedades.setItem(i, 8, QtWidgets.QTableWidgetItem(registro[2]))

                    var.ui.tablaPropiedades.item(i, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaPropiedades.item(i, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaPropiedades.item(i, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaPropiedades.item(i, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaPropiedades.item(i, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaPropiedades.item(i, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
                    var.ui.tablaPropiedades.item(i, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
                    var.ui.tablaPropiedades.item(i, 7).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaPropiedades.item(i, 8).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                    i += 1

            except Exception as e:
                print("Error al filtrar propiedades por tipo:", e)

        else:
            Propiedades.cargaTablaPropiedades(self, 0)

    def controlDeCheckbox(self):
        if var.ui.txtPrecioAlquilerprop.text() == "":
            var.ui.chkAlquilerprop.setChecked(False)
            var.ui.chkAlquilerprop.setEnabled(False)
        else:
            var.ui.chkAlquilerprop.setChecked(True)
            var.ui.chkAlquilerprop.setEnabled(True)

        if var.ui.txtPrecioVentaprop.text() == "":
            var.ui.chkVentaprop.setChecked(False)
            var.ui.chkVentaprop.setEnabled(False)
        else:
            var.ui.chkVentaprop.setChecked(True)
            var.ui.chkVentaprop.setEnabled(True)

    def controlDeRadioButtons(self):
        if var.ui.txtBajaprop.text() == "":
            var.ui.rbDisponibleprop.setEnabled(True)
            var.ui.rbDisponibleprop.setChecked(True)
            var.ui.rbAlquilerprop.setChecked(False)
            var.ui.rbVentaprop.setChecked(False)
            var.ui.rbAlquilerprop.setEnabled(False)
            var.ui.rbVentaprop.setEnabled(False)
        else:
            var.ui.rbDisponibleprop.setChecked(False)
            var.ui.rbDisponibleprop.setEnabled(False)
            var.ui.rbAlquilerprop.setChecked(True)
            var.ui.rbAlquilerprop.setEnabled(True)
            var.ui.rbVentaprop.setEnabled(True)
