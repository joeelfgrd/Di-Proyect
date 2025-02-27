from datetime import datetime
from PyQt6 import QtWidgets, QtGui, QtCore

import conexion
import conexionserver
import eventos
import var


class Clientes:

    @staticmethod
    def checkDNI(dni):
        """
        :param dni: dni del cliente
        :type dni: str

        Función que se encarga de comprobar si un dni es correcto y cambiar el color del texto en caso de que sea inválido
        """
        try:
            dni = str(dni).upper()
            var.ui.txtDnicli.setText(str(dni))
            check = eventos.Eventos.validarDNIcli(dni)
            if check:
                var.ui.txtDnicli.setStyleSheet('background-color:rgb(255,255,220);')
            else:
                var.ui.txtDnicli.setStyleSheet('background-color:#FFC0CB;')
                var.ui.txtDnicli.setText(None)
                var.ui.txtDnicli.setText("dni no válido")
                var.ui.txtDnicli.setFocus()
        except Exception as e:
            print("error en check cliente ", e)

    @staticmethod
    def altaCliente():
        """
        Función que se encarga de dar de alta un cliente en la base de datos
        """

        try:
            nuevoCli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text(),
                        var.ui.txtNomcli.text(), var.ui.txtEmailcli.text(), var.ui.txtMovilcli.text(),
                        var.ui.txtDireccioncli.text(), var.ui.cmbProvinciacli.currentText(),
                        var.ui.cmbMunicipiocli.currentText()]

            mensajes_error = [
                "Falta ingresar DNI",
                "Falta ingresar fecha de alta",
                "Falta ingresar apellido",
                "Falta ingresar nombre",
                None,
                "Falta ingresar móvil",
                "Falta ingresar dirección",
                "Falta seleccionar provincia",
                "Falta seleccionar municipio"
            ]

            for i, dato in enumerate(nuevoCli):
                if i == 4:  # Saltamos la validación para el email (índice 4)
                    continue
                if dato == "telefono no válido":
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setWindowTitle("Error en los datos")
                    mbox.setText("El teléfono no es válido.")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.exec()
                    return
                if dato == "dni no válido":
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setWindowTitle("Error en los datos")
                    mbox.setText("El dni no es válido")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.exec()
                    return
                if dato == '':
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setWindowTitle("Error en los datos")
                    mbox.setText(mensajes_error[i])
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.exec()
                    return

            try:
                if conexion.Conexion.altaCliente(nuevoCli):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowTitle("Aviso")
                    mbox.setText("Se ha insertado el cliente correctamente.")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()
                    Clientes.cargaTablaClientes()
            except Exception as e:
                print(e)
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText('Error al insertar el cliente. Intente nuevamente.')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()

        except Exception as e:
            print("error altaCliente", e)


    @staticmethod
    def checkEmail(mail):
        """
        :param mail: email del cliente
        :type mail: string

        Función que comprueba si un email es válido o no, cambiando el color de la caja de texto en caso de que sea incorrecto
        """
        try:
            mail = str(var.ui.txtEmailcli.text())
            if eventos.Eventos.validarMail(mail):
                var.ui.txtEmailcli.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtEmailcli.setText(mail.lower())

            else:
                var.ui.txtEmailcli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtEmailcli.setText(None)
                var.ui.txtEmailcli.setText("correo no válido")
                var.ui.txtEmailcli.setFocus()

        except Exception as error:
            print("error check cliente", error)

    @staticmethod
    def checkTelefono(telefono):
        """
        :param telefono: teléfono del cliente
        :type telefono: str

        Función que comprueba si un teléfono es válido o no, cambiando el color de la caja de texto en caso de que sea incorrecto
        """
        try:
            telefono = str(var.ui.txtMovilcli.text())
            if eventos.Eventos.validarTelefono(telefono):
                var.ui.txtMovilcli.setStyleSheet('background-color: rgb(255, 252, 220);')
            else:
                var.ui.txtMovilcli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtMovilcli.setText(None)
                var.ui.txtMovilcli.setText("telefono no válido")
                var.ui.txtMovilcli.setFocus()
        except Exception as error:
            print("error check cliente", error)

    @staticmethod
    def cargaTablaClientes():
        """
        Función que carga la tabla de clientes, implementando la función de avanzar entre páginas
        """
        try:
            listado = conexion.Conexion.listadoClientes()
            if listado is None:
                listado = []
            index = 0
            for registro in listado:
                var.ui.tablaClientes.setRowCount(index + 1)
                var.ui.tablaClientes.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[2])))
                var.ui.tablaClientes.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[3])))
                var.ui.tablaClientes.setItem(index, 3, QtWidgets.QTableWidgetItem("    " + str(registro[5]) + "    "))
                var.ui.tablaClientes.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[7])))
                var.ui.tablaClientes.setItem(index, 5, QtWidgets.QTableWidgetItem(str(registro[8])))
                var.ui.tablaClientes.setItem(index, 6, QtWidgets.QTableWidgetItem(str(registro[9])))
                var.ui.tablaClientes.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaClientes.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaClientes.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                index += 1

            if var.rowsClientes == 15:
                var.ui.btnAnteriorCli.setEnabled(False)
            else:
                var.ui.btnAnteriorCli.setEnabled(True)

            if len(listado) < 15:
                var.ui.btnSiguienteCli.setEnabled(False)
            else:
                var.ui.btnSiguienteCli.setEnabled(True)

        except Exception as e:
            print("error cargaTablaClientes", e)

    @staticmethod
    def cargaOneCliente():
        """
        Función que carga los datos del cliente en pantalla al seleccionar uno en la tabla
        """
        try:
            fila = var.ui.tablaClientes.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = conexion.Conexion.datosOneCliente(str(datos[0]))
            listado = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli, var.ui.txtNomcli, var.ui.txtEmailcli,
                       var.ui.txtMovilcli, var.ui.txtDireccioncli, var.ui.cmbProvinciacli, var.ui.cmbMunicipiocli, var.ui.txtBajacli]
            for i in range(len(listado)):
                if i in (7,8):
                    listado[i].setCurrentText(registro[i])
                else:
                    listado[i].setText(registro[i])
            var.ui.txtDniFactura.setText(registro[0])
            var.ui.txtDniClienteContrato.setText(registro[0])
        except Exception as e:
            print("error cargaOneCliente en clientes", e)

    @staticmethod
    def modifCliente():
        """
        Función que modifica los datos de un cliente y valida que todos los campos sean correctos. En caso de que la operación falle por cualquier
        motivo mandará un mensaje especificando el error
        """
        try:
            modifCli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text(),
                        var.ui.txtNomcli.text(), var.ui.txtEmailcli.text(), var.ui.txtMovilcli.text(),
                        var.ui.txtDireccioncli.text(), var.ui.cmbProvinciacli.currentText(),
                        var.ui.cmbMunicipiocli.currentText(), var.ui.txtBajacli.text()]

            print(modifCli)

            mensajes_error = [
                "Falta ingresar DNI",
                "Falta ingresar fecha de alta",
                "Falta ingresar apellido",
                "Falta ingresar nombre",
                None,
                None,
                "Falta ingresar móvil",
                "Falta ingresar dirección",
                "Falta seleccionar provincia",
                "Falta seleccionar municipio"
            ]

            for i, dato in enumerate(modifCli):
                if i == 4:  # Saltamos la validación para el email (índice 4)
                    continue
                if dato == '' and i != 5 and i != 9:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setWindowTitle("Error en los datos")
                    mbox.setText(mensajes_error[i])
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.exec()
                    return
                if dato == "telefono no válido":
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setWindowTitle("Error en los datos")
                    mbox.setText("El teléfono no es válido.")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.exec()
                    return

            if conexion.Conexion.modifCliente(modifCli):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/icono.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText('Datos del cliente modificados')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Clientes.cargaTablaClientes()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('./img/icono.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText('Error en actualizacion Datos del cliente')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
        except Exception as e:
            print("error modifCliente en clientes", e)

    @staticmethod
    def bajaCliente():
        """
        Función que da de baja a un cliente a partir del dni que esté seleccionado en la interfaz. Si la operación
        falla o funciona mandará un mensaje informativo
        """
        try:
            if var.ui.txtBajacli.text() == '':
                eventos.Eventos.crearMensajeError("Error", "Falta escribir el DNI del cliente")
                return
            now = datetime.now()
            formatted_date = now.strftime("%d/%m/%Y")
            var.ui.txtBajacli.setText(formatted_date)
            datos = [formatted_date, var.ui.txtDnicli.text()] #CAMBIADO
            if conexion.Conexion.bajaCliente(datos):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/icono.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText('Cliente dado de baja')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('./img/icono.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText('Error en dar de baja al cliente')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
            Clientes.cargaTablaClientes()
        except Exception as e:
            print("error bajaCliente en clientes", e)

    @staticmethod
    def historicoCli():
        """
        Función que gestiona el botón de histórico y el cambio de páginas
        """
        try:
            if var.ui.chkHistoriacli.isChecked():
                var.historicoCli = 1
            else:
                var.historicoCli = 0
            var.rowsClientes = 15
            Clientes.cargaTablaClientes()
        except Exception as e:
            print("checkbox historico error ", e)

    @staticmethod
    def cargaClienteDni():
        """
        Función que carga un cliente a partir de su dni, si lo encuentra carga sus datos y si no lo encuentra
        salta un mensaje emergente diciendo que no se encontró
        """
        try:
            dni = var.ui.txtDnicli.text()
            registro = conexion.Conexion.datosOneCliente(dni)
            if not registro:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Aviso")
                mbox.setText("No se ha encontrado el cliente")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                return

            listado = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli,
                        var.ui.txtNomcli, var.ui.txtEmailcli, var.ui.txtMovilcli,
                        var.ui.txtDireccioncli, var.ui.cmbProvinciacli,
                        var.ui.cmbMunicipiocli, var.ui.txtBajacli]

            for i, casilla in enumerate(listado):
                if isinstance(casilla, QtWidgets.QComboBox):
                    casilla.setCurrentText(registro[i])
                else:
                    casilla.setText(registro[i])

        except Exception as e:
            print("Error cargar Clientes por dni", e)