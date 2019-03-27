import tkinter as tk
import threading as th

from nonogram import Nonogram
from nonogram import Header
from nonogram import NonogramSolver
import nono_db

cell_width = 20
cell_height = 20


class NonogramMain:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("Nonogram")
        self.listbox = tk.Listbox(master, height=20, width=50, selectmode=tk.SINGLE)
        names = nono_db.get_file_names_all()
        for n in names:
            self.listbox.insert(tk.END, n)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar = tk.Scrollbar(master)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox['yscrollcommand'] = self.scrollbar.set
        self.listbox.bind('<Double-1>', selection)

    def run(self):
        self.master.mainloop()


class NonogramSolverView:
    def __init__(self, master: tk.Tk, solver: NonogramSolver,
                 event_next_step: th.Event, event_update: th.Event):
        self.master = master
        self.master.title("Nonogram solver")
        self.solver = solver
        self.event_next_step = event_next_step
        self.event_update = event_update

        # self.frame_header_empty = tk.Frame(self.master, bg='green', height=120, width=100, bd=1)
        # self.frame_header_top = tk.Frame(self.master, bg='red', height=120, width=200, bd=1)
        # self.frame_header_left = tk.Frame(self.master, bg='blue', height=200, width=100, bd=1)
        # self.frame_nonogram_solve = tk.Frame(self.master, bg='yellow', height=200, width=200, bd=1)

        self.frame_header_empty = tk.Frame(self.master)
        self.frame_header_top = tk.Frame(self.master)
        self.frame_header_left = tk.Frame(self.master)
        self.frame_nonogram_solve = tk.Frame(self.master)

        self.frame_header_empty.grid(row=1, column=1)
        self.frame_header_top.grid(row=1, column=2)
        self.frame_header_left.grid(row=2, column=1)
        self.frame_nonogram_solve.grid(row=2, column=2)

        self.canvas_header_empty = tk.Canvas(self.frame_header_empty, bd=0, highlightthickness=0,
                                             width=100, height=120)

        self.canvas_header_top = tk.Canvas(self.frame_header_top, bd=0, highlightthickness=0,
                                           width=100, height=120)
        self.canvas_header_left = tk.Canvas(self.frame_header_left, bd=0, highlightthickness=0)
        self.canvas_solve = tk.Canvas(self.frame_nonogram_solve, bd=0, highlightthickness=0)

        self.canvas_header_empty.pack(fill=tk.BOTH, expand=1)
        self.canvas_header_top.pack(fill=tk.BOTH, expand=1)
        self.canvas_header_left.pack(fill=tk.BOTH, expand=1)
        self.canvas_solve.pack(fill=tk.BOTH, expand=1)

        self.buttonNextStep = tk.Button(self.canvas_header_empty, text='Next step',
                                        command = self.btn_next_step_handler)
        self.buttonNextStep.pack(fill=tk.BOTH, expand=1)

        self.master.after(100, self.process_event)

    def process_event(self):
        if self.event_update.is_set():
            self.event_update.clear()
            self.update()
        self.master.after(100, self.process_event)

    def run(self):
        self.nonogram_solver_draw()
        self.master.mainloop()

    def btn_next_step_handler(self):
        self.event_next_step.set()

    def nonogram_solver_draw(self):
        nonogram = self.solver.nonogram
        if not nonogram:
            print('Nonogram not exist')
        else:
            top_header_len = len(nonogram.header.columns)
            max_column = max(nonogram.header.columns, key=len)
            top_header_height = len(max_column)

            max_row = max(nonogram.header.rows, key=len)
            left_header_width = len(max_row)
            left_header_len = len(nonogram.header.rows)

            empty_width = left_header_width * cell_width
            empty_height = top_header_height * cell_height

            self.canvas_header_empty.delete('all')
            self.canvas_header_empty.config(width=empty_width, height=empty_height)

            self.canvas_header_top.delete('all')
            self.canvas_header_top.config(width=top_header_len * cell_width,
                                          height=empty_height)

            self.canvas_header_left.delete('all')
            self.canvas_header_left.config(width=empty_width,
                                           height=left_header_len*cell_height)

            self.canvas_solve.delete('all')
            self.canvas_solve.config(width=top_header_len*cell_width,
                                     height=left_header_len * cell_height)

            # draw header top
            columns = nonogram.header.columns
            for i in range(top_header_height, 0, -1):
                for j in range(top_header_len):
                    x0 = j * cell_width
                    y0 = (top_header_height - i) * cell_height
                    if len(columns[j]) >= i:
                        cell_data = columns[j][len(columns[j]) - i]
                    else:
                        cell_data = 0

                    self.draw_header_cell(self.canvas_header_top, x0, y0, cell_data)

            # draw header left
            rows = nonogram.header.rows
            for i in range(left_header_len):
                for j in range(left_header_width, 0, -1):
                    x0 = (left_header_width - j) * cell_width
                    y0 = i * cell_height
                    if len(rows[i]) >= j:
                        cell_data = rows[i][len(rows[i]) - j]
                    else:
                        cell_data = 0
                    self.draw_header_cell(self.canvas_header_left, x0, y0, cell_data)

            self.draw_solve()

    def draw_solve(self):
        self.canvas_solve.delete('all')
        answer = self.solver.solvedField
        for i in range(answer.shape[0]):
            for j in range(answer.shape[1]):
                x0 = j * cell_width
                y0 = i * cell_height
                self.draw_nono_cell(self.canvas_solve, x0, y0, answer[i][j])

    def update(self):
        print('Nonogram solver view Update')
        self.draw_solve()

    @staticmethod
    def draw_header_cell(canvas: tk.Canvas, x0, y0, cell_data):
        x1 = x0 + cell_width
        y1 = y0 + cell_height
        canvas.create_rectangle(x0, y0, x1, y1, activeoutline='red',
                                fill='lightgray', outline='black', width=1)
        if cell_data:
            canvas.create_text(x0 + cell_width / 2, y0 + cell_height / 2, fill="darkblue", font=("Times", 11),
                               text=str(cell_data))

    @staticmethod
    def draw_nono_cell(canvas: tk.Canvas, x0, y0, cell_data):
        x1 = x0 + cell_width
        y1 = y0 + cell_height
        # canvas.create_rectangle(x0, y0, x1, y1, activeoutline='red',
        #                         fill='lightgray', outline='black', width=1)
        if cell_data:
            canvas.create_rectangle(x0, y0, x1, y1, activeoutline='red',
                                    fill='black', outline='black', width=1)  # activedash=(5, 4)
        else:
            canvas.create_rectangle(x0, y0, x1, y1, activeoutline='red',
                                    fill='white', outline='black', width=1)  # activedash=(5, 4)


# Nono_window = tk.Tk()
# Canvas_answer = Canvas(Nono_window, bd=0, highlightthickness=0)
# Canvas_answer.pack(fill=BOTH, expand=1)

# Nono_solve_window = Tk()
# Canvas_solve = Canvas(Nono_solve_window, bd=0, highlightthickness=0)
# Canvas_solve.pack(fill=BOTH, expand=1)


def selection(event):
    try:
        print('Select!')
        # index = listbox.curselection()[0]
        # sel_name = listbox.get(index)
        # nono = nono_db.get_nonogram_from_file_name(sel_name)
        # if nono:
        #     nono_draw(Canvas_answer, nono)
        #     # Nonogram_Solver = NonogramSolver(nono, nonogram_solver_change)
        #     nono_solve_draw(Canvas_solve, nono)
    except Exception as e:
        print(e)


def nono_draw(canvas: tk.Canvas, nonogram):
    # print('Nonogram ', end='')
    # nono = nono_db.get_nonogram_from_id(19005)
    # window.pack_forget()
    if not nonogram:
        print('Nonogram not exist')
    # else:
    #     # print('load: ', nonogram.name)
    #
    #     answer = nonogram.answer
    #     ROWS_NUMBER = nonogram.answer.shape[0]
    #     COLUMNS_NUMBER = nonogram.answer.shape[1]
    #     canvas_width = COLUMNS_NUMBER * cell_width + 1
    #     canvas_height = ROWS_NUMBER * cell_height + 1
    #     canvas.delete('all')
    #     canvas.config(width=canvas_width, height=canvas_height)
    #     for i in range(ROWS_NUMBER):
    #         for j in range(COLUMNS_NUMBER):
    #             x0 = j * cell_width
    #             y0 = i * cell_height
    #             x1 = x0 + cell_width
    #             y1 = y0 + cell_height
    #             if answer[i][j]:
    #                 canvas.create_rectangle(x0, y0, x1, y1, activeoutline='red',
    #                                         fill='black', outline='black', width=1)  # activedash=(5, 4)
    #             else:
    #                 canvas.create_rectangle(x0, y0, x1, y1, activeoutline='red',
    #                                         fill='white', outline='black', width=1)  # activedash=(5, 4)


# names = nono_db.get_file_names_all()
# root = Tk()
# listbox = Listbox(root, height=20, width=50, selectmode=SINGLE)
# for n in names:
#     listbox.insert(END, n)
# listbox.pack(side=LEFT, fill=BOTH)
# scrollbar = Scrollbar(root)
# scrollbar.pack(side=RIGHT, fill=Y)
# scrollbar.config(command=listbox.yview)
# listbox['yscrollcommand'] = scrollbar.set
# # selectButton = Button(text='Select', underline=0, command=selection)
# # selectButton.pack()
# listbox.bind('<Double-1>', selection)
# root.mainloop()

def start_solver(solver: NonogramSolver):
    solver.solve()


def main():
    nono = nono_db.get_nonogram_from_id(20566)

    event_next_step = th.Event()
    event_update = th.Event()
    event_stop = th.Event()
    event_next_step.clear()

    nono_solver = NonogramSolver(nono, event_next_step, event_update, event_stop)

    root = tk.Tk()
    nono_solver_win = NonogramSolverView(root, nono_solver, event_next_step, event_update)
    # root.after(1000, start_solver(nono_solver))
    t1 = th.Thread(target=nono_solver.solve)
    t1.start()
    # t1.join()
    nono_solver_win.run()
    event_next_step.set()
    event_stop.set()


if __name__ == "__main__":
    main()
