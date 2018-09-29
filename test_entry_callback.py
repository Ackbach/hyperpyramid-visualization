import tkinter as tk

root = tk.Tk()
sv = tk.StringVar()


def callback():
    print(sv.get())
    sv.set('Set Text.')
    return True


e = tk.Entry(root, textvariable=sv, validate="focusout", validatecommand=callback)
e.grid()
e = tk.Entry(root)
e.grid()
root.mainloop()
