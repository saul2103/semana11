from typing import Dict, Any
import uuid

class Producto:
    # esta clase guarda la info base de cada producto y valida que todo este en orden
    def __init__(self, nombre: str, precio: float, categoria: str, stock: int, codigo: str = None) -> None:
        self._validar_nombre(nombre)
        self._validar_precio(precio)
        self._validar_categoria(categoria)
        self._validar_stock(stock)
        self._nombre: str = nombre
        self._precio: float = precio
        self._categoria: str = categoria
        self._stock: int = stock
        self._codigo: str = codigo or str(uuid.uuid4())[:5]

    # se revisa que el nombre tenga texto y no quede vacio
    def _validar_nombre(self, nombre: str) -> None:
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        if len(nombre.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")

    # el precio debe ser real y mayor que cero para que no haya valores invalidos
    def _validar_precio(self, precio: float) -> None:
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0.")
        if not isinstance(precio, (int, float)):
            raise TypeError("El precio debe ser un número.")

    # la categoria necesita estar dentro de las opciones del restaurante
    def _validar_categoria(self, categoria: str) -> None:
        if not categoria or not categoria.strip():
            raise ValueError("La categoría no puede estar vacía.")
        categorias_validas = ["entrada", "plato fuerte", "bebida", "postre"]
        if categoria.strip().lower() not in categorias_validas:
            raise ValueError(f"Categoría inválida. Debe ser una de: {categorias_validas}")

    # el stock no puede quedar en negativo, por eso se valida aqui
    def _validar_stock(self, stock: int) -> None:
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        if not isinstance(stock, int):
            raise TypeError("El stock debe ser un número entero.")

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._validar_nombre(valor)
        self._nombre = valor.strip()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        self._validar_precio(valor)
        self._precio = float(valor)

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        self._validar_categoria(valor)
        self._categoria = valor.strip().lower()

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        self._validar_stock(valor)
        self._stock = int(valor)

    @property
    def codigo(self) -> str:
        return self._codigo

    # conversion a diccionario para que se pueda guardar en JSON sin perder la estructura
    def to_dict(self) -> Dict[str, Any]:
        return {
            "codigo": self._codigo,
            "nombre": self._nombre,
            "precio": self._precio,
            "categoria": self._categoria,
            "stock": self._stock
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Producto':
        return cls(
            nombre=data["nombre"],
            precio=float(data["precio"]),
            categoria=data["categoria"],
            stock=int(data["stock"]),
            codigo=data.get("codigo")
        )

    def __str__(self) -> str:
        return f"Producto: {self._nombre} | Precio: ${self._precio:.2f} | Categoría: {self._categoria} | Stock: {self._stock} | Código: {self._codigo}"