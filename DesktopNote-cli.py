import cmd
import os
import sys
import pathlib as plb
import pickle as pkl

TEXT: list[str] = []


class TextRevise(cmd.Cmd):
    prompt = '<revise>'
    x = 0
    y = 0

    def screen(self):
        os.system('cls')
        for _i, _x in enumerate(TEXT):
            if _i == self.y:
                if TEXT[self.y] == '':
                    print(str(_i) + '>', '><')
                else:
                    print(
                        str(_i) + '>',
                        (
                            TEXT[self.y][:self.x]
                            + '>' + TEXT[self.y][self.x] + '<'
                            + TEXT[self.y][self.x + 1:]
                        )
                    )
            else:
                print(str(_i) + '>', _x)

    def do_mv(self, arg):
        '''Move to a location
        mv <row_order :: int> <char_order :: int>'''
        arg = [int(x) for x in arg.split()]
        self.x = arg[1]
        self.y = arg[0]
        self.screen()

    def do_r(self, arg):
        '''Right move
        r <length :: int>'''
        self.x += int(arg)
        self.screen()

    def do_l(self, arg):
        '''Left move
        l <length :: int>'''
        self.x -= int(arg)
        self.screen()

    def do_u(self, arg):
        '''Up move
        u <length :: int>'''
        self.y -= int(arg)
        self.screen()

    def do_d(self, arg):
        '''Down move
        d <length :: int>'''
        self.y += int(arg)
        self.screen()

    def do_rm(self, arg):
        '''Delete a char or chars
        rm [[<row_order :: int> <char_order :: int> [<length :: int>]] | [<length>]]'''
        arg = [int(x) for x in arg.split()]
        _leng = len(arg)
        # Delete string
        if _leng == 0:
            TEXT[self.y] = TEXT[self.y][:self.x] + TEXT[self.y][self.x + 1:]
        elif _leng == 1:
            _l = arg[0]
            TEXT[self.y] = TEXT[self.y][:self.x] + TEXT[self.y][self.x + _l:]
        elif _leng == 2:
            _x = arg[1]
            _y = arg[0]
            TEXT[_y] = TEXT[_y][:_x] + TEXT[_y][_x + 1:]
        elif _leng == 3:
            _x = arg[1]
            _y = arg[0]
            _l = arg[2]
            TEXT[_y] = TEXT[_y][:_x] + TEXT[_y][_x + _l:]
        # Move pointer
        if _leng == 2 or _leng == 3:
            self.x = _x
            self.y = _y
        _leng_s = len(TEXT[self.y])
        if self.x >= _leng_s:
            if _leng_s == 0:
                self.x = 0
            else:
                self.x = _leng_s - 1
        self.screen()

    def do_ad(self, arg):
        '''Add a string on the right side
        ad [<row_order :: int> <char_order :: int>]'''
        arg = [int(x) for x in arg.split()]
        _leng = len(arg)
        # Add string
        _s = input('Added string: ')
        if _leng == 0:
            TEXT[self.y] = TEXT[self.y][:self.x + 1] + _s + TEXT[self.y][self.x + 1:]
        elif _leng == 2:
            _x = arg[1]
            _y = arg[0]
            TEXT[_y] = TEXT[_y][:_x + 1] + _s + TEXT[_y][_x + 1:]
        # Move pointer
        _leng_s = len(_s)
        if _leng == 2:
            self.x = _x
            self.y = _y
        self.x += _leng_s
        self.screen()

    def do_rv(self, arg):  # (x, y)或无, 将一个字符修改; (x, y, l)或l, 将 l 个字符修改
        '''Revise a char or chars
        rv [[<row_order :: int> <char_order :: int> [<length :: int>]] | [<length>]]'''
        arg = [int(x) for x in arg.split()]
        _leng = len(arg)
        # Revise string
        _s = input('New string: ')
        if _leng == 0:
            TEXT[self.y] = TEXT[self.y][:self.x] + _s + TEXT[self.y][self.x + 1:]
        elif _leng == 1:
            _l = arg[0]
            TEXT[self.y] = TEXT[self.y][:self.x] + _s + TEXT[self.y][self.x + _l:]
        elif _leng == 2:
            _x = arg[1]
            _y = arg[0]
            TEXT[_y] = TEXT[_y][:_x] + _s + TEXT[_y][_x + 1:]
        elif _leng == 3:
            _x = arg[1]
            _y = arg[0]
            _l = arg[2]
            TEXT[_y] = TEXT[_y][:_x] + _s + TEXT[_y][_x + _l:]
        # Move pointer
        _leng_s = len(_s)
        if _leng == 2 or _leng == 3:
            self.x = _x
            self.y = _y
        _leng_ss = TEXT[self.y]
        if self.x >= len(TEXT[self.y]):
            if _leng_ss == 0:
                self.x = 0
            else:
                self.x = _leng_ss - 1
        else:
            self.x += _leng_s - 1
        self.screen()

    def do_ex(self, _):
        '''Exit revising shell
        ex'''
        return True


class Note(cmd.Cmd):
    intro = '''
        A notebook used on the desktop in a cmd interface.
    ==========================================================
    '''
    prompt = '<note>'

    def __init__(self):
        super().__init__()
        self.path = plb.Path('note.dat')
        if not self.path.exists():
            with open(self.path, 'wb') as fp:
                pkl.dump([], fp)
            self.note: list[list[str, list[str]]] = []
        else:
            with open(self.path, 'rb') as fp:
                self.note: list[list[str, list[str]]] = pkl.load(fp)

    def do_show(self, arg):
        '''Show the notes
        show [<note_order :: int>]'''
        os.system('cls')
        print('    ==========================================================')
        try:
            arg = int(arg)
            print('Title:', arg, self.note[arg][0])
            print('Text:')
            for i, s in enumerate(self.note[arg][1]):
                print(str(i) + '>', s)
            print('    ==========================================================')
        except ValueError:
            for i, x in enumerate(self.note):
                print('Title:', i, x[0])
                print('Text:')
                for j, s in enumerate(x[1]):
                    print(str(j) + '>', s)
                print('    ==========================================================')

    def do_write(self, _):
        '''Write a new note
        write'''
        temp_title = input('New note title: ')
        temp_text: list[str] = []
        print('New note text(end with END):')
        while (s := input()) != 'END':
            temp_text.append(s)
        self.note.append([temp_title, temp_text])
        with open(self.path, 'wb') as fp:
            pkl.dump(self.note, fp)

    def do_revise(self, arg):
        '''Revise a note
        revise <note_order :: int>'''
        try:
            arg = int(arg)
            global TEXT
            TEXT = self.note[arg][1]
            for i, x in enumerate(self.note[arg][1]):
                if i == 0:
                    if x == '':
                        print('0>', '><')
                    else:
                        print('0>', '>' + x[0] + '<' + x[1:])
                print(str(i) + '>', x)
            TextRevise().cmdloop()
            self.note[arg][1] = TEXT
            with open(self.path, 'wb') as fp:
                pkl.dump(self.note, fp)
        except ValueError:
            pass

    def do_delete(self, arg):
        '''Delete a note
        delete <note_order :: int>'''
        try:
            arg = int(arg)
            self.note.pop(arg)
            with open(self.path, 'wb') as fp:
                pkl.dump(self.note, fp)
        except ValueError:
            pass

    def do_exit(self, _):
        '''Exit DesktopNote
        exit'''
        return sys.exit(0)

    def postcmd(self, stop: bool, line: str) -> bool:
        return False


Note().cmdloop()
