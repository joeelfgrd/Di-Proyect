from PyQt6.uic.Compiler.qtproxies import QtWidgets, QtCore

import conexion
import eventos
import var


class Facturas:

    def altaVenta(self):
        try:
            nuevafactura = [var.ui.txtFechaFactura.text(), var.ui.txtDniVentas.text()]
            if (conexion.Conexion.altaFactura(nuevafactura)):
                eventos.Eventos.crearMensajeInfo("Aviso", "Factura Guardada")
                Facturas.mostrarTablaFacturas(self)
            else:
                eventos.Eventos.crearMensajeInfo("Aviso", "Error al guardar la factura")
        except Exception as error:
            print('Error altaVenta: %s' % str(error))

    def mostrarTablaFacturas(self):
        try:
            index = 0
            registros = conexion.Conexion.listadoFacturas(self)
            for registro in registros:
                var.ui.tablaVentas.setRowCount(index + 1)
                var.ui.tablaVentas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaVentas.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                var.ui.tablaVentas.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
                var.ui.tablaVentas.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                var.ui.tablaVentas.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[2])))
                var.ui.tablaVentas.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                #btn borrar
        except Exception as error:
            print('Error mostrarTablaFacturas: %s' % str(error))