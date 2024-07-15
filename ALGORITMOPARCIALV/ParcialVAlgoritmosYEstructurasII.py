import csv
from datetime import datetime, timedelta

class Node:
    def __init__(self, proyecto):
        self.proyecto = proyecto
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def insert(self, root, proyecto):
        if not root:
            return Node(proyecto)
        elif proyecto.dias_restantes < root.proyecto.dias_restantes:
            root.left = self.insert(root.left, proyecto)
        else:
            root.right = self.insert(root.right, proyecto)

        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and proyecto.dias_restantes < root.left.proyecto.dias_restantes:
            return self.rightRotate(root)

        if balance < -1 and proyecto.dias_restantes > root.right.proyecto.dias_restantes:
            return self.leftRotate(root)

        if balance > 1 and proyecto.dias_restantes > root.left.proyecto.dias_restantes:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and proyecto.dias_restantes < root.right.proyecto.dias_restantes:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def delete(self, root, proyecto):
        if not root:
            return root

        if proyecto.dias_restantes < root.proyecto.dias_restantes:
            root.left = self.delete(root.left, proyecto)
        elif proyecto.dias_restantes > root.proyecto.dias_restantes:
            root.right = self.delete(root.right, proyecto)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp

            temp = self.minValueNode(root.right)
            root.proyecto = temp.proyecto
            root.right = self.delete(root.right, temp.proyecto)

        if root is None:
            return root

        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)

        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)

        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

class Proyecto:
    def __init__(self, id, nombre, gerente, fecha_inicio, fecha_fin, estado):
        self.id = id
        self.nombre = nombre
        self.gerente = gerente
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.dias_restantes = (fecha_fin - fecha_inicio).days

class EmpresaCliente:
    def __init__(self, id, nombre, descripcion, fecha_creacion, direccion, telefono, correo, gerente, equipo_contacto):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.gerente = gerente
        self.equipo_contacto = equipo_contacto
        self.proyectos = []

    def agregar_proyecto(self, proyecto):
        arbol = AVLTree()
        root = None
        root = arbol.insert(root, proyecto)
        self.proyectos.append(root)

    def eliminar_proyecto(self, proyecto):
        self.proyectos.remove(proyecto)

def cargar_datos_desde_csv():
    empresas_clientes = []
    try:
        with open('empresas_clientes.csv', 'r') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            next(lector_csv)  # Saltar la fila de encabezado
            for fila in lector_csv:
                id, nombre, descripcion, fecha_creacion, direccion, telefono, correo, gerente, equipo_contacto = fila
                empresa = EmpresaCliente(id, nombre, descripcion, datetime.strptime(fecha_creacion, '%Y-%m-%d'), direccion, telefono, correo, gerente, equipo_contacto)
                empresas_clientes.append(empresa)
    except FileNotFoundError:
        pass
    return empresas_clientes

def guardar_datos_en_csv(empresas_clientes):
    with open('empresas_clientes.csv', 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow(['ID', 'Nombre', 'Descripción', 'Fecha Creación', 'Dirección', 'Teléfono', 'Correo', 'Gerente', 'Equipo Contacto'])
        for empresa in empresas_clientes:
            fila = [empresa.id, empresa.nombre, empresa.descripcion, empresa.fecha_creacion.strftime('%Y-%m-%d'), empresa.direccion, empresa.telefono, empresa.correo, empresa.gerente, empresa.equipo_contacto]
            escritor_csv.writerow(fila)

def menu_principal():
    print("Bienvenido al Programa de Gestión de Empresas Clientes")
    print("1. Gestión de Empresas Clientes")
    print("2. Gestión de Proyectos")
    print("3. Salir")
    opcion = input("Seleccione una opción (1-3): ")
    return opcion

def menu_empresas_clientes(empresas_clientes):
    print("\nGestión de Empresas Clientes")
    print("1. Crear Empresa Cliente")
    print("2. Modificar Empresa Cliente")
    print("3. Consultar Empresa Cliente")
    print("4. Eliminar Empresa Cliente")
    print("5. Listar Empresas Clientes")
    print("6. Volver al Menú Principal")
    opcion = input("Seleccione una opción (1-6): ")
    
    if opcion == "1":
        crear_empresa_cliente(empresas_clientes)
    elif opcion == "2":
        modificar_empresa_cliente(empresas_clientes)
    elif opcion == "3":
        consultar_empresa_cliente(empresas_clientes)
    elif opcion == "4":
        eliminar_empresa_cliente(empresas_clientes)
    elif opcion == "5":
        listar_empresas_clientes(empresas_clientes)
    elif opcion == "6":
        return
    else:
        print("Opción inválida. Intente de nuevo.")
    menu_empresas_clientes(empresas_clientes)

def menu_proyectos(empresa_cliente):
    print(f"\nGestión de Proyectos para {empresa_cliente.nombre}")
    print("1. Crear Proyecto")
    print("2. Modificar Proyecto")
    print("3. Consultar Proyecto")
    print("4. Eliminar Proyecto")
    print("5. Listar Proyectos")
    print("6. Volver al Menú Principal")
    opcion = input("Seleccione una opción (1-6): ")
    
    if opcion == "1":
        crear_proyecto(empresa_cliente)
    elif opcion == "2":
        modificar_proyecto(empresa_cliente)
    elif opcion == "3":
        consultar_proyecto(empresa_cliente)
    elif opcion == "4":
        eliminar_proyecto(empresa_cliente)
    elif opcion == "5":
        listar_proyectos(empresa_cliente)
    elif opcion == "6":
        return
    else:
        print("Opción inválida. Intente de nuevo.")
    menu_proyectos(empresa_cliente)

def crear_empresa_cliente(empresas_clientes):
    id = input("Ingrese el ID de la empresa cliente: ")
    nombre = input("Ingrese el nombre de la empresa cliente: ")
    descripcion = input("Ingrese la descripción de la empresa cliente: ")
    fecha_creacion = datetime.strptime(input("Ingrese la fecha de creación (AAAA-MM-DD): "), '%Y-%m-%d')
    direccion = input("Ingrese la dirección de la empresa cliente: ")
    telefono = input("Ingrese el teléfono de la empresa cliente: ")
    correo = input("Ingrese el correo de la empresa cliente: ")
    gerente = input("Ingrese el nombre del gerente: ")
    equipo_contacto = input("Ingrese el equipo de contacto: ")
    
    empresa = EmpresaCliente(id, nombre, descripcion, fecha_creacion, direccion, telefono, correo, gerente, equipo_contacto)
    empresas_clientes.append(empresa)
    print("Empresa cliente creada exitosamente.")

def modificar_empresa_cliente(empresas_clientes):
    id = input("Ingrese el ID de la empresa cliente a modificar: ")
    empresa = next((e for e in empresas_clientes if e.id == id), None)
    if empresa:
        empresa.nombre = input(f"Ingrese el nuevo nombre (actual: {empresa.nombre}): ")
        empresa.descripcion = input(f"Ingrese la nueva descripción (actual: {empresa.descripcion}): ")
        empresa.fecha_creacion = datetime.strptime(input(f"Ingrese la nueva fecha de creación (actual: {empresa.fecha_creacion.strftime('%Y-%m-%d')}): "), '%Y-%m-%d')
        empresa.direccion = input(f"Ingrese la nueva dirección (actual: {empresa.direccion}): ")
        empresa.telefono = input(f"Ingrese el nuevo teléfono (actual: {empresa.telefono}): ")
        empresa.correo = input(f"Ingrese el nuevo correo (actual: {empresa.correo}): ")
        empresa.gerente = input(f"Ingrese el nuevo nombre del gerente (actual: {empresa.gerente}): ")
        empresa.equipo_contacto = input(f"Ingrese el nuevo equipo de contacto (actual: {empresa.equipo_contacto}): ")
        print("Empresa cliente modificada exitosamente.")
    else:
        print("No se encontró la empresa cliente.")

def consultar_empresa_cliente(empresas_clientes):
    id = input("Ingrese el ID de la empresa cliente a consultar: ")
    empresa = next((e for e in empresas_clientes if e.id == id), None)
    if empresa:
        print(f"ID: {empresa.id}")
        print(f"Nombre: {empresa.nombre}")
        print(f"Descripción: {empresa.descripcion}")
        print(f"Fecha de Creación: {empresa.fecha_creacion.strftime('%Y-%m-%d')}")
        print(f"Dirección: {empresa.direccion}")
        print(f"Teléfono: {empresa.telefono}")
        print(f"Correo: {empresa.correo}")
        print(f"Gerente: {empresa.gerente}")
        print(f"Equipo de Contacto: {empresa.equipo_contacto}")
    else:
        print("No se encontró la empresa cliente.")

def eliminar_empresa_cliente(empresas_clientes):
    id = input("Ingrese el ID de la empresa cliente a eliminar: ")
    empresa = next((e for e in empresas_clientes if e.id == id), None)
    if empresa:
        empresas_clientes.remove(empresa)
        print("Empresa cliente eliminada exitosamente.")
    else:
        print("No se encontró la empresa cliente.")

def listar_empresas_clientes(empresas_clientes):
    if not empresas_clientes:
        print("No hay empresas clientes registradas.")
    else:
        print("\nListado de Empresas Clientes:")
        for empresa in empresas_clientes:
            print(f"ID: {empresa.id} - Nombre: {empresa.nombre}")

def crear_proyecto(empresa_cliente):
    id = input("Ingrese el ID del proyecto: ")
    nombre = input("Ingrese el nombre del proyecto: ")
    gerente = input("Ingrese el gerente del proyecto: ")
    fecha_inicio = datetime.strptime(input("Ingrese la fecha de inicio (AAAA-MM-DD): "), '%Y-%m-%d')
    fecha_fin = datetime.strptime(input("Ingrese la fecha de finalización (AAAA-MM-DD): "), '%Y-%m-%d')
    estado = input("Ingrese el estado del proyecto: ")
    
    proyecto = Proyecto(id, nombre, gerente, fecha_inicio, fecha_fin, estado)
    root = None
    mytree = AVLTree()
    root = mytree.insert(root, proyecto)
    empresa_cliente.agregar_proyecto(proyecto)
    print("Proyecto creado exitosamente.")

def modificar_proyecto(empresa_cliente):
    id = input("Ingrese el ID del proyecto a modificar: ")
    proyecto = next((p for p in empresa_cliente.proyectos if p.id == id), None)
    if proyecto:
        proyecto.nombre = input(f"Ingrese el nuevo nombre (actual: {proyecto.nombre}): ")
        proyecto.gerente = input(f"Ingrese el nuevo gerente (actual: {proyecto.descripcion}): ")
        proyecto.fecha_inicio = datetime.strptime(input(f"Ingrese la nueva fecha de inicio (actual: {proyecto.fecha_inicio.strftime('%Y-%m-%d')}): "), '%Y-%m-%d')
        proyecto.fecha_fin = datetime.strptime(input(f"Ingrese la nueva fecha de finalización (actual: {proyecto.fecha_fin.strftime('%Y-%m-%d')}): "), '%Y-%m-%d')
        proyecto.estado = input(f"Ingrese el nuevo estado (actual: {proyecto.estado}): ")
        print("Proyecto modificado exitosamente.")
    else:
        print("No se encontró el proyecto.")

def consultar_proyecto(empresa_cliente):
    id = input("Ingrese el ID del proyecto a consultar: ")
    proyecto = next((p for p in empresa_cliente.proyectos if p.id == id), None)
    if proyecto:
        print(f"ID: {proyecto.id}")
        print(f"Nombre: {proyecto.nombre}")
        print(f"Gerente: {proyecto.gerente}")
        print(f"Fecha de Inicio: {proyecto.fecha_inicio.strftime('%Y-%m-%d')}")
        print(f"Fecha de Finalización: {proyecto.fecha_fin.strftime('%Y-%m-%d')}")
        print(f"Estado: {proyecto.estado}")
    else:
        print("No se encontró el proyecto.")

def eliminar_proyecto(empresa_cliente):
    id = input("Ingrese el ID del proyecto a eliminar: ")
    proyecto = next((p for p in empresa_cliente.proyectos if p.id == id), None)
    if proyecto:
        empresa_cliente.eliminar_proyecto(proyecto)
        print("Proyecto eliminado exitosamente.")
    else:
        print("No se encontró el proyecto.")

def listar_proyectos(empresa_cliente):
    if not empresa_cliente.proyectos:
        print("No hay proyectos registrados para esta empresa cliente.")
    else:
        print(f"\nListado de Proyectos para {empresa_cliente.nombre}:")
        for nodo in empresa_cliente.proyectos:
            print(f"ID: {nodo.proyecto.id} - Nombre: {nodo.proyecto.nombre}")

def main():
    empresas_clientes = cargar_datos_desde_csv()
    while True:
        opcion = menu_principal()
        if opcion == "1":
            menu_empresas_clientes(empresas_clientes)
        elif opcion == "2":
            id_empresa = input("Ingrese el ID de la empresa cliente: ")
            empresa = next((e for e in empresas_clientes if e.id == id_empresa), None)
            if empresa:
                menu_proyectos(empresa)
            else:
                print("No se encontró la empresa cliente.")
        elif opcion == "3":
            guardar_datos_en_csv(empresas_clientes)
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

main()