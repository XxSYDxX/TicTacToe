from re import S
from src.engine import Engine

import tkinter as t


class GUI:
    
    def __init__(self):
        self.palate = ['#131414', '#FFFFFF', '#FF0000']  # [bg, fg, fg2]
        self.table = [0] * 9
        self.e = Engine()
        self.ptype = 'O'
        self.etype = 'X'

        self.root = root = t.Tk()
        root.config(bg=self.palate[0])
        root.title("TicTacToe")
        root.resizable(False, False)
        root.configure(background='grey')

        self.frs = []

        for i in range(9):
            box = t.Canvas(root, width=150, height=150, bg='black', borderwidth=0, highlightthickness=2)
            inr = box.create_text(75, 75, text="", fill='black', font=('', 110, 'bold'))
            box.bind('<Button-1>', lambda e, i=i: self.move(i))

            box.grid(row=i//3, column=i%3)
            box.columnconfigure(0, weight=0)

            self.frs.append((inr, box))
        
        self.counts = {1: 0, 2: 0, 3: 0}
        self.c_wids = {}
        
        self.c_wids['t'] = t.Label(root, bg=self.palate[0], fg=self.palate[1], font=('', 12))
        self.c_wids['t'].grid(row=3, column=1, sticky='ew')

        self.c_wids['e'] = t.Label(root, bg=self.palate[0], fg=self.palate[1], font=('', 12))
        self.c_wids['e'].grid(row=3, column=0, sticky='ew')

        self.c_wids['p'] = t.Label(root, bg=self.palate[0], fg=self.palate[1], font=('', 12))
        self.c_wids['p'].grid(row=3, column=2, sticky='ew')

        self.ng = t.Button(root, text='new game', bg=self.palate[0], fg=self.palate[2], disabledforeground=self.palate[0], command=self.new_game)
        self.ng.grid(row=4, column=0, columnspan=3, sticky='nsew')

        self.new_game()
        root.mainloop()
    
    def clear(self):
        self.table = [0] * 9
        self.update()
    
    def inactivate(self):
        for i in range(9):
            inr, box = self.frs[i]
            box.bind('<Button-1>', lambda e, i=i: self.on_random_click(i))
    
    def activate(self):
        for i in range(9):
            inr, box = self.frs[i]
            box.bind('<Button-1>', lambda e, i=i: self.move(i))

    def new_game(self):
        self.clear()
        self.update()
        self.inactivate()
        self.ng.config(state='disabled')

        def set_ptype(p):
            self.ptype = p
            self.etype = 'X' if p == 'O' else 'O'
            
            f.destroy()
            if self.etype == 'X':
                self.table[self.e.engine_move(self.table)] = 2
                self.update()

            self.ng.config(state='normal')
            self.activate()
        
        # Making a frame that asks user for a choice of player type
        f = t.Frame(self.root, bg=self.palate[0], bd=2)
        f.place(x=95, y=160, height=71*2, width=138*2)
        
        x = t.Label(f, text='✕', bg=self.palate[0], fg=self.palate[1], font=('', 100, 'bold'))
        x.place(relx=0.25, rely=0.5, anchor='center')

        x.bind('<Enter>', lambda e: x.config(bg='black', fg=self.palate[2]))
        x.bind('<Leave>', lambda e: x.config(bg=self.palate[0], fg=self.palate[1]))
        x.bind('<Button-1>', lambda e: set_ptype('X'))

        o = t.Label(f, text='〇', bg=self.palate[0], fg=self.palate[1], font=('', 100, 'bold'))
        o.place(relx=0.75, rely=0.5, anchor='center')

        o.bind('<Enter>', lambda e: o.config(bg='black', fg=self.palate[2]))
        o.bind('<Leave>', lambda e: o.config(bg=self.palate[0], fg=self.palate[1]))
        o.bind('<Button-1>', lambda e: set_ptype('O'))
    
    def update(self):
        for i in range(9):
            inr, box = self.frs[i]
            box: t.Canvas
            box.config(bg='black')
            if self.table[i] == 1:
                box.itemconfig(inr, fill='white', text='✕' if self.ptype == 'X' else '〇')
            elif self.table[i] == 2:
                box.itemconfig(inr, fill='white', text='✕' if self.etype == 'X' else '〇')
            else:
                box.itemconfig(inr, fill='black', text='')
        
        self.c_wids['e'].config(text=f'engine ({self.etype.lower()})\n{self.counts[2]}')
        self.c_wids['t'].config(text=f'tie\n{self.counts[3]}')
        self.c_wids['p'].config(text=f'player ({self.ptype.lower()})\n{self.counts[1]}')

    def on_random_click(self, i):
        self.new_game()
    
    def move(self, i):
        if self.e.state(self.table) != 0:
            self.new_game()
        if self.table[i] != 0: return

        self.table[i] = 1
        self.update()

        if 0 in self.table:
            self.table[self.e.engine_move(self.table)] = 2
            self.update()
        
        state = self.e.state(self.table)
        if state in (1, 2):
            if state == 1:
                self.counts[1] += 1
                self.inactivate()
            elif state == 2:
                self.counts[2] += 1
                
            self.update()

            l = self.e.checked_indices(self.table)
            for i in range(9):
                if i in l:
                    inr, box = self.frs[i]
                    box: t.Canvas
                    box.config(bg=self.palate[0])
                else:
                    inr, box = self.frs[i]
                    box: t.Canvas
                    box.itemconfig(inr, fill='#999999')
                
            self.inactivate()
            self.table = [0] * 9
            return     
        
        elif state == 3:
            self.inactivate()
            self.counts[3] += 1
            self.update()
            for i in range(9):
                inr, box = self.frs[i]
                box: t.Canvas
                box.itemconfig(inr, fill='#999999')
            return


if __name__ == '__main__':
    GUI()
