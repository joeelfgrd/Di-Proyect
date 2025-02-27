import os
from datetime import datetime, date

from PyQt6 import QtGui, QtSql, QtWidgets, QtCore

import var


class Conexion:

    @staticmethod
    def db_conexion():
        """
        :return:  operación exitosa
        :rtype: bolean

        Módulo para establecer la conexión con la base de datos.
        Si éxito devuelve true, en caso contrario devuelve false.
        """
        if not os.path.isfile('bbdd.sqlite'):
            QtWidgets.QMessageBox.critical(None, 'Error', 'El archivo de la base de datos no existe.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('bbdd.sqlite')

        if db.open():
            query = QtSql.QSqlQuery()
            query.exec("SELECT name FROM sqlite_master WHERE type='table';")

            if not query.next():  # Si no hay tablas
                QtWidgets.QMessageBox.critical(None, 'Error', 'Base de datos vacía o no válida.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
                return False
            else:
                QtWidgets.QMessageBox.information(None, 'Aviso', 'Conexión Base de Datos realizada',
                                                  QtWidgets.QMessageBox.StandardButton.Ok)
                return True
        else:
            QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo abrir la base de datos.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False

    '''
    ZONA LOCALIDADES
    '''

    @staticmethod
    def listaProv():
        """
        :return: lista provincias
        :rtype: bytearray

        Query que obtiene listado provincias en la base de datos.
        """
        listaprov = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")
        if query.exec():
            while query.next():
                listaprov.append(query.value(1))
        return listaprov

    @staticmethod
    def listaMunicipios(provincia):
        """
        :param provincia: nombre provincia
        :type provincia: str
        :return: lista municipios
        :rtype: list

        Query que obtiene listado municipios en la base de datos de una provincia concreta.
        """
        try:
            listamunicipios = []
            query = QtSql.QSqlQuery()
            query.prepare(
                "SELECT * FROM municipios where idprov = (select idprov from provincias where provincia = :provincia)")
            query.bindValue(":provincia", provincia)
            if query.exec():
                while query.next():
                    listamunicipios.append(query.value(1))
            return listamunicipios
        except Exception as e:
            print("error lista municipios", e)

    @staticmethod
    def listaTodosMunicipios():
        """
        :return: lista municipios
        :rtype: list

        Query que obtiene listado de todos los municipios en la base de datos.
        """
        try:
            listamunicipios = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM municipios")
            if query.exec():
                while query.next():
                    listamunicipios.append(query.value(1))
            return listamunicipios
        except Exception as e:
            print("error lista municipios", e)

    '''
    ZONA CLIENTES
    '''

    @staticmethod
    def altaCliente(nuevocli):
        """
        :param nuevocli: array con los datos del cliente
        :type nuevocli: list
        :return: operación exitosa
        :rtype: booleano

        Query que inserta un nuevo cliente en la base de datos.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "INSERT INTO CLIENTES (dnicli, altacli, apelcli, nomecli, emailcli, movilcli, dircli, provcli, municli) "
                "VALUES (:dnicli, :altacli, :apelcli, :nomecli, :emailcli, :movilcli, :dircli, :provcli, :municli)")
            query.bindValue(":dnicli", str(nuevocli[0]))
            query.bindValue(":altacli", str(nuevocli[1]))
            query.bindValue(":apelcli", str(nuevocli[2]))
            query.bindValue(":nomecli", str(nuevocli[3]))
            query.bindValue(":emailcli", str(nuevocli[4]))
            query.bindValue(":movilcli", str(nuevocli[5]))
            query.bindValue(":dircli", str(nuevocli[6]))
            query.bindValue(":provcli", str(nuevocli[7]))
            query.bindValue(":municli", str(nuevocli[8]))

            return query.exec()

        except Exception as e:
            print("error altaCliente en conexion", e)

    @staticmethod
    def listadoClientes():
        """
        :return: listado de clientes
        :rtype: list

        Query que obtiene listado de clientes en la base de datos.
        """
        try:
            listado = []

            numRows = var.rowsClientes

            offset = (numRows - 15) if numRows >= 15 else 0

            if var.historicoCli == 1:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM clientes ORDER BY apelcli, nomecli ASC LIMIT 15 OFFSET :offset")
                query.bindValue(":offset", offset)
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
            else:
                query = QtSql.QSqlQuery()
                query.prepare(
                    "SELECT * FROM clientes WHERE bajacli IS NULL ORDER BY apelcli, nomecli ASC LIMIT 15 OFFSET :offset")
                query.bindValue(":offset", offset)
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)

            if not listado:
                var.rowsClientes -= 15

            return listado
        except Exception as e:
            print("Error al listar clientes", e)

    @staticmethod
    def datosOneCliente(dni):
        """
        :param dni: dni del cliente
        :type dni: str
        :return: datos del cliente
        :rtype: list

        Query que obtiene los datos de un cliente en la base de datos a partir de un dni
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM CLIENTES WHERE dnicli = :dni")
            query.bindValue(":dni", dni)
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as e:
            print("error datosOneCliente en conexion", e)

    @staticmethod
    def modifCliente(registro):
        """
        :param registro: datos del cliente
        :type registro: list
        :return: operación exitosa
        :rtype: booleano

        Query que modifica los datos de un cliente en la base de datos.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from clientes where dnicli = :dni")
            query.bindValue(":dni", str(registro[0]))
            if query.exec():
                if query.next() and query.value(0) > 0:
                    if query.exec():
                        query = QtSql.QSqlQuery()
                        query.prepare(
                            "UPDATE clientes SET altacli = :altacli, apelcli = :apelcli, nomecli = :nomecli, emailcli = :emailcli, "
                            " movilcli = :movilcli, dircli = :dircli, provcli = :provcli, municli = :municli, bajacli = :bajacli WHERE dnicli = :dnicli")
                        query.bindValue(":dnicli", str(registro[0]))
                        query.bindValue(":altacli", str(registro[1]))
                        query.bindValue(":apelcli", str(registro[2]))
                        query.bindValue(":nomecli", str(registro[3]))
                        query.bindValue(":emailcli", str(registro[4]))
                        query.bindValue(":movilcli", str(registro[5]))
                        query.bindValue(":dircli", str(registro[6]))
                        query.bindValue(":provcli", str(registro[7]))
                        query.bindValue(":municli", str(registro[8]))
                        if registro[9] == "":
                            query.bindValue(":bajacli", QtCore.QVariant())
                        else:
                            query.bindValue(":bajacli", str(registro[9]))
                        return query.exec()
                    else:
                        return False
                else:
                    return False
        except Exception as error:
            print("error modificar cliente", error)

    @staticmethod
    def bajaCliente(datos):
        """
        :param datos: datos del cliente
        :type datos: list
        :return: operación exitosa
        :rtype: booleano

        Query que da de baja a un cliente en la base de datos.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE clientes SET bajacli = :bajacli WHERE dnicli = :dni")
            query.bindValue(":dni", str(datos[1]))
            query.bindValue(":bajacli", str(datos[0]))
            return query.exec()
        except Exception as e:
            print("error bajaCliente en conexion", e)

    '''
    ZONA PROPIEDADES
    '''

    @staticmethod
    def altaTipoPropiedad(tipo):
        """
        :param tipo: tipo de propiedad
        :type tipo: str
        :return: operación exitosa
        :rtype: booleano

        Query que da de alta un nuevo tipo de propiedad en la base de datos.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO tipoprop (tipo) VALUES (:tipo)")
            query.bindValue(":tipo", tipo)
            return query.exec()
        except Exception as error:
            print("Error en alta tipo propiedad: ", error)

    @staticmethod
    def bajaTipoPropiedad(tipo):
        """
        :param tipo: tipo de propiedad
        :type tipo: str
        :return: operación exitosa
        :rtype: booleano

        Query que borra un tipo de propiedad en la base de datos.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM tipoprop WHERE tipo = :tipo")
            query.bindValue(":tipo", tipo)
            return query.exec()
        except Exception as error:
            print("Error en baja tipo propiedad: ", error)

    @staticmethod
    def cargarTipoProp():
        """
        :return: tipos de propiedad
        :rtype: list

        Query que obtiene los tipos de propiedad de la base de datos.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT tipo FROM tipoprop")
            if query.exec():
                registro = []
                while query.next():
                    registro.append(str(query.value(0)))
                return registro
        except Exception as e:
            print("error cargarTipoProp en conexion", e)

    @staticmethod
    def altaPropiedad(propiedad):
        """
        :param propiedad: array con los datos de la propiedad
        :type propiedad: list
        :return: operación exitosa
        :rtype: booleano

        Query que da de alta una nueva propiedad en la base de datos.
        """
        try:
            campos_obligatorios = [propiedad[1], propiedad[2], propiedad[3], propiedad[4], propiedad[7], propiedad[10],
                                   propiedad[14], propiedad[15]]
            if any(not campo for campo in campos_obligatorios) or propiedad[15] == "telefono no válido":
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowTitle('Aviso')
                mbox.setText(
                    'Los campos Dirección, Provincia, Municipio, Tipo de Propiedad, Superficie, CP, Propietario y Teléfono son obligatorios y el teléfono no puede ser "telefono no válido".')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                return False

            query = QtSql.QSqlQuery()
            query.prepare(
                " INSERT into PROPIEDADES (altaprop, dirprop, provprop, muniprop, tipoprop, habprop, banprop, "
                " superprop, prealquiprop, prevenprop, cpprop, obserprop, tipooper, estadoprop, nomeprop, movilprop) "
                " VALUES (:altaprop, :dirprop, :provprop, :muniprop, :tipoprop, :habprop, :banprop, :superprop, "
                " :prealquiprop, :prevenprop, :cpprop, :obserprop, :tipooper, :estadoprop, :nomeprop, :movilprop)")
            query.bindValue(":altaprop", str(propiedad[0]))
            query.bindValue(":dirprop", str(propiedad[1]))
            query.bindValue(":provprop", str(propiedad[2]))
            query.bindValue(":muniprop", str(propiedad[3]))
            query.bindValue(":tipoprop", str(propiedad[4]))
            query.bindValue(":habprop", str(propiedad[5]))
            query.bindValue(":banprop", int(propiedad[6]))
            query.bindValue(":superprop", float(propiedad[7]))
            query.bindValue(":prealquiprop", float(propiedad[8]) if propiedad[8] else QtCore.QVariant())
            query.bindValue(":prevenprop", float(propiedad[9]) if propiedad[9] else QtCore.QVariant())
            query.bindValue(":cpprop", str(propiedad[10]))
            query.bindValue(":obserprop", str(propiedad[11]))
            query.bindValue(":tipooper", str(propiedad[12]))
            query.bindValue(":estadoprop", str(propiedad[13]))
            query.bindValue(":nomeprop", str(propiedad[14]))
            query.bindValue(":movilprop", str(propiedad[15]))
            return query.exec()

        except Exception as e:
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setWindowTitle('Aviso')
            mbox.setText('Error en dar de alta')
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
            mbox.exec()
            print("error altaPropiedad en conexion", e)

    @staticmethod
    def listadoPropiedades():
        """
        :return: listado de propiedades
        :rtype: list

        Query que obtiene listado de propiedades en la base de datos.
        """
        try:
            listado = []

            numRows = var.rowsPropiedades

            offset = (numRows - 11) if numRows >= 11 else 0

            if var.historicoProp == 1:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM propiedades ORDER BY muniprop ASC LIMIT 11 OFFSET :offset")
                query.bindValue(":offset", offset)
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
            else:
                query = QtSql.QSqlQuery()
                query.prepare(
                    "SELECT * FROM propiedades WHERE bajaprop IS NULL OR bajaprop = '' ORDER BY muniprop ASC LIMIT 11 OFFSET :offset")
                query.bindValue(":offset", offset)
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)

            if not listado:
                var.rowsPropiedades -= 11

            return listado

        except Exception as e:
            print("Error al abrir el archivo:", e)

    @staticmethod
    def datosOnePropiedad(codigo):
        """
        :param codigo: código de la propiedad
        :type codigo: str
        :return: datos de la propiedad
        :rtype: list

        Query que obtiene los datos de una propiedad en la base de datos.
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM PROPIEDADES WHERE codigo = :codigo")
            query.bindValue(":codigo", codigo)
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as e:
            print("error datosOnePropiedad en conexion", e)

    @staticmethod
    def modifPropiedades(registro):
        """
        :param registro: datos de la propiedad
        :type registro: list
        :return: operación exitosa
        :rtype: booleano

        Query que modifica los datos de una propiedad en la base de datos.
        """
        try:
            if registro[15] == "telefono no válido":
                return False

            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from propiedades where codigo = :codigo")
            query.bindValue(":codigo", str(registro[16]))
            if query.exec():
                if query.next() and query.value(0) > 0:
                    query = QtSql.QSqlQuery()
                    query.prepare(
                        "UPDATE propiedades SET altaprop = :altaprop, dirprop = :dirprop, provprop = :provprop, muniprop = :muniprop, "
                        "tipoprop = :tipoprop, habprop = :habprop, banprop = :banprop, superprop = :superprop, prealquiprop = :prealquiprop, "
                        "prevenprop = :prevenprop, cpprop = :cpprop, obserprop = :obserprop, tipooper = :tipooper, estadoprop = :estadoprop, "
                        "nomeprop = :nomeprop, movilprop = :movilprop, bajaprop = :bajaprop WHERE codigo = :codigo")
                    query.bindValue(":altaprop", str(registro[0]))
                    query.bindValue(":dirprop", str(registro[1]))
                    query.bindValue(":provprop", str(registro[2]))
                    query.bindValue(":muniprop", str(registro[3]))
                    query.bindValue(":tipoprop", str(registro[4]))
                    query.bindValue(":habprop", str(registro[5]))
                    query.bindValue(":banprop", int(registro[6]))
                    query.bindValue(":superprop", float(registro[7]))
                    query.bindValue(":prealquiprop", float(registro[8]) if registro[8] else QtCore.QVariant())
                    query.bindValue(":prevenprop", float(registro[9]) if registro[9] else QtCore.QVariant())
                    query.bindValue(":cpprop", str(registro[10]))
                    query.bindValue(":obserprop", str(registro[11]))
                    query.bindValue(":tipooper", str(registro[12]))
                    query.bindValue(":estadoprop", str(registro[13]))
                    query.bindValue(":nomeprop", str(registro[14]))
                    query.bindValue(":movilprop", str(registro[15]))
                    query.bindValue(":codigo", str(registro[16]))
                    query.bindValue(":bajaprop", QtCore.QVariant() if registro[17] == "" else str(registro[17]))
                    return query.exec()
                else:
                    return False
            else:
                return False
        except Exception as error:
            print("error modificar propiedad", error)

    @staticmethod
    def bajaPropiedad(datos):
        """
        :param datos: datos de la propiedad
        :type datos: list
        :return: operación exitosa
        :rtype: booleano

        Query que da de baja una propiedad en la base de datos.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE propiedades SET bajaprop = :bajaprop WHERE codigo = :codigo")
            query.bindValue(":codigo", str(datos[1]))
            query.bindValue(":bajaprop", str(datos[0]))
            return query.exec()
        except Exception as e:
            print("error bajaPropiedad en conexion", e)

    @staticmethod
    def listadoFiltrado(datos):
        """
        :param datos: datos
        :type datos: list
        :return: listado de propiedades
        :rtype: list

        Query que obtiene un listado de propiedades filtrado por tipo de propiedad y municipio.
        """
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM propiedades WHERE tipoprop = :tipoprop and muniprop = :muniprop")
            query.bindValue(":tipoprop", datos[0])
            query.bindValue(":muniprop", datos[1])
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("error listadoFiltrado en conexion", e)

    @staticmethod
    def cambiarEstadoPropiedad(idProp, estadoProp):
        """
        :param idProp: id de la propiedad
        :type idProp: int
        :param estadoProp: estado de la propiedad
        :type estadoProp: int
        :return: operación exitosa
        :rtype: booleano
        """
        try:
            nuevoEstado = ""
            fecha_hoy = date.today()
            fecha_formateada = fecha_hoy.strftime("%d/%m/%Y")
            query = QtSql.QSqlQuery()

            if estadoProp == 0:
                nuevoEstado = "Disponible"
                query.prepare(
                    "UPDATE propiedades SET estadoprop = :estadoprop, bajaprop = :bajaprop WHERE codigo = :codigo")
                query.bindValue(":codigo", idProp)
                query.bindValue(":bajaprop", "")
                query.bindValue(":estadoprop", nuevoEstado)
                return query.exec()
            elif estadoProp == 1:
                nuevoEstado = "Vendido"
            elif estadoProp == 2:
                nuevoEstado = "Alquilado"
            query.prepare(
                "UPDATE propiedades SET estadoprop = :estadoprop, bajaprop = :bajaprop WHERE codigo = :codigo")
            query.bindValue(":codigo", idProp)
            query.bindValue(":bajaprop", fecha_formateada)
            query.bindValue(":estadoprop", nuevoEstado)
            return query.exec()
        except Exception as e:
            print("error cambiarEstadoPropiedad en conexion", e)

    '''
    ZONA VENDEDORES
    '''

    @staticmethod
    def altaVendedor(nuevoVendedor):
        """
        :param nuevoVendedor: datos del vendedor
        :type nuevoVendedor: list
        :return: true o false
        :rtype: booleano

        Query que da de alta un nuevo vendedor en la base de datos.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "INSERT INTO VENDEDORES (dniVendedor, nombreVendedor, altaVendedor, movilVendedor, mailVendedor, delegacionVendedor) "
                "VALUES (:dniVend, :nombreVend, :altaVend, :movilVend, :mailVend, :delegacionVend)")
            query.bindValue(":dniVend", str(nuevoVendedor[0]))
            query.bindValue(":nombreVend", str(nuevoVendedor[1]))
            query.bindValue(":altaVend", str(nuevoVendedor[2]))
            query.bindValue(":movilVend", str(nuevoVendedor[3]))
            query.bindValue(":mailVend", str(nuevoVendedor[4]))
            query.bindValue(":delegacionVend", str(nuevoVendedor[5]))

            return query.exec()

        except Exception as e:
            print("error altaVendedor en conexion", e)

    @staticmethod
    def listadoVendedores():
        """
        :return: listado de vendedores
        :rtype: bytearray

        Query que obtiene un listado de vendedores en la base de datos con los distintos filtrados
        """
        try:
            listado = []

            # numRows = var.rowsVendedores

            # offset = (numRows - 10) if numRows >= 10 else 0

            if var.historicoVend == 1:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT idVendedo, nombreVendedor, movilVendedor, delegacionVendedor "
                              "FROM vendedores ORDER BY idVendedo ASC")
                # query.prepare("SELECT idVendedo, nombreVendedor, movilVendedor, delegacionVendedor "
                #              "FROM vendedores ORDER BY idVendedo ASC LIMIT 10 OFFSET :offset")
                # query.bindValue(":offeset", offset)
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
            else:
                query = QtSql.QSqlQuery()
                query.prepare(
                    "SELECT idVendedo, nombreVendedor, movilVendedor, delegacionVendedor "
                    "FROM vendedores WHERE bajaVendedor IS NULL or bajaVendedor = '' ORDER BY idVendedo ASC")
                # query.prepare(
                #    "SELECT idVendedo, nombreVendedor, movilVendedor, delegacionVendedor "
                #    "FROM vendedores WHERE bajaVendedor IS NULL or bajaVendedor = '' ORDER BY idVendedo ASC LIMIT 10 OFFSET :offset")
                # query.bindValue(":offeset", offset)
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)

            # if not listado:
            #   var.rowsVendedores -= 10

            return listado
        except Exception as e:
            print("Error al listar vendedores", e)

    @staticmethod
    def listadoVendedoresNormal():
        """
        :return: listado de vendedores
        :rtype: bytearray

        Query que obtiene un listado de vendedores en la base de datos.
        """
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare(
                "SELECT idVendedo, nombreVendedor, movilVendedor, delegacionVendedor, dniVendedor, altaVendedor, bajaVendedor, mailVendedor "
                "FROM vendedores ORDER BY idVendedo ASC")
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("Error al listar vendedores", e)

    @staticmethod
    def datosOneVendedor(idVendedor):
        """
        :param idVendedor: id del vendedor
        :type idVendedor: str
        :return: datos del vendedor
        :rtype: bytearray

        Query que obtiene los datos de un vendedor en la base de datos.
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM VENDEDORES WHERE idVendedo = :idVendedo")
            query.bindValue(":idVendedo", idVendedor)
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as e:
            print("error datosOneVendedor en conexion", e)

    @staticmethod
    def datosVendedoresByTelefono(telefono):
        """
        :param telefono: teléfono del vendedor
        :type telefono: str
        :return: datos del vendedor
        :rtype: bytearray

        Query que obtiene los datos de un vendedor en la base de datos a partir de un teléfono.
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare(
                "SELECT idVendedo, nombreVendedor, movilVendedor, delegacionVendedor FROM VENDEDORES WHERE movilVendedor = :movilVendedor")
            query.bindValue(":movilVendedor", str(telefono))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as e:
            print("error datosOneVendedor en conexion", e)

    @staticmethod
    def modifVendedor(registro):
        """
        :param registro: datos del vendedor
        :type registro: list
        :return: operacion exitosa
        :rtype: booleano

        Query que modifica los datos de un vendedor en la base de datos.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "UPDATE vendedores SET nombreVendedor = :nombreVendedor, altaVendedor = :altaVendedor, movilVendedor = :movilVendedor, "
                " mailVendedor = :mailVendedor, delegacionVendedor = :delegacionVendedor, bajaVendedor = :bajaVendedor WHERE idVendedo = :idVendedo")
            query.bindValue(":idVendedo", str(registro[0]))
            query.bindValue(":nombreVendedor", str(registro[1]))
            query.bindValue(":altaVendedor", str(registro[2]))
            query.bindValue(":movilVendedor", str(registro[3]))
            query.bindValue(":mailVendedor", str(registro[4]))
            query.bindValue(":delegacionVendedor", str(registro[5]))
            query.bindValue(":bajaVendedor", str(registro[6]))
            return query.exec()

        except Exception as error:
            print("error modificar cliente", error)
            return False

    @staticmethod
    def bajaVendedor(id, fecha):
        """
        :param id: id del vendedor
        :type id: str
        :param fecha: fecha de baja del vendedor
        :type fecha: date
        :return: operacion exitosa
        :rtype: booleano

        Query que da de baja a un vendedor en la base de datos.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE vendedores SET bajaVendedor = :bajaVendedor WHERE idVendedo = :idVendedo")
            query.bindValue(":idVendedo", id)
            query.bindValue(":bajaVendedor", fecha)
            return query.exec()
        except Exception as e:
            print("error bajaVendedor en conexion", e)

    '''
    ZONA FACTURACIÓN
    '''

    @staticmethod
    def guardarFactura(nuevaFactura):
        """
        :param nuevaFactura: datos de la factura a grabar
        :type nuevaFactura: list
        :return: operación exitosa
        :rtype: booleano

        Query que inserta una nueva factura en la base de datos
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "INSERT INTO FACTURAS (fechafac, dnifac) "
                "VALUES (:fechafac, :dnifac)")
            query.bindValue(":fechafac", str(nuevaFactura[0]))
            query.bindValue(":dnifac", str(nuevaFactura[1]))
            return query.exec()

        except Exception as e:
            print("error altaFactura en conexion", e)

    @staticmethod
    def listadoFacturas():
        """
        :return: listado de las facturas
        :rtype: list

        Query que obtiene un listado de todas las facturas en la base de datos
        """
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM facturas ORDER BY id ASC")
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("error listadoFacturas en conexion", e)

    @staticmethod
    def deleteFactura(id):
        """
        :param id: id de la factura a borrar
        :type id: int
        :return: operación exitosa
        :rtype: boolean

        Query que borra una factura de la base de datos a partir de la id
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("Delete from facturas where id = :id")
            query.bindValue(":id", str(id))
            return query.exec()
        except Exception as error:
            print("Error al eliminar la factura", error)

    @staticmethod
    def getLastIdFactura():
        """
        :return: id de la última factura guardada
        :rtype: int

        Query que obtiene el id de la última factura guardada en la base de datos
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select id from facturas order by id desc")
            if query.exec() and query.next():
                return query.value(0)
            else:
                print(query.lastError().text())
        except Exception as exec:
            print("Error al guardar la factura", exec)

    @staticmethod
    def grabarVenta(nuevaVenta):
        """
        :param nuevaVenta: datos de la venta a grabar
        :type nuevaVenta: list
        :return: operación exitosa
        :rtype: boolean

        Query que inserta una nueva venta en la base de datos
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO VENTAS (facventa, codprop, agente) "
                          "VALUES (:factura, :propiedad, :vendedor)")
            query.bindValue(":factura", str(nuevaVenta[0]))
            query.bindValue(":propiedad", str(nuevaVenta[2]))
            query.bindValue(":vendedor", str(nuevaVenta[1]))
            return query.exec()
        except Exception as exec:
            print("Error al guardar la venta", exec)

    @staticmethod
    def cargarTablaVentas(idFactura):
        """
        :param idFactura: id de la factura
        :type idFactura: int
        :return: lista de ventas de la factura
        :rtype: list

        Query que recupera la información de todas las ventas cuya factura es
        la identificada por el id pasado por parámetro
        """
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare(
                "select v.idventa, v.codprop, p.dirprop, p.muniprop, p.tipoprop, p.prevenprop "
                "from ventas as v inner join propiedades as p on v.codprop = p.codigo "
                "where v.facventa = :idFactura")
            query.bindValue(":idFactura", idFactura)
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as error:
            print("Error al recuperar el listado de ventas")

    @staticmethod
    def obtenerTotalFactura(idFactura):
        """
        :param idFactura: id de la factura
        :type idFactura: int
        :return: total de la factura
        :rtype: float

        Query que recupera el total de la factura identificada por el id pasado por parámetro
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "select sum(p.prevenprop) "
                "from ventas as v inner join propiedades as p on v.codprop = p.codigo "
                "where v.facventa = :idFactura")
            query.bindValue(":idFactura", idFactura)
            if query.exec() and query.next():
                return query.value(0)
            else:
                return 0
        except Exception as error:
            print("Error al recuperar el total de la factura", error)

    @staticmethod
    def checkFacturaTieneVenta(idFactura):
        """
        :param idFactura: id de la factura
        :type idFactura: int
        :return: comprobar si tiene o no ventas
        :rtype: boolean

        Query que comprueba si una factura tiene ventas asociadas
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from ventas where facventa = :idFactura")
            query.bindValue(":idFactura", idFactura)
            if query.exec() and query.next():
                return query.value(0) > 0
            else:
                return False
        except Exception as error:
            print("Error al comprobar si la factura tiene ventas", error)

    @staticmethod
    def deleteVenta(idVenta):
        """
        :param idVenta: id de la venta
        :type idVenta: int
        :return: operación exitosa
        :rtype: boolean

        Query que borra una venta de la base de datos a partir de la id
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("Delete from ventas where idventa = :idVenta")
            query.bindValue(":idVenta", idVenta)
            return query.exec()
        except Exception as error:
            print("Error al eliminar la venta", error)

    @staticmethod
    def datosOneFactura(id):
        """
        :param id: id de la factura
        :type id: int
        :return: datos de la factura
        :rtype: list

        Función que recupera una lista con los datos de la factura cuyo id es el pasado por parámetros
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM facturas where id = :id")
            query.bindValue(":id", str(id))
            if query.exec() and query.next():
                registro = [query.value(i) for i in range(query.record().count())]
            return registro
        except Exception as error:
            print("Error al abrir el archivo")

    '''
    ZONA ALQUILERES
    '''

    @staticmethod
    def grabarContrato(infoContrato):
        """
        :param infoContrato: información del contrato a subir en la bbdd
        :type infoContrato: list
        :return: operación exitosa
        :rtype: boolean
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "INSERT INTO ALQUILERES (idPropiedad, clienteDNI, idAgente, fechaInicio, fechaFin, precioAlquiler) "
                "VALUES (:idPropiedad, :clienteDNI, :idAgente, :fechaInicio, :fechaFin, :precioAlquiler)")
            query.bindValue(":idPropiedad", str(infoContrato[0]))
            query.bindValue(":clienteDNI", str(infoContrato[1]))
            query.bindValue(":idAgente", str(infoContrato[2]))
            query.bindValue(":fechaInicio", str(infoContrato[3]))
            query.bindValue(":fechaFin", str(infoContrato[4]))
            query.bindValue(":precioAlquiler", str(Conexion.datosOnePropiedad(infoContrato[0])[10]))
            return query.exec()
        except Exception as exec:
            print("Error al guardar el contrato", exec)

    @staticmethod
    def listadoAlquileres():
        """
        Función que recupera un listado de todos los alquileres de la base de datos
        """
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare("select id, clienteDNI from alquileres")
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as error:
            print("Error al recuperar el listado de ventas")

    @staticmethod
    def borrarContrato(idFactura):
        """
        :param idFactura: id de la factura a borrar
        :type idFactura: int
        :return: operación exitosa
        :rtype: boolean

        Función que borra un contrato de la base de datos a partir de su id
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "DELETE FROM ALQUILERES WHERE id = :idFactura")
            query.bindValue(":idFactura", str(idFactura))
            return query.exec()
        except Exception as exec:
            print("Error al guardar el contrato", exec)

    @staticmethod
    def datosOneContrato(id):
        """
        :param id: id del contrato
        :type id: int
        :return: datos del contrato
        :rtype: list

        Query que recupera los datos de un contrato a partir de su id
        """
        try:
            registro = []
            var.ui.chkHistoricoMensualidades.setEnabled(True)
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM ALQUILERES where id = :id")
            query.bindValue(":id", str(id))
            if query.exec() and query.next():
                registro = [query.value(i) for i in range(query.record().count())]
            return registro
        except Exception as error:
            print("Error al abrir el archivo" + error)

    @staticmethod
    def grabarMensualidadesContrato(fecha, idContrato):
        """
        :param fecha: fecha del mes de esa mensualidad
        :type fecha: str
        :param idContrato: id del contrato
        :type idContrato: int
        :return: operación exitosa
        :rtype: boolean

        Query que inserta una nueva mensualidad en la base de datos
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO MENSUALIDADES (idAlquiler, mes, pagado) "
                          "VALUES (:idAlquiler, :fecha, :pagado)")
            query.bindValue(":idAlquiler", idContrato)
            query.bindValue(":fecha", fecha)
            query.bindValue(":pagado", 0)
            if not query.exec():
                print("Error SQL:", query.lastError().text())  # <-- Esto muestra el error real
                return False
            return True
        except Exception as exec:
            print("Error al guardar las mensualidades del contrato", exec)

    @staticmethod
    def borrarMensualidadesContrato(idContrato):
        """
        :param idContrato: id del contrato
        :type idContrato: int
        :return: operación exitosa
        :rtype: boolean

        Query que borra las mensualidades de un contrato a partir de su id
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "DELETE FROM MENSUALIDADES WHERE idAlquiler = :idContrato")
            query.bindValue(":idContrato", str(idContrato))
            return query.exec()
        except Exception as exec:
            print("Error al borrar las mensualidades del contrato", exec)

    @staticmethod
    def listadoMensualidadesAlquiler(id):
        """
        :param id: id del contrato
        :type id: int
        :return: listado de mensualidades del contrato
        :rtype: list

        Query que recupera las mensualidades de un contrato a partir de su id
        """
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare(
                "select idmensualidad, idalquiler, mes, pagado from mensualidades where idalquiler = :idalquiler")
            query.bindValue(":idalquiler", id)
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            else:
                print("Error en listadoMensualidadesAlquiler" + query.lastError().text())
            return listado
        except Exception as error:
            print("Error al recuperar el listado de mensualidades")

    @staticmethod
    def setMensualidadPagada(codigo, pagado):
        """
        :param codigo: codigo de la mensualidad
        :type codigo: int
        :param pagado: si está pagado o no
        :type pagado: boolean
        :return: operación exitosa
        :rtype: boolean

        Query que marca una mensualidad como pagada o no pagada
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("update mensualidades set pagado = :pagado where idmensualidad = :codigo")
            query.bindValue(":codigo", codigo)
            query.bindValue(":pagado", 1 if pagado else 0)
            if query.exec():
                QtSql.QSqlDatabase.database().commit()
                return True
            else:
                print("Error en setMensualidad pagada" + query.lastError().text())
                return False
        except Exception as error:
            print("Error al marcar la mensualidad como pagada", error)

    @staticmethod
    def obtenerUltimoContrato():
        """
        :return: id del último contrato
        :rtype: int

        Query que recupera el id del último contrato guardado en la base de datos
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select id from alquileres order by id desc limit 1")
            if query.exec() and query.next():
                return query.value(0)
            else:
                return 0
        except Exception as error:
            print("Error al recuperar el último contrato", error)

    @staticmethod
    def listadoMensualidadesSinPagar(id):
        """
        :param id: id del contrato
        :type id: int
        :return: listado de mensualidades del contrato
        :rtype: list

        Query que recupera las mensualidades no pagadas de un contrato a partir de su id
        """
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare(
                "SELECT idmensualidad, idalquiler, mes, pagado FROM mensualidades WHERE idalquiler = :idalquiler AND pagado = 0")
            query.bindValue(":idalquiler", id)
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            else:
                print("Error en listadoMensualidadesSinPagar:", query.lastError().text())
            return listado
        except Exception as error:
            print("Error al recuperar el listado de mensualidades sin pagar:", error)
            return []

    @staticmethod
    def datosOneMensualidad(idMensaulidad):
        """
        :param idMensaulidad: id de la mensualidad
        :type idMensaulidad: str
        :return: datos de la mensualidad a buscar
        :rtype: list

        Función que devuelve los datos de una mensualidad a partir de su id
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM MENSUALIDADES WHERE idmensualidad = :idmensualidad")
            query.bindValue(":idmensualidad", idMensaulidad)
            if query.exec() and query.next():
                registro = [query.value(i) for i in range(query.record().count())]
            return registro
        except Exception as error:
            print("Error al obtener mensualidad por id: ", error)
            return []