import csv
import json
import os.path
from datetime import datetime

from PyQt6 import QtWidgets, QtGui

import sys
import time
import re

import clientes
import conexion
import eventos
import propiedades
import var
import locale
import zipfile
import shutil
import conexionserver

# Establecer configuración regional

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
locale.setlocale(locale.LC_MONETARY, 'es_ES.UTF-8')

class Eventos():

    @staticmethod
    def crearMensajeInfo(titulo_ventana, mensaje):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
        mbox.setWindowIcon(QtGui.QIcon('img/icono.png'))
        mbox.setWindowTitle(titulo_ventana)
        mbox.setText(mensaje)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
        mbox.exec()

    @staticmethod
    def crearMensajeError(titulo_ventana, mensaje):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        mbox.setWindowIcon(QtGui.QIcon('img/icono.png'))
        mbox.setWindowTitle(titulo_ventana)
        mbox.setText(mensaje)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
        mbox.exec()

    def mensajeSalir(self=None):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        mbox.setWindowIcon(QtGui.QIcon('img/icono.ico'))
        mbox.setWindowTitle('Salir')
        mbox.setText('Desea usted Salir?')
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Si')
        mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')

        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            mbox.hide()

    def cargarProv(self):
        var.ui.cmbProvinciacli.clear()
        listado = conexion.Conexion.listaProv(self)
        #listado = conexionserver.ConexionServer.listaProv(self)
        var.ui.cmbProvinciacli.addItems(listado)
        var.ui.cmbProvinciaPro.addItems(listado)
        var.ui.cmbDelegacionVend.addItems(listado)

    def cargarMunicipiosCli(self):
        var.ui.cmbMunicipiocli.clear()
        provincia = var.ui.cmbProvinciacli.currentText()
        listado = conexion.Conexion.listaMunicipios(provincia)
        #listado = conexionserver.ConexionServer.listaMuniProv(provincia)
        var.ui.cmbMunicipiocli.addItems(listado)

    def cargarMunicipiosPro(self):
        var.ui.cmbMunicipioPro.clear()
        provincia = var.ui.cmbProvinciaPro.currentText()
        listado = conexion.Conexion.listaMunicipios(provincia)
        #listado = conexionserver.ConexionServer.listaMuniProv(provincia)
        var.ui.cmbMunicipioPro.addItems(listado)


    def validarDNIcli(dni):
        try:
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            reemplazos = {'X': '0', 'Y': '1', 'Z': '2'}

            if len(dni) != 9:
                return False

            digito_control = dni[-1].upper()
            numero_base = dni[:-1]

            if numero_base[0] in reemplazos:
                numero_base = numero_base.replace(numero_base[0], reemplazos[numero_base[0]])

            if not numero_base.isdigit():
                return False

            numero = int(numero_base)
            letra_calculada = tabla[numero % 23]
            return letra_calculada == digito_control

        except Exception as e:
            print("Error al validar el DNI:", e)
            return False

    def abrirCalendar(btn):
        try:
            var.btn = btn
            var.uicalendar.show()
        except Exception as error:
            print("error en abrir calendar ", error)

    def cargaFecha(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if var.btn == 0:
                var.ui.txtAltacli.setText(str(data))
            elif var.btn == 1:
                var.ui.txtBajacli.setText(str(data))
            elif var.btn == 2:
                var.ui.txtPublicacionPro .setText(str(data))
            elif var.btn == 3:
                var.ui.txtFechabajaPro.setText(str(data))
            elif var.btn == 4:
                var.ui.txtBajaVend.setText(str(data))
            elif var.btn == 5:
                var.ui.txtAltaVend.setText(str(data))
            elif var.btn == 6:
                var.ui.txtFechaFactura.setText(str(data))
            time.sleep(0.125)
            var.uicalendar.hide()
            return data
        except Exception as error:
            print("error en cargar fecha: ", error)


    def validarMail(mail):
        try:
            mail = mail.lower()
            regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(regex, mail))
        except Exception as e:
            print("Error al validar el email:", e)
            return False

    def validarTelefono(telefono):
        try:
            regex = r'^[6-7]\d{8}$'
            if re.match(regex, telefono):
                return True
            else:
                return False
        except Exception as error:
            print("error en validar telefono: ", error)
            return False


    def resizeTablaClientes(self):
        try:
            header = var.ui.tablaClientes.horizontalHeader()
            for i in range(header.count()):
                if i in (1,2,4,5):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                header_items = var.ui.tablaClientes.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)
        except Exception as e:
            print("error en resize tabla clientes: ", e)

    def resizeTablaPropiedades(self):
        try:
            header = var.ui.tablaPropiedades.horizontalHeader()
            for i in range(header.count()):
                if (i in (1,2)):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                header_items = var.ui.tablaPropiedades.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)
        except Exception as e:
            print("error en resize tabla clientes: ", e)

    def resizeTablaVendedores(self):
        try:
            header = var.ui.tablaVendedores.horizontalHeader()
            for i in range(header.count()):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                header_items = var.ui.tablaVendedores.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)
        except Exception as e:
            print("error en resize tabla clientes: ", e)

    def crearBackup(self):
        try:
            fecha = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            copia = str(fecha) + '_backup.zip'
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Guardar Copia Seguridad", copia, '.zip')
            if var.dlgabrir.accept and fichero:
                fichzip = zipfile.ZipFile(fichero, 'w')
                fichzip.write('bbdd.sqlite', os.path.basename('bbdd.sqlite'), zipfile.ZIP_DEFLATED)
                fichzip.close()
                shutil.move(fichero, directorio)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('img/icono.ico'))
                mbox.setWindowTitle('Copia Seguridad')
                mbox.setText('Copia Seguridad Creada')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()

        except Exception as error:
            print("error en crear backup: ", error)

    def restaurarBackup(self):
        try:
            filename = var.dlgabrir.getOpenFileName(None, "Restaurar Copia Seguridad", '', '*.zip;;All Files(*)')
            file = filename[0]
            if file:
                with zipfile.ZipFile(file, 'r') as bbdd:
                    bbdd.extractall(pwd=None)
                bbdd.close()
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('img/icono.ico'))
                mbox.setWindowTitle('Copia Seguridad')
                mbox.setText('Copia Seguridad Restaurada')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                conexion.Conexion.db_conexion(self)
                eventos.Eventos.cargarProv(self)
                clientes.Clientes.cargaTablaClientes(self)
        except Exception as error:
            print("error en restaurar backup: ", error)

    def limpiarPanel(self):
        objetosPanelcli = [
            var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli, var.ui.txtNomcli, var.ui.txtEmailcli,
            var.ui.txtMovilcli, var.ui.txtDireccioncli, var.ui.cmbProvinciacli, var.ui.cmbMunicipiocli,
            var.ui.txtBajacli
        ]

        objetosPanelvend = [var.ui.txtIdVend, var.ui.txtDniVend, var.ui.txtNombreVend, var.ui.txtAltaVend,
                   var.ui.txtBajaVend, var.ui.txtTelefonoVend, var.ui.txtEmailVend,
                   var.ui.cmbDelegacionVend]

        for i, dato in enumerate(objetosPanelcli):
            if i not in (7, 8):
                dato.setText("")

        for i, dato in enumerate(objetosPanelvend):
            if i not in (0, 7):
                dato.setText("")
            elif i == 0:
                var.ui.txtIdVend.setText("")

        eventos.Eventos.cargarProv(self)
        var.ui.cmbMunicipiocli.clear()

        objetospanelprop = [var.ui.txtPublicacionPro, var.ui.txtFechabajaPro, var.ui.txtDireccionPro,
                            var.ui.txtSuperficiePro, var.ui.txtPrecioAlquilerPro,
                            var.ui.txtPrecioVentaPro, var.ui.txtCpPro, var.ui.artxtDescripcionPro, var.ui.txtPropietarioPro,
                            var.ui.txtMovilPro]

        for i, dato in enumerate(objetospanelprop):
            dato.setText("")

        var.ui.cmbProvinciaPro.clear()
        var.ui.cmbMunicipioPro.clear()
        var.ui.cmbTipoPro.clear()
        var.ui.spbHabitacionesPro.setValue(0)
        var.ui.spbBanosPro.setValue(0)
        var.ui.lblCodigoProp.setText("")
        if var.ui.cbxAlquilerPro.isChecked():
            var.ui.cbxAlquilerPro.setChecked(False)
        if var.ui.cbxVentaPro.isChecked():
            var.ui.cbxVentaPro.setChecked(False)
        if var.ui.cbxIntercambioPro.isChecked():
            var.ui.cbxIntercambioPro.setChecked(False)
        eventos.Eventos.cargarProv(self)
        eventos.Eventos.cargarTipoPropiedad(self)
        clientes.Clientes.cargaTablaClientes(self)
        propiedades.Propiedades.cargarTablaPropiedades(self, 0)

    def abrirTipoProp(self):
        try:
            var.dlggestion.show()
        except Exception as error:
            print("error en abrir gestion propiedades ", error)

    def cargarTipoPropiedad(self):
        try:
            registro = conexion.Conexion.cargarTipoProp()
            if registro:
                var.ui.cmbTipoPro.clear()
                var.ui.cmbTipoPro.addItems(registro)
        except Exception as error:
            print("Error en cargar tipo propiedad: ", error)

    def exportCSVprop(self):
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = str(fecha + "DatosPropiedades.csv")
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Exporta Datos en CSV", file, '.csv')
            if fichero:
                historicoGuardar = var.historicoProp
                var.historicoProp = 1
                registros = conexion.Conexion.listadoPropiedades(self)
                var.historicoProp = historicoGuardar
                with open(fichero, "w", newline="", encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Codigo", "Alta", "Baja", "Direccion", "Provincia", "Municipio", "Tipo"
                                        , "Nº Habitaciones", "Nº Baños", "Superficie", "Precio Alquiler",
                                     "Precio Compra",
                                     "Codigo Postal", "Observaciones", "Operacion", "Estado", "Propietario", "Movil"])
                    for registro in registros:
                        writer.writerow(registro)
                shutil.move(fichero, directorio)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowIcon(QtGui.QIcon("img/icono.ico"))
                mbox.setWindowTitle('Error')
                mbox.setText('Error en la exportacion de csv')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
        except Exception as e:
            print(e)

    def exportJSONprop(self):
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = str(fecha + "DatosPropiedades.json")
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Exporta Datos en CSV", file, '.csv')
            if fichero:
                keys = ["Codigo", "Alta", "Baja", "Direccion", "Provincia", "Municipio", "Tipo"
                    , "Nº Habitaciones", "Nº Baños", "Superficie", "Precio Alquiler", "Precio Compra",
                        "Codigo Postal", "Observaciones", "Operacion", "Estado", "Propietario", "Movil"]
                historicoGuardar = var.historicoProp
                var.historicoProp = 1
                registros = conexion.Conexion.listadoPropiedades(self)
                var.historicoProp = historicoGuardar
                listapropiedades = [dict(zip(keys, registro)) for registro in registros]
                with open(fichero, "w", newline="", encoding="utf-8") as jsonfile:
                    json.dump(listapropiedades, jsonfile, ensure_ascii=False, indent=4)
                shutil.move(fichero, directorio)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowIcon(QtGui.QIcon("img/icono.ico"))
                mbox.setWindowTitle('Error')
                mbox.setText('Error en la exportacion de csv')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
        except Exception as e:
            print(e)

    def abrirAbout(self):
        try:
            var.dlgAbout.show()
        except Exception as error:
            print("error en abrir about ", error)

    def abrirBuscarLocalidad(self):
        try:
            var.dlgLocalidad.show()
        except Exception as error:
            print("error en abrir BuscarLocalidad ", error)

    def movimientoPaginas(self, avance, tabla):
        try:
            if tabla == "Clientes":
                if avance == 0:
                    if var.rowsClientes >= 15:
                        var.rowsClientes -= 15
                else:
                    var.rowsClientes += 15
                clientes.Clientes.cargaTablaClientes(self)
            elif tabla == "Propiedades":
                if avance == 0:
                    if var.rowsPropiedades >= 11:
                        var.rowsPropiedades -= 11
                else:
                    var.rowsPropiedades += 11
                propiedades.Propiedades.cargarTablaPropiedades(self, 0)
        except Exception as error:
            print("error en pagina clientes: ", error)

    def exportJSONvendedores(self):
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = str(fecha + "DatosVendedores.json")
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Exporta Datos en CSV", file, '.csv')
            if fichero:
                keys = ["Id", "Nombre", "Movil", "Delegacion", "Dni", "Alta", "Baja", "Mail"]
                historicoGuardar = var.historicoVend
                var.historicoVend = 1
                registros = conexion.Conexion.listadoDatosVendedores(self)
                var.historicoVend = historicoGuardar
                listadoVendedores = [dict(zip(keys, registro)) for registro in registros]
                with open(fichero, "w", newline="", encoding="utf-8") as jsonfile:
                    json.dump(listadoVendedores, jsonfile, ensure_ascii=False, indent=4)
                shutil.move(fichero, directorio)
                eventos.Eventos.crearMensajeInfo("Bien", "Se han exportado los datos bien")
            else:
                eventos.Eventos.crearMensajeError("Error", "Error al exportar los datos")
        except Exception as e:
            print(e)