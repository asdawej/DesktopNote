import cmd
import os
import pickle

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
                    print(str(_i)+'>', '><')
                else:
                    print(
                        str(_i)+'>',
                        (
                            TEXT[self.y][:self.x]
                            + '>'+TEXT[self.y][self.x]+'<'
                            + TEXT[self.y][self.x+1:]
                        )
                    )
            else:
                print(str(_i)+'>', _x)

    def do_mv(self, arg):
        '''Move to a location\
        \n=====\
        \nmv <row_order :: int> <char_order :: int>'''
        arg = [int(x) for x in arg.split()]
        self.x = arg[1]
        self.y = arg[0]
        self.screen()

    def do_r(self, arg):
        '''Right move\
        \n=====\
        \nr <length :: int>'''
        self.x += int(arg)
        self.screen()

    def do_l(self, arg):
        '''Left move\
        \n=====\
        \nl <length :: int>'''
        self.x -= int(arg)
        self.screen()

    def do_u(self, arg):
        '''Up move\
        \n=====\
        \nu <length :: int>'''
        self.y -= int(arg)
        self.screen()

    def do_d(self, arg):
        '''Down move\
        \n=====\
        \nd <length :: int>'''
        self.y += int(arg)
        self.screen()

    def do_rm(self, arg):
        '''Delete a char or chars\
        \n=====\
        \nrm [[<row_order :: int> <char_order :: int> [<length :: int>]] | [<length>]]'''
        arg = [int(x) for x in arg.split()]
        _leng = len(arg)
        # Delete string
        if _leng == 0:
            TEXT[self.y] = TEXT[self.y][:self.x]+TEXT[self.y][self.x+1:]
        elif _leng == 1:
            _l = arg[0]
            TEXT[self.y] = TEXT[self.y][:self.x]+TEXT[self.y][self.x+_l:]
        elif _leng == 2:
            _x = arg[1]
            _y = arg[0]
            TEXT[_y] = TEXT[_y][:_x]+TEXT[_y][_x+1:]
        elif _leng == 3:
            _x = arg[1]
            _y = arg[0]
            _l = arg[2]
            TEXT[_y] = TEXT[_y][:_x]+TEXT[_y][_x+_l:]
        # Move pointer
        if _leng == 2 or _leng == 3:
            self.x = _x
            self.y = _y
        _leng_s = len(TEXT[self.y])
        if self.x >= _leng_s:
            if _leng_s == 0:
                self.x = 0
            else:
                self.x = _leng_s-1
        self.screen()

    def do_ad(self, arg):
        '''Add a string on the right side\
        \n=====\
        \nad [<row_order :: int> <char_order :: int>]'''
        arg = [int(x) for x in arg.split()]
        _leng = len(arg)
        # Add string
        _s = input('Added string: ')
        if _leng == 0:
            TEXT[self.y] = TEXT[self.y][:self.x+1]+_s+TEXT[self.y][self.x+1:]
        elif _leng == 2:
            _x = arg[1]
            _y = arg[0]
            TEXT[_y] = TEXT[_y][:_x+1]+_s+TEXT[_y][_x+1:]
        # Move pointer
        _leng_s = len(_s)
        if _leng == 2:
            self.x = _x
            self.y = _y
        self.x += _leng_s
        self.screen()

    def do_rv(self, arg):  # (x, y)或无, 将一个字符修改; (x, y, l)或l, 将 l 个字符修改
        '''Revise a char or chars\
        \n=====\
        \nrv [[<row_order :: int> <char_order :: int> [<length :: int>]] | [<length>]]'''
        arg = [int(x) for x in arg.split()]
        _leng = len(arg)
        # Revise string
        _s = input('New string: ')
        if _leng == 0:
            TEXT[self.y] = TEXT[self.y][:self.x]+_s+TEXT[self.y][self.x+1:]
        elif _leng == 1:
            _l = arg[0]
            TEXT[self.y] = TEXT[self.y][:self.x]+_s+TEXT[self.y][self.x+_l:]
        elif _leng == 2:
            _x = arg[1]
            _y = arg[0]
            TEXT[_y] = TEXT[_y][:_x]+_s+TEXT[_y][_x+1:]
        elif _leng == 3:
            _x = arg[1]
            _y = arg[0]
            _l = arg[2]
            TEXT[_y] = TEXT[_y][:_x]+_s+TEXT[_y][_x+_l:]
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
                self.x = _leng_ss-1
        else:
            self.x += _leng_s-1
        self.screen()

    def do_ex(self, arg):
        '''Exit revising shell\
        \n=====\
        \nex'''
        return True


class Note(cmd.Cmd):
    intro = '''
        A notebook used on the desktop in a cmd interface.
    ==========================================================
    '''
    prompt = '<note>'
    try:
        fnote = open('note.dat', 'rb')
    except:
        fnote = open('note.dat', 'wb')
        pickle.dump([], fnote)
        fnote.close()
        fnote = open('note.dat', 'rb')
    note: list[list[str, list[str]]] = pickle.load(fnote)
    fnote.close()

    def do_show(self, arg):
        '''Show the notes\
        \n=====\
        \nshow [<note_order :: int>]'''
        os.system('cls')
        print('    ==========================================================')
        try:
            arg = int(arg)
            print('Title:', arg, self.note[arg][0])
            print('Text:')
            for i, s in enumerate(self.note[arg][1]):
                print(str(i)+'>', s)
            print('    ==========================================================')
        except:
            for i, x in enumerate(self.note):
                print('Title:', i, x[0])
                print('Text:')
                for j, s in enumerate(x[1]):
                    print(str(j)+'>', s)
                print('    ==========================================================')

    def do_write(self, arg):
        '''Write a new note\
        \n=====\
        \nwrite'''
        temp_title = input('New note title: ')
        temp_text: list[str] = []
        print('New note text(end with END):')
        while (s := input()) != 'END':
            temp_text.append(s)
        self.note.append([temp_title, temp_text])
        self.fnote = open('note.dat', 'wb')
        pickle.dump(self.note, self.fnote)
        self.fnote.close()

    def do_revise(self, arg):
        '''Revise a note\
        \n=====\
        \nrevise <note_order :: int>'''
        arg = int(arg)
        global TEXT
        TEXT = self.note[arg][1]
        for i, x in enumerate(self.note[arg][1]):
            if i == 0:
                if x == '':
                    print('0>', '><')
                else:
                    print('0>', '>'+x[0]+'<'+x[1:])
            print(str(i)+'>', x)
        TextRevise().cmdloop()
        self.note[arg][1] = TEXT
        self.fnote = open('note.dat', 'wb')
        pickle.dump(self.note, self.fnote)
        self.fnote.close()

    def do_delete(self, arg):
        '''Delete a note\
        \n=====\
        \ndelete <note_order :: int>'''
        arg = int(arg)
        self.note.pop(arg)
        self.fnote = open('note.dat', 'wb')
        pickle.dump(self.note, self.fnote)
        self.fnote.close()

    def do_exit(self, arg):
        '''Exit DesktopNote\
        \n=====\
        \nexit'''
        exit(0)

    def postcmd(self, stop: bool, line: str) -> bool:
        return False


Note().cmdloop()
