#!/usr/bin/env python3
"""
Command-line GUI for SigilMaker
"""
import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from sigilmaker.core import get_symbols, draw_sigil
from sigilmaker.shapes import SHAPES

class SigilMakerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('SigilMaker')
        self.geometry('550x400')
        self.patterns = list(SHAPES.keys())
        self.palette = None  # Use default palettes in core
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill='both', expand=True)

        ttk.Label(frm, text='Mantra:').grid(row=0, column=0, sticky='w')
        self.entry = ttk.Entry(frm)
        self.entry.grid(row=0, column=1, columnspan=3, sticky='ew')

        ttk.Label(frm, text='Patterns:').grid(row=1, column=0, sticky='nw')
        self.lst = tk.Listbox(frm, selectmode='multiple', height=8)
        for i, p in enumerate(self.patterns):
            self.lst.insert(i, p)
        self.lst.selection_set(0, 1)
        self.lst.grid(row=1, column=1, sticky='ew')

        self.radial = tk.BooleanVar()
        ttk.Checkbutton(frm, text='Radial Text', variable=self.radial).grid(row=2, column=1, sticky='w')

        ttk.Button(frm, text='Randomize', command=self.randomize).grid(row=2, column=2)
        ttk.Button(frm, text='Load Palette', command=self.load_palette).grid(row=3, column=0)
        ttk.Button(frm, text='Batch File', command=self.load_batch).grid(row=3, column=1)
        ttk.Button(frm, text='Generate', command=self.generate).grid(row=4, column=0)
        ttk.Button(frm, text='Save As...', command=self.save_as).grid(row=4, column=1)
        ttk.Button(frm, text='Quit', command=self.destroy).grid(row=4, column=3)

        frm.columnconfigure(1, weight=1)

    def randomize(self):
        self.lst.selection_clear(0, tk.END)
        count = random.randint(1, len(self.patterns))
        for i in random.sample(range(len(self.patterns)), count):
            self.lst.selection_set(i)

    def load_palette(self):
        path = filedialog.askopenfilename(filetypes=[('JSON','*.json')])
        if not path:
            return
        try:
            import json
            data = json.load(open(path))
            self.palette = data
            messagebox.showinfo('Palette', 'Custom palette loaded')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def load_batch(self):
        path = filedialog.askopenfilename(filetypes=[('Text','*.txt')])
        if not path:
            return
        with open(path) as f:
            for line in f:
                mantra = line.strip()
                if mantra:
                    self._generate(mantra, save=True)
        messagebox.showinfo('Batch', 'Batch generation complete')

    def generate(self):
        mantra = self.entry.get().strip()
        if mantra:
            self._generate(mantra)

    def save_as(self):
        mantra = self.entry.get().strip()
        if not mantra:
            return
        filename = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG','*.png'),('SVG','*.svg')])
        if filename:
            self._generate(mantra, save=True, out=filename)

    def _generate(self, mantra, save=False, out=None):
        sy = get_symbols(mantra)
        if len(sy) < 3:
            messagebox.showerror('Error', 'Need at least 3 symbols')
            return
        random.seed(hash(mantra))
        selected = [self.lst.get(i) for i in self.lst.curselection()] or self.patterns
        fmt = os.path.splitext(out or '')[1].lstrip('.') or 'png'
        draw_sigil(
            symbols=sy,
            patterns=selected,
            radial=self.radial.get(),
            out_path=out if save else None,
            fmt=fmt,
            palette=self.palette
        )

if __name__ == '__main__':
    SigilMakerGUI().mainloop()
