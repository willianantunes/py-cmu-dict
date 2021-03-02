import csv
import pathlib


def number_of_lines(file_name: str) -> int:
    with open(file_name, mode="r") as file:
        return sum(1 for row in csv.reader(file))


def each_row_from_file(file_name: str) -> str:
    with open(file_name, mode="r") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            yield row
