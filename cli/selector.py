
import os
import sys
import termios
import tty

from blessings import Terminal


class ListSelector:

    def __init__(self, data, on_select):
        self.data = data
        self.selected = 0
        self.term = Terminal()
        self.on_select = on_select
        self.list_offset = 0
        self.debug = False

    def display_height(self):
        return self.term.height - 2

    def list_height(self):
        term_list_height = self.term.height - 3
        len_data = len(self.data)
        if term_list_height > len_data:
            return len_data
        else:
            return term_list_height

    def make_room(self):
        for i in range(1, self.display_height()):
            print()
        print("[Return] to select, [Q] to quit")

    def show_data(self):
        if self.debug:
            with self.term.location(60, 0):
                print(f'height: {self.term.height}, display height: {self.display_height()}, list height: {self.list_height()},selected: {self.selected}__, offset: {self.list_offset}_____')

        for i in range(0, self.list_height()):
            idx = i + self.list_offset
            with self.term.location(0, i + 1):
                if idx == self.selected:
                    print(self.term.black + self.term.on_white + self.data[idx] + self.term.normal)

                else:
                    print(self.data[idx])

    def move_down(self):
        if self.selected < len(self.data) - 1:
            self.selected += 1
            if self.list_height() <= self.selected:
                self.list_offset += 1
        self.show_data()

    def move_up(self):
        if self.selected > 0:
            self.selected -= 1
            if self.list_offset > 0:
                self.list_offset = self.list_offset - 1
        self.show_data()

    def select(self):
        self.on_select(self.selected)

    def getkey(self):
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        try:
            while True:
                b = os.read(sys.stdin.fileno(), 3).decode()
                if len(b) == 3:
                    k = ord(b[2])
                else:
                    k = ord(b)
                key_mapping = {
                    127: 'backspace',
                    10: 'return',
                    32: 'space',
                    9:  'tab',
                    27: 'esc',
                    65: 'up',
                    66: 'down',
                    67: 'right',
                    68: 'left'
                }
                return key_mapping.get(k, chr(k))
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    def start(self):
        self.make_room()
        self.show_data()

        try:
            while True:
                k = self.getkey()
                if k == 'up':
                    self.move_up()
                elif k == 'down':
                    self.move_down()
                elif k == 'return':
                    self.select()
                    break
                elif k == 'esc' or k == 'q':
                    break

        except (KeyboardInterrupt, SystemExit):
            os.system('stty sane')
            print('stopping.')


def main():
    data = [f"Item {i}                                                                             " for i in range(15)]

    listener = lambda i: print(f'selected: {i}')

    ls = ListSelector(data, listener)
    ls.debug = True
    ls.start()



if __name__ == '__main__':
    main()

