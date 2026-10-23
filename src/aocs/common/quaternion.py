from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Quaternion:
    scalar: int | float
    i: int | float
    j: int | float
    k: int | float

    def __iter__(self) -> Iterator[int | float]:
        return iter((self.scalar, self.i, self.j, self.k))

    @classmethod
    def from_array(cls, array: list[int | float]) -> "Quaternion":
        return cls(*array)


def product(p: Quaternion, q: Quaternion) -> Quaternion:
    """Return the Hamilton product p * q."""
    p0, p1, p2, p3 = p
    q0, q1, q2, q3 = q

    new_scalar = (p0 * q0) - (p1 * q1) - (p2 * q2) - (p3 * q3)
    new_i = (p0 * q1) + (p1 * q0) + (p2 * q3) - (p3 * q2)
    new_j = (p0 * q2) - (p1 * q3) + (p2 * q0) + (p3 * q1)
    new_k = (p0 * q3) + (p1 * q2) - (p2 * q1) + (p3 * q0)

    return Quaternion(new_scalar, new_i, new_j, new_k)
