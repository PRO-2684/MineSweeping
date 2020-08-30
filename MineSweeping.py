from os import system
from time import sleep

class MineField():
    def __init__(self, x, y, n):
        if x <= 10 and y <=10 and n <x*y:self.x = x; self.y = y; self.n = n
        else: raise ValueError('Invalid input.')
        self.field = []
        for i in range(x*y): self.field.append({'type': 0, 'status': 0})
        self.flagged = 0; self.known = 0; self.status = 0
        self.theme = (10*('-'), (' ', '1', '2', '3', '4', '5', '6', '7', '8', '*'), 10*('!'))
        '''
        type        status          self.status
        0   nothing 0       unknown -1      defeat
        1-8 numbers 1       known   0       unknown
        9   mine    2       flagged 1       victory
        '''
    
    def surroundings(self, n):
        result = set()
        y = n // self.x; x = n % self.x
        possible = {(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)}
        for d in possible:
            tx = d[0] + x; ty = d[1] + y
            if 0 <= tx < self.x and 0 <= ty < self.y: result.add(ty * self.x + tx)
        return result

    def generate(self):
        mines = set(); count = 0; self.known = 0
        x = self.x; y = self.y
        while count < self.n:
            tmp = rnd(0, x*y)
            while tmp in mines: tmp = rnd(0, x*y)
            mines.add(tmp); count += 1
        print(mines)
        for mine in mines:
            self.field[mine]['type'] = 9
            for surrounding in self.surroundings(mine):
                if self.field[surrounding]['type'] != 9: self.field[surrounding]['type'] += 1# ; print(surrounding,'+= 1')# debug
        
    def show(self):
        s = f'{self.flagged}/{self.n}\n '
        t = 0
        for i in range(self.x): s += str(i)
        for y in range(self.y):
            s += '\n'; s += str(y)
            for x in range(self.x):
                info = self.field[t]
                s += self.theme[info['status']][info['type']]
                t += 1
        return s
    
    def open_unknown(self, n):
        t = self.field[n]['type']
        if t == 0:
            self.field[n]['status'] = 1; self.known += 1
            for surrounding in self.surroundings(n):
                if self.field[surrounding]['status'] == 0: 
                    self.open_unknown(surrounding)
        elif t == 9: self.field[n]['status'] = 1; self.known += 1; self.status = -1
        else: self.field[n]['status'] = 1; self.known += 1

    def open_known(self, n):
        surroundings = self.surroundings(n)
        flagged = 0
        for surrounding in surroundings:
            if self.field[surrounding]['status'] == 2: flagged += 1
        if flagged == self.field[n]['type']:
            for surrounding in surroundings:
                if self.field[surrounding]['status'] == 0: self.open_unknown(surrounding)

    def open(self, n):
        t = self.field[n]['status']
        if t == 0: self.open_unknown(n)
        elif t == 1: self.open_known(n)
        else: pass
        if self.known + self.n == self.x * self.y: self.status = 1

    def flag(self, n):
        self.flagged += 1 - self.field[n]['status']
        self.field[n]['status'] = 2 - self.field[n]['status']

m = MineField(10,10,4)
m.generate()

while m.status == 0:
    system('cls')
    print(m.show())
    i = input('>')
    cmd = i.split()
    if cmd[0] == 'open' or cmd[0] == 'o':
        target = int(cmd[1]) + int(cmd[2]) * m.x
        m.open(target)
    elif cmd[0] == 'flag' or cmd[0] == 'f':
        target = int(cmd[1]) + int(cmd[2]) * m.x
        m.flag(target)
    elif cmd[0] == 'exit': break
    elif cmd[0] == 'help':
        system('cls')
        print('Help:\nopen: open/o x y\nflag: flag/f x y\nexit: exit')
        input('Press enter to continue...')
    else:
        system('cls')
        print('Invalid!')
        input('Press enter to continue...')
if m.status == 1:
    system('cls')
    print(m.show())
    for c in 'You ': print(c, end='', flush=True); sleep(0.15)
    for c in 'WON!': print(c, end='', flush=True); sleep(0.5)
    print()
    input('Press enter to exit...')
elif m.status == -1:
    system('cls')
    print(m.show())
    for c in 'You ': print(c, end='', flush=True); sleep(0.15)
    for c in 'LOST!': print(c, end='', flush=True); sleep(0.5)
    print()
    if input('Inspect?(y)') == 'y':
        m.theme = ((' ', '1', '2', '3', '4', '5', '6', '7', '8', '*'), (' ', '1', '2', '3', '4', '5', '6', '7', '8', '*'), (' ', '1', '2', '3', '4', '5', '6', '7', '8', '*'))
        print(m.show())
        input('Press enter to exit...')
