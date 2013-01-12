import curses
import fcntl
import struct
import termios
import threading
import time

__version_info__ = (1, 0, 1)
__version__ = '.'.join(map(str, __version_info__))


def tail_files(filenames):
    """
    `filenames` is a list of files to tail simultaneously.
    """
    columns, rows = _terminal_size()
    half_columns = columns / 2

    windows = []
    if len(filenames) == 1:
        windows.append(curses.newwin(rows, columns, 0, 0))
    elif len(filenames) == 2:
        windows.append(curses.newwin(rows, half_columns, 0, 0))
        windows.append(curses.newwin(rows, half_columns, 0, half_columns))
    elif len(filenames) == 3:
        windows.append(curses.newwin(rows, columns / 3, 0, 0))
        windows.append(curses.newwin(rows, columns / 3, 0, columns / 3))
        windows.append(curses.newwin(rows, columns / 3, 0, 2 * columns / 3))
    elif len(filenames) == 4:
        windows.append(curses.newwin(rows / 2, half_columns, 0, 0))
        windows.append(curses.newwin(rows / 2, half_columns, 0, half_columns))
        windows.append(curses.newwin(rows / 2, half_columns, rows / 2, 0))
        windows.append(curses.newwin(rows / 2, half_columns, rows / 2, half_columns))

    lock = threading.Lock()
    threads = set()
    for filename, window in zip(filenames, windows):
        window.border()
        thread = threading.Thread(
                target=_tail_in_window, args=(filename, window, lock))
        thread.daemon = True
        threads.add(thread)
        thread.start()

    try:
        while threads:
            alive_threads = set()
            for thread in threads:
                thread.join(1)
                if thread.is_alive():
                    alive_threads.add(thread)
            threads = alive_threads
    except KeyboardInterrupt:
        return


def _seek_to_n_lines_from_end(f, numlines=10):
    """
    Seek to `numlines` lines from the end of the file `f`.
    """
    buf = ""
    buf_pos = 0
    f.seek(0, 2)  # seek to the end of the file
    line_count = 0

    while line_count < numlines:
        newline_pos = buf.rfind("\n", 0, buf_pos)
        file_pos = f.tell()

        if newline_pos == -1:
            if file_pos == 0:
                # start of file
                break
            else:
                toread = min(1024, file_pos)
                f.seek(-toread, 1)
                buf = f.read(toread) + buf[:buf_pos]
                f.seek(-toread, 1)
                buf_pos = len(buf) - 1
        else:
            # found a line
            buf_pos = newline_pos
            line_count += 1

    if line_count == numlines:
        f.seek(buf_pos + 1, 1)


def _tail(filename, starting_lines=10):
    """
    A generator for reading new lines off of the end of a file.  To start with,
    the last `starting_lines` lines will be read from the end.
    """
    f = open(filename)
    _seek_to_n_lines_from_end(f, starting_lines)
    while True:
        where = f.tell()
        line = f.readline()
        if not line:
            time.sleep(0.25)
            f.seek(where)
        else:
            yield line


def _tail_in_window(filename, window, lock):
    """
    Update a curses window with tailed lines from a file.
    """
    title = " %s " % (filename,)
    max_lines, max_chars = window.getmaxyx()
    max_line_len = max_chars - 2
    window.move(1, 0)

    for line in _tail(filename, max_lines - 2):
        if len(line) > max_line_len:
            first_portion = line[0:max_line_len - 1] + "\n"
            trailing_len = max_line_len - (len("> ") + 1)
            remaining = ["> " + line[i:i + trailing_len] + "\n"
                         for i in range(max_line_len - 1, len(line), trailing_len)]
            remaining[-1] = remaining[-1][0:-1]
            line_portions = [first_portion] + remaining
        else:
            line_portions = [line]

        for line_portion in line_portions:
            with lock:
                try:
                    y, x = window.getyx()
                    if y >= max_lines - 1:
                        window.move(1, 1)
                        window.deleteln()
                        window.move(y - 1, 1)
                        window.deleteln()
                        window.addstr(line_portion)
                    else:
                        window.move(y, x + 1)
                        window.addstr(line_portion)

                    window.border()
                    y, x = window.getyx()
                    window.addstr(0, max_chars / 2 - len(title) / 2, title)
                    window.move(y, x)
                    window.refresh()
                except KeyboardInterrupt:
                    return

def _terminal_size():
    h, w, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return w, h
