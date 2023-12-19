from dataclasses import dataclass
from copy import deepcopy


@dataclass(frozen=True)
class Part:
    x: int
    m: int
    a: int
    s: int

    @staticmethod
    def from_string(description):
        description = description[1:-1]
        properties = {
            prop.split("=")[0]: int(prop.split("=")[1])
            for prop in description.split(",")
        }
        return Part(**properties)


@dataclass(frozen=True)
class Rule:
    check_property: str
    check_type: str
    check_value: int
    success_target: str

    def accepts(self, part):
        return eval(f"part.{self.check_property} {self.check_type} {self.check_value}")

    @staticmethod
    def from_string(description):
        operation, target = description.split(":")
        return Rule(
            check_property=operation[0],
            check_type=operation[1],
            check_value=int(operation[2:]),
            success_target=target,
        )


@dataclass(frozen=True)
class Workflow:
    name: str
    target: str
    rules: list[Rule]

    @staticmethod
    def from_string(description):
        name, rules_desc = description.split("{")

        rules_desc = rules_desc[:-1].split(",")

        rules = [Rule.from_string(rule_desc) for rule_desc in rules_desc[:-1]]

        return Workflow(name=name, target=rules_desc[-1], rules=rules)

    def get_result(self, part):
        for rule in self.rules:
            if rule.accepts(part):
                return rule.success_target
        return self.target


def read_input(file_name="input.txt"):
    with open(file_name, "r") as f:
        lines = [l.rstrip() for l in f.readlines()]

    workflows = {}
    parts = []

    is_workflow = True
    for line in lines:
        if line == "":
            is_workflow = False
            continue

        if is_workflow:
            workflow = Workflow.from_string(line)
            workflows[workflow.name] = workflow
        else:
            parts.append(Part.from_string(line))

    return workflows, parts


def subtask_1(workflows, parts):
    rejected_sum = 0

    for part in parts:
        cur_workflow = "in"

        while cur_workflow not in ("A", "R"):
            cur_workflow = workflows[cur_workflow].get_result(part)

        if cur_workflow == "A":
            rejected_sum += part.a + part.x + part.m + part.s

    return rejected_sum


def subtask_2(workflows):
    constrained = []

    def walk_with_constrains(cur_workflow, constrains):
        nonlocal constrained
        negative_constrains = deepcopy(constrains)

        if cur_workflow == "A":
            constrained.append(negative_constrains)
            return

        if cur_workflow == "R":
            return

        for rule in workflows[cur_workflow].rules:
            positive_constrains = deepcopy(negative_constrains)

            if rule.check_type == ">":
                positive_constrains[rule.check_property][0] = max(
                    positive_constrains[rule.check_property][0], rule.check_value + 1
                )
                negative_constrains[rule.check_property][1] = min(
                    positive_constrains[rule.check_property][1], rule.check_value
                )
            else:
                positive_constrains[rule.check_property][1] = min(
                    positive_constrains[rule.check_property][1], rule.check_value - 1
                )
                negative_constrains[rule.check_property][0] = max(
                    positive_constrains[rule.check_property][0], rule.check_value
                )

            walk_with_constrains(rule.success_target, positive_constrains)

        walk_with_constrains(workflows[cur_workflow].target, negative_constrains)

    walk_with_constrains("in", {p: [1, 4000] for p in "xmas"})

    answer = 0
    for constrain in constrained:
        constrain_total = 1
        for range_min, range_max in constrain.values():
            constrain_total *= max(0, range_max - range_min + 1)
        answer += constrain_total

    return answer


def main():
    workflows, parts = read_input()

    print("Subtask 1:", subtask_1(workflows, parts))
    print("Subtask 2:", subtask_2(workflows))


if __name__ == "__main__":
    main()
