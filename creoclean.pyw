#!/usr/bin/env python
# file: creoclean.pyw
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2022 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2022-02-11T19:27:02+0100
# Last modified: 2022-02-11T23:15:45+0100

from tkinter import filedialog
from tkinter import ttk
from tkinter.font import nametofont
from types import SimpleNamespace
import glob
import os
import re
import sys
import threading
import tkinter as tk


__version__ = "2022.02.11"
widgets = SimpleNamespace()


def create_widgets(root, w):
    """Create the window and its widgets.

    Arguments:
        root: the root window.
        w: SimpleNamespace to store widgets.
    """
    # Set the font.
    default_font = nametofont("TkDefaultFont")
    default_font.configure(size=12)
    root.option_add("*Font", default_font)
    # General commands and bindings
    root.bind_all("q", do_exit)
    root.wm_title("Creoclean v" + __version__)
    root.columnconfigure(3, weight=1)
    root.rowconfigure(5, weight=1)
    # First row
    ttk.Label(root, text="(1)").grid(row=0, column=0, sticky="ew")
    w.fb = ttk.Button(root, text="Select directory", command=do_directory)
    w.fb.grid(row=0, column=1, columnspan=2, sticky="w")
    w.dn = ttk.Label(root)
    w.dn.grid(row=0, column=3, columnspan=2, sticky="ew")
    # Second row
    ttk.Label(root, text="(2)").grid(row=1, column=0, sticky="ew")
    w.dry = tk.IntVar()
    w.dry.set(0)
    ttk.Checkbutton(root, text="dry run", variable=w.dry).grid(
        row=1, column=1, sticky="ew"
    )
    w.extra = tk.IntVar()
    w.extra.set(1)
    ttk.Checkbutton(root, text="clean miscellaneous", variable=w.extra).grid(
        row=1, column=2, sticky="ew"
    )
    # Third row
    ttk.Label(root, text="(3)").grid(row=2, column=0, sticky="ew")
    w.gobtn = ttk.Button(root, text="Go!", command=do_start, state=tk.DISABLED)
    w.gobtn.grid(row=2, column=1, sticky="ew")
    # Fourth row
    ttk.Label(root, text="(4)").grid(row=3, column=0, sticky="ew")
    ttk.Label(root, text="Progress:").grid(row=3, column=1, sticky="w")
    # Fifth row
    sb = tk.Scrollbar(root, orient="vertical")
    w.status = tk.Listbox(root, width=60, yscrollcommand=sb.set)
    w.status.grid(row=4, rowspan=5, column=1, columnspan=3, sticky="nsew")
    sb.grid(row=4, rowspan=5, column=5, sticky="ns")
    sb.config(command=w.status.yview)
    # Ninth row
    w.quitbtn = ttk.Button(root, text="Quit", command=do_exit)
    w.quitbtn.grid(row=9, column=1, sticky="ew")


def do_exit(arg=None):
    """
    Callback to handle quitting.
    """
    root.destroy()


def do_directory():
    """Callback to open a directory"""
    dn = filedialog.askdirectory(title="Directory to clean", parent=root)
    widgets.dn["text"] = dn
    widgets.gobtn['state'] = 'enabled'
    widgets.status.delete(0, tk.END)


def statusmsg(text):
    """Append a message to the status listbox, and make sure it is visible."""
    widgets.status.insert(tk.END, text)
    widgets.status.see(tk.END)


def clean_versioned(path, dry_run):  # noqa
    """
    Clean up Creo versioned files in the named directory.

    Arguments:
        path: The path of the directory to clean.
        dry_run: Boolean to indicate a dry run.
    """
    filenames = [e for e in os.listdir(path) if os.path.isfile(os.path.join(path, e))]
    statusmsg(f"Found {len(filenames)} files")
    splits = [re.split("^(.*)\.([^\.]{3})\.([0-9]+)$", fn) for fn in filenames]
    splits = [s[1:-1] for s in splits if len(s) == 5]
    exts = sorted(set([s[1] for s in splits]))
    os.chdir(path)
    for ext in exts:
        data = [s for s in splits if s[1] == ext]
        cnt = len(data)
        if cnt < 2:
            statusmsg(f"Not enough '{ext}' files; skipping")
            continue
        statusmsg(f"Found {cnt} '{ext}' files")
        names = set(p[0] for p in data)
        statusmsg(f"Found {len(names)} unique '{ext}' file names")
        for nm in names:
            numbers = [int(p[2]) for p in data if p[0] == nm]
            if len(numbers) > 1:
                numbers.sort()
                for n in numbers[:-1]:
                    fn = f"{nm}.{ext}.{n}"
                    statusmsg(f"Removing '{fn}'")
                    if not dry_run:
                        try:
                            os.remove(fn)
                        except OSError as e:
                            statusmsg(f"Removing '{fn}' failed: {e}")
            oldfn = f"{nm}.{ext}.{numbers[-1]}"
            newfn = f"{nm}.{ext}.{1}"
            if oldfn != newfn:
                statusmsg(f"Renaming '{oldfn}' to '{newfn}'")
                if not dry_run:
                    try:
                        os.rename(oldfn, newfn)
                    except OSError as e:
                        statusmsg(f"Renaming '{oldfn}' failed: {e}")


def clean_miscellaneous(path, dry_run):
    """
    Clean up Creo log files in the named directory.

    Arguments:
        path: The path of the directory to clean.
        dry_run: Boolean to indicate a dry run.
    """
    os.chdir(path)
    log = glob.glob("*.log*")
    statusmsg(f"Found {len(log)} log files.")
    xml = glob.glob("*log.xml")
    statusmsg(f"Found {len(xml)} log.xml files.")
    inf = glob.glob("*.inf.*")
    statusmsg(f"Found {len(inf)} inf files.")
    txt = glob.glob("*.txt.*")
    statusmsg(f"Found {len(txt)} txt files.")
    mp = glob.glob("*.m_p")
    statusmsg(f"Found {len(mp)} m_p files.")
    xt = glob.glob("*.x_t")
    statusmsg(f"Found {len(xt)} x_t files.")
    files = log + xml + inf + txt + mp + xt
    for fn in files:
        statusmsg(f"Removing '{fn}'")
        if not dry_run:
            try:
                os.remove(fn)
            except OSError as e:
                statusmsg(f"Removing '{fn}' failed: {e}")


def do_start():
    worker = threading.Thread(target=process_creofiles_thread)
    worker.start()


def process_creofiles_thread():
    widgets.fb["state"] = tk.DISABLED
    widgets.gobtn["state"] = tk.DISABLED
    widgets.quitbtn["state"] = tk.DISABLED
    clean_versioned(widgets.dn["text"], widgets.dry.get() > 0)
    if widgets.extra.get() > 0:
        clean_miscellaneous(widgets.dn["text"], widgets.dry.get() > 0)
    widgets.fb["state"] = tk.NORMAL
    widgets.gobtn["state"] = tk.NORMAL
    widgets.quitbtn["state"] = tk.NORMAL


if __name__ == "__main__":
    # Detach from the command line on UNIX systems.
    if os.name == "posix":
        if os.fork():
            sys.exit()
    # Create the GUI window.
    root = tk.Tk(None)
    # Use a dialog window so that it floats even when using a tiling window manager.
    if os.name == "posix":
        root.attributes("-type", "dialog")
    # Don't show hidden files in the file dialog
    # https://stackoverflow.com/questions/53220711/how-to-avoid-hidden-files-in-file-picker-using-tkinter-filedialog-askopenfilenam
    try:
        # call a dummy dialog with an impossible option to initialize the file
        # dialog without really getting a dialog window; this will throw a
        # TclError, so we need a try...except :
        try:
            root.tk.call("tk_getOpenFile", "-foobarbaz")
        except tk.TclError:
            pass
        # now set the magic variables accordingly
        root.tk.call("set", "::tk::dialog::file::showHiddenBtn", "1")
        root.tk.call("set", "::tk::dialog::file::showHiddenVar", "0")
    except Exception:
        pass
    create_widgets(root, widgets)
    root.mainloop()
