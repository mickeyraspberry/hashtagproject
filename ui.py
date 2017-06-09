import re
import tkinter as tk
from tkinter import ttk

text = ''


class Aplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.resizable(width=False, height=False)

        ttk.Style().configure("TButton", font="Arial 14 bold")

        self.title('Аналитика хештега в VK.com')

        tk.Label(text="Введите хештег без знака '#'", font= "Arial 18").pack(padx=5, pady=5)

        self.txt = tk.Text(self, width=21, height=1, font="Arial 16 bold", bd=0, fg='Red')
        self.txt.pack(padx=5, pady=5)
        self.reg = re.compile('^[а-яА-Я\w]+$')

        ttk.Button(self,width=21, text="Начать визуализацию", command=self.start).pack(padx=5, pady=10)

    def start(self):
        global text
        tmp = self.reg.match(self.txt.get(1.0,tk.END))

        if not tmp:
            return

        text = tmp.group()

        self.destroy()


if __name__ == "__main__":
    Aplication().mainloop()

    if text != '':
        import graph
        graph.startAnim(text)