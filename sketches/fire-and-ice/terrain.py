"""A smooth surface through scattered control points: a thin-plate spline, solved and evaluated in the standard
library.

A thin-plate spline is the surface of least bending that passes near every control point, so a flat cluster of
points stays flat, a ring of rising points rises without a crease, and the space between two groups of points is
bridged by one continuous sheet rather than by two edges meeting. `smooth` lets it pass near a point rather than
through it, which is what keeps a cluster of slightly uneven points from rippling.
"""
import math


def _kernel(r2):
    return 0.0 if r2 <= 1e-12 else 0.5 * r2 * math.log(r2)


def fit(points, smooth=0.5, scale=10.0):
    """`points` is a list of (x, z, height). Returns a function of (x, z)."""
    n = len(points)
    xs = [p[0] / scale for p in points]
    zs = [p[1] / scale for p in points]
    size = n + 3
    matrix = [[0.0] * (size + 1) for _ in range(size)]
    for i in range(n):
        row = matrix[i]
        for j in range(n):
            row[j] = _kernel((xs[i] - xs[j]) ** 2 + (zs[i] - zs[j]) ** 2)
        row[i] += smooth
        row[n], row[n + 1], row[n + 2] = 1.0, xs[i], zs[i]
        row[size] = points[i][2]
    for j in range(n):
        matrix[n][j], matrix[n + 1][j], matrix[n + 2][j] = 1.0, xs[j], zs[j]
    for col in range(size):                                  # Gaussian elimination with partial pivoting
        pivot = max(range(col, size), key=lambda r: abs(matrix[r][col]))
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        lead = matrix[col][col]
        if abs(lead) < 1e-12:
            continue
        inverse = 1.0 / lead
        pivot_row = matrix[col]
        for r in range(col + 1, size):
            factor = matrix[r][col] * inverse
            if factor:
                row = matrix[r]
                for c in range(col, size + 1):
                    row[c] -= factor * pivot_row[c]
    solution = [0.0] * size
    for r in range(size - 1, -1, -1):
        total = matrix[r][size] - sum(matrix[r][c] * solution[c] for c in range(r + 1, size))
        solution[r] = total / matrix[r][r] if abs(matrix[r][r]) > 1e-12 else 0.0
    weights, (a0, ax, az) = solution[:n], solution[n:]

    def height(x, z):
        u, v = x / scale, z / scale
        total = a0 + ax * u + az * v
        for k in range(n):
            total += weights[k] * _kernel((u - xs[k]) ** 2 + (v - zs[k]) ** 2)
        return total
    return height
