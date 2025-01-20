import os
from PyQt6 import QtGui, QtSql, QtWidgets, QtCore
from PyQt6.uic.properties import QtGui

import var


class Conexion:

    @staticmethod
    def db_conexion(self):
        """

        :param self: None
        :type self: None
        :return:  False or True
        :rtype: Booleano

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

    @staticmethod
    def listaProv(self):
        """

        :param self: None
        :type self: None
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
        :rtype: bytearray

        Query que obtiene listado municipios en la base de datos de una provincia concreta.

        """
        try:
            listamunicipios = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM municipios where idprov = (select idprov from provincias where provincia = :provincia)")
            query.bindValue(":provincia", provincia)
            if query.exec():
                while query.next():
                    listamunicipios.append(query.value(1))
            return listamunicipios
        except Exception as e:
            print("error lista municipios", e)

    @staticmethod
    def listaTodosMunicipios(self):
        """

        :param self: None
        :type self: None
        :return: lista municipios
        :rtype: bytearray

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

    @staticmethod
    def altaCliente(nuevocli):
        """

        :param nuevocli: array con los datos del cliente
        :type nuevocli: list
        :return: true o false
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

            if query.exec():
                return True
            else:
                return False

        except Exception as e:
            print("error altaCliente en conexion", e)

    @staticmethod
    def listadoClientes(self):
        """

        :param self: None
        :type self: None
        :return: listado de clientes
        :rtype: bytearray

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
        :rtype: bytearray

        Query que obtiene los datos de un cliente en la base de datos.
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
        :return: true o false
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
        :return: true o false
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

    @staticmethod
    def altaTipoPropiedad(tipo):
        """

        :param tipo: tipo de propiedad
        :type tipo: str
        :return: true o false
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
        :return: true o false
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
            query.prepare(" INSERT into PROPIEDADES (altaprop, dirprop, provprop, muniprop, tipoprop, habprop, banprop, "
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
    def listadoPropiedades(self):
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
                    "SELECT * FROM propiedades WHERE bajaprop IS NULL ORDER BY muniprop ASC LIMIT 11 OFFSET :offset")
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
    def altaVendedor(nuevoVendedor):
        try:
            print("hello")
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

            if query.exec():
                return True
            else:
                return False

        except Exception as e:
            print("error altaVendedor en conexion", e)

    @staticmethod
    def listadoVendedores(self):
        try:
            listado = []

            if var.historicoVend == 1:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT idVendedo, nombreVendedor, movilVendedor, delegacionVendedor "
                              "FROM vendedores ORDER BY idVendedo ASC")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
            else:
                query = QtSql.QSqlQuery()
                query.prepare(
                    "SELECT idVendedo, nombreVendedor, movilVendedor, delegacionVendedor "
                              "FROM vendedores WHERE bajaVendedor IS NULL or bajaVendedor = '' ORDER BY idVendedo ASC")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
            return listado
        except Exception as e:
            print("Error al listar vendedores", e)

    @staticmethod
    def listadoDatosVendedores(self):
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT idVendedo, nombreVendedor, movilVendedor, delegacionVendedor, dniVendedor, altaVendedor, bajaVendedor, mailVendedor "
                          "FROM vendedores ORDER BY idVendedo ASC")
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("Error al listar vendedores", e)

    @staticmethod
    def datosOneVendedor(self, idVendedor):
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
    def datosVendedoresByTelefono(self, telefono):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT idVendedo, nombreVendedor, movilVendedor, delegacionVendedor FROM VENDEDORES WHERE movilVendedor = :movilVendedor")
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

    def listadoFacturas(self):
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM facturas ORDER BY fechafac ASC")
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("error listadoFacturas en conexion", e)