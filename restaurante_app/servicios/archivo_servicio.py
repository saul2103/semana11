import json
import os
from typing import List, Dict, Any
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

class ArchivoServicio:
    # aqui se centraliza la carga y guardado de la info del sistema en JSON
    def __init__(self) -> None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ruta_productos = os.path.join(base_dir, "datos", "productos.json")
        self.ruta_usuarios = os.path.join(base_dir, "datos", "usuarios.json")
        self.ruta_ventas = os.path.join(base_dir, "datos", "ventas.json")
        self._crear_directorios()

    # si no existe la carpeta de datos, se crea automaticamente
    def _crear_directorios(self) -> None:
        directorio = os.path.dirname(self.ruta_productos)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)

    # guarda la lista de objetos como JSON legible
    def _guardar_json(self, ruta: str, datos: List[Dict[str, Any]]) -> bool:
        ruta_temporal = f"{ruta}.tmp"
        try:
            with open(ruta_temporal, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            os.replace(ruta_temporal, ruta)
            return True
        except (PermissionError, OSError) as e:
            print(f"Error al guardar {ruta}: {e}")
        except (TypeError, ValueError) as e:
            print(f"Datos inválidos para guardar en {ruta}: {e}")
        finally:
            if os.path.exists(ruta_temporal):
                os.remove(ruta_temporal)
        return False

    # carga el JSON y reconstruye los objetos del sistema
    def _cargar_json(self, ruta: str, clase_modelo) -> List[Any]:
        if not os.path.exists(ruta):
            return []

        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                if not isinstance(datos, list):
                    print(f"El archivo {ruta} no contiene una lista válida.")
                    return []

                objetos = []
                for item in datos:
                    try:
                        if not isinstance(item, dict):
                            continue
                        objeto = clase_modelo.from_dict(item)
                        objetos.append(objeto)
                    except (KeyError, ValueError, TypeError) as e:
                        print(f"Registro inválido omitido en {ruta}: {e}")
                        continue
                return objetos
        except json.JSONDecodeError:
            print(f"Error: El archivo {ruta} no tiene un formato JSON válido.")
            return []
        except PermissionError:
            print(f"Error: No tienes permisos para leer {ruta}.")
            return []
        except Exception as e:
            print(f"Error inesperado al cargar {ruta}: {e}")
            return []

    def guardar_productos(self, productos: List[Producto]) -> bool:
        return self._guardar_json(self.ruta_productos, [p.to_dict() for p in productos])

    def cargar_productos(self) -> List[Producto]:
        return self._cargar_json(self.ruta_productos, Producto)

    def guardar_usuarios(self, usuarios: List[Usuario]) -> bool:
        return self._guardar_json(self.ruta_usuarios, [u.to_dict() for u in usuarios])

    def cargar_usuarios(self) -> List[Usuario]:
        return self._cargar_json(self.ruta_usuarios, Usuario)

    def guardar_ventas(self, ventas: List[Venta]) -> bool:
        return self._guardar_json(self.ruta_ventas, [v.to_dict() for v in ventas])

    def cargar_ventas(self) -> List[Venta]:
        return self._cargar_json(self.ruta_ventas, Venta)