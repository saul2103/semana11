from typing import Dict, Any
from datetime import datetime
import uuid

class Venta:
    # representa la relacion entre un usuario y un producto vendido
    def __init__(self, usuario_codigo: str, producto_codigo: str, cantidad: int, 
                 fecha: str = None, codigo: str = None) -> None:
        self._validar_cantidad(cantidad)
        self._usuario_codigo: str = usuario_codigo
        self._producto_codigo: str = producto_codigo
        self._cantidad: int = cantidad
        self._fecha: str = fecha or datetime.now().isoformat()
        self._codigo: str = codigo or str(uuid.uuid4())[:8]

    # la cantidad vendida debe ser valida para no registrar ventas absurdas
    def _validar_cantidad(self, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        if not isinstance(cantidad, int):
            raise TypeError("La cantidad debe ser un número entero.")

    @property
    def usuario_codigo(self) -> str:
        return self._usuario_codigo

    @property
    def producto_codigo(self) -> str:
        return self._producto_codigo

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @property
    def fecha(self) -> str:
        return self._fecha

    @property
    def codigo(self) -> str:
        return self._codigo

    # se guarda la venta como diccionario para conservarla en JSON
    def to_dict(self) -> Dict[str, Any]:
        return {
            "codigo": self._codigo,
            "usuario_codigo": self._usuario_codigo,
            "producto_codigo": self._producto_codigo,
            "cantidad": self._cantidad,
            "fecha": self._fecha
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Venta':
        return cls(
            usuario_codigo=data["usuario_codigo"],
            producto_codigo=data["producto_codigo"],
            cantidad=int(data["cantidad"]),
            fecha=data.get("fecha"),
            codigo=data.get("codigo")
        )

    def __str__(self) -> str:
        return f"Venta #{self._codigo} | Usuario: {self._usuario_codigo} | Producto: {self._producto_codigo} | Cantidad: {self._cantidad} | Fecha: {self._fecha}"