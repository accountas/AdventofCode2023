from math import ceil, floor, sqrt


def read_input(file_name="input.txt"):
    with open(file_name, "r") as f:
        lines = f.readlines()

    times = [int(t) for t in lines[0].split(":")[1].split()]
    distances = [int(t) for t in lines[1].split(":")[1].split()]

    return times, distances


def number_of_ways_to_win(time, distance):
    """
    distance_traveled = t_press * (t_race - t_press)
    distance_traveled > d_race
    t_press * (t_race - t_press) > d_race
    find min and max of t_press (neg parabola)
    - t_press^2 + t_race * t_press - d_race = 0
    t_press = 0.5(+- sqrt(t_race^2 - 4*d_race) + t_race)
    """

    distance += 1
    min_press = 0.5 * (-sqrt(time**2 - 4 * distance) + time)
    min_press = ceil(max(0, min_press))

    max_press = 0.5 * (+sqrt(time**2 - 4 * distance) + time)
    max_press = floor(min(time - 1, max_press))

    return max_press - min_press + 1


def subtask_1(times, distances):
    answer = 1

    for t, d in zip(times, distances):
        answer *= number_of_ways_to_win(t, d)

    return answer


def subtask_2(times, distances):
    time = int("".join([str(i) for i in times]))
    distance = int("".join([str(i) for i in distances]))

    return number_of_ways_to_win(time, distance)


def main():
    times, distances = read_input()

    print("Subtask 1:", subtask_1(times, distances))
    print("Subtask 12", subtask_2(times, distances))


if __name__ == "__main__":
    main()
