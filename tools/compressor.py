"""
Simple compressor GUI that lets you select files/folders and compress them to .7z, .zip or .rar.
Uses py7zr for .7z (if installed), zipfile for .zip, and the external 'rar' binary for .rar (if available).

Features:
- Add files / Add folder
- List of selected items
- Buttons: Compress to 7z, zip, rar
- Log pane with trace of compression steps

"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import time
import zipfile
import shutil
import subprocess

try:
    import py7zr
    HAS_PY7ZR = True
except Exception:
    HAS_PY7ZR = False


class CompressorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Compressor')
        self.geometry('800x500')

        frame = ttk.Frame(self)
        frame.pack(fill='both', expand=True, padx=8, pady=8)

        left = ttk.LabelFrame(frame, text='Selected items')
        left.pack(side='left', fill='both', expand=True, padx=4, pady=4)

        # Use Treeview to show per-file progress
        self.items_tv = ttk.Treeview(left, columns=('path','type','progress','status'), show='headings')
        self.items_tv.heading('path', text='Path')
        self.items_tv.heading('type', text='Type')
        self.items_tv.heading('progress', text='Progress')
        self.items_tv.heading('status', text='Status')
        self.items_tv.pack(fill='both', expand=True, padx=4, pady=4)

        btns = ttk.Frame(left)
        btns.pack(fill='x')
        ttk.Button(btns, text='Add files', command=self.add_files).pack(side='left')
        ttk.Button(btns, text='Add folder', command=self.add_folder).pack(side='left', padx=4)
        ttk.Button(btns, text='Remove', command=self.remove_selected).pack(side='left', padx=4)
        ttk.Button(btns, text='Clear', command=self._clear_items).pack(side='left', padx=4)

        right = ttk.LabelFrame(frame, text='Actions & Logs')
        right.pack(side='right', fill='both', expand=True, padx=4, pady=4)

        act_frame = ttk.Frame(right)
        act_frame.pack(fill='x', padx=4, pady=4)

        ttk.Button(act_frame, text='Compress -> .7z', command=self.compress_7z).pack(side='left')
        ttk.Button(act_frame, text='Compress -> .zip', command=self.compress_zip).pack(side='left', padx=6)
        ttk.Button(act_frame, text='Compress -> .rar', command=self.compress_rar).pack(side='left', padx=6)

        self.log_text = tk.Text(right, height=20)
        self.log_text.pack(fill='both', expand=True, padx=4, pady=4)

    def _log(self, msg):
        ts = time.strftime('%H:%M:%S')
        line = f'[{ts}] {msg}\n'
        def append():
            try:
                self.log_text.insert('end', line)
                self.log_text.see('end')
            except Exception:
                pass
        self.after(0, append)

    def add_files(self):
        files = filedialog.askopenfilenames()
        for f in files:
            self.items_tv.insert('', 'end', values=(f, 'file', '0%', 'queued'))

    def add_folder(self):
        d = filedialog.askdirectory()
        if d:
            self.items_tv.insert('', 'end', values=(d, 'dir', '0%', 'queued'))

    def remove_selected(self):
        sel = self.items_tv.selection()
        for it in sel:
            self.items_tv.delete(it)

    def _clear_items(self):
        for it in self.items_tv.get_children():
            self.items_tv.delete(it)

    def _gather_items_with_ids(self):
        items = []
        for it in self.items_tv.get_children():
            path, typ, prog, status = self.items_tv.item(it, 'values')
            items.append((it, path, typ))
        return items

    # old _gather_items removed; use _gather_items_with_ids instead

    def compress_zip(self):
        items = [p for _,p,t in self._gather_items_with_ids()]
        if not items:
            messagebox.showwarning('No items', 'Select items to compress')
            return
        out = filedialog.asksaveasfilename(defaultextension='.zip', filetypes=[('ZIP','*.zip')])
        if not out:
            return
        threading.Thread(target=self._do_compress_zip, args=(items, out), daemon=True).start()

    def compress_7z(self):
        if not HAS_PY7ZR:
            messagebox.showerror('Missing dependency', 'py7zr is not installed. Install with: pip install py7zr')
            return
        items = [p for _,p,t in self._gather_items_with_ids()]
        if not items:
            messagebox.showwarning('No items', 'Select items to compress')
            return
        out = filedialog.asksaveasfilename(defaultextension='.7z', filetypes=[('7z','*.7z')])
        if not out:
            return
        threading.Thread(target=self._do_compress_7z, args=(items, out), daemon=True).start()

    def compress_rar(self):
        items = [p for _,p,t in self._gather_items_with_ids()]
        if not items:
            messagebox.showwarning('No items', 'Select items to compress')
            return
        out = filedialog.asksaveasfilename(defaultextension='.rar', filetypes=[('RAR','*.rar')])
        if not out:
            return
        rar_bin = shutil.which('rar') or shutil.which('winrar')
        if not rar_bin:
            messagebox.showerror('rar not found', 'RAR/WinRAR executable not found in PATH. Install WinRAR or provide rar.exe')
            return
        threading.Thread(target=self._do_compress_rar, args=(items, out, rar_bin), daemon=True).start()

    def _do_compress_zip(self, items, out_path):
        try:
            self._log(f'Creating ZIP {out_path}')
            with zipfile.ZipFile(out_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
                # Add files with streaming copy to enable progress
                for it, p, typ in self._gather_items_with_ids():
                    if typ == 'dir' or p.endswith(os.sep):
                        root = p.rstrip(os.sep)
                        for base, dirs, files in os.walk(root):
                            for fname in files:
                                full = os.path.join(base, fname)
                                rel = os.path.relpath(full, os.path.dirname(root))
                                self._log(f'Adding {full} as {rel}')
                                # write with chunked copy
                                with open(full, 'rb') as src, zf.open(rel, 'w') as dest:
                                    total = os.path.getsize(full)
                                    copied = 0
                                    while True:
                                        chunk = src.read(8192)
                                        if not chunk:
                                            break
                                        dest.write(chunk)
                                        copied += len(chunk)
                                        percent = int((copied/total)*100) if total else 100
                                        try:
                                            self.items_tv.item(it, values=(p, typ, f'{percent}%', 'compressing'))
                                        except Exception:
                                            pass
                                self.items_tv.item(it, values=(p, typ, '100%', 'done'))
                    else:
                        arc = os.path.basename(p)
                        self._log(f'Adding {p} as {arc}')
                        with open(p, 'rb') as src, zf.open(arc, 'w') as dest:
                            total = os.path.getsize(p)
                            copied = 0
                            while True:
                                chunk = src.read(8192)
                                if not chunk:
                                    break
                                dest.write(chunk)
                                copied += len(chunk)
                                percent = int((copied/total)*100) if total else 100
                                try:
                                    self.items_tv.item(it, values=(p, typ, f'{percent}%', 'compressing'))
                                except Exception:
                                    pass
                        self.items_tv.item(it, values=(p, typ, '100%', 'done'))
            self._log(f'ZIP completed: {out_path} (size {os.path.getsize(out_path)} bytes)')
        except Exception as e:
            self._log(f'ZIP failed: {e}')

    def _do_compress_7z(self, items, out_path):
        try:
            self._log(f'Creating 7z {out_path} (preset=9)')
            # py7zr doesn't provide per-chunk callbacks easily; we'll add files one-by-one and update status per-file
            with py7zr.SevenZipFile(out_path, 'w', filters=[{'id': 'LZMA2', 'preset': 9}]) as archive:
                for it, p, typ in self._gather_items_with_ids():
                    try:
                        if typ == 'dir' or p.endswith(os.sep):
                            root = p.rstrip(os.sep)
                            self._log(f'Adding directory {root} as {os.path.basename(root)}')
                            self.items_tv.item(it, values=(p, typ, '0%', 'queued'))
                            archive.writeall(root, os.path.basename(root))
                        else:
                            self._log(f'Adding file {p} as {os.path.basename(p)}')
                            self.items_tv.item(it, values=(p, typ, '0%', 'queued'))
                            archive.write(p, os.path.basename(p))
                        self.items_tv.item(it, values=(p, typ, '100%', 'done'))
                    except Exception as e:
                        self.items_tv.item(it, values=(p, typ, '0%', f'error: {e}'))
            self._log(f'7z completed: {out_path} (size {os.path.getsize(out_path)} bytes)')
        except Exception as e:
            self._log(f'7z failed: {e}')

    def _do_compress_rar(self, items, out_path, rar_bin):
        try:
            # Build rar command: rar a -ep1 output files...
            cmd = [rar_bin, 'a', '-ep1', out_path]
            # rar wants paths without trailing sep
            for p in items:
                cmd.append(p.rstrip(os.sep))
            self._log(f'Executing: {" ".join(cmd)}')
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in proc.stdout:
                self._log(line.rstrip())
            proc.wait()
            if proc.returncode == 0:
                self._log(f'RAR completed: {out_path} (size {os.path.getsize(out_path)} bytes)')
            else:
                self._log(f'RAR failed with exit code {proc.returncode}')
        except Exception as e:
            self._log(f'RAR failed: {e}')


def main():
    app = CompressorApp()
    app.mainloop()


if __name__ == '__main__':
    main()
