from typing import List, Optional, Dict, Any
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

class Restaurante:
    def __init__(self) -> None:
        self._productos: List[Producto] = []
        self._usuarios: List[Usuario] = []
        self._ventas: List[Venta] = []

    # Metodos para productos
    def cargar_productos(self, productos: List[Producto]) -> None:
        self._productos = productos

    def obtener_productos(self) -> List[Producto]:
        return self._productos.copy()

    def registrar_producto(self, producto: Producto) -> bool:
        for p in self._productos:
            if p.codigo == producto.codigo:
                return False
            if p.nombre.lower() == producto.nombre.lower():
                return False
        self._productos.append(producto)
        return True

    def buscar_producto_por_codigo(self, codigo: str) -> Optional[Producto]:
        for producto in self._productos:
            if producto.codigo == codigo:
                return producto
        return None

    def buscar_producto_por_nombre(self, nombre: str) -> Optional[Producto]:
        for producto in self._productos:
            if producto.nombre.lower() == nombre.lower():
                return producto
        return None

    def actualizar_producto(self, codigo: str, nuevo_nombre: Optional[str] = None,
                           nuevo_precio: Optional[float] = None,
                           nueva_categoria: Optional[str] = None,
                           nuevo_stock: Optional[int] = None) -> bool:
        producto = self.buscar_producto_por_codigo(codigo)
        if not producto:
            return False

        if nuevo_nombre is not None:
            if any(
                otro.codigo != producto.codigo
                and otro.nombre.casefold() == nuevo_nombre.strip().casefold()
                for otro in self._productos
            ):
                raise ValueError("Ya existe otro producto con ese nombre.")
            producto._validar_nombre(nuevo_nombre)
        if nuevo_precio is not None:
            producto._validar_precio(nuevo_precio)
        if nueva_categoria is not None:
            producto._validar_categoria(nueva_categoria)
        if nuevo_stock is not None:
            producto._validar_stock(nuevo_stock)

        if nuevo_nombre is not None:
            producto.nombre = nuevo_nombre
        if nuevo_precio is not None:
            producto.precio = nuevo_precio
        if nueva_categoria is not None:
            producto.categoria = nueva_categoria
        if nuevo_stock is not None:
            producto.stock = nuevo_stock
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto_por_codigo(codigo)
        if producto:
            self._productos.remove(producto)
            return True
        return False

    def listar_productos(self) -> List[Producto]:
        return self._productos.copy()

    # Metodos para usuarios
    def cargar_usuarios(self, usuarios: List[Usuario]) -> None:
        self._usuarios = usuarios

    def obtener_usuarios(self) -> List[Usuario]:
        return self._usuarios.copy()

    def registrar_usuario(self, usuario: Usuario) -> bool:
        for u in self._usuarios:
            if u.codigo == usuario.codigo:
                return False
            if u.email.lower() == usuario.email.lower():
                return False
        self._usuarios.append(usuario)
        return True

    def buscar_usuario_por_codigo(self, codigo: str) -> Optional[Usuario]:
        for usuario in self._usuarios:
            if usuario.codigo == codigo:
                return usuario
        return None

    def buscar_usuario_por_email(self, email: str) -> Optional[Usuario]:
        for usuario in self._usuarios:
            if usuario.email.lower() == email.lower():
                return usuario
        return None

    def listar_usuarios(self) -> List[Usuario]:
        return self._usuarios.copy()

    # Metodos para ventas
    def cargar_ventas(self, ventas: List[Venta]) -> None:
        self._ventas = ventas

    def obtener_ventas(self) -> List[Venta]:
        return self._ventas.copy()

    def realizar_venta(self, usuario_codigo: str, producto_codigo: str, cantidad: int) -> Dict[str, Any]:
        # la relacion principal del sistema es usuario + producto + cantidad
        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            return {"exito": False, "mensaje": "La cantidad debe ser un numero entero."}
        if cantidad <= 0:
            return {"exito": False, "mensaje": "La cantidad debe ser mayor a cero."}

        usuario = self.buscar_usuario_por_codigo(usuario_codigo)
        if not usuario:
            return {"exito": False, "mensaje": "Usuario no encontrado."}

        producto = self.buscar_producto_por_codigo(producto_codigo)
        if not producto:
            return {"exito": False, "mensaje": "Producto no encontrado."}

        if producto.stock < cantidad:
            return {"exito": False, "mensaje": f"Stock insuficiente. Disponible: {producto.stock}"}

        try:
            venta = Venta(usuario_codigo, producto_codigo, cantidad)
            self._ventas.append(venta)
            producto.stock = producto.stock - cantidad
            return {
                "exito": True,
                "mensaje": "Venta realizada exitosamente.",
                "venta": venta
            }
        except ValueError as e:
            return {"exito": False, "mensaje": str(e)}

    def consultar_ventas_por_usuario(self, usuario_codigo: str) -> List[Venta]:
        codigo_normalizado = usuario_codigo.strip().casefold()
        return [
            venta for venta in self._ventas
            if venta.usuario_codigo.strip().casefold() == codigo_normalizado
        ]

    def consultar_ventas_por_producto(self, producto_codigo: str) -> List[Venta]:
        codigo_normalizado = producto_codigo.strip().casefold()
        return [
            venta for venta in self._ventas
            if venta.producto_codigo.strip().casefold() == codigo_normalizado
        ]

    def listar_ventas(self) -> List[Venta]:
        return self._ventas.copy()