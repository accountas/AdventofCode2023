from copy import copy
from dataclasses import dataclass


@dataclass
class MapRange:
    source_start: int
    target_start: int
    length: int


@dataclass
class SourceTargetMap:
    type_from: str
    type_to: str
    mappings: list[MapRange]

    def map(this, source):
        for mapping in this.mappings:
            if mapping.source_start <= source <= mapping.source_start + mapping.length - 1:
                return mapping.target_start + source - mapping.source_start
        return source

    def map_range(this, range_start, range_end):
        sorted_mappings = sorted(this.mappings, key=lambda m: m.source_start)

        # Find inclusive ranges list[(start, end)] that are mapped by mappings
        mapped_ranges = [
            (
                max(mapping.source_start, range_start),
                min(mapping.source_start + mapping.length - 1, range_end),
            )
            for mapping in sorted_mappings
            if mapping.source_start <= range_end and mapping.source_start + mapping.length > range_start
        ]

        # Find non mapped ranges (gaps between mapped ranges)
        non_mapped_ranges = []

        if len(mapped_ranges) == 0:
            non_mapped_ranges.append((range_start, range_end))
        else:
            # To find gaps between range start end end
            mapped_ranges_tmp = copy(mapped_ranges)
            mapped_ranges_tmp.append((range_end + 1, range_end + 1))
            mapped_ranges_tmp = [(range_start - 1, range_start - 1)] + mapped_ranges_tmp

            for i in range(len(mapped_ranges_tmp) - 1):
                if mapped_ranges_tmp[i][1] < mapped_ranges_tmp[i + 1][0] - 1:
                    non_mapped_ranges.append((mapped_ranges_tmp[i][1] + 1, mapped_ranges_tmp[i + 1][0] - 1))

        # Apply mapping to the mapped ranges
        mapped_ranges = [(this.map(r[0]), this.map(r[1])) for r in mapped_ranges]

        # Return all ranges (including unmapped ones)
        final_ranges = mapped_ranges + non_mapped_ranges

        return final_ranges


def read_input(file_name="input.txt"):
    with open(file_name, "r") as f:
        lines = [l.rstrip() for l in f.readlines()]
        lines = [l for l in lines if len(l) > 0]

    seeds_line, mapping_lines = lines[0], lines[1:]

    seeds = [int(s) for s in seeds_line.split(":")[1].split()]

    maps = []

    for line in mapping_lines:
        if "map" in line:
            from_type, to_type = line.split()[0].split("-")[::2]
            maps.append(SourceTargetMap(from_type, to_type, []))
        else:
            ranges = [int(i) for i in line.split()]
            maps[-1].mappings.append(MapRange(source_start=ranges[1], target_start=ranges[0], length=ranges[2]))

    return seeds, maps


def subtask_1(seeds, maps):
    min_location = 1e99
    for seed in seeds:
        cur_id = seed
        for map in maps:
            cur_id = map.map(cur_id)
        min_location = min(min_location, cur_id)

    return min_location


def subtask_2(seeds, maps):
    min_location = 1e99
    for i in range(0, len(seeds), 2):
        start, end = seeds[i], seeds[i] + seeds[i + 1]

        ranges = [(start, end)]
        for map in maps:
            new_ranges = []
            for r in ranges:
                new_ranges += map.map_range(r[0], r[1])
            ranges = new_ranges

        min_location = min(min_location, min([r[0] for r in ranges]))

    return min_location


def main():
    seeds, maps = read_input()

    print("Subtask 1:", subtask_1(seeds, maps))
    print("Subtask 2:", subtask_2(seeds, maps))


if __name__ == "__main__":
    main()
