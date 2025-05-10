import traceback

from PyQt6 import QtSql
from reportlab.pdfgen import canvas
from datetime import datetime
from PIL import Image
import os

import conexion
import var


class Informes:
    @staticmethod
    def reportClientes():
        """
        Función que genera un informe en PDF con el listado de clientes
        """
        try:
            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            fecha = datetime.today()
            fecha = fecha.strftime("%Y_%m_%d_%H_%M_%S")
            nomepdfcli = fecha + "_listadoclientes.pdf"
            pdf_path = os.path.join(rootPath, nomepdfcli)
            var.report = canvas.Canvas(pdf_path)
            titulo = "Listado Clientes"
            Informes.topInforme(titulo)

            # Calculate total pages

            paginas = 0
            query0 = QtSql.QSqlQuery()
            query0.exec("select count(*) from clientes")
            if (query0.next()):
                registros = int(query0.value(0))
                paginas = int(registros / 20)
            Informes.footInforme(titulo, paginas)
            items = ['DNI', 'APELLIDOS', 'NOMBRE', 'MOVIL', 'PROVINCIA', 'MUNICIPIO']
            var.report.setFont('Helvetica-Bold', size=10)
            var.report.drawString(55, 650, str(items[0]))  # DNI
            var.report.drawString(100, 650, str(items[1]))  # APELLIDOS
            var.report.drawString(190, 650, str(items[2]))  # NOMBRE
            var.report.drawString(280, 650, str(items[3]))  # MOVIL
            var.report.drawString(360, 650, str(items[4]))  # PROVINCIA
            var.report.drawString(450, 650, str(items[5]))  # MUNICIPIO
            var.report.line(50, 645, 525, 645)
            query0.prepare("SELECT dniCli, apelCli, nomeCli, movilCli, provCli, muniCli from clientes order by apelCli")
            if query0.exec():
                x = 60
                y = 630
                while query0.next():
                    if y <= 90:
                        var.report.setFont('Helvetica-Oblique', size=8)  # HELVETICA OBLIQUE PARA LA FUENTE ITALIC
                        var.report.drawString(450, 80, 'Página siguiente...')
                        var.report.showPage()  # CREAMOS UNA PAGINA NUEVA
                        Informes.topInforme(titulo)
                        Informes.footInforme(titulo, paginas)
                        items = ['DNI', 'APELLIDOS', 'NOMBRE', 'MOVIL', 'PROVINCIA', 'MUNICIPIO']
                        var.report.setFont('Helvetica-Bold', size=10)
                        var.report.drawString(55, 650, str(items[0]))  # DNI
                        var.report.drawString(100, 650, str(items[1]))  # APELLIDOS
                        var.report.drawString(190, 650, str(items[2]))  # NOMBRE
                        var.report.drawString(280, 650, str(items[3]))  # MOVIL
                        var.report.drawString(360, 650, str(items[4]))  # PROVINCIA
                        var.report.drawString(450, 650, str(items[5]))  # MUNICIPIO
                        var.report.line(50, 645, 525, 645)
                        x = 60
                        y = 630

                    var.report.setFont('Helvetica', size=8)
                    dni = '****' + str(query0.value(0)[4:7] + '****')
                    var.report.drawCentredString(x + 5, y, str(dni))  # DNI
                    var.report.drawString(x + 40, y, str(query0.value(1)))  # APELLIDOS
                    var.report.drawString(x + 130, y, str(query0.value(2)))  # NOMBRE
                    var.report.drawString(x + 220, y, str(query0.value(3)))  # MOVIL
                    var.report.drawString(x + 310, y, str(query0.value(4)))  # PROVINCIA
                    var.report.drawString(x + 390, y, str(query0.value(5)))  # MUNICIPIO
                    y = y - 25.

            var.report.save()
            for file in os.listdir(rootPath):
                if file.endswith(nomepdfcli):
                    os.startfile(pdf_path)
        except Exception as error:
            print(error)

    def reportPropiedades(localidad):
        """
        :param localidad: localidad de dónde se va a sacar el informe
        :type localidad: str

        Función que genera un informe en PDF con el listado de propiedades a partir de una determinada localidad
        """
        try:
            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            fecha = datetime.today()
            fecha = fecha.strftime("%Y_%m_%d_%H_%M_%S")
            nomepdfProp = fecha + "_listadopropiedades.pdf"
            pdf_path = os.path.join(rootPath, nomepdfProp)
            var.report = canvas.Canvas(pdf_path)
            titulo = "Listado Propiedades de " + str(localidad)
            Informes.topInforme(titulo)

            # Calculate total pages

            paginas = 1
            query0 = QtSql.QSqlQuery()
            query0.exec("select count(*) from propiedades where muniProp = :localidad")
            query0.bindValue(':localidad', localidad)
            if (query0.next()):
                registros = int(query0.value(0))
                paginas = int(registros / 20)
            Informes.footInforme(titulo, paginas)
            items = ['CODIGO', 'DIRECCION', 'TIPO', 'OPERACION', 'VENTA €', 'ALQUILER €']
            var.report.setFont('Helvetica-Bold', size=10)
            var.report.drawString(55, 650, str(items[0]))  # CODIGO
            var.report.drawString(110, 650, str(items[1]))  # DIRECCION
            var.report.drawString(260, 650, str(items[2]))  # TIPO
            var.report.drawString(310, 650, str(items[3]))  # TIPO OPERACION
            var.report.drawString(415, 650, str(items[4]))  # PRECIO VENTA
            var.report.drawString(470, 650, str(items[5]))  # PRECIO ALQUILER
            var.report.line(50, 645, 525, 645)
            query0.prepare(
                "SELECT codigo, dirprop, tipoprop, tipooper, prevenprop, prealquiprop from propiedades where muniProp = :localidad order by codigo")
            query0.bindValue(':localidad', localidad)
            if query0.exec():
                x = 60
                y = 630
                while query0.next():
                    if y <= 90:
                        var.report.setFont('Helvetica-Oblique', size=8)  # HELVETICA OBLIQUE PARA LA FUENTE ITALIC
                        var.report.drawString(450, 80, 'Página siguiente...')
                        var.report.showPage()  # CREAMOS UNA PAGINA NUEVA
                        Informes.topInforme(titulo)
                        Informes.footInforme(titulo, paginas)
                        items = ['CODIGO', 'DIRECCION', 'TIPO', 'OPERACION', 'VENTA €', 'ALQUILER €']
                        var.report.setFont('Helvetica-Bold', size=10)
                        var.report.drawString(55, 650, str(items[0]))  # CODIGO
                        var.report.drawString(120, 650, str(items[1]))  # DIRECCION
                        var.report.drawString(250, 650, str(items[2]))  # TIPO
                        var.report.drawString(325, 650, str(items[3]))  # TIPO OPERACION
                        var.report.drawString(405, 650, str(items[4]))  # PRECIO VENTA
                        var.report.drawString(475, 650, str(items[5]))  # PRECIO ALQUILER
                        var.report.line(50, 645, 525, 645)
                        x = 60
                        y = 630

                    var.report.setFont('Helvetica', size=8)
                    dni = str(query0.value(0))
                    var.report.drawCentredString(x + 5, y, str(dni))  # CODIGO
                    var.report.drawString(x + 60, y, str(query0.value(1)))  # DIRECCION
                    var.report.drawString(x + 205, y, str(query0.value(2)))  # TIPO
                    var.report.drawString(x + 250, y, str(query0.value(3)))  # TIPO OPERACION
                    var.report.drawString(x + 370, y, str(query0.value(4)))  # PRECIO VENTA
                    var.report.drawString(x + 420, y, str(query0.value(5)))  # PRECIO ALQUILER
                    y = y - 25.

            var.report.save()
            for file in os.listdir(rootPath):
                if file.endswith(nomepdfProp):
                    os.startfile(pdf_path)
        except Exception as error:
            print(error)

    @staticmethod
    def reportVentas(id):
        """
        Genera un informe PDF para la factura especificada con totales bien alineados.
        """
        try:
            import os
            from datetime import datetime
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas

            rootPath = ".\\informes"
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)

            fecha = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            nomepdfventas = fecha + "_listadoventas.pdf"
            pdf_path = os.path.join(rootPath, nomepdfventas)

            var.report = canvas.Canvas(pdf_path, pagesize=A4)
            titulo = "Factura Código " + id
            listado_ventas = conexion.Conexion.cargarTablaVentas(id)
            Informes.topInforme(titulo)
            Informes.footInforme(titulo, 1)

            # Cliente
            cliente = conexion.Conexion.datosOneCliente(conexion.Conexion.datosOneFactura(id)[2])
            Informes.topDatosClienteFactura(cliente)

            # Encabezado
            items = ["Venta", "Código", "Dirección", "Localidad", "Tipo", "Precio"]
            x_positions = [55, 100, 160, 320, 420, 490]
            var.report.setFont("Helvetica-Bold", size=10)
            for i, item in enumerate(items):
                var.report.drawString(x_positions[i], 650, item)
            var.report.line(50, 645, 525, 645)


            # Cuerpo
            y = 630
            subtotal = 0.0
            descuento_total = 0.0

            var.report.setFont("Helvetica", size=8)
            for registro in listado_ventas:
                venta_id = registro[0]
                codigo = registro[1]
                direccion = registro[2].title()
                localidad = registro[3]
                tipo = registro[4].title()
                precio = float(registro[5])
                descuento_pct = float(registro[6]) if registro[6] else 0.0
                descuento = precio * descuento_pct / 100

                subtotal += precio
                descuento_total += descuento

                fila = [venta_id, codigo, direccion, localidad, tipo, f"{precio:,.2f} €"]
                for i, valor in enumerate(fila):
                    var.report.drawString(x_positions[i], y, str(valor))
                y -= 20

            # Totales bien alineados a la derecha
            x_label = 450
            x_valor = 520
            y -= 420
            subtotal_con_dto = subtotal - descuento_total
            impuestos = subtotal_con_dto * 0.10
            comisiones = subtotal_con_dto * 0.10
            total = subtotal_con_dto + impuestos + comisiones

            var.report.setFont("Helvetica-Bold", size=9)
            var.report.drawRightString(x_label, y, "Subtotal (sin descuentos):")
            var.report.drawRightString(x_valor, y, f"{subtotal:,.2f} €")
            y -= 20
            var.report.drawRightString(x_label, y, f"Subtotal (descuento aplicado: {descuento_total:,.2f} €):")
            var.report.drawRightString(x_valor, y, f"{subtotal_con_dto:,.2f} €")
            y -= 20
            var.report.drawRightString(x_label, y, "Impuestos (10%):")
            var.report.drawRightString(x_valor, y, f"{impuestos:,.2f} €")
            y -= 20
            var.report.drawRightString(x_label, y, "Comisiones (10%):")
            var.report.drawRightString(x_valor, y, f"{comisiones:,.2f} €")
            y -= 20
            var.report.drawRightString(x_label, y, "Total factura:")
            var.report.drawRightString(x_valor, y, f"{total:,.2f} €")

            var.report.save()

            for file in os.listdir(rootPath):
                if file.endswith(nomepdfventas):
                    os.startfile(pdf_path)

        except Exception as error:
            print("Error en reportVentas:", error)
            traceback.print_exc()

    @staticmethod
    def reportMensualidad(mensualidad):
        """
        :param mensualidad: id de la mensualidad
        :type mensualidad: str

        Función que genera un informe en PDF con el recibo de la mensualidad
        """
        xid = 55
        xmes = xid + 70
        xdireccion = xmes + 70
        xlocalidad = xdireccion + 120
        xtipo = xlocalidad + 100
        try:
            rootPath = ".\\informes"
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            mes = mensualidad[2]
            anno = mensualidad[3]
            nomepdfcli = "alquiler_" + str(mensualidad[1]) + "_recibo_" + str(mes) + str(anno) + ".pdf"
            pdf_path = os.path.join(rootPath, nomepdfcli)
            print(pdf_path)
            var.report = canvas.Canvas(pdf_path)
            titulo = "Mensualidad"
            alquiler = conexion.Conexion.datosOneContrato(mensualidad[1])
            cliente = conexion.Conexion.datosOneCliente(alquiler[2])
            propiedad = conexion.Conexion.datosOnePropiedad(alquiler[1])
            Informes.topInforme(titulo)
            Informes.topDatosClienteMensualidad(cliente, "")
            Informes.footInforme(titulo, 1)
            var.report.setFont('Helvetica', size=9)
            var.report.drawString(55, 600, 'Propiedad: ' + str(propiedad[0]))
            var.report.drawString(55, 580, 'Dirección: ' + str(propiedad[3]))
            var.report.drawString(55, 560, 'Localidad: ' + str(propiedad[5]))
            var.report.drawString(55, 540, 'Provincia: ' + str(propiedad[4]))
            var.report.drawString(355, 600, 'Fecha Mensualidad: ' + "1-" + str(mes) + "-" + str(anno))
            var.report.drawString(355, 580, 'Contrato : ' + str(alquiler[0]))
            var.report.drawString(355, 560, 'Recibo : ' + str(mensualidad[0]))
            var.report.drawString(355, 540, 'Precio Alquiler: ' + str(propiedad[11]) + " €")
            estado = "pagado" if mensualidad[4] else "no pagado"
            var.report.drawString(355, 520, 'Estado: ' + estado)
            var.report.drawString(355, 500, 'Metodo de pago: ' + str(alquiler[7]))

            var.report.save()

            for file in os.listdir(rootPath):
                if file.endswith(nomepdfcli):
                    os.startfile(pdf_path)

        except Exception as error:
            print("Error al general el recibo de la mensualidad" + str(error))

    @staticmethod
    def topInforme(titulo):
        """
        :param titulo: titulo del informe
        :type titulo: str

        Función que genera la cabecera del informe
        """
        try:
            ruta_logo = '.\\img\\icono.png'
            logo = Image.open(ruta_logo)

            if isinstance(logo, Image.Image):
                var.report.line(50, 800, 525, 800)
                var.report.setFont('Helvetica-Bold', size=14)
                var.report.drawString(55, 785, 'Inmobiliaria Teis')
                var.report.drawCentredString(297.5, 670, titulo)  # Título centrado
                var.report.line(50, 665, 525, 665)

                var.report.drawImage(ruta_logo, 480, 725, width=40, height=40)

                var.report.setFont('Helvetica', size=9)
                var.report.drawString(55, 770, 'CIF: A12345678')
                var.report.drawString(55, 755, 'Avda. Galicia - 101')
                var.report.drawString(55, 740, 'Vigo - 36216 - España')
                var.report.drawString(55, 725, 'Teléfono: 986 132 456')
                var.report.drawString(55, 710, 'e-mail: joelteisinmo@mail.com')
            else:
                print(f'Error: No se pudo cargar la imagen en {ruta_logo}')
        except Exception as error:
            print('Error en cabecera informe:', error)

    @staticmethod
    def footInforme(titulo, totalPaginas):
        """
        :param titulo: titulo del informe
        :type titulo: str
        :param totalPaginas: número total de páginas
        :type totalPaginas: int

        Función que genera el pie del informe
        """
        try:
            total_pages = totalPaginas
            var.report.line(50, 50, 525, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d-%m-%Y %H:%M:%S')
            var.report.setFont('Helvetica-Oblique', size=7)
            var.report.drawString(50, 40, str(fecha))
            var.report.drawString(250, 40, str(titulo))
            var.report.drawString(490, 40, f'Página {var.report.getPageNumber()} / {total_pages}')
        except Exception as error:
            print('Error en pie informe de cualquier tipo: ', error)

    @staticmethod
    def topDatosClienteFactura(cliente):
        """
        :param cliente: id del cliente
        :type cliente: str

        Función que genera la cabecera del informe de factura con el cliente
        """
        try:
            var.report.setFont('Helvetica', size=9)
            var.report.drawString(55, 770, 'CIF: A12345678')
            var.report.drawString(55, 755, 'Avda. Galicia - 101')
            var.report.drawString(55, 740, 'Vigo - 36216 - España')
            var.report.drawString(55, 725, 'Teléfono: 986 132 456')
            var.report.drawString(55, 710, 'e-mail: joelteisinmo@mail.com')
            var.report.drawString(55, 695, 'Cliente: ' + cliente[2])
        except Exception as error:
            print('Error en cabecera informe facturas :', error)

    @staticmethod
    def topDatosClienteMensualidad(cliente, fecha):
        try:
            var.report.setFont('Helvetica-Bold', size=8)
            var.report.drawString(300, 770, 'DNI Cliente:')
            var.report.drawString(300, 752, 'Nombre:')
            var.report.drawString(300, 734, 'Dirección:')
            var.report.drawString(300, 716, 'Localidad:')

            var.report.setFont('Helvetica', size=8)
            var.report.drawString(360, 770, cliente[0])
            var.report.drawString(360, 752, cliente[3] + " " + cliente[2])
            var.report.drawString(360, 734, cliente[6])
            var.report.drawString(360, 716, cliente[8])
            if fecha:
                var.report.drawString(55, 682, "Fecha Factura:")
                var.report.drawString(120, 682, fecha)
        except Exception as error:
            print('Error en cabecera informe mensualidad :', error)

    @staticmethod
    def reportComisionesVendedores():
        """
        Función que genera un informe en PDF con las comisiones acumuladas por cada agente vendedor.
        """
        try:
            from reportlab.pdfgen import canvas
            import os
            from datetime import datetime

            rootPath = ".\\informes"
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)

            fecha = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            nomepdf = f"{fecha}_comisiones_vendedores.pdf"
            pdf_path = os.path.join(rootPath, nomepdf)

            var.report = canvas.Canvas(pdf_path)
            titulo = "Informe de Comisiones por Vendedor"

            # Cabecera y pie
            Informes.topInforme(titulo)
            Informes.footInforme(titulo, 1)

            # Encabezado de tabla
            var.report.setFont("Helvetica-Bold", 10)
            var.report.drawString(55, 650, "ID")
            var.report.drawString(100, 650, "Nombre")
            var.report.drawString(280, 650, "Móvil")
            var.report.drawString(400, 650, "Comisiones (€)")
            var.report.line(50, 645, 525, 645)

            # Contenido
            listado = conexion.Conexion.comisionesPorVendedor()
            var.report.setFont("Helvetica", 9)

            y = 630
            for fila in listado:
                if y <= 90:
                    var.report.drawString(450, 80, 'Página siguiente...')
                    var.report.showPage()
                    Informes.topInforme(titulo)
                    Informes.footInforme(titulo, 1)
                    var.report.setFont("Helvetica-Bold", 10)
                    var.report.drawString(55, 650, "ID")
                    var.report.drawString(100, 650, "Nombre")
                    var.report.drawString(280, 650, "Móvil")
                    var.report.drawString(400, 650, "Comisiones (€)")
                    var.report.line(50, 645, 525, 645)
                    var.report.setFont("Helvetica", 9)
                    y = 630

                var.report.drawString(55, y, str(fila[0]))
                var.report.drawString(100, y, str(fila[1]))
                var.report.drawString(280, y, str(fila[2]))
                var.report.drawRightString(490, y, f"{float(fila[3]):,.2f} €")
                y -= 20

            var.report.save()

            for file in os.listdir(rootPath):
                if file.endswith(nomepdf):
                    os.startfile(pdf_path)

        except Exception as e:
            print("Error al generar informe de comisiones por vendedor:", e)

    @staticmethod
    def reportPropiedadesAlquiladas():
        """
        Genera un informe PDF con las propiedades alquiladas incluyendo:
        código propiedad, nombre del inquilino, fecha de contrato y mensualidad.
        """
        try:
            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)

            fecha = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            nomepdf = f"{fecha}_propiedades_alquiladas.pdf"
            pdf_path = os.path.join(rootPath, nomepdf)

            var.report = canvas.Canvas(pdf_path)
            titulo = "Listado de Propiedades Alquiladas"
            Informes.topInforme(titulo)
            Informes.footInforme(titulo, 1)

            # Cabecera de tabla
            var.report.setFont('Helvetica-Bold', size=10)
            y = 650
            var.report.drawString(55, y, "Código")
            var.report.drawString(120, y, "Inquilino")
            var.report.drawString(280, y, "Fecha Contrato")
            var.report.drawString(400, y, "Mensualidad (€)")
            var.report.line(50, y - 5, 525, y - 5)

            # Contenido
            listado = conexion.Conexion.listadoPropiedadesAlquiladas()
            y -= 25
            var.report.setFont('Helvetica', size=9)

            for fila in listado:
                if y < 90:
                    var.report.showPage()
                    Informes.topInforme(titulo)
                    Informes.footInforme(titulo, 1)
                    y = 650
                    var.report.setFont('Helvetica-Bold', size=10)
                    var.report.drawString(55, y, "Código")
                    var.report.drawString(120, y, "Inquilino")
                    var.report.drawString(280, y, "Fecha Contrato")
                    var.report.drawString(400, y, "Mensualidad (€)")
                    var.report.line(50, y - 5, 525, y - 5)
                    y -= 25
                    var.report.setFont('Helvetica', size=9)

                var.report.drawString(55, y, str(fila[0]))
                var.report.drawString(120, y, str(fila[1]))
                var.report.drawString(280, y, str(fila[2]))
                var.report.drawRightString(480, y, f"{float(fila[3]):,.2f} €")
                y -= 20

            var.report.save()

            for file in os.listdir(rootPath):
                if file.endswith(nomepdf):
                    os.startfile(pdf_path)

        except Exception as e:
            print("Error al generar informe de propiedades alquiladas:", e)

    @staticmethod
    def reportPropiedadesVendidas():
        """
        Genera un informe PDF con el listado de propiedades vendidas,
        incluyendo: código, comprador, vendedor, fecha de venta y precio.
        """
        try:
            from datetime import datetime
            import os

            rootPath = ".\\informes"
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)

            fecha = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            nombre_pdf = f"{fecha}_propiedades_vendidas.pdf"
            pdf_path = os.path.join(rootPath, nombre_pdf)

            var.report = canvas.Canvas(pdf_path)
            titulo = "Listado de Propiedades Vendidas"
            Informes.topInforme(titulo)
            Informes.footInforme(titulo, 1)

            var.report.setFont("Helvetica-Bold", 10)
            var.report.drawString(55, 650, "Código")
            var.report.drawString(110, 650, "Comprador")
            var.report.drawString(260, 650, "Vendedor")
            var.report.drawString(400, 650, "Fecha Venta")
            var.report.drawString(480, 650, "Precio (€)")
            var.report.line(50, 645, 525, 645)


            y = 630
            listado = conexion.Conexion.listadoPropiedadesVendidas()
            var.report.setFont("Helvetica", 9)

            for fila in listado:
                if y <= 80:
                    var.report.showPage()
                    Informes.topInforme(titulo)
                    Informes.footInforme(titulo, 1)
                    var.report.setFont("Helvetica-Bold", 10)
                    var.report.drawString(55, 650, "Código")
                    var.report.drawString(110, 650, "Comprador")
                    var.report.drawString(260, 650, "Vendedor")
                    var.report.drawString(400, 650, "Fecha Venta")
                    var.report.drawString(480, 650, "Precio (€)")
                    var.report.line(50, 645, 525, 645)

                    y = 630
                    var.report.setFont("Helvetica", 9)

                var.report.drawString(55, y, str(fila[0]))
                var.report.drawString(110, y, str(fila[1]))
                var.report.drawString(260, y, str(fila[2]))
                var.report.drawString(400, y, str(fila[3]))
                var.report.drawRightString(540, y, f"{float(fila[4]):,.2f} €")
                y -= 20

            var.report.save()

            for file in os.listdir(rootPath):
                if file.endswith(nombre_pdf):
                    os.startfile(pdf_path)

        except Exception as error:
            print("Error al generar informe de propiedades vendidas:", error)
