from collections.abc import Iterator
from types import NotImplementedType


class Quaternion:
    def __init__(
        self,
        scalar: float,
        i: float,
        j: float,
        k: float,
    ) -> None:
        self.scalar = scalar
        self.i = i
        self.j = j
        self.k = k

    def __repr__(self) -> str:
        return (
            f"Quaternion(scalar={self.scalar!r}, i={self.i!r}, "
            f"j={self.j!r}, k={self.k!r})"
        )

    def __iter__(self) -> Iterator[int | float]:
        return iter((self.scalar, self.i, self.j, self.k))

    @classmethod
    def from_array(cls, array: list[int | float]) -> "Quaternion":
        return cls(*array)

    def conjugate(self) -> "Quaternion":
        """Return the conjugate of this quaternion."""
        return Quaternion(self.scalar, -self.i, -self.j, -self.k)

    def __mul__(
        self, other: object
    ) -> "Quaternion | NotImplementedType":
        if not isinstance(other, Quaternion):
            return NotImplemented

        p0, p1, p2, p3 = self
        q0, q1, q2, q3 = other

        new_scalar = (p0 * q0) - (p1 * q1) - (p2 * q2) - (p3 * q3)
        new_i = (p0 * q1) + (p1 * q0) + (p2 * q3) - (p3 * q2)
        new_j = (p0 * q2) - (p1 * q3) + (p2 * q0) + (p3 * q1)
        new_k = (p0 * q3) + (p1 * q2) - (p2 * q1) + (p3 * q0)

        return Quaternion(new_scalar, new_i, new_j, new_k)
