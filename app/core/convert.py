from math import floor
from typing import Self


class Storage:
    _K2B = 10**3
    _KI2B = 2 ** 10
    _M2B = 10**6
    _MI2B = 2 ** 20
    _G2B = 10**9
    _GI2B = 2 ** 30
    _T2B = 10**12
    _TI2B = 2 ** 40

    _b: int

    def __init__(
        self,
        *,
        tebibytes: int = 0,
        terabytes: int = 0,
        gibibytes: int = 0,
        gigabytes: int = 0,
        mebibytes: int = 0,
        megabytes: int = 0,
        kibibytes: int = 0,
        kilobytes: int = 0,
        bytes: int = 0
    ):
        self._b = floor(
            tebibytes * self._TI2B
            +
            terabytes * self._T2B
            +
            gibibytes * self._GI2B
            +
            gigabytes * self._G2B
            +
            mebibytes * self._MI2B
            +
            megabytes * self._M2B
            +
            kibibytes * self._KI2B
            +
            kilobytes * self._K2B
            +
            bytes
        )

    @classmethod
    def empty(cls) -> Self:
        return cls()

    @property
    def bytes(self) -> float:
        return self._b

    @property
    def kilobytes(self) -> float:
        return self._b / self._K2B

    @property
    def kibibytes(self) -> float:
        return self._b / self._KI2B

    @property
    def megabytes(self) -> float:
        return self._b / self._M2B

    @property
    def mebibytes(self) -> float:
        return self._b / self._MI2B

    @property
    def gigabytes(self) -> float:
        return self._b / self._G2B

    @property
    def gibibytes(self) -> float:
        return self._b / self._GI2B

    @property
    def terabytes(self) -> float:
        return self._b / self._T2B

    @property
    def tebibytes(self) -> float:
        return self._b / self._TI2B
    

storage = Storage
    
    