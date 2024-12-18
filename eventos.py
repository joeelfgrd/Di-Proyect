import csv
import json
import sys
import re
import zipfile
import shutil
from PyQt6 import QtWidgets, QtSql
from PyQt6.QtGui import QIcon
from PyQt6.uic.properties import QtGui
import vendedores
import VenPrincipal
import clientes
import conexion
import eventos
import propiedades
import var
import locale
import time
from datetime import datetime
import conexionserver
import os

#Establecer configuracion regional

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
locale.setlocale(locale.LC_MONETARY, 'es_ES.UTF-8')




class Eventos():

    @staticmethod
    def crearMensajeSalida(titulo_ventana, mensaje):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        mbox.setWindowIcon(QIcon('./img/logo.ico'))
        mbox.setText(mensaje)
        mbox.setWindowTitle(titulo_ventana)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Sí')
        mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')
        return mbox


    @staticmethod
    def crearMensajeInfo(titulo_ventana, mensaje):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
        mbox.setWindowIcon(QIcon('./img/logo.ico'))
        mbox.setWindowTitle(titulo_ventana)
        mbox.setText(mensaje)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
        return mbox


    @staticmethod
    def crearMensajeError(titulo_ventana, mensaje):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        mbox.setWindowIcon(QIcon('./img/logo.ico'))
        mbox.setWindowTitle(titulo_ventana)
        mbox.setText(mensaje)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
        mbox.exec()
        return mbox



    def mensajeSalir(self=None):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        
        # mbox.setWindowIcon(QtGui.QIcon('./img/icono.ico')) # PONER UN ICONO .SVG
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
        listaprov = conexion.Conexion.listaProv(self)
        cmbprovcli = var.ui.cmbProvCli
        cmbprovprop = var.ui.cmbProvprop
        cmbprovvend= var.ui.cmbProvVend
        cmbprovcli.clear()
        cmbprovprop.clear()
        cmbprovvend.clear()
        cmbprovcli.addItems(listaprov)
        cmbprovprop.addItems(listaprov)
        cmbprovvend.addItems(listaprov)

    def cargaMuniCli(self):
        listado = []
        provincia = var.ui.cmbProvCli.currentText()
        listado = conexion.Conexion.listaMuniprov(str(provincia))
        var.ui.cmbMuniCli.clear()
        var.ui.cmbMuniCli.addItems(listado)
    def cargaMuniProp(self):
        var.ui.cmbMuniprop.clear()
        listado = conexion.Conexion.listaMuniprov(var.ui.cmbProvprop.currentText())
        var.ui.cmbMuniprop.addItems(listado)
    def cargaMuniVend(self):
        var.var.ui.cmbMuniprop.clear()
        listado = conexion.Conexion.listaMuniprov(var.ui.cmbProvprop.currentText())
        var.ui.cmbMuniprop.addItems(listado)


    def validarDNIcli(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDniCli.setText(str(dni))
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    var.ui.txtDniCli.setStyleSheet('background-color:rgb(255,255,220);')
                    return True
                else:
                    var.ui.txtDniCli.setStyleSheet('background-color:#FFC0CB;')
                    var.ui.txtDniCli.setText(None)
                    var.ui.txtDniCli.setFocus()
            else:
                var.ui.txtDniCli.setStyleSheet('background-color:#FFC0CB;')
                var.ui.txtDniCli.setText(None)
                var.ui.txtDniCli.setFocus()

        except Exception as error:
            print("error en validar dni ", error)

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

    def abrirCalendar(btn):
        try:
            var.btn = btn
            var.uicalendar.show()
        except Exception as error:
            print("error en abrir calendar ", error)

    def cargaFecha(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if  var.btn == 0:
                var.ui.txtAltaCli.setText(str(data))
            elif  var.btn == 1:
                var.ui.txtBajaCli.setText(str(data))
            elif  var.btn == 2:
                var.ui.txtFechaprop.setText(str(data))
            elif var.btn == 3:
                var.ui.txtBajaprop.setText(str(data))
            elif var.btn == 4:
                var.ui.txtAltaVend.setText(str(data))
            elif var.btn == 5:
                var.ui.txtBajaVend.setText(str(data))
            time.sleep(0.125)
            var.uicalendar.hide()
            return data
        except Exception as error:
            print("error en cargar fecha: ", error)

    def validarMail(mail):
        mail = mail.lower()
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if re.match(regex, mail) or mail =="":

            return True
        else:
            return False
    def resizeTableClientes(self):
        try:
            header = var.ui.tabClientes.horizontalHeader()
            for i in range(header.count()):
                if i in (1, 2, 4,5):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_items = var.ui.tabClientes.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as error:
            print("error en resize table clientes ", error)

    def resizeTablaPropiedades(self):
        try:
            header = var.ui.tablaPropiedades.horizontalHeader()
            for i in range(header.count()):
                if (i == 1 or i == 2):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                header_items = var.ui.tablaPropiedades.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)
        except Exception as e:
            print("error en resize tabla propiedades: ", e)

    def crearBackup(self):
        try:
            copia = str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '_backup.zip'
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Guardar Copia Seguridad", copia, ".zip")
            if var.dlgabrir.accept and fichero:
                fichzip = zipfile.ZipFile(fichero, "w")
                fichzip.write("bbdd.sqlite", os.path.basename("bbdd.sqlite"), zipfile.ZIP_DEFLATED)
                fichzip.close()
                shutil.move(fichero, directorio)

                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Backup')
                mbox.setText('Backup Creado')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()

        except Exception as error:
            print("Error en crear backup: ", error)


        except Exception as error:
            print("Error en backupDB: ", error)

    def restaurarBackup(self):
        try:
            filename = var.dlgabrir.getOpenFileName(None, "Restaurat Copia Seguridad", "", "*.zip;;All Files(*)")
            file = filename[0]
            if file:
                with zipfile.ZipFile(file, "r") as bbdd:
                    bbdd.extractall(pwd=None)
                bbdd.close()

                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Backup')
                mbox.setText('Base de Datos Restaurada')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()

                conexion.Conexion.db_conexion(self)
                Eventos.cargarProv(self)
                clientes.Clientes.cargaTablaClientes(self)

        except Exception as e:
            print(e)


    def limpiarPanel(self):
        objetospanelcli = [var.ui.txtDniCli, var.ui.txtAltaCli,
                           var.ui.txtApelCli, var.ui.txtNomCli,
                           var.ui.txtEmailCli, var.ui.txtMovilCli,
                           var.ui.txtDirCli, var.ui.cmbProvCli, var.ui.cmbMuniCli,
                           var.ui.txtBajaCli]
        for i, dato in enumerate(objetospanelcli):
            if i == 7 or i == 8:
                pass
            else:
                dato.setText("")
        eventos.Eventos.cargarProv(self)
        var.ui.cmbMuniCli.clear()
        objetospanelprop = [var.ui.txtFechaprop, var.ui.txtBajaprop, var.ui.txtDirprop,
                            var.ui.txtSuperprop, var.ui.txtPrecioAlquilerprop,
                            var.ui.txtPrecioVentaprop, var.ui.txtCPprop, var.ui.txtDescriprop, var.ui.txtNomeprop,
                            var.ui.txtMovilprop]
        for i, dato in enumerate(objetospanelprop):
            dato.setText("")

        var.ui.cmbProvprop.clear()
        var.ui.cmbMuniprop.clear()
        var.ui.cmbTipoprop.clear()
        var.ui.spinHabprop.setValue(0)
        var.ui.spinBanosprop.setValue(0)
        var.ui.lblprop.setText("")
        if var.ui.chkAlquilerprop.isChecked():
            var.ui.chkAlquilerprop.setChecked(False)
        if var.ui.chkVentaprop.isChecked():
            var.ui.chkVentaprop.setChecked(False)
        if var.ui.chkIntercambioprop.isChecked():
            var.ui.chkIntercambioprop.setChecked(False)
        eventos.Eventos.cargarProv(self)
        eventos.Eventos.cargarTipoprop(self)

    def abrirTipoProp(self):
        try:
            var.dlgGestion.show()
        except Exception as error:
            print("Error en abrir tipo propiedades: ", error)

    def cargarTipoprop(self):
        try :
            registro = conexion.Conexion.cargarTipoProp(self)
            if registro:
                var.ui.cmbTipoprop.clear()
                var.ui.cmbTipoprop.addItems(registro)
        except Exception as error:
            print("Error en cargar tipo propiedad: ", error)

    def controlarBtnBuscar(self):
        var.ui.btnTipoProp.setChecked(not var.ui.btnTipoProp.isChecked())
        propiedades.Propiedades.cargaTablaPropiedades(self, 1)

    def exportCSVProp(self):
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = str(fecha + "DatosPropiedades.csv")
            directorio,fichero = var.dlgabrir.getSaveFileName(None,"Exporta Datos en CSV", file,'.csv')
            if fichero:
                historicoGuardar = var.historico
                var.historico = 0
                registros = conexion.Conexion.listadoPropiedades(self)
                var.historico = historicoGuardar
                with open(fichero,"w",newline="",encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Codigo","Alta","Baja","Direccion","Provincia","Municipio","Tipo"
                                     ,"Nº Habitaciones", "Nº Baños", "Superficie", "Precio Alquiler", "Precio Compra",
                                     "Codigo Postal", "Observaciones", "Operacion", "Estado", "Propietario", "Movil"])
                    for registro in registros:
                        writer.writerow(registro)
                shutil.move(fichero,directorio)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowIcon(QtGui.QIcon("./img/logo.ico"))
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
        historiaGuardart = var.historico
        var.historico = 0
        fecha = datetime.today()
        fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
        file = (str(fecha) + "_DatosPropiedades.json")
        directorio, fichero = var.dlgabrir.getSaveFileName(None, "Exporta Datos en JSON", file, '.json')
        if fichero :
            keys = ["Codigo", "Alta", "Baja", "Direccion", "Provincia", "Municipio", "Tipo","Nº Habitaciones",
                    "Nº Baños", "Superficie", "Precio Alquiler", "Precio Compra","Codigo Postal", "Observaciones",
                    "Operacion", "Estado", "Propietario", "Movil"]
            registros = conexion.Conexion.listadoPropiedades(self)
            var.historico = historiaGuardart
            lista_propiedades = [dict(zip(keys, registro)) for registro in registros]
            with open(fichero, "w",newline='', encoding="utf-8") as jsonfile:
                json.dump(lista_propiedades, jsonfile, ensure_ascii=False , indent=4)
            shutil.move(fichero, directorio)
        else:
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setWindowIcon(QtGui.QIcon("./img/logo.ico"))
            mbox.setWindowTitle('Error')
            mbox.setText('Error en la exportacion de json')
            mbox.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
            mbox.exec()
    def abrirAbout(self):
        try:
            var.dlgAbout.show()
        except Exception as error:
            print("Error en abrir about: ", error)
    def cerrarAbout(self):
        try:
            var.dlgAbout.hide()
        except Exception as error:
            print("Error en cerrar about: ", error)





