import curses
from backend.file_system import FileSystem


class FileSystemTUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.fs = FileSystem()
        self.selected = 0
        self.files = []

    def init_colors(self):
        curses.start_color()
        curses.use_default_colors()

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Selected
        curses.init_pair(2, curses.COLOR_CYAN, -1)   # Details text
        curses.init_pair(3, curses.COLOR_GREEN, -1)  # Footer
        curses.init_pair(4, curses.COLOR_CYAN, -1)   # Help text

    def refresh(self):
        self.files = self.fs.list_files()
        if self.selected >= len(self.files):
            self.selected = max(0, len(self.files) - 1)

    def draw(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        mid = w // 2

        # Headers (HIGH VISIBILITY)
        self.stdscr.attron(curses.A_BOLD | curses.A_UNDERLINE)
        self.stdscr.addstr(0, 2, "FILES")
        self.stdscr.addstr(0, mid + 2, "DETAILS")
        self.stdscr.attroff(curses.A_BOLD | curses.A_UNDERLINE)

        # File list
        for i, f in enumerate(self.files):
            if i + 2 >= h - 3:
                break
            if i == self.selected:
                self.stdscr.attron(curses.color_pair(1))
            self.stdscr.addstr(i + 2, 2, f"📄 {f}"[: mid - 4])
            if i == self.selected:
                self.stdscr.attroff(curses.color_pair(1))

        # Details panel
        if self.files:
            info = self.fs.file_info(self.files[self.selected])
            y = 2
            self.stdscr.attron(curses.color_pair(2))
            for k, v in info.items():
                if y < h - 3:
                    self.stdscr.addstr(y, mid + 2, f"{k}: {v}")
                    y += 1
            self.stdscr.attroff(curses.color_pair(2))

        # Footer
        self.stdscr.attron(curses.color_pair(3))
        self.stdscr.addstr(
            h - 2,
            2,
            "F1 Help  F5 Create  F6 Delete  F7 Rename  F8 Write  F10 Exit",
        )
        self.stdscr.attroff(curses.color_pair(3))

        self.stdscr.refresh()

    def prompt(self, msg):
        self.stdscr.addstr(1, 2, " " * 60)
        self.stdscr.addstr(1, 2, msg)
        curses.echo()
        value = self.stdscr.getstr().decode()
        curses.noecho()
        return value

    def show_help(self):
        h, w = self.stdscr.getmaxyx()
        win_h, win_w = 12, 50
        y, x = (h - win_h) // 2, (w - win_w) // 2
        win = curses.newwin(win_h, win_w, y, x)
        win.box()

        win.attron(curses.color_pair(4))
        help_text = [
            "HELP – File System TUI",
            "",
            "↑ / ↓   : Navigate files",
            "F5      : Create file",
            "F6      : Delete file",
            "F7      : Rename file",
            "F8      : Write content",
            "F10     : Exit",
            "",
            "Press any key to close",
        ]

        for i, line in enumerate(help_text):
            win.addstr(i + 1, 2, line)

        win.attroff(curses.color_pair(4))
        win.refresh()
        win.getch()
        del win

    def run(self):
        self.init_colors()
        self.refresh()

        while True:
            self.draw()
            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                self.selected = max(0, self.selected - 1)

            elif key == curses.KEY_DOWN:
                self.selected = min(len(self.files) - 1, self.selected + 1)

            elif key == curses.KEY_F1:
                self.show_help()

            elif key == curses.KEY_F5:
                name = self.prompt("New filename: ")
                if name:
                    self.fs.create_file(name)

            elif key == curses.KEY_F6 and self.files:
                self.fs.delete_file(self.files[self.selected])

            elif key == curses.KEY_F7 and self.files:
                new = self.prompt("Rename to: ")
                if new:
                    self.fs.rename_file(self.files[self.selected], new)

            elif key == curses.KEY_F8 and self.files:
                data = self.prompt("Write content: ")
                self.fs.write_file(self.files[self.selected], data)

            elif key == curses.KEY_F10:
                break

            self.refresh()


def main(stdscr):
    curses.curs_set(0)
    app = FileSystemTUI(stdscr)
    app.run()


if __name__ == "__main__":
    curses.wrapper(main)
