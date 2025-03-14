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
        :param id: id de la factura
        :type id: str

        Función que genera un informe en PDF con el listado de ventas a partir de una determinada factura
        """
        xidventa = 55
        xidpropiedad = xidventa + 50
        xdireccion = xidpropiedad + 80
        xlocalidad = xdireccion + 150
        xtipo = xlocalidad + 100
        xprecio = xtipo + 50
        ymax = 630
        ymin = 90
        ystep = 30
        try:
            rootPath = ".\\informes"
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            fecha = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            nomepdfventas = fecha + "_listadoventas.pdf"
            pdf_path = os.path.join(rootPath, nomepdfventas)
            print(pdf_path)
            var.report = canvas.Canvas(pdf_path)
            titulo = "Factura Código " + id
            listado_ventas = conexion.Conexion.cargarTablaVentas(id)
            Informes.topInforme(titulo)
            Informes.footInforme(titulo, 1)
            items = ["Venta", "Código", "Direccion", "Localidad", "Tipo", "Precio"]
            var.report.setFont("Helvetica-Bold", size=10)
            var.report.drawString(xidventa, 650, str(items[0]))
            var.report.drawString(xidpropiedad, 650, str(items[1]))
            var.report.drawString(xdireccion, 650, str(items[2]))
            var.report.drawString(xlocalidad, 650, str(items[3]))
            var.report.drawString(xtipo, 650, str(items[4]))
            var.report.drawString(xprecio, 650, str(items[5]))
            var.report.line(50, 645, 525, 645)
            cliente = conexion.Conexion.datosOneCliente(conexion.Conexion.datosOneFactura(id)[2])
            Informes.topDatosClienteFactura(cliente)
            y = ymax
            for registro in listado_ventas:
                var.report.setFont("Helvetica", size=8)
                var.report.drawCentredString(xidventa + 10, y, str(registro[0]))
                var.report.drawCentredString(xidpropiedad + 15, y, str(registro[1]).title())
                var.report.drawString(xdireccion, y, str(registro[2]).title())
                var.report.drawString(xlocalidad, y, str(registro[3]).title())
                var.report.drawString(xtipo, y, str(registro[4]).title())
                var.report.drawCentredString(xprecio + 15, y, str(registro[5]).title() + " €")
                y -= ystep

            xmenuinferior = 400
            xtotal = 450
            y = 180
            subtotal = conexion.Conexion.obtenerTotalFactura(id)
            iva = 10 * subtotal / 100
            total = subtotal + iva
            var.report.drawString(xmenuinferior, y, "Subtotal")
            var.report.drawString(xtotal, y, f"{subtotal:,.2f}" + " €")
            y -= ystep
            var.report.drawString(xmenuinferior, y, "Impuestos")
            var.report.drawString(xtotal, y, f"{iva:,.2f}" + " €")
            y -= ystep
            var.report.drawString(xmenuinferior, y, "Total")
            var.report.drawString(xtotal, y, f"{total:,.2f}" + " €")
            y -= ystep

            var.report.save()

            for file in os.listdir(rootPath):
                if file.endswith(nomepdfventas):
                    os.startfile(pdf_path)

        except Exception as error:
            print(error)
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
            var.report.drawString(55, 510, 'Metodo de pago: ' + str(alquiler[7]))

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

            # Asegúrate de que el objeto 'logo' sea de tipo 'PngImageFile'
            if isinstance(logo, Image.Image):
                var.report.line(50, 800, 525, 800)
                var.report.setFont('Helvetica-Bold', size=14)
                var.report.drawString(55, 785, 'Inmobiliaria Teis')
                var.report.drawString(230, 670, titulo)
                var.report.line(50, 665, 525, 665)

                # Dibuja la imagen en el informe
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