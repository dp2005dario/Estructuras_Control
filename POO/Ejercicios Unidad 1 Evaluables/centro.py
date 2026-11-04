import json

# 1. Definición de la clase Taller
class Taller:
    def __init__(self, codigo, nombre, capacidad, inscritos=0):
        self.codigo = codigo
        self.nombre = nombre
        self.capacidad = capacidad
        self.inscritos = inscritos

    def inscribir(self):
        # Aumenta en uno si queda sitio (si inscritos es menor que la capacidad)
        if self.inscritos < self.capacidad:
            self.inscritos = self.inscritos + 1
            return True
        return False

    def cancelar(self):
        # Reduce en uno si hay al menos una inscripción
        if self.inscritos > 0:
            self.inscritos = self.inscritos - 1
            return True
        return False

    def plazas_libres(self):
        # Devuelve la capacidad menos los inscritos
        return self.capacidad - self.inscritos


# 2. Definición de la clase Centro
class Centro:
    def __init__(self, archivo_json="talleres.json"):
        self.archivo_json = archivo_json
        self.talleres = []
        self.cargar_datos()

    def buscar(self, codigo):
        for t in self.talleres:
            if t.codigo == codigo:
                return t
        return None

    def agregar(self, taller):
        if self.buscar(taller.codigo) is None:
            self.talleres.append(taller)
            return True
        return False

    def inscribir(self, codigo):
        t = self.buscar(codigo)
        if t is not None:
            return t.inscribir()
        return False

    def cancelar(self, codigo):
        t = self.buscar(codigo)
        if t is not None:
            return t.cancelar()
        return False

    def total_inscritos(self):
        suma = 0
        for t in self.talleres:
            suma = suma + t.inscritos
        return suma

    def guardar_datos(self):
        lista_datos = []
        for t in self.talleres:
            diccionario = {
                "codigo": t.codigo,
                "nombre": t.nombre,
                "capacidad": t.capacidad,
                "inscritos": t.inscritos
            }
            lista_datos.append(diccionario)
            
        with open(self.archivo_json, "w", encoding="utf-8") as f:
            json.dump(lista_datos, f, ensure_ascii=False, indent=4)

    def cargar_datos(self):
        try:
            with open(self.archivo_json, "r", encoding="utf-8") as f:
                lista_datos = json.load(f)
                for d in lista_datos:
                    # Crea el taller con 0 inscritos y recupera las inscripciones con un bucle como pide la práctica
                    t = Taller(d["codigo"], d["nombre"], d["capacidad"], 0)
                    for i in range(d["inscritos"]):
                        t.inscribir()
                    self.talleres.append(t)
        except FileNotFoundError:
            # Si no existe el archivo, crea los dos talleres de ejemplo del enunciado
            t1 = Taller("T1", "Fotografía", 3, 0)
            t2 = Taller("T2", "Cerámica", 2, 0)
            self.talleres.append(t1)
            self.talleres.append(t2)
            self.guardar_datos()


# 3. Menú principal por consola
def menu():
    mi_centro = Centro()
    
    while True:
        print("\n--- CENTRO DE TALLERES ---")
        print("1. Listar talleres, inscritos y plazas libres.")
        print("2. Inscribir a una persona en un taller.")
        print("3. Cancelar una inscripción.")
        print("4. Consultar el total de inscripciones del centro.")
        print("0. Guardar y salir.")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            print("\n--- LISTADO DE TALLERES ---")
            if len(mi_centro.talleres) == 0:
                print("No hay talleres registrados.")
            else:
                for t in mi_centro.talleres:
                    print("Código:", t.codigo, "| Nombre:", t.nombre, "| Inscritos:", t.inscritos, "| Plazas libres:", t.plazas_libres())
                    
        elif opcion == "2":
            codigo = input("Introduzca el código del taller: ").strip()
            t = mi_centro.buscar(codigo)
            if t is None:
                print("Aviso: El taller con código", codigo, "no existe.")
                continue
                
            exito = mi_centro.inscribir(codigo)
            if exito:
                print("¡Inscripción realizada con éxito en", t.nombre, "! Inscritos actuales:", t.inscritos)
            else:
                print("Operación rechazada: El taller está completo.")
                
        elif opcion == "3":
            codigo = input("Introduzca el código del taller: ").strip()
            t = mi_centro.buscar(codigo)
            if t is None:
                print("Aviso: El taller con código", codigo, "no existe.")
                continue
                
            exito = mi_centro.cancelar(codigo)
            if exito:
                print("¡Inscripción cancelada con éxito en", t.nombre, "! Inscritos actuales:", t.inscritos)
            else:
                print("Operación rechazada: No hay ninguna inscripción en este taller.")
                
        elif opcion == "4":
            total = mi_centro.total_inscritos()
            print("\nEl total de inscripciones en todo el centro es de:", total)
            
        elif opcion == "0":
            mi_centro.guardar_datos()
            print("Datos guardados en 'talleres.json'. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

if __name__ == "__main__":
    menu()

# PRUEBA REALIZADA:
# Prueba: Se ejecutó el programa por primera vez creando 'talleres.json' con Fotografía (capacidad 3) 
# y Cerámica (capacidad 2). Se inscribieron 3 personas en Fotografía (aceptadas), y al intentar una 4ª 
# se rechazó por estar completo. Se canceló una inscripción (dejando 2 inscritos y 1 libre). 
# Se intentó cancelar con 0 inscritos y se rechazó.Luego se probo cadena de texto HOLA Y ADIOS y me dio operación no valida, Se consultó el total de inscritos, 
# se probó un código inexistente (T9) dando aviso, y al pulsar 0 se guardó y comprobó que al reabrir  se conservaban los datos.