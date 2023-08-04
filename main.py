from tkinter import *
from cell import Cell
import settings
import utils


def main():
    root = Tk()
    # Override the settings of the window.
    root.configure(bg="black")
    root.geometry(f"{settings.WIDTH}x{settings.HEIGHT}")
    root.title("Minesweeper")
    root.resizable(False, False)

    top_frame = Frame(
        root,
        bg="black",
        width=settings.WIDTH,
        height=utils.height_pct(20),
    )
    top_frame.place(x=0, y=0)
    game_title = Label(
        top_frame, bg="black", fg="white", text="Minesweeper", font=("", 48)
    )
    game_title.place(x=utils.width_pct(30), y=0)
    left_frame = Frame(
        root,
        bg="black",
        width=utils.width_pct(25),
        height=utils.height_pct(80),
    )
    left_frame.place(x=0, y=utils.height_pct(20))

    center_frame = Frame(
        root,
        bg="black",
        width=utils.width_pct(75),
        height=utils.height_pct(80),
    )

    center_frame.place(x=utils.width_pct(25), y=utils.height_pct(20))

    for x in range(settings.GRID_SIZE):
        for y in range(settings.GRID_SIZE):
            c = Cell(x, y)
            c.create_btn_obj(center_frame)
            c.cell_btn_object.grid(row=x, column=y)

    # Call the label from the cell class
    Cell.create_cell_count_label(left_frame)
    Cell.cell_count_label.place(x=0, y=0)
    Cell.create_number_of_mines_label(left_frame)
    Cell.number_of_mines.place(x=0, y=utils.height_pct(20))

    Cell.randomize_mines()

    # Run window
    root.mainloop()


if __name__ == "__main__":
    main()
