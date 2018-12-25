from tkinter import *
from tkinter import Tk
from pathlib import Path
from tkinter.filedialog import askopenfilename
from PIL import Image
import time
from mazes import Maze
from factory import SolverFactory
import os
import fnmatch
import shutil

# Read command line arguments - the python argparse class is convenient here.
import argparse

global new_folder_name
new_folder_name = "/Solved/"

window = Tk()
window.title("Maze Solver")
lbl = Label(window, text="Please select a Maze file")
lbl.grid(column=0, row=0)
lbl2 = Label(window, text="")
lbl2.grid(column=0, row=1)
textbox=Text(window)
textbox.grid()

def solve(factory, method, input_file, output_file):
    # Load Image
    print("Loading Image")
    im = Image.open(input_file)

    # Create the maze (and time it) - for many mazes this is more time consuming than solving the maze
    print("Creating Maze")
    t0 = time.time()
    maze = Maze(im)
    t1 = time.time()
    print("Node Count:", maze.count)
    total = t1-t0
    print("Time elapsed:", total, "\n")

    # Create and run solver
    [title, solver] = factory.createsolver(method)
    print("Starting Solve:", title)

    t0 = time.time()
    [result, stats] = solver(maze)
    t1 = time.time()

    total = t1-t0

    # print solve stats
    print("Nodes explored: ", stats[0])
    if (stats[2]):
        print("Path found, length", stats[1])
    else:
        print("No Path Found")
    print("Time elapsed: ", total, "\n")

    """
    Create and save the output image.
    This is simple drawing code that travels between each node in turn, drawing either
    a horizontal or vertical line as required. Line colour is roughly interpolated between
    blue and red depending on how far down the path this section is.
    """

    print("Saving Image")
    im = im.convert('RGB')
    impixels = im.load()

    resultpath = [n.Position for n in result]

    length = len(resultpath)

    for i in range(0, length - 1):
        a = resultpath[i]
        b = resultpath[i+1]

        """
        Blue - red
        r = int((i / length) * 255)
        px = (r, 0, 255 - r)

        Teal - Green
        r = int((i / length) * 255)
        px = (0, 255, 255 - r)

        """

        r = int((i / length) * 255)
        px = (0, 255, 255 - r)

        if a[0] == b[0]:
            # Ys equal - horizontal line
            for x in range(min(a[1], b[1]), max(a[1], b[1])):
                impixels[x, a[0]] = px
        elif a[1] == b[1]:
            # Xs equal - vertical line
            for y in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
                impixels[a[1], y] = px

    im.save(output_file)

def open_file():
    textbox.delete(1.0,END)
    global input_file
    input_file = askopenfilename()
    res = os.path.basename(input_file)
    lbl.configure(text="You chose:")
    lbl2.configure(text=res)


def execute():
    file_name = os.path.basename(input_file)
    dir_name = os.path.dirname(input_file)
    out_folder = os.path._getfullpathname(dir_name + new_folder_name)
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)
    else:
        print("")
    global output_file
    output_file = os.path.join(out_folder + file_name)
    args = parser.parse_args()
    solve(sf, args.method, input_file, output_file)

def main():
    btn = Button(window, text="Open File", command=open_file)
    btn.grid(column=1, row=0)
    Go = Button(window, text="Go", command=execute)
    Go.grid(column=1, row=1)
    global sf
    sf = SolverFactory()
    global parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--method", nargs='?', const=sf.Default, default=sf.Default,
                        choices=sf.Choices)
    window.mainloop()
    
def redirector(inputStr):
    textbox.insert(INSERT, inputStr)

sys.stdout.write = redirector #whenever sys.stdout.write is called, redirector is called.

if __name__ == "__main__":
    main()
