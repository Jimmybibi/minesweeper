from tkinter import Button, Label
import random
import settings
import ctypes
import sys


class Cell:
    all = []
    cell_count_label = None
    cell_count = settings.CELL_COUNT
    number_of_mines = None

    def __init__(self, x, y, is_mine=False) -> None:
        self.is_mine = is_mine
        self.is_open = False
        self.cell_btn_object = None
        self.x = x
        self.y = y
        self.is_mine_candidate = False
        # Append instances to the Cell.all list
        Cell.all.append(self)

    def create_btn_obj(self, location):
        btn = Button(location, width="10", height="4")
        btn.bind("<Button-1>", self.left_click_actions)  # left click
        btn.bind("<Button-3>", self.right_click_actions)  # right click
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        label = Label(
            location,
            text=f"Cells Left: {Cell.cell_count}",
            bg="black",
            fg="white",
            width=12,
            height=4,
            font=("", 30),
        )
        Cell.cell_count_label = label

    @staticmethod
    def create_number_of_mines_label(location):
        mines_count = Label(
            location,
            text=f"Mines: {settings.MINES_COUNT}",
            bg="black",
            fg="white",
            width=12,
            height=4,
            font=("", 30),
        )
        Cell.number_of_mines = mines_count

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_number == 0:
                for cell_object in self.surrounded_cells:
                    cell_object.show_cell()
            self.show_cell()
            # Logic for winning the game i.e. when Mines count equals number of cells left.
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(
                    0, "Congratulations!\n You won the game.", "Winner!!!", 0
                )
                sys.exit()

        # cancel left click and events if the cell is already open
        self.cell_btn_object.unbind("<Button-1>")
        self.cell_btn_object.unbind("<Button-3>")

    def get_cell_by_axis(self, x, y) -> object:
        # Return a cell object based on the value of the x and y axis given.
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self) -> list:
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1),
        ]
        cells = [cell for cell in cells if cell]
        return cells

    @property
    def surrounded_cells_mines_number(self) -> int:
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1
        return counter

    def show_cell(self):
        if not self.is_open:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_number)
            if Cell.cell_count_label:
                Cell.cell_count_label.configure(text=f"Cells Left: {Cell.cell_count}")
        self.is_open = True
        # Change the colour of the cell back to default anytime it is left clicked if it was initially
        # right-clicked and labeled a mine candidate
        self.cell_btn_object.configure(bg="SystemButtonFace")

    def show_mine(self):
        self.cell_btn_object.configure(bg="red")
        ctypes.windll.user32.MessageBoxW(0, "You clicked on a mine!", "Game Over", 0)
        sys.exit()

    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(bg="orange")
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(bg="SystemButtonFace")
            self.is_mine_candidate = False

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all, settings.MINES_COUNT)
        for cell in picked_cells:
            cell.is_mine = True
        return picked_cells

    def __repr__(self) -> str:
        return f"Cell({self.x}, {self.y})"
