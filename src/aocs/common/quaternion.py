from collections.abc import Iterator, Sequence
from math import cos, hypot, isclose, sin
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
            f"Quaternion(scalar={self.scalar:.4f}, i={self.i:.4f}, "
            f"j={self.j:.4f}, k={self.k:.4f})"
        )

    def __iter__(self) -> Iterator[int | float]:
        return iter((self.scalar, self.i, self.j, self.k))

    @classmethod
    def from_array(cls, array: list[int | float]) -> "Quaternion":
        return cls(*array)

    @classmethod
    def from_vector(cls, vector: Sequence[int | float]) -> "Quaternion":
        """Create a pure quaternion from a three-component vector."""
        if len(vector) != 3:
            raise ValueError("A vector must have exactly three components.")

        x, y, z = vector
        return cls(0, x, y, z)

    @classmethod
    def from_axis_angle(cls, theta: float, axis: Sequence[int | float]) -> "Quaternion":
        """Create a rotation quaternion from an angle in radians and an axis."""
        if len(axis) != 3:
            raise ValueError("The rotation axis must have exactly three components.")

        x, y, z = axis
        axis_length = hypot(x, y, z)
        if axis_length == 0:
            raise ValueError("The rotation axis must be non-zero.")

        half_theta = theta / 2
        scale = sin(half_theta) / axis_length
        return cls(cos(half_theta), x * scale, y * scale, z * scale)

    def conjugate(self) -> "Quaternion":
        """Return the conjugate of this quaternion."""
        return Quaternion(self.scalar, -self.i, -self.j, -self.k)

    def is_close(
        self,
        other: object,
        *,
        rel_tol: float = 1e-9,
        abs_tol: float = 1e-9,
    ) -> bool:
        """Return whether all components are close within the given tolerances."""
        if not isinstance(other, Quaternion):
            return False

        return all(
            isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)
            for a, b in zip(self, other)
        )

    def __mul__(self, other: object) -> "Quaternion | NotImplementedType":
        if not isinstance(other, Quaternion):
            return NotImplemented

        p0, p1, p2, p3 = self
        q0, q1, q2, q3 = other

        new_scalar = (p0 * q0) - (p1 * q1) - (p2 * q2) - (p3 * q3)
        new_i = (p0 * q1) + (p1 * q0) + (p2 * q3) - (p3 * q2)
        new_j = (p0 * q2) - (p1 * q3) + (p2 * q0) + (p3 * q1)
        new_k = (p0 * q3) + (p1 * q2) - (p2 * q1) + (p3 * q0)

        return Quaternion(new_scalar, new_i, new_j, new_k)
