import os
os.system("cls")

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import Restaurante

# ayuda a mantener la vista mas ordenada en la consola

def limpiar_pantalla() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def mostrar_menu() -> None:
    print("\n" + "=" * 40)
    print("          RECETAS DE MI SIERRA")
    print("=" * 40)
    print("1. Registrar producto")
    print("2. Buscar producto")
    print("3. Actualizar producto")
    print("4. Eliminar producto")
    print("5. Listar productos")
    print("-" * 40)
    print("6. Registrar usuario")
    print("7. Listar usuarios")
    print("-" * 40)
    print("8. Realizar venta")
    print("9. Consultar ventas")
    print("10. Listar todas las ventas")
    print("-" * 40)
    print("11. Mostrar categorías")
    print("12. Salir")
    print("=" * 40)

def registrar_producto(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    try:
        nombre = input("Nombre del producto: ").strip()
        precio = float(input("Precio del producto: "))
        categoria = input("Categoría (entrada/plato fuerte/bebida/postre): ").strip()
        stock = int(input("Stock del producto: "))
        
        producto = Producto(nombre, precio, categoria, stock)
        if restaurante.registrar_producto(producto):
            if archivo.guardar_productos(restaurante.obtener_productos()):
                print(f"Producto '{nombre}' registrado exitosamente.")
            else:
                print(f"Producto '{nombre}' registrado en memoria, pero no se pudo guardar.")
        else:
            print(f"El producto '{nombre}' ya existe.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

def buscar_producto(restaurante: Restaurante) -> None:
    print("1. Buscar por código")
    print("2. Buscar por nombre")
    opcion = input("Seleccione opción: ").strip()
    
    if opcion == "1":
        codigo = input("Código del producto: ").strip()
        producto = restaurante.buscar_producto_por_codigo(codigo)
    elif opcion == "2":
        nombre = input("Nombre del producto: ").strip()
        producto = restaurante.buscar_producto_por_nombre(nombre)
    else:
        print("Opción inválida.")
        return
    
    if producto:
        print(producto)
    else:
        print("Producto no encontrado.")

def actualizar_producto(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    codigo = input("Código del producto a actualizar: ").strip()
    producto = restaurante.buscar_producto_por_codigo(codigo)
    if not producto:
        print("Producto no encontrado.")
        return

    try:
        nuevo_nombre = input(f"Nuevo nombre ({producto.nombre}): ").strip()
        nuevo_precio = input(f"Nuevo precio ({producto.precio}): ").strip()
        nueva_categoria = input(f"Nueva categoría ({producto.categoria}): ").strip()
        nuevo_stock = input(f"Nuevo stock ({producto.stock}): ").strip()

        restaurante.actualizar_producto(
            codigo,
            nuevo_nombre if nuevo_nombre else None,
            float(nuevo_precio) if nuevo_precio else None,
            nueva_categoria if nueva_categoria else None,
            int(nuevo_stock) if nuevo_stock else None
        )
        if archivo.guardar_productos(restaurante.obtener_productos()):
            print("Producto actualizado exitosamente.")
        else:
            print("Producto actualizado en memoria, pero no se pudo guardar.")
    except ValueError as e:
        print(f"Error: {e}")

def eliminar_producto(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    codigo = input("Código del producto a eliminar: ").strip()
    if restaurante.eliminar_producto(codigo):
        if archivo.guardar_productos(restaurante.obtener_productos()):
            print("Producto eliminado exitosamente.")
        else:
            print("Producto eliminado en memoria, pero no se pudo guardar.")
    else:
        print("Producto no encontrado.")

def listar_productos(restaurante: Restaurante) -> None:
    productos = restaurante.listar_productos()
    if not productos:
        print("No hay productos registrados.")
        return
    
    print("\n--- LISTA DE PRODUCTOS ---")
    for i, producto in enumerate(productos, 1):
        print(f"{i}. {producto}")

def registrar_usuario(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    try:
        nombre = input("Nombre del usuario: ").strip()
        email = input("Email del usuario: ").strip()
        
        usuario = Usuario(nombre, email)
        if restaurante.registrar_usuario(usuario):
            if archivo.guardar_usuarios(restaurante.obtener_usuarios()):
                print(f"Usuario '{nombre}' registrado exitosamente.")
            else:
                print(f"Usuario '{nombre}' registrado en memoria, pero no se pudo guardar.")
        else:
            print(f"El usuario con email '{email}' ya existe.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

def listar_usuarios(restaurante: Restaurante) -> None:
    usuarios = restaurante.listar_usuarios()
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    
    print("\n--- LISTA DE USUARIOS ---")
    for i, usuario in enumerate(usuarios, 1):
        print(f"{i}. {usuario}")

def realizar_venta(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    try:
        print("\n--- REALIZAR VENTA ---")
        print("Usuarios registrados:")
        for usuario in restaurante.listar_usuarios():
            print(f"  {usuario.codigo} - {usuario.nombre} ({usuario.email})")
        
        usuario_codigo = input("Código del usuario: ").strip()
        
        print("\nProductos disponibles:")
        for producto in restaurante.listar_productos():
            print(f"  {producto.codigo} - {producto.nombre} (Stock: {producto.stock})")
        
        producto_codigo = input("Código del producto: ").strip()
        cantidad = int(input("Cantidad a comprar: "))
        
        resultado = restaurante.realizar_venta(usuario_codigo, producto_codigo, cantidad)
        
        if resultado["exito"]:
            print(resultado["mensaje"])
            print(f"Venta registrada: {resultado['venta']}")
            productos_guardados = archivo.guardar_productos(restaurante.obtener_productos())
            ventas_guardadas = archivo.guardar_ventas(restaurante.obtener_ventas())
            if not productos_guardados or not ventas_guardadas:
                print("Advertencia: la venta quedó en memoria, pero no se pudo guardar todo el estado.")
        else:
            print(f"Error: {resultado['mensaje']}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

def consultar_ventas_por_usuario(restaurante: Restaurante) -> None:
    print("1. Consultar por usuario")
    print("2. Consultar por producto")
    opcion = input("Seleccione opción: ").strip()

    if opcion == "1":
        print("\nUsuarios registrados:")
        for usuario in restaurante.listar_usuarios():
            print(f"  {usuario.codigo} - {usuario.nombre}")

        codigo = input("Código del usuario: ")
        ventas = restaurante.consultar_ventas_por_usuario(codigo)
        etiqueta = f"usuario {codigo.strip()}"
    elif opcion == "2":
        print("\nProductos registrados:")
        for producto in restaurante.listar_productos():
            print(f"  {producto.codigo} - {producto.nombre}")

        codigo = input("Código del producto: ")
        ventas = restaurante.consultar_ventas_por_producto(codigo)
        etiqueta = f"producto {codigo.strip()}"
    else:
        print("Opción inválida.")
        return
    
    if not ventas:
        print(f"No se encontraron ventas para este {etiqueta}.")
        return
    
    print(f"\n--- VENTAS DEL {etiqueta.upper()} ---")
    for i, venta in enumerate(ventas, 1):
        print(f"{i}. {venta}")

def listar_ventas(restaurante: Restaurante) -> None:
    ventas = restaurante.listar_ventas()
    if not ventas:
        print("No hay ventas registradas.")
        return
    
    print("\n--- LISTA DE VENTAS ---")
    for i, venta in enumerate(ventas, 1):
        print(f"{i}. {venta}")

def mostrar_categorias(restaurante: Restaurante) -> None:
    categorias = set(p.categoria for p in restaurante.listar_productos())
    if not categorias:
        print("No hay categorías registradas.")
        return
    print("\n--- CATEGORÍAS DISPONIBLES ---")
    for categoria in sorted(categorias):
        print(f"- {categoria}")

def guardar_estado(restaurante: Restaurante, archivo: ArchivoServicio) -> bool:
    # se guarda el estado actual para recuperar la informacion al abrir el sistema
    productos_guardados = archivo.guardar_productos(restaurante.obtener_productos())
    usuarios_guardados = archivo.guardar_usuarios(restaurante.obtener_usuarios())
    ventas_guardadas = archivo.guardar_ventas(restaurante.obtener_ventas())
    return productos_guardados and usuarios_guardados and ventas_guardadas


def main() -> None:
    restaurante = Restaurante()
    archivo = ArchivoServicio()

    productos = archivo.cargar_productos()
    if productos:
        restaurante.cargar_productos(productos)
        print(f"Se cargaron {len(productos)} productos.")

    usuarios = archivo.cargar_usuarios()
    if usuarios:
        restaurante.cargar_usuarios(usuarios)
        print(f"Se cargaron {len(usuarios)} usuarios.")

    ventas = archivo.cargar_ventas()
    if ventas:
        restaurante.cargar_ventas(ventas)
        print(f"Se cargaron {len(ventas)} ventas.")

    while True:
        mostrar_menu()
        try:
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                registrar_producto(restaurante, archivo)
            elif opcion == "2":
                buscar_producto(restaurante)
            elif opcion == "3":
                actualizar_producto(restaurante, archivo)
            elif opcion == "4":
                eliminar_producto(restaurante, archivo)
            elif opcion == "5":
                listar_productos(restaurante)
            elif opcion == "6":
                registrar_usuario(restaurante, archivo)
            elif opcion == "7":
                listar_usuarios(restaurante)
            elif opcion == "8":
                realizar_venta(restaurante, archivo)
            elif opcion == "9":
                consultar_ventas_por_usuario(restaurante)
            elif opcion == "10":
                listar_ventas(restaurante)
            elif opcion == "11":
                mostrar_categorias(restaurante)
            elif opcion == "12":
                if not guardar_estado(restaurante, archivo):
                    print("Advertencia: no se pudo guardar todo el estado.")
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")
        except ValueError:
            print("Error: Ingrese un número válido.")
        except KeyboardInterrupt:
            guardar_estado(restaurante, archivo)
            print("\nSistema cerrado correctamente.")
            break
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()