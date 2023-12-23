from enum import Enum
from collections import deque
from math import lcm
from copy import deepcopy


class Pulse(Enum):
    LOW = 0
    HIGH = 1
    NONE = 2


class Broadcaster:
    def __init__(self, children):
        self.children = children


class FlipFlop:
    def __init__(self, children):
        self._on = False
        self.children = children

    def receive_and_send(self, sender, pulse):
        if pulse == Pulse.LOW:
            self._on = not self._on
            return Pulse.HIGH if self._on else Pulse.LOW
        else:
            return Pulse.NONE


class Conjunction:
    def __init__(self, children):
        self.children = children
        self._parent_states = {}

    def add_parent(self, module):
        self._parent_states[module] = Pulse.LOW

    def receive_and_send(self, sender, pulse):
        self._parent_states[sender] = pulse

        if all(p == Pulse.HIGH for p in self._parent_states.values()):
            return Pulse.LOW
        else:
            return Pulse.HIGH


def read_input(file_name="input.txt"):
    with open(file_name, "r") as file:
        lines = [l.rstrip() for l in file]

    modules = {}
    for line in lines:
        module, children = line.split(" -> ")
        children = children.split(", ")

        if module[0] == "%":
            modules[module[1:]] = FlipFlop(children)
        elif module[0] == "&":
            modules[module[1:]] = Conjunction(children)
        elif module == "broadcaster":
            modules[module] = Broadcaster(children)
        else:
            raise NotImplemented("Module not supported")

    for module_name, module in modules.items():
        for child in module.children:
            if child in modules and isinstance(modules[child], Conjunction):
                modules[child].add_parent(module_name)

    return modules


def press_button(modules):
    pulse_queue = deque()

    all_pulses = []

    for child in modules["broadcaster"].children:
        pulse_queue.append((child, "broadcaster", Pulse.LOW))

    while len(pulse_queue) > 0:
        module, sender, pulse = pulse_queue.popleft()

        all_pulses.append((module, sender, pulse))

        if module not in modules:
            continue

        output = modules[module].receive_and_send(sender, pulse)

        if output == Pulse.NONE:
            continue

        for child in modules[module].children:
            pulse_queue.append((child, module, output))

    return all_pulses


def subtask_1(modules):
    times = 1000

    pulse_counts = {Pulse.LOW: times, Pulse.HIGH: 0}

    for _ in range(times):
        pulses = press_button(modules)
        for pulse in pulses:
            pulse_counts[pulse[2]] += 1

    return pulse_counts[Pulse.HIGH] * pulse_counts[Pulse.LOW]


def print_edges(modules):
    def verbose_name(name, module):
        if isinstance(module, Conjunction):
            return "AND_" + name

        if isinstance(module, FlipFlop):
            return "FLIP_" + name

        return name

    for module_name, module in modules.items():
        for child in module.children:
            a = verbose_name(module_name, module)
            b = verbose_name(child, modules.get(child))
            print(a, "->", b)


def subtask_2(modules):
    periods = {"jm": None, "rh": None, "jg": None, "hf": None}
    for i in range(1, 1000000):
        pulses = press_button(modules)
        for pulse in pulses:
            for module, period in periods.items():
                if period is not None:
                    continue

                for pulse in pulses:
                    if pulse[1] == module and pulse[2] == Pulse.HIGH:
                        periods[module] = i

        if all(p is not None for p in periods.values()):
            break

    return lcm(*periods.values())


def main():
    modules = read_input()

    # Put this into GraphViz, needed for subtask 2
    print_edges(modules)

    print("Subtask 1:", subtask_1(deepcopy(modules)))
    print("Subtask 2:", subtask_2(deepcopy(modules)))


if __name__ == "__main__":
    main()
