from dataclasses import dataclass, replace
from pprint import pprint
from decimal import Decimal
from math import sqrt
import z3


@dataclass(frozen=True)
class Vec3:
    x: Decimal
    y: Decimal
    z: Decimal

    def sum(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)


def read_input(file_name="input.txt"):
    with open(file_name, "r") as f:
        lines = [l.rstrip() for l in f.readlines()]

    hailstones = []
    for line in lines:
        a, b = line.split(" @ ")
        hailstones.append(
            [
                Vec3(*[Decimal(i) for i in a.split(", ")]),
                Vec3(*[Decimal(i) for i in b.split(", ")]),
            ]
        )

    return hailstones


def subtask_1(hailstones):
    lim = (200000000000000, 400000000000000)

    def get_k_b(pos1, pos2):
        k = (pos2.y - pos1.y) / (pos2.x - pos1.x)
        b = (pos2.x * pos1.y - pos2.y * pos1.x) / (pos2.x - pos1.x)
        return k, b

    def get_intersection(k1, b1, k2, b2):
        if k1 == k2:
            return None if b1 != b2 else lim

        x = (-b1 + b2) / (k1 - k2)
        y = x * k1 + b1
        return x, y

    def sign(x):
        return x / abs(x)

    intersect_count = 0

    for i in range(len(hailstones)):
        for j in range(i + 1, len(hailstones)):
            k1, b1 = get_k_b(hailstones[i][0], hailstones[i][0].sum(hailstones[i][1]))
            k2, b2 = get_k_b(hailstones[j][0], hailstones[j][0].sum(hailstones[j][1]))

            intersect = get_intersection(k1, b1, k2, b2)

            if (
                intersect is not None
                and all(lim[0] <= l <= lim[1] for l in intersect)
                and sign(hailstones[i][1].x) == sign(intersect[0] - hailstones[i][0].x)
                and sign(hailstones[i][1].y) == sign(intersect[1] - hailstones[i][0].y)
                and sign(hailstones[j][1].x) == sign(intersect[0] - hailstones[j][0].x)
                and sign(hailstones[j][1].y) == sign(intersect[1] - hailstones[j][0].y)
            ):
                intersect_count += 1

    return intersect_count


def subtask_2(hailstones):
    """
    Eh... this is not satisfying. Also needed to take some inspiration
    from reddit to just plug this into Z3
    """
    x = z3.Real("x")
    y = z3.Real("y")
    z = z3.Real("z")

    dx = z3.Real("dx")
    dy = z3.Real("dy")
    dz = z3.Real("dz")

    solver = z3.Solver()

    i = 0
    for start, dir in hailstones:
        t = z3.Real(f"t_{i}")
        i += 1
        solver.add(x + dx * t == start.x + t * dir.x)
        solver.add(y + dy * t == start.y + t * dir.y)
        solver.add(z + dz * t == start.z + t * dir.z)

    solver.check()
    return solver.model().eval(x + y + z)


def main():
    hailstones = read_input()

    print("Subtask 1:", subtask_1(hailstones))
    print("Subtask 2:", subtask_2(hailstones))


if __name__ == "__main__":
    main()
