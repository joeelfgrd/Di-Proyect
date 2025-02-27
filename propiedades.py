from datetime import datetime

from PyQt6 import QtWidgets, QtGui, QtCore

import conexion
import eventos
import facturas
import var


class Propiedades():

    def checkTelefono(telefono):
        try:
            telefono = str(var.ui.txtMovilPro.text())
            if eventos.Eventos.validarTelefono(telefono):
                var.ui.txtMovilPro.setStyleSheet('background-color: rgb(255, 252, 220);')
            else:
                var.ui.txtMovilPro.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtMovilPro.setText(None)
                var.ui.txtMovilPro.setText("telefono no válido")
                var.ui.txtMovilPro.setFocus()
        except Exception as error:
            print("error check cliente", error)

    @staticmethod
    def altaTipoPropiedad():
        try:
            tipo = var.dlggestion.ui.txtGestipoprop.text().title()
            registro = conexion.Conexion.altaTipoPropiedad(tipo)
            if registro:
                eventos.Eventos.cargarTipoPropiedad()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText('Ya existe el tipo.')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
            var.dlggestion.ui.txtGestipoprop.setText('')
        except Exception as error:
            print("Error en alta tipo propiedad: ", error)

    @staticmethod
    def bajaTipoPropiedad():
        try:
            tipo = var.dlggestion.ui.txtGestipoprop.text().title()
            registro = conexion.Conexion.bajaTipoPropiedad(tipo)
            if registro:
                eventos.Eventos.cargarTipoPropiedad()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText('No existe el tipo.')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
            var.dlggestion.ui.txtGestipoprop.setText('')
        except Exception as error:
            print("Error en baja tipo propiedad: ", error)

    @staticmethod
    def altaPropiedad():
        try:
            # var.ui.txtFechabajaPro.text(), var.ui.txtPropietarioPro.text(), var.ui.txtMovilPro.text()
            propiedad = [var.ui.txtPublicacionPro.text(), var.ui.txtDireccionPro.text(),
                        var.ui.cmbProvinciaPro.currentText(), var.ui.cmbMunicipioPro.currentText(),
                        var.ui.cmbTipoPro.currentText(), var.ui.spbHabitacionesPro.text(),
                        var.ui.spbBanosPro.text(), var.ui.txtSuperficiePro.text(),
                        var.ui.txtPrecioAlquilerPro.text(), var.ui.txtPrecioVentaPro.text(),
                        var.ui.txtCpPro.text(), var.ui.artxtDescripcionPro.toPlainText()]

            obligatorios = [var.ui.txtDireccionPro.text(), var.ui.txtPropietarioPro, var.ui.txtMovilPro,
                            var.ui.cmbProvinciaPro.currentText(), var.ui.cmbMunicipioPro.currentText(),
                            var.ui.cmbTipoPro.currentText(), var.ui.txtSuperficiePro.text(), var.ui.txtCpPro.text()]

            for i in obligatorios:
                if i == "":
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                    mbox.setWindowIcon(QtGui.QIcon('./img/icono.ico'))
                    mbox.setWindowTitle('Aviso')
                    mbox.setText('Rellena los campos obligatorios (los amarillos)')
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()
                    return

            tipoper = []
            if var.ui.cbxAlquilerPro.isChecked():
                tipoper.append(var.ui.cbxAlquilerPro.text())
            if var.ui.cbxVentaPro.isChecked():
                tipoper.append(var.ui.cbxVentaPro.text())
            if var.ui.cbxIntercambioPro.isChecked():
                tipoper.append(var.ui.cbxIntercambioPro.text())
            propiedad.append(", ".join(tipoper))
            if var.ui.rbtnDisponiblePro.isChecked():
                propiedad.append(var.ui.rbtnDisponiblePro.text())
            if var.ui.rbtnAlquiladoPro.isChecked():
                propiedad.append(var.ui.rbtnAlquiladoPro.text())
            if var.ui.rbtnVendidoPro.isChecked():
                propiedad.append(var.ui.rbtnVendidoPro.text())
            propiedad.append(var.ui.txtPropietarioPro.text())
            propiedad.append(var.ui.txtMovilPro.text())

            conexion.Conexion.altaPropiedad(propiedad)
            Propiedades.cargarTablaPropiedades(0)

        except Exception as error:
            print(error)

    @staticmethod
    def cargarTablaPropiedades(contexto):
        try:
            if contexto == 0:
                listado = conexion.Conexion.listadoPropiedades()
            elif contexto == 1:
                datosNecesarios = [var.ui.cmbTipoPro.currentText(), var.ui.cmbMunicipioPro.currentText()]
                listado = conexion.Conexion.listadoFiltrado(datosNecesarios)
            index = 0
            var.ui.tablaPropiedades.setRowCount(0)
            for registro in listado:
                var.ui.tablaPropiedades.setRowCount(index + 1)
                var.ui.tablaPropiedades.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaPropiedades.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[5])))
                var.ui.tablaPropiedades.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[6])))
                var.ui.tablaPropiedades.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[7])))
                var.ui.tablaPropiedades.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[8])))
                var.ui.tablaPropiedades.setItem(index, 5, QtWidgets.QTableWidgetItem(
                    str(registro[10]) + " €" if str(registro[10]) else "- €"))
                var.ui.tablaPropiedades.setItem(index, 6, QtWidgets.QTableWidgetItem(
                    str(registro[11]) + " €" if str(registro[11]) else "- €"))
                var.ui.tablaPropiedades.setItem(index, 7, QtWidgets.QTableWidgetItem(str(registro[14])))
                var.ui.tablaPropiedades.setItem(index, 8, QtWidgets.QTableWidgetItem(str(registro[2])))

                var.ui.tablaPropiedades.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 7).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 8).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                index += 1
            if len(listado) == 0:
                var.ui.tablaPropiedades.setRowCount(1)
                var.ui.tablaPropiedades.setItem(0, 2, QtWidgets.QTableWidgetItem("No hay propiedades"))

            if var.rowsPropiedades == 11:
                var.ui.btnAnteriorPro.setEnabled(False)
            else:
                var.ui.btnAnteriorPro.setEnabled(True)

            if len(listado) < 11:
                var.ui.btnSiguientePro.setEnabled(False)
            else:
                var.ui.btnSiguientePro.setEnabled(True)

        except Exception as e:
            print("error cargaTablaPropiedades", e)


    @staticmethod
    def cargaOnePropiedad():
        try:
            Propiedades.manageCheckbox()
            Propiedades.manageRadioButtons()
            fila = var.ui.tablaPropiedades.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = conexion.Conexion.datosOnePropiedad(str(datos[0]))
            facturas.Facturas.cargaPropiedadVenta(registro)
            listado = [var.ui.lblCodigoProp, var.ui.txtPublicacionPro, var.ui.txtFechabajaPro,
                        var.ui.txtDireccionPro, var.ui.cmbProvinciaPro, var.ui.cmbMunicipioPro,
                        var.ui.cmbTipoPro, var.ui.spbHabitacionesPro, var.ui.spbBanosPro,
                        var.ui.txtSuperficiePro, var.ui.txtPrecioAlquilerPro, var.ui.txtPrecioVentaPro,
                        var.ui.txtCpPro, var.ui.artxtDescripcionPro, var.ui.cbxAlquilerPro,
                        var.ui.rbtnDisponiblePro, var.ui.txtPropietarioPro, var.ui.txtMovilPro]

            for i, casilla in enumerate(listado):
                if isinstance(casilla, QtWidgets.QComboBox):
                    casilla.setCurrentText(str(registro[i]))
                elif isinstance(casilla, QtWidgets.QCheckBox):
                    if ("Alquiler") in registro[i]:
                        var.ui.cbxAlquilerPro.setChecked(True)
                    else:
                        var.ui.cbxAlquilerPro.setChecked(False)
                    if ("Venta") in registro[i]:
                        var.ui.cbxVentaPro.setChecked(True)
                    else:
                        var.ui.cbxVentaPro.setChecked(False)
                    if ("Intercambio") in registro[i]:
                        var.ui.cbxIntercambioPro.setChecked(True)
                    else:
                        var.ui.cbxIntercambioPro.setChecked(False)
                elif isinstance(casilla, QtWidgets.QRadioButton):
                    if registro[i] == "Vendido":
                        var.ui.rbtnVendidoPro.setChecked(True)
                    elif registro[i] == "Disponible":
                        var.ui.rbtnDisponiblePro.setChecked(True)
                    else:
                        var.ui.rbtnAlquiladoPro.setChecked(True)
                elif isinstance(casilla, QtWidgets.QSpinBox):
                    casilla.setValue(int(registro[i]))
                elif isinstance(casilla, QtWidgets.QTextEdit):
                    casilla.setPlainText(str(registro[i]))
                else:
                    casilla.setText(str(registro[i]))
            Propiedades.manageCheckbox()
            Propiedades.manageRadioButtons()

            var.ui.txtPropiedadContrato.setText(var.ui.lblCodigoProp.text())

        except Exception as e:
            print("error cargaOnePropiedad en propiedades", e)

    @staticmethod
    def modifPropiedad():
        try:
            facturas.Facturas.limpiarFactura()
            propiedad = [var.ui.txtPublicacionPro.text(), var.ui.txtDireccionPro.text(),
                         var.ui.cmbProvinciaPro.currentText(), var.ui.cmbMunicipioPro.currentText(),
                         var.ui.cmbTipoPro.currentText(), var.ui.spbHabitacionesPro.text(),
                         var.ui.spbBanosPro.text(), var.ui.txtSuperficiePro.text(),
                         var.ui.txtPrecioAlquilerPro.text(), var.ui.txtPrecioVentaPro.text(),
                         var.ui.txtCpPro.text(), var.ui.artxtDescripcionPro.toPlainText()]

            obligatorios = [var.ui.txtDireccionPro.text(), var.ui.txtPropietarioPro, var.ui.txtMovilPro,
                            var.ui.cmbProvinciaPro.currentText(), var.ui.cmbMunicipioPro.currentText(),
                            var.ui.cmbTipoPro.currentText(), var.ui.txtSuperficiePro.text(), var.ui.txtCpPro.text()]

            for i in obligatorios:
                if obligatorios[2] == "telefono no válido":
                    return
                if i == "":
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                    mbox.setWindowIcon(QtGui.QIcon('./img/icono.ico'))
                    mbox.setWindowTitle('Aviso')
                    mbox.setText('Rellena los campos obligatorios')
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()
                    return

            if var.ui.rbtnDisponiblePro.isChecked() and var.ui.txtFechabajaPro.text() != "":
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('./img/icono.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText('No puedes modificar la baja de una propiedad disponible')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
            else:
                tipoper = []
                if var.ui.cbxAlquilerPro.isChecked():
                    tipoper.append(var.ui.cbxAlquilerPro.text())
                if var.ui.cbxVentaPro.isChecked():
                    tipoper.append(var.ui.cbxVentaPro.text())
                if var.ui.cbxIntercambioPro.isChecked():
                    tipoper.append(var.ui.cbxIntercambioPro.text())
                propiedad.append(", ".join(tipoper))
                if var.ui.rbtnDisponiblePro.isChecked():
                    propiedad.append(var.ui.rbtnDisponiblePro.text())
                if var.ui.rbtnAlquiladoPro.isChecked():
                    propiedad.append(var.ui.rbtnAlquiladoPro.text())
                if var.ui.rbtnVendidoPro.isChecked():
                    propiedad.append(var.ui.rbtnVendidoPro.text())

                propiedad.append(var.ui.txtPropietarioPro.text())
                propiedad.append(var.ui.txtMovilPro.text())
                propiedad.append(var.ui.lblCodigoProp.text())

                if var.ui.txtFechabajaPro.text() == "":
                    propiedad.append("")
                else:
                    fecha_publicacion = datetime.strptime(var.ui.txtPublicacionPro.text(), "%d/%m/%Y")
                    fecha_baja = datetime.strptime(var.ui.txtFechabajaPro.text(), "%d/%m/%Y")
                    if fecha_baja > fecha_publicacion:
                        propiedad.append(var.ui.txtFechabajaPro.text())
                    else:
                        mbox = QtWidgets.QMessageBox()
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                        mbox.setWindowTitle('Error')
                        mbox.setText('La fecha de baja debe ser posterior a la fecha de publicación')
                        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                        mbox.exec()

                if conexion.Conexion.modifPropiedades(propiedad):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowIcon(QtGui.QIcon('./img/icono.ico'))
                    mbox.setWindowTitle('Aviso')
                    mbox.setText('Datos de la propiedad modificados')
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()
                    Propiedades.cargarTablaPropiedades(0)
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                    mbox.setWindowIcon(QtGui.QIcon('./img/icono.ico'))
                    mbox.setWindowTitle('Aviso')
                    mbox.setText('Error en actualizacion Datos de la propiedad')
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()
                Propiedades.cargarTablaPropiedades(0)
                facturas.Facturas.limpiarFactura()
                Propiedades.manageCheckbox()
                Propiedades.manageRadioButtons()
        except Exception as error:
            print("error modifPropiedad en propiedades", error)

    @staticmethod
    def bajaPropiedad():
        try:
            facturas.Facturas.limpiarFactura()
            if var.ui.rbtnDisponiblePro.isChecked():
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('./img/icono.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText('La propiedad no puede darse de baja si está disponible')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
            else:
                fecha_baja = datetime.strptime(var.ui.txtFechabajaPro.text(), "%d/%m/%Y").strftime("%d/%m/%Y")
                datos = [fecha_baja, var.ui.lblCodigoProp.text()]
                fecha_publicacion = datetime.strptime(var.ui.txtPublicacionPro.text(), "%d/%m/%Y").strftime("%d/%m/%Y")
                if datetime.strptime(fecha_baja, "%d/%m/%Y") > datetime.strptime(fecha_publicacion, "%d/%m/%Y"):
                    if conexion.Conexion.bajaPropiedad(datos):
                        mbox = QtWidgets.QMessageBox()
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                        mbox.setWindowIcon(QtGui.QIcon('./img/icono.ico'))
                        mbox.setWindowTitle('Aviso')
                        mbox.setText('Propiedad dada de baja')
                        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                        mbox.exec()
                        Propiedades.cargarTablaPropiedades(0)
                    else:
                        mbox = QtWidgets.QMessageBox()
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                        mbox.setWindowIcon(QtGui.QIcon('./img/icono.ico'))
                        mbox.setWindowTitle('Aviso')
                        mbox.setText('Error en la baja de la propiedad')
                        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                        mbox.exec()
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                    mbox.setWindowTitle('Error')
                    mbox.setText('La fecha de baja debe ser posterior a la fecha de publicación')
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.exec()
                Propiedades.cargarTablaPropiedades(0)
                facturas.Facturas.limpiarFactura()
                Propiedades.manageCheckbox()
                Propiedades.manageRadioButtons()
        except Exception as error:
            print("error bajaPropiedad en propiedades", error)

    @staticmethod
    def historicoProp():
        try:
            if var.ui.chkHistoricoPro.isChecked():
                var.historicoProp = 1
            else:
                var.historicoProp = 0
            var.rowsPropiedades = 11
            Propiedades.cargarTablaPropiedades(0)
        except Exception as e:
            print("checkbox historico error ", e)

    @staticmethod
    def filtrarPropiedades():
        if not var.ui.cmbTipoPro.currentText() or not var.ui.cmbMunicipioPro.currentText():
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setWindowIcon(QtGui.QIcon('./img/icono.ico'))
            mbox.setWindowTitle('Aviso')
            mbox.setText('Los campos Tipo y Municipio han de contener algo')
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
            mbox.exec()
        elif var.lupaState == 0:
            var.lupaState = 1
            Propiedades.cargarTablaPropiedades(1)
        elif var.lupaState == 1:
            var.lupaState = 0
            Propiedades.cargarTablaPropiedades(0)

    @staticmethod
    def manageCheckbox():

        var.ui.cbxAlquilerPro.setEnabled(False)
        var.ui.cbxVentaPro.setEnabled(False)

        if var.ui.txtPrecioAlquilerPro.text() == "":
            var.ui.cbxAlquilerPro.setChecked(False)
        else:
            var.ui.cbxAlquilerPro.setChecked(True)

        if var.ui.txtPrecioVentaPro.text() == "":
            var.ui.cbxVentaPro.setChecked(False)
        else:
            var.ui.cbxVentaPro.setChecked(True)

        if var.ui.txtPrecioAlquilerPro.text() == "" and var.ui.txtPrecioVentaPro.text() == "":
            var.ui.cbxIntercambioPro.setChecked(False)

    @staticmethod
    def manageRadioButtons():
        var.ui.rbtnDisponiblePro.setEnabled(False)

        if var.ui.txtFechabajaPro.text() == "":
            var.ui.rbtnDisponiblePro.setChecked(True)
            var.ui.rbtnAlquiladoPro.setChecked(False)
            var.ui.rbtnVendidoPro.setChecked(False)
            var.ui.rbtnAlquiladoPro.setEnabled(False)
            var.ui.rbtnVendidoPro.setEnabled(False)
        else:

            if conexion.Conexion.datosOnePropiedad(var.ui.lblCodigoProp.text())[15] == "Alquilado":
                var.ui.rbtnAlquiladoPro.setEnabled(True)
                var.ui.rbtnAlquiladoPro.setChecked(False)
                var.ui.rbtnVendidoPro.setEnabled(True)
                var.ui.rbtnVendidoPro.setChecked(False)

            elif conexion.Conexion.datosOnePropiedad(var.ui.lblCodigoProp.text())[15] == "Vendido":
                var.ui.rbtnAlquiladoPro.setEnabled(True)
                var.ui.rbtnAlquiladoPro.setChecked(False)
                var.ui.rbtnVendidoPro.setEnabled(True)
                var.ui.rbtnVendidoPro.setChecked(False)

            else:
                var.ui.rbtnDisponiblePro.setChecked(False)
                var.ui.rbtnAlquiladoPro.setEnabled(True)
                var.ui.rbtnAlquiladoPro.setChecked(False)
                var.ui.rbtnVendidoPro.setEnabled(True)
                var.ui.rbtnVendidoPro.setChecked(True)