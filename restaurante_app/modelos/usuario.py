from typing import Dict, Any
import re
import uuid

class Usuario:
    # esta clase representa a la persona que puede hacer una compra en el sistema
    def __init__(self, nombre: str, email: str, codigo: str = None) -> None:
        self._validar_nombre(nombre)
        self._validar_email(email)
        self._nombre: str = nombre.strip()
        self._email: str = email.strip().lower()
        self._codigo: str = codigo or str(uuid.uuid4())[:8]

    # el nombre debe tener contenido para identificar al usuario
    def _validar_nombre(self, nombre: str) -> None:
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        if len(nombre.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")

    # el correo se valida para evitar datos invalidos y duplicados
    def _validar_email(self, email: str) -> None:
        if not email or not email.strip():
            raise ValueError("El email no puede estar vacío.")
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, email.strip()):
            raise ValueError("El email no tiene un formato válido.")

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._validar_nombre(valor)
        self._nombre = valor.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        self._validar_email(valor)
        self._email = valor.strip().lower()

    @property
    def codigo(self) -> str:
        return self._codigo

    # se transforma el usuario a un formato JSON para guardarlo
    def to_dict(self) -> Dict[str, Any]:
        return {
            "codigo": self._codigo,
            "nombre": self._nombre,
            "email": self._email
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Usuario':
        return cls(
            nombre=data["nombre"],
            email=data["email"],
            codigo=data.get("codigo")
        )

    def __str__(self) -> str:
        return f"Usuario: {self._nombre} | Email: {self._email} | Código: {self._codigo}"