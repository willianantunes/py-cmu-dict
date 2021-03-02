def number_of_lines(file_name: str) -> int:
    with open(file_name, mode="r") as file:
        return sum(1 for line in file)


def each_line_from_file(file_name: str) -> str:
    with open(file_name, mode="r") as file:
        for line in file:
            yield line
