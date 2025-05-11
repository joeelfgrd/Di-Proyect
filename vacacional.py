from datetime import datetime

from PyQt6 import QtWidgets, QtCore
import conexion
import eventos
import informes
import propiedades
import var

class Vacacional:

    @staticmethod
    def grabarAlquiler():
        try:
            id_prop = var.ui.lblCodigoPropVacacional.text()
            dni_cliente = var.ui.txtDniFactura.text()
            fecha_inicio = var.ui.txtFechaInicioVacacional.text()
            fecha_fin = var.ui.txtFechaFinVacacional.text()
            precio_dia = var.ui.txtPrecioVacacional.text().replace("€", "").replace(",", ".").strip()
            gastos_limpieza = var.ui.txtGastosLimpiezaVacacional.text().replace("€", "").replace(",", ".").strip()
            id_agente = var.ui.txtVendedorVacacional.text()

            if not (id_prop and dni_cliente and fecha_inicio and fecha_fin and precio_dia and id_agente):
                eventos.Eventos.crearMensajeError("Error", "Todos los campos obligatorios deben estar cubiertos")
                return

            if not conexion.Conexion.propiedadDisponibleParaVacacional(id_prop):
                eventos.Eventos.crearMensajeError("Error", "La propiedad no está disponible para alquiler vacacional")
                return

            dias = Vacacional.calcularDias(fecha_inicio, fecha_fin)
            subtotal = dias * float(precio_dia) + float(gastos_limpieza or 0.0)
            precio_total = round(subtotal * 1.21, 2)  # Incluye IVA

            info = [
                id_prop,
                dni_cliente,
                fecha_inicio,
                fecha_fin,
                float(precio_dia),
                float(gastos_limpieza or 0.0),
                var.ui.chkWifi.isChecked(),
                var.ui.chkCocina.isChecked(),
                var.ui.chkTV.isChecked(),
                id_agente,
                precio_total,
                dias
            ]

            if conexion.Conexion.grabarAlquilerVacacional(info):
                conexion.Conexion.cambiarEstadoPropiedad(id_prop, 2)
                eventos.Eventos.crearMensajeInfo("Correcto", "El alquiler vacacional se ha registrado correctamente")
                Vacacional.cargarTablaVacacional()
                Vacacional.limpiarFormulario()
            else:
                eventos.Eventos.crearMensajeError("Error", "No se pudo guardar el alquiler")

        except Exception as e:
            print("Error al grabar alquiler vacacional:", e)

    @staticmethod
    def calcularDias(fecha_ini, fecha_fin):
        try:
            fmt = "%d/%m/%Y"
            f1 = datetime.strptime(fecha_ini, fmt)
            f2 = datetime.strptime(fecha_fin, fmt)
            return (f2 - f1).days
        except Exception:
            return -1

    @staticmethod
    def limpiarFormulario():
        campos = [
            var.ui.lblCodigoPropVacacional, var.ui.txtTipoPropVacacional, var.ui.txtPrecioVacacional,
            var.ui.txtDireccionPropVacacional, var.ui.txtLocalidadVacacional,
            var.ui.txtApelClieVacacional, var.ui.txtNomCliVacacional,
            var.ui.txtVendedorVacacional, var.ui.txtFechaInicioVacacional,
            var.ui.txtFechaFinVacacional, var.ui.txtGastosLimpiezaVacacional
        ]
        for campo in campos:
            campo.setText("")

        var.ui.chkWifi.setChecked(False)
        var.ui.chkCocina.setChecked(False)
        var.ui.chkTV.setChecked(False)

    @staticmethod
    def cargarClienteDesdeFactura():
        try:
            dni = var.ui.txtDniFactura.text()
            cliente = conexion.Conexion.datosOneCliente(dni)
            if cliente:
                var.ui.txtApelClieVacacional.setText(cliente[2])
                var.ui.txtNomCliVacacional.setText(cliente[3])
        except Exception as e:
            print("Error al cargar cliente en vacacional:", e)

    @staticmethod
    def cargarPropiedadVacacional():
        try:
            fila = var.ui.tablaPropiedades.selectedItems()
            if not fila or len(fila) < 1:
                return

            id_prop = fila[0].text()
            datos = conexion.Conexion.datosOnePropiedad(id_prop)
            if not datos:
                return

            var.ui.lblCodigoPropVacacional.setText(str(datos[0]))
            var.ui.txtTipoPropVacacional.setText(str(datos[7]))

            precio_mensual = datos[10]
            if precio_mensual:
                precio_dia = round(float(precio_mensual) / 30, 2)
                var.ui.txtPrecioVacacional.setText(f"{precio_dia:.2f}")
            else:
                var.ui.txtPrecioVacacional.setText("")

            var.ui.txtDireccionPropVacacional.setText(str(datos[4]))
            var.ui.txtLocalidadVacacional.setText(str(datos[6]))

        except Exception as e:
            print("Error al cargar propiedad vacacional:", e)

    @staticmethod
    def cargarTablaVacacional():
        try:
            offset = var.rowsVacacional - 10 if var.rowsVacacional >= 10 else 0
            datos = conexion.Conexion.cargarTablaVacacional(offset)
            var.ui.tablaVacacional.setRowCount(0)

            for index, fila in enumerate(datos):
                var.ui.tablaVacacional.setRowCount(index + 1)
                for col in range(5):
                    item = QtWidgets.QTableWidgetItem(str(fila[col]))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaVacacional.setItem(index, col, item)

            var.ui.btnAnteriorVacacional.setEnabled(var.rowsVacacional > 10)
            var.ui.btnSiguienteVacacional.setEnabled(len(datos) == 10)

        except Exception as e:
            print("Error al cargar tabla vacacional:", e)

    @staticmethod
    def paginarVacacional(avance):
        try:
            if avance == 0 and var.rowsVacacional >= 10:
                var.rowsVacacional -= 10
            elif avance == 1:
                var.rowsVacacional += 10
            Vacacional.cargarTablaVacacional()
        except Exception as e:
            print("Error en paginación vacacional:", e)

    @staticmethod
    def cargarOneAlquilerVacacional():
        try:
            fila = var.ui.tablaVacacional.selectedItems()
            if not fila or len(fila) < 1:
                return

            id_alquiler = fila[0].text()
            datos = conexion.Conexion.datosOneAlquilerVacacional(id_alquiler)

            if not datos:
                return

            var.ui.lblCodigoPropVacacional.setText(str(datos["idPropiedad"]))
            var.ui.txtFechaInicioVacacional.setText(str(datos["fechaEntrada"]))
            var.ui.txtFechaFinVacacional.setText(str(datos["fechaSalida"]))
            var.ui.txtPrecioVacacional.setText(str(datos["precioDia"]))
            var.ui.txtGastosLimpiezaVacacional.setText(str(datos["gastosLimpieza"]))
            var.ui.chkWifi.setChecked(bool(datos["wifi"]))
            var.ui.chkCocina.setChecked(bool(datos["cocina"]))
            var.ui.chkTV.setChecked(bool(datos["tv"]))
            var.ui.txtDniFactura.setText(str(datos["dniCliente"]))
            var.ui.txtVendedorVacacional.setText(str(datos["idAgente"]))
            var.ui.txtApelClieVacacional.setText(str(datos["apelcli"]))
            var.ui.txtNomCliVacacional.setText(str(datos["nomecli"]))

            propiedad = conexion.Conexion.datosOnePropiedad(datos["idPropiedad"])
            if propiedad:
                var.ui.txtTipoPropVacacional.setText(str(propiedad[7]))
                var.ui.txtDireccionPropVacacional.setText(str(propiedad[4]))
                var.ui.txtLocalidadVacacional.setText(str(propiedad[6]))

        except Exception as e:
            print("Error al cargar datos de alquiler vacacional:", e)

    @staticmethod
    def generarFacturaVacacional():
        try:
            fila = var.ui.tablaVacacional.currentRow()
            if fila == -1:
                eventos.Eventos.crearMensajeError("Error", "Debes seleccionar un alquiler vacacional")
                return

            id_alquiler = var.ui.tablaVacacional.item(fila, 0).text()
            datos = conexion.Conexion.datosAlquilerVacacional(id_alquiler)
            if not datos:
                eventos.Eventos.crearMensajeError("Error", "No se pudo recuperar la información del alquiler")
                return

            subtotal = float(datos['precio_total'])
            iva = subtotal * 0.21
            total = subtotal + iva

            factura = {
                'id': datos['id'],
                'cliente': datos['cliente'],
                'dni': datos['dni'],
                'direccion': datos['direccion'],
                'propiedad': datos['propiedad'],
                'fechaEntrada': datos['fechaEntrada'],
                'fechaSalida': datos['fechaSalida'],
                'dias': datos['dias'],
                'precioDia': datos['precioDia'],
                'gastosLimpieza': datos['gastosLimpieza'],
                'extras': datos['extras'],
                'subtotal': subtotal,
                'iva': iva,
                'total': total
            }

            informes.Informes.reportFacturaVacacional(factura)

        except Exception as e:
            print("Error al generar factura vacacional:", e)






