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
    solvedField: ndarray
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
        for cell in row:
            self.row.append(cell)


class SolverHeader:
    def __init__(self, header: Header):
        self.rows = self.create_solve_rows(header.rows)
        self.columns = self.create_solve_rows(header.columns)

    @staticmethod
    def create_solve_rows(nono_rows: list)-> list:
        solve_rows = []
        for c in nono_rows:
            solve_rows.append(SolverRow(c))
        return solve_rows


class NonogramSolver:
    def __init__(self, nonogram: Nonogram, event_wait: th.Event,
                 event_change: th.Event, event_stop: th.Event):
        self.nonogram = nonogram
        self.event_stop = event_stop
        self.event_wait = event_wait
        self.event_change = event_change
        self.solveHeader = SolverHeader(nonogram.header)
        self.solvedField = np.full((len(nonogram.header.rows), len(nonogram.header.columns)), 0)

    def solve(self):
        # self.event_wait.wait()
        while not self.event_stop.is_set():
            # не работает без этой строчки
            time.sleep(1)

            is_changed = 0
            is_changed += self.check_rows(self.solveHeader.rows)
            is_changed += self.check_rows(self.solveHeader.columns)
            # TODO: придумать, что делать, если решать больше нечего
            if not is_changed:
                pass

            print('Solver step')
            self.update()
        else:
            print('Solver stop')

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

    def update(self):
        if self.event_change:
            self.event_change.set()

# print("max header row len =", max_header_row_len)
# print("max header column len =", maxHeaderColumnLen)

# for i in range(maxHeaderColumnLen, 0, -1):
#     s = ' ' * 3 * max_header_row_len + "|"
#     for column in header_columns:
#         if len(column) >= i:
#             j = column[len(column) - i]
#             if j > 9:
#                 s += str(j) + '|'
#             else:
#                 s += ' ' + str(j) + '|'
#         else:
#             s += '  |'
#     print(s)
#
# for r in header_rows:
#     s = "|"
#     for j in r:
#         if j > 9:
#             s += str(j) + '|'
#         else:
#             s += ' ' + str(j) + '|'
#     for f in range(len(r), max_header_row_len):
#         print('|  ', end='')
#     print(s)
