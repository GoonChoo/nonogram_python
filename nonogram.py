import numpy as np
import threading as th
import time

from numpy.core.multiarray import ndarray


class Header:
    rows = []
    columns = []

    def __init__(self, r, c):
        self.rows = r
        self.columns = c


class Nonogram:
    header = Header
    name = ''

    def __init__(self, nono_id, name: str, header: Header, answer):
        self.header = header
        self.answer = answer
        self.name = name
        self.id = nono_id


class SolverRow:
    is_changed = True
    row = []

    def __init__(self, row: list):
        self.row = list(row)

    def __len__(self):
        return len(self.row)

    def __iter__(self):
        return iter(self.row)

    def __getitem__(self, item):
        return self.row[item]


class SolverHeader:
    def __init__(self, header: Header):
        self.rows = self.create_solve_rows(header.rows)
        self.columns = self.create_solve_rows(header.columns)

    @staticmethod
    def create_solve_rows(rows: list)-> list:
        return [SolverRow(row) for row in rows]


class NonogramSolver:
    solvedField: ndarray

    def __init__(self, nonogram: Nonogram):
        self.nonogram = nonogram
        self.solveHeader = SolverHeader(nonogram.header)
        self.solvedField = np.full((len(nonogram.header.rows), len(nonogram.header.columns)), 0)

    def solve_step(self):
        is_changed = False
        is_changed += self.check_rows(self.solveHeader.rows)
        is_changed += self.check_rows(self.solveHeader.columns)
        # TODO: придумать, что делать, если решать больше нечего
        if not is_changed:
            pass

    def check_rows(self, rows: SolverRow)-> bool:

        is_solved = False
        for row in self.solveHeader.rows:
            if row.is_changed:
                # Если в строке есть измененеия, то отдать ее на обработку
                self.row_process(row)
                is_solved = False
        return is_solved

    @staticmethod
    def row_process(row: SolverRow):
        """Применить к строке методы решения"""
        # TODO: тут происходит вызов всех методов решения

    def overlap(self):
        pass