from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

DELTA_T = 0.1  # seconds
MASS = 1.0  # kg
SIDE = 10.0  # cm
TAU = 0.01  # Nm

I = (1 / 6) * MASS * (SIDE * SIDE)  # kgms^2
ALPHA = TAU / I  # rads^2


def rotation_matrix(theta: float) -> np.ndarray:
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=float)


def rotate_square(theta: float, square: np.ndarray) -> np.ndarray:
    return (rotation_matrix(theta) @ square.T).T


base_square = np.array(
    [
        (-SIDE, SIDE),
        (SIDE, SIDE),
        (SIDE, -SIDE),
        (-SIDE, -SIDE),
    ],
    dtype=float,
)

omega = 0.0
theta = 0.0
time_s = 0.0
frames = []
current_square = base_square.copy()

for _ in range(100):
    current_square = rotate_square(theta, current_square)
    frames.append((time_s, theta, omega, current_square.copy()))
    time_s = time_s + DELTA_T
    theta = theta + (omega * DELTA_T)
    omega = omega + (ALPHA * DELTA_T)


fig, ax = plt.subplots(figsize=(7, 7))
ax.set_aspect("equal")
ax.set_xlim(-15, 15)
ax.set_ylim(-15, 15)
ax.set_title("Rotating square")
ax.set_xlabel("x")
ax.set_ylabel("y")

(line,) = ax.plot([], [], "o-", lw=2, color="tab:blue")
text = ax.text(0.02, 0.96, "", transform=ax.transAxes, va="top")


def update(frame_index: int):
    time_s, theta, omega, square = frames[frame_index]
    rotated = np.vstack([square, square[0]])
    line.set_data(rotated[:, 0], rotated[:, 1])
    text.set_text(
        f"t = {time_s:.1f} s\ntheta = {theta:.2f} rad\nomega = {omega:.4f} rad/s"
    )
    return line, text


animation = FuncAnimation(fig, update, frames=len(frames), interval=50, blit=False)
output_dir = Path(__file__).resolve().parents[1] / "output"
output_dir.mkdir(parents=True, exist_ok=True)
animation.save(output_dir / "square_rotation.gif", writer=PillowWriter(fps=24))
plt.close(fig)
print(f"Saved animated square rotation to {output_dir / 'square_rotation.gif'}")
