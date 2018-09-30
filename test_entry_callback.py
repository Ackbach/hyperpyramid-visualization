import tkinter as tk

root = tk.Tk()
sv = tk.StringVar()


def callback():
    global e1
    global root

    print(sv.get())
    sv.set('Set Text.')
    root.after_idle(lambda: e1.config(validate="focusout"))
    return True


e1 = tk.Entry(root, textvariable=sv, validate="focusout", validatecommand=callback)
e1.grid()
e2 = tk.Entry(root)
e2.grid()
root.mainloop()
