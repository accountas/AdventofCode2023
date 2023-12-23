from dataclasses import dataclass


@dataclass(frozen=True)
class Vec3:
    x: int
    y: int
    z: int

    def sum(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def diff(self, other):
        return self.sum(Vec3(-other.x, -other.y, -other.z))

    def i_norm(self):
        return Vec3(
            self.x // abs(self.x) if self.x != 0 else 0,
            self.y // abs(self.y) if self.y != 0 else 0,
            self.z // abs(self.z) if self.z != 0 else 0,
        )


DIR_DOWN = Vec3(0, 0, -1)
DIR_UP = Vec3(0, 0, 1)


def read_input(file_name="input.txt"):
    with open(file_name, "r") as f:
        lines = [l.rstrip() for l in f.readlines()]

    bricks = []
    for line in lines:
        a, b = line.split("~")
        bricks.append(
            [
                Vec3(*[int(i) for i in a.split(",")]),
                Vec3(*[int(i) for i in b.split(",")]),
            ]
        )

    return bricks


def brick_iter(brick):
    dir = brick[1].diff(brick[0]).i_norm()
    cur_pos = brick[0]

    yield cur_pos
    while cur_pos != brick[1]:
        cur_pos = cur_pos.sum(dir)
        yield cur_pos


def compute_occupied_cubes(bricks):
    occupied = {}

    for idx, brick in enumerate(bricks):
        for pos in brick_iter(brick):
            occupied[pos] = idx

    return occupied


def drop_bricks(bricks):
    occupied = compute_occupied_cubes(bricks)

    while True:
        any_brick_fell = False

        for idx, brick in enumerate(bricks):
            while True:
                can_fall = True
                for pos in brick_iter(brick):
                    down = pos.sum(DIR_DOWN)
                    if down in occupied and occupied[down] != idx or pos.z < 0:
                        can_fall = False
                        break
                if can_fall:
                    for pos in brick_iter(brick):
                        occupied.pop(pos)
                    brick[0] = brick[0].sum(DIR_DOWN)
                    brick[1] = brick[1].sum(DIR_DOWN)
                    for pos in brick_iter(brick):
                        occupied[pos] = idx
                        any_brick_fell = True
                else:
                    break

        if not any_brick_fell:
            break


def main():
    bricks = read_input()
    bricks = sorted(bricks, key=lambda b: min(b[0].z, b[1].z))

    drop_bricks(bricks)

    occupied = compute_occupied_cubes(bricks)

    supported_by = {i: set() for i in range(len(bricks))}
    supports = {i: set() for i in range(len(bricks))}

    for idx, brick in enumerate(bricks):
        for pos in brick_iter(brick):
            down = pos.sum(DIR_DOWN)
            up = pos.sum(DIR_UP)

            if occupied.get(down, idx) != idx:
                supported_by[idx].add(occupied[down])

            if occupied.get(up, idx) != idx:
                supports[idx].add(occupied[up])

    def fall_count_on_destroy(brick_idx, destroyed):
        count = 0
        destroyed.add(brick_idx)
        for supported_brick in supports[brick_idx] - destroyed:
            if len(supported_by[supported_brick] - destroyed) == 0:
                count += 1
                count += fall_count_on_destroy(supported_brick, destroyed)

        return count

    safe_to_destroy = 0
    number_of_falls = 0

    for brick_idx in range(len(bricks)):
        count = fall_count_on_destroy(brick_idx, set())

        print(count)
        if count == 0:
            safe_to_destroy += 1
        else:
            number_of_falls += count

    print("Subtask 1:", safe_to_destroy)
    print("Subtask 2:", number_of_falls)


if __name__ == "__main__":
    main()
