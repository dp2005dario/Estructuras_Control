import json

# 1. Definición de la clase Producto
class Producto:
    def __init__(self, codigo, nombre, stock=0):
        self.codigo = codigo
        self.nombre = nombre
        self.stock = stock

    def reponer(self, cantidad):
        # Comprueba que la cantidad sea un número entero positivo
        if type(cantidad) == int and cantidad > 0:
            self.stock = self.stock + cantidad
            return True
        return False

    def vender(self, cantidad):
        # Comprueba que sea entero positivo y que haya suficiente stock
        if type(cantidad) == int and cantidad > 0 and self.stock >= cantidad:
            self.stock = self.stock - cantidad
            return True
        return False


# 2. Definición de la clase Almacen
class Almacen:
    def __init__(self):
        self.productos = []
        self.archivo_json = "almacen.json"
        self.cargar_datos()

    def buscar(self, codigo):
        # Busca el producto por su código
        for p in self.productos:
            if p.codigo == codigo:
                return p
        return None

    def agregar(self, producto):
        # Añade el producto si no existe ya
        if self.buscar(producto.codigo) is None:
            self.productos.append(producto)
            return True
        return False

    def reponer(self, codigo, cantidad):
        p = self.buscar(codigo)
        if p is not None:
            return p.reponer(cantidad)
        return False

    def vender(self, codigo, cantidad):
        p = self.buscar(codigo)
        if p is not None:
            return p.vender(cantidad)
        return False

    def guardar_datos(self):
        # Guarda la lista de productos convirtiéndolos en diccionarios
        lista_datos = []
        for p in self.productos:
            diccionario = {
                "codigo": p.codigo,
                "nombre": p.nombre,
                "stock": p.stock
            }
            lista_datos.append(diccionario)
            
        with open(self.archivo_json, "w", encoding="utf-8") as f:
            json.dump(lista_datos, f, ensure_ascii=False, indent=4)

    def cargar_datos(self):
        try:
            with open(self.archivo_json, "r", encoding="utf-8") as f:
                lista_datos = json.load(f)
                # Reconstruye los objetos Producto a partir de los diccionarios
                for d in lista_datos:
                    prod = Producto(d["codigo"], d["nombre"], d["stock"])
                    self.productos.append(prod)
        except FileNotFoundError:
            # Si no existe el archivo, crea los datos iniciales pedidos en el ejemplo
            p1 = Producto("P1", "Cuaderno")
            p1.reponer(10)  # Establece existencias iniciales usando reponer
            
            p2 = Producto("P2", "Bolígrafo")
            p2.reponer(20)  # Establece existencias iniciales usando reponer
            
            self.productos.append(p1)
            self.productos.append(p2)
            self.guardar_datos()


# 3. Menú principal por consola
def menu():
    mi_almacen = Almacen()
    
    while True:
        print("\n--- GESTIÓN DE ALMACÉN ---")
        print("1. Listar productos y existencias.")
        print("2. Reponer unidades.")
        print("3. Vender unidades.")
        print("0. Guardar y salir.")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            print("\n--- LISTADO DE PRODUCTOS ---")
            if len(mi_almacen.productos) == 0:
                print("No hay productos.")
            else:
                for p in mi_almacen.productos:
                    print("Código:", p.codigo, "| Nombre:", p.nombre, "| Stock:", p.stock)
                    
        elif opcion == "2":
            codigo = input("Introduzca el código del producto: ").strip()
            
            # Comprobar si el producto existe
            p = mi_almacen.buscar(codigo)
            if p is None:
                print("Aviso: El producto con código", codigo, "no existe.")
                continue
                
            cantidad_texto = input("Introduzca la cantidad a reponer: ").strip()
            
            # Control por si introducen texto en vez de números
            try:
                cantidad = int(cantidad_texto)
            except ValueError:
                print("Aviso: Debe introducir un número entero válido. Volviendo al menú.")
                continue
                
            exito = mi_almacen.reponer(codigo, cantidad)
            if exito:
                print("¡Operación exitosa! Nuevo stock de", p.nombre, ":", p.stock)
            else:
                print("Operación rechazada: La cantidad debe ser un número positivo.")
                
        elif opcion == "3":
            codigo = input("Introduzca el código del producto: ").strip()
            
            # Comprobar si el producto existe
            p = mi_almacen.buscar(codigo)
            if p is None:
                print("Aviso: El producto con código", codigo, "no existe.")
                continue
                
            cantidad_texto = input("Introduzca la cantidad a vender: ").strip()
            
            # Control por si introducen texto en vez de números
            try:
                cantidad = int(cantidad_texto)
            except ValueError:
                print("Aviso: Debe introducir un número entero válido. Volviendo al menú.")
                continue
                
            exito = mi_almacen.vender(codigo, cantidad)
            if exito:
                print("¡Venta realizada con éxito! Stock restante de", p.nombre, ":", p.stock)
            else:
                print("Operación rechazada: Cantidad inválida o no hay suficiente stock.")
                
        elif opcion == "0":
            mi_almacen.guardar_datos()
            print("Datos guardados en 'almacen.json'. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

if __name__ == "__main__":
    menu()

# PRUEBA REALIZADA:
# Prueba: Se arrancó el script por primera vez generando automáticamente 'almacen.json' con 
# 10 cuadernos (P1) y 20 bolígrafos (P2). Se listaron los productos correctamente. 
# Se intentó reponer poniendo "hola" como cantidad, saltando el aviso de texto incorrecto 
# sin romper el programa. Se vendieron 3 cuadernos (dejando 7), se intentó vender 8 (se rechazó 
# por falta de stock quedando 7) y se repusieron 5 (llegando a 12). 
# Al pulsar 0, se guardó el estado y al reabrir el programa las 12 unidades seguían intactas.