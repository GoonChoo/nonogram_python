import numpy as np
import threading as th
import time


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
        self.solvedField = np.full((len(header.rows), len(header.columns)), 0)


class NonogramSolver:
    def __init__(self, nonogram: Nonogram, event_wait: th.Event,
                 event_change: th.Event, event_stop: th.Event):
        self.nonogram = nonogram
        self.event_stop = event_stop
        self.event_wait = event_wait
        self.event_change = event_change

    def solve(self):
        # self.event_wait.wait()
        while not self.event_stop.is_set():
            time.sleep(1)
            if self.event_wait.wait():
                self.event_wait.clear()
                print('Solver step')
                self.nonogram.solvedField[2][2] = not self.solvedField[2][2]
                self.update()

            # self.event_wait.wait()
            # self.event_wait.clear()
            # self.solvedField[2][2] = not self.solvedField[2][2]
            # self.update()
            # print('Solver step')
        else:
            print('Solver stop')

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
