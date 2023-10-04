import re
import json
import datetime

__author__ = 'REBECA GONZÁLEZ BALADO'

# lista de contactos
listacontactos = []

# comprobador email
regexcorreo = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# comprobador fecha
formatofecha = '%d-%m-%Y'


class Contacto:
    def __init__(self, nombre, correo, fechanac):
        self.nombre = nombre
        self.correo = correo
        self.fechanac = fechanac

    def __str__(self):
        return f'{self.nombre} - Correo: {self.correo} / Fecha nacimiento: {self.fechanac}'


# comprueba si un correo tiene una sintaxis correcta
def comprobarcorreo(correo):
    return True if re.fullmatch(regexcorreo, correo) else False


# comprueba si una fecha es correcta
def comprobarfecha(fecha):
    try:
        return datetime.datetime.strptime(fecha, formatofecha)
    except ValueError:
        return False


# importa los contactos del json a una lista
def importarcontactos():
    print('\nImportando contactos...')

    try:
        # cargamos la lista de contactos del json
        contactos = open('contactos.json')
        datos = json.load(contactos)

        for d in datos['contactos']:
            contacto = Contacto(d['nombre'], d['correo'], d['fechanac'])
            listacontactos.append(contacto)

        contactos.close()

    # si el json no existe o esta vacio, ignoramos la importacion
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print('No hay contactos a importar.')
    else:
        print('Contactos importados satisfactoriamente.')


# graba la lista en el fichero json
def escribirjson():
    # ordenamos albafeticamente la lista
    listacontactos.sort(key=lambda cont: cont.nombre)

    # mapeamos los objetos de la lista
    listadict = []
    for contacto in listacontactos:
        listadict.append(contacto.__dict__)

    contactos = {
        'contactos': listadict
    }

    # volcamos la lista de contactos a json
    with open('contactos.json', 'w') as salida:
        json.dump(contactos, salida, indent=3)


# muestra la lista de contactos existentes
def listarcontactos():
    print('\nLista contactos')

    # si esta vacia, no recorremos la lista
    if len(listacontactos) == 0:
        print('La lista de contactos se encuentra vacía.')

    # si existen contactos, imprimimos la lista
    else:
        for contacto in listacontactos:
            print(contacto)


# busca contactos a partir de un dato y/o los elimina
def buscareliminarcontacto(eliminar):
    while True:
        if eliminar:
            print('\nEliminar contacto')
        else:
            print('\nBuscar contacto')

        print('N - Nombre')
        print('C - Correo electrónico')
        print('F - Fecha de nacimiento')
        print('X - Volver')
        opcion = str(input('\nElija un parámetro con el que buscar: '))

        # selector menu
        if opcion.casefold() == 'n':
            nombre = str(input('\nIntroduzca el nombre a buscar: '))
            buscareliminarfun(eliminar, 1, nombre)
            break

        elif opcion.casefold() == 'c':
            correo = str(input('\nIntroduzca el correo a buscar: '))
            buscareliminarfun(eliminar, 2, correo)
            break

        elif opcion.casefold() == 'f':
            fechanac = str(input('\nIntroduzca la fecha de nacimiento a buscar (dd-mm-aaaa): '))
            buscareliminarfun(eliminar, 3, fechanac)
            break

        elif opcion.casefold() == 'x':
            break
        else:
            print('Elige una opción válida.')


def buscareliminarfun(eliminar, tipo, valor):
    # buscamos todos los valores que coincidan
    listacontactoseliminar = []

    for contacto in listacontactos:
        if (tipo == 1 and contacto.nombre == valor) \
                or (tipo == 2 and contacto.correo == valor) \
                or (tipo == 3 and contacto.fechanac == valor):
            listacontactoseliminar.append(contacto)
            print(f'{len(listacontactoseliminar)}: {contacto}')

    if len(listacontactoseliminar) == 0:
        print('No se encontró ningún contacto con el parámetro introducido.')

    # si esta en modo eliminar, elegimos un contacto a eliminar
    elif eliminar:
        while True:
            try:
                contactoeliminar = int(input('\nElija un contacto a eliminar (introduzca su número): '))
                if contactoeliminar < 1:
                    raise ValueError()

                # eliminamos el contacto introducido de la lista de contactos
                for contacto in listacontactos:
                    if contacto == listacontactoseliminar[contactoeliminar - 1]:
                        listacontactos.remove(contacto)

                # guardamos los cambios en el fichero json
                escribirjson()

                break

            except (ValueError, IndexError):
                print('Introduzca un valor válido.')


# añade un nuevo contacto a partir de sus datos y lo guarda en un json
def annadircontacto():
    print('\nAñadir contacto')

    while True:
        nombre = str(input('Introduzca el nombre: '))

        # comprobamos que el nombre no esta vacio
        if len(nombre) > 0:
            break
        else:
            print('Introduzca un nombre válido.\n')

    while True:
        correo = str(input('Introduzca el correo electrónico: '))

        # comprobamos que la sintaxis del correo es correcta
        if comprobarcorreo(correo):
            break
        else:
            print('Introduzca un correo válido (nombre@dominio.dom).\n')

    while True:
        fechanac = str(input('Introduzca la fecha de nacimiento: '))

        # convertimos la fecha introducida a formato fecha
        fechanac = comprobarfecha(fechanac)

        # comprobamos que la fecha es correcta
        if not fechanac:
            print('Introduzca una fecha válida (dd-mm-aaaa).\n')

        # si es correcta, la devolvemos a string
        else:
            fechanac = fechanac.strftime(formatofecha)
            break

    # añadimos el nuevo contacto
    contacto = Contacto(nombre, correo, fechanac)
    listacontactos.append(contacto)

    # guardamos los cambios en el fichero json
    escribirjson()


# impresion menu
def menu():
    while True:
        print('\nAgenda de contactos')
        print('L - Listar contactos')
        print('B - Buscar contacto')
        print('A - Añadir contacto')
        print('E - Eliminar contacto')
        print('X - Salir')
        opcion = str(input('\nElija una opción: '))

        # selector menu
        if opcion.casefold() == 'l':
            listarcontactos()
        elif opcion.casefold() == 'b':
            buscareliminarcontacto(False)
        elif opcion.casefold() == 'a':
            annadircontacto()
        elif opcion.casefold() == 'e':
            buscareliminarcontacto(True)
        elif opcion.casefold() == 'x':
            break
        else:
            print('Elige una opción válida.')


def main():
    importarcontactos()
    menu()


if __name__ == '__main__':
    main()
