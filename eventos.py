import sys
import re
import zipfile
import shutil
from PyQt6 import QtWidgets, QtSql

import clientes
import conexion
import eventos
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
        cmbprovcli.clear()
        cmbprovprop.clear()
        cmbprovcli.addItems(listaprov)
        cmbprovprop.addItems(listaprov)

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
        try:
            if var.ui.panPrincipal.currentIndex() == 0:
                listado = [var.ui.txtDniCli, var.ui.txtAltaCli,
                           var.ui.txtApelCli, var.ui.txtNomCli,
                           var.ui.txtEmailCli, var.ui.txtMovilCli,
                           var.ui.txtDirCli, var.ui.cmbProvCli, var.ui.cmbMuniCli,
                           var.ui.txtBajaCli]

                for i, dato in enumerate(listado):
                    if i in (7, 8):
                        pass
                    dato.setText('')

                Eventos.cargarProv(self)
                var.ui.cmbMuniCli.clear()

        except Exception as error:
            print("Error en limpiar panel: ", error)
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




