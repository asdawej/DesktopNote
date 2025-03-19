import pathlib as plb
import pickle as pkl

import easygui as eg

path = plb.Path('note.dat')
if not path.exists():
    with open(path, 'wb') as fp:
        pkl.dump([], fp)
    note: list[list[str, list[str]]] = []
else:
    with open('note.dat', 'rb') as fp:
        note: list[list[str, list[str]]] = pkl.load(fp)


def choices_from_note() -> list[str]:
    return [f'{x[0]}: {x[1][0][:10]}' if len(x[1]) != 0 else f'{x[0]}(empty)' for x in note]


def msg_from_note(idx: int) -> str:
    return f'===== {note[idx][0]} =====\n\n' + '\n'.join(note[idx][1])


TITLE = 'DesktopNote'
while True:
    opt = eg.buttonbox(
        msg='Choose one option:',
        title=TITLE,
        choices=[
            'show all',
            'show',
            'write',
            'revise',
            'delete',
            'exit'])
    if opt is None:
        break
    match opt:
        case 'show all':
            eg.msgbox(msg='\n\n'.join([msg_from_note(idx) for idx in range(len(note))]), title=TITLE)
        case 'show':
            choices = choices_from_note()
            opt = eg.choicebox(msg='Choose one note:', title=TITLE, choices=choices)
            if opt is None:
                continue
            idx = choices.index(opt)
            eg.msgbox(msg=msg_from_note(idx), title=TITLE)
        case 'write':
            note_title = eg.enterbox(msg='Please input note title:', title=TITLE)
            if not opt:
                continue
            note_msg = eg.textbox(msg='Text your note:', title=TITLE)
            if note_msg is None:
                continue
            note.append([note_title, note_msg.split('\n')])
            with open(path, 'wb') as fp:
                pkl.dump(note, fp)
        case 'revise':
            choices = choices_from_note()
            opt = eg.choicebox(msg='Choose one note:', title=TITLE, choices=choices)
            if opt is None:
                continue
            idx = choices.index(opt)
            note_msg = eg.textbox(msg='Revise your note:', title=TITLE, text='\n'.join(note[idx][1]))
            if note_msg is None:
                continue
            note[idx][1] = note_msg.split('\n')
            with open(path, 'wb') as fp:
                pkl.dump(note, fp)
        case 'delete':
            choices = choices_from_note()
            opt = eg.choicebox(msg='Choose one note:', title=TITLE, choices=choices)
            if opt is None:
                continue
            idx = choices.index(opt)
            del note[idx]
            with open(path, 'wb') as fp:
                pkl.dump(note, fp)
        case _:
            break
