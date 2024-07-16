import csv
from datetime import datetime, timedelta
import json

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
    
class Tarea:
    def __init__(self, id, nombre, cliente_empresa, descripcion, fecha_inicio, fecha_vencimiento, estado, porcentaje):
        self.id = id
        self.nombre = nombre
        self.cliente_empresa = cliente_empresa
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = estado
        self.porcentaje = porcentaje
        self.subtareas = []
        self.nivel = 0

    def agregar_subtarea(self, subtarea):
        self.subtareas.append(subtarea)

    def __str__(self):
        return f"Tarea {self.id}: {self.nombre} ({self.estado})"
    
class subtarea:
    def __init__(self, id, nombre, cliente_empresa, descripcion, fecha_inicio, fecha_vencimiento, estado, porcentaje):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado

class ArbolDeTareas:
    def __init__(self):
        self.tareas = []

    def agregar_tarea(self, tarea, padre=None, nivel=0):
        tarea.nivel = nivel
        self.tareas.append(tarea)
        if padre:
            padre.agregar_subtarea(tarea)

    def obtener_tarea(self, id):
        for tarea in self.tareas:
            if tarea.id == id:
                return tarea
        return None

    def listar_tareas_en_nivel(self, nivel):
        tareas_en_nivel = []
        for tarea in self.tareas:
            if tarea.nivel == nivel:
                tareas_en_nivel.append(tarea)
        return tareas_en_nivel

    def mostrar_subtareas(self, tarea):
        print(f"Subtareas de {tarea.nombre}:")
        for subtarea in tarea.subtareas:
            print(f"  {subtarea.nombre}")

    def serializar_a_json(self):
        arbol_de_tareas_json = {"tareas": []}
        for tarea in self.tareas:
            tarea_json = {
                "id": tarea.id,
                "nombre": tarea.nombre,
                "cliente_empresa": tarea.cliente_empresa,
                "descripcion": tarea.descripcion,
                "fecha_inicio": tarea.fecha_inicio,
                "fecha_vencimiento": tarea.fecha_vencimiento,
                "estado": tarea.estado,
                "porcentaje": tarea.porcentaje,
                "subtareas": []
            }
            for subtarea in tarea.subtareas:
                tarea_json["subtareas"].append(subtarea.id)
            arbol_de_tareas_json["tareas"].append(tarea_json)
        return json.dumps(arbol_de_tareas_json)

    def cargar_desde_json(self, cadena_json):
        arbol_de_tareas_json = json.loads(cadena_json)
        for tarea_json in arbol_de_tareas_json["tareas"]:
            tarea = Tarea(
                tarea_json["id"],
                tarea_json["nombre"],
                tarea_json["cliente_empresa"],
                tarea_json["descripcion"],
                tarea_json["fecha_inicio"],
                tarea_json["fecha_vencimiento"],
                tarea_json["estado"],
                tarea_json["porcentaje"]
            )
            for subtarea_id in tarea_json["subtareas"]:
                subtarea = self.obtener_tarea(subtarea_id)
                if subtarea:
                    tarea.agregar_subtarea(subtarea)
            self.agregar_tarea(tarea)

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

class Proyecto:
    def __init__(self, id, nombre, gerente, fecha_inicio, fecha_fin, estado):
        self.id = id
        self.nombre = nombre
        self.gerente = gerente
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.dias_restantes = (fecha_fin - fecha_inicio).days
        self.tareas = []

class Task:
    def __init__(self, id, name, client, description, start_date, 
                 due_date, status, percentage):
        self.id = id
        self.name = name
        self.client = client
        self.description = description
        self.start_date = start_date
        self.due_date = due_date
        self.status = status
        self.percentage = percentage
        self.subtask = []

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'client': self.client,
            'description': self.description,
            'start_date': self.start_date,
            'due_date': self.due_date,
            'status': self.status,
            'percentage': self.percentage,
            'subtasks': [subtask.to_dict() for subtask in self.subtasks]
        }
    
    def from_dict(cls, data):
        task = cls(
            id=data['id'],
            name=data['name'],
            client=data['client'],
            description=data['description'],
            start_date=data['start_date'],
            due_date=data['due_date'],
            status=data['status'],
            percentage=data['percentage']
        )
        task.subtasks = [cls.from_dict(subtask) for subtask in data['subtasks']]
        return task

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

class Tarea:
    def __init__(self, id, nombre, descripcion, estado):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, tarea):
        if not self.head:
            self.head = tarea
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = tarea

    def to_list(self):
        tarea_list = []
        current = self.head
        while current:
            tarea_list.append(current)
            current = current.next
        return tarea_list

class Sprint:
    def __init__(self, id, nombre, fecha_inicio, fecha_fin, estado, objetivos, equipo):
        self.id = id
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.objetivos = objetivos
        self.equipo = equipo
        self.tareas = LinkedList()

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)

    def mostrar_tareas(self):
        return self.tareas.to_list()

class AVLNode:
    def __init__(self, sprint):
        self.sprint = sprint
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, sprint):
        if not self.root:
            self.root = AVLNode(sprint)
        else:
            self._insert(self.root, sprint)

    def _insert(self, node, sprint):
        if sprint.id < node.sprint.id:
            if node.left:
                self._insert(node.left, sprint)
            else:
                node.left = AVLNode(sprint)
        else:
            if node.right:
                self._insert(node.right, sprint)
            else:
                node.right = AVLNode(sprint)

    def show_sprints_at_level(self, level):
        result = []
        self._show_sprints_at_level(self.root, level, result)
        return result

    def _show_sprints_at_level(self, node, level, result):
        if node:
            if level == 0:
                result.append(node.sprint)
            else:
                self._show_sprints_at_level(node.left, level - 1, result)
                self._show_sprints_at_level(node.right, level - 1, result)

    def show_subtareas(self, tarea_id):
        result = []
        self._show_subtareas(self.root, tarea_id, result)
        return result

    def _show_subtareas(self, node, tarea_id, result):
        if node:
            for tarea in node.sprint.tareas.to_list():
                if tarea.id == tarea_id:
                    result.append(tarea)
                    for subtarea in tarea.subtareas:
                        result.append(subtarea)
                    return
            self._show_subtareas(node.left, tarea_id, result)
            self._show_subtareas(node.right, tarea_id, result)

def load_data(file_path):
    avl_tree = AVLTree()
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sprint = Sprint(int(row['id']), row['nombre'], row['fecha_inicio'], row['fecha_fin'], row['estado'], row['objetivos'], row['equipo'])
            avl_tree.insert(sprint)
    return avl_tree

def save_data(avl_tree, file_path):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'nombre', 'fecha_inicio', 'fecha_fin', 'estado', 'objetivos', 'equipo'])
        for sprint in avl_tree.show_sprints_at_level(0):
            writer.writerow([sprint.id, sprint.nombre, sprint.fecha_inicio, sprint.fecha_fin, sprint.estado, sprint.objetivos, sprint.equipo])

def buscar_sprint(avl_tree, sprint_id):
    current = avl_tree.root
    while current:
        if current.sprint.id == sprint_id:
            return current.sprint
        elif sprint_id < current.sprint.id:
            current = current.left
        else:
            current = current.right
    return None

# Carga de datos
avl_tree = load_data('data.csv')

# Agregar tarea a un sprint
sprint_id = 1
tarea_id = 2
sprint = buscar_sprint(avl_tree, sprint_id)
if sprint:
    tarea = Tarea(tarea_id, 'Tarea 2', 'Descripción de la tarea 2', 'pendiente')
    sprint.agregar_tarea(tarea)
else:
    print("Sprint no encontrado")

# Mostrar tareas de un sprint
sprint_id = 1
sprint = buscar_sprint(avl_tree, sprint_id)
if sprint:
    tareas = sprint.mostrar_tareas()
    for tarea in tareas:
        print(f"Tarea {tarea.id}: {tarea.nombre} - {tarea.descripcion} - {tarea.estado}")
else:
    print("Sprint no encontrado")

# Guardar datos
save_data(avl_tree, 'data.csv')

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
