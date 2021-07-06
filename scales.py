import tkinter as tk

class CounterFrame(tk.Frame):

    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_counter()

    
    def init_counter(self):
        self.pack()

        self.counter = tk.IntVar(0)

        left_label = tk.Label(self, text = "Licznik wynosi: ")
        left_label.pack(side = "left")

        scale = tk.Scale(self, from_=0, to=100, variable=self.counter, orient='horizontal')
        scale.pack(side="right")

    
    def clicked(self):
        self.counter.set(self.counter.get() + 1)

class EntryFrame(tk.Frame):

    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_entry()

    
    def init_entry(self):
        self.pack()

        self.text = tk.StringVar()
        self.integer = tk.IntVar()

        left_label = tk.Label(self, text = "Text: ")
        left_label.pack(side = "left")

        entry = tk.Entry(self, textvariable = self.text)
        entry.pack()
        button = tk.Button(self, text = "Set", command=self.submit)
        button.pack(side="right")

    
    def submit(self):
        self.integer.set(self.text.get())

root = tk.Tk()

counter1 = CounterFrame(root)
counter2 = EntryFrame(root)

root.mainloop()