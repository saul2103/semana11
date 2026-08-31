# Sistema de Gestion de Restaurante - Recetas de mi Sierra

**Estudiante:** Bryan Saul Iza Llano

## Que es este proyecto

Este proyecto es un sistema de gestion para un restaurante, pensado para registrar productos, usuarios y ventas de forma ordenada. Permite controlar el stock disponible, mantener la relacion entre un usuario y un producto vendido y conservar la informacion en archivos JSON para que el estado del sistema se recupere al volver a ejecutar la aplicacion.

## Estructura del proyecto

```text
project/
|-- README.md                          # Este archivo de documentacion
|-- restaurante_app/
|   |-- main.py                        # Archivo principal donde se ejecuta el programa
|   |-- __init__.py                    # Marca el paquete Python
|   |-- datos/
|   |   |-- productos.json             # Archivo donde se guardan los productos
|   |   |-- usuarios.json              # Archivo donde se guardan los usuarios
|   |   |-- ventas.json                # Archivo donde se guardan las ventas
|   |
|   |-- modelos/
|   |   |-- __init__.py                # Marca el paquete de modelos
|   |   |-- producto.py                # Clase que define un Producto
|   |   |-- usuario.py                 # Clase que define un Usuario
|   |   |-- venta.py                   # Clase que define una Venta
|   |
|   |-- servicios/
|       |-- __init__.py                # Marca el paquete de servicios
|       |-- restaurante.py             # Clase que maneja la logica del restaurante
|       |-- archivo_servicio.py        # Clase que guarda y carga los datos en JSON
```

## Responsabilidad de los componentes

### Main
La clase principal del programa se encarga de mostrar el menu, solicitar datos al usuario y llamar a las operaciones del servicio. No debe modificar directamente las colecciones internas, sino que debe delegar esa tarea a la logica del restaurante.

### Modelo Producto
Representa cada producto del restaurante. Tiene atributos como nombre, precio, categoria y stock. Sus validaciones evitan que se registren datos invalidos o inconsistentes.

### Modelo Usuario
Representa a la persona que puede realizar una compra. Guarda el nombre y el email del usuario y valida que estos datos tengan un formato correcto.

### Modelo Venta
Es la entidad clave para la relacion principal del sistema. Una venta guarda quien compra, cual producto se vende y la cantidad solicitada.

### Servicio Restaurante
Es el nucleo del negocio. Aqui se gestionan los productos, los usuarios y las ventas. Ademas se aplican las reglas del dominio, como validar existencia del usuario, existencia del producto y disponibilidad de stock.

### ArchivoServicio
Centraliza la persistencia. Se encarga de guardar cada coleccion en JSON y de cargarla nuevamente cuando la aplicacion vuelva a ejecutarse.

## Funcionamiento del stock

El stock es un dato muy importante dentro del sistema. Cada producto registrado tiene una cantidad disponible. Cuando se realiza una venta, el proceso es el siguiente:

1. Se valida que el usuario exista.
2. Se valida que el producto exista.
3. Se valida que la cantidad pedida sea mayor a cero.
4. Se compara la cantidad requerida con el stock disponible.
5. Si el stock es suficiente, se registra la venta y se descuenta la cantidad vendida del producto.
6. Si el stock es insuficiente, la venta no se realiza y se muestra un mensaje de error.

Esto garantiza que no se vendan mas productos de los que existen en inventario.

## Relacion Usuario-Producto mediante Venta

La operacion principal del sistema es la venta. La relacion se representa de la siguiente manera:

Usuario registrado -> selecciona un producto -> valida cantidad -> valida stock -> crea una Venta -> guarda la venta -> descuenta stock del producto.

La clase Venta hace visible esta relacion porque guarda la referencia del usuario y del producto involucrado, junto con la cantidad vendida. De esta forma, el sistema no solo descuenta stock, sino que tambien conserva el registro historico de cada compra.

## Persistencia de productos, usuarios y ventas

La persistencia se realiza con archivos JSON dentro de la carpeta datos.

- productos.json: almacena todos los productos registrados
- usuarios.json: almacena todos los usuarios registrados
- ventas.json: almacena todas las ventas realizadas

Al iniciar la aplicacion, estos archivos se cargan automaticamente y se convierten nuevamente en objetos del sistema. Al cerrar la aplicacion, el estado actual se vuelve a guardar para que se mantenga la informacion.

Esto permite que el sistema recuerde los registros anteriores y no pierda los datos cada vez que se ejecuta.

## Excepciones controladas

El proyecto maneja errores de forma controlada para evitar que la aplicacion falle de manera abrupta. Algunas excepciones que se controlan son:

- valores invalidos al ingresar numeros
- nombre vacio
- precio invalido o menor o igual a cero
- categoria no permitida
- stock negativo
- email con formato incorrecto
- usuario no encontrado
- producto no encontrado
- cantidad menor o igual a cero
- stock insuficiente

Estas validaciones se muestran al usuario con mensajes claros para que pueda corregir la entrada o comprender por que la accion no se pudo completar.

## Forma de ejecucion

Para ejecutar el sistema, se debe abrir una terminal en la carpeta principal del proyecto y correr el siguiente comando:

```bash
python restaurante_app/main.py
```

Una vez ejecutado, el programa muestra el menu principal y permite acceder a las opciones de registro, busqueda, actualizacion, eliminacion, ventas y consultas.

## Pruebas realizadas

Se realizaron pruebas basicas de funcionamiento para comprobar que el sistema responde correctamente a los escenarios principales:

- registro de un producto nuevo
- registro de un usuario nuevo
- venta con stock suficiente
- venta con stock insuficiente
- consulta de ventas por usuario
- carga de informacion desde JSON al reiniciar la aplicacion
- guardado del estado actual al cerrar el programa

Estas pruebas permitieron verificar que la logica de negocio funciona de forma coherente y que la persistencia conserva la informacion de manera correcta.
