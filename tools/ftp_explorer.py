"""
Explorador FTP simple con GUI para seleccionar archivos locales y subir via FTP/FTPS.
Usa Tkinter para la UI y reutiliza las funciones de `ftp_upload.py` para subir.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import threading
import ftplib
import os
import json
from ftp_upload import connect_ftp, upload_file, ensure_remote_dirs
try:
    from sftp_upload import connect_sftp, upload_file_sftp, upload_dir_sftp, sftp_mkdirs
except Exception:
    connect_sftp = None
    upload_file_sftp = None
    upload_dir_sftp = None
    sftp_mkdirs = None
import sys
import time
import shutil
import tempfile
import json as _json
import platform


def probe_protocols(host, ftp_port=21, timeout=2.0):
    """Quickly probe which protocols the server likely supports.

    Returns a dict with keys: sftp (bool), ftps (bool), ftp (bool)
    """
    res = {'sftp': False, 'ftps': False, 'ftp': False}
    # Probe SFTP by checking TCP port 22
    try:
        import socket
        with socket.create_connection((host, 22), timeout=timeout):
            res['sftp'] = True
    except Exception:
        res['sftp'] = False

    # Probe FTP/FTPS by trying simple FTP connection and AUTH TLS
    try:
        import ftplib as _ft
        ftp = _ft.FTP()
        ftp.connect(host=host, port=ftp_port, timeout=timeout)
        ftp.login(user='anonymous', passwd='anonymous@')
        res['ftp'] = True
        try:
            # send AUTH TLS to check FTPS support
            resp = ftp.sendcmd('AUTH TLS')
            if resp and resp.startswith('234'):
                res['ftps'] = True
        except Exception:
            res['ftps'] = False
        try:
            ftp.quit()
        except Exception:
            try:
                ftp.close()
            except Exception:
                pass
    except Exception:
        res['ftp'] = False
        res['ftps'] = False

    return res


def _format_bytes(n):
    for unit in ['B','KB','MB','GB','TB']:
        if n < 1024.0:
            return f"{n:.1f}{unit}"
        n /= 1024.0
    return f"{n:.1f}PB"


def _format_speed(bytes_count, seconds):
    if seconds <= 0:
        return '0B/s'
    per_sec = bytes_count / seconds
    return f"{_format_bytes(per_sec)}/s"


def unzip_file_with_progress(zip_path, target_dir, overwrite=False, progress_callback=None, file_callback=None):
    """Extract zip_path into target_dir streaming member files and calling callbacks.

    progress_callback(done_bytes, total_bytes)
    file_callback(action, path)  # action in {'extracted','skipped','error'}
    """
    import zipfile
    CHUNK = 64 * 1024
    total_bytes = 0
    with zipfile.ZipFile(zip_path, 'r') as zf:
        infos = [info for info in zf.infolist() if not info.is_dir()]
        for info in infos:
            total_bytes += info.file_size

        done = 0
        for info in infos:
            member_path = info.filename
            dest_path = os.path.join(target_dir, *member_path.split('/'))
            # ensure directories
            if info.is_dir():
                os.makedirs(dest_path, exist_ok=True)
                continue
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            if os.path.exists(dest_path) and not overwrite:
                done += info.file_size
                if file_callback:
                    try:
                        file_callback('skipped', dest_path)
                    except Exception:
                        pass
                if progress_callback:
                    try:
                        progress_callback(done, total_bytes)
                    except Exception:
                        pass
                continue

            try:
                with zf.open(info, 'r') as src, open(dest_path, 'wb') as dst:
                    while True:
                        chunk = src.read(CHUNK)
                        if not chunk:
                            break
                        dst.write(chunk)
                        done += len(chunk)
                        if progress_callback:
                            try:
                                progress_callback(done, total_bytes)
                            except Exception:
                                pass
                if file_callback:
                    try:
                        file_callback('extracted', dest_path)
                    except Exception:
                        pass
            except Exception as ex:
                if file_callback:
                    try:
                        file_callback('error', dest_path)
                    except Exception:
                        pass
                # continue with next file
                continue


class FTPExplorer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('FTP Explorer')
        self.geometry('800x500')

        # Connection frame
        conn_frame = ttk.LabelFrame(self, text='Connection')
        conn_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(conn_frame, text='Host:').grid(row=0, column=0)
        self.host_var = tk.StringVar(value='ftp.softool.org')
        ttk.Entry(conn_frame, textvariable=self.host_var, width=30).grid(row=0, column=1)

        ttk.Label(conn_frame, text='User:').grid(row=0, column=2)
        self.user_var = tk.StringVar(value='anonymous')
        ttk.Entry(conn_frame, textvariable=self.user_var, width=20).grid(row=0, column=3)

        ttk.Label(conn_frame, text='Password:').grid(row=0, column=4)
        self.pass_var = tk.StringVar(value='anonymous@')
        ttk.Entry(conn_frame, textvariable=self.pass_var, width=20, show='*').grid(row=0, column=5)

        ttk.Button(conn_frame, text='Connect', command=self.connect).grid(row=0, column=6, padx=5)

        ttk.Label(conn_frame, text='Remote target:').grid(row=1, column=0)
        self.remote_target_var = tk.StringVar(value='/')
        ttk.Entry(conn_frame, textvariable=self.remote_target_var, width=30).grid(row=1, column=1)
        # Protocol hint label
        self.protocol_label_var = tk.StringVar(value='Protocol: unknown')
        ttk.Label(conn_frame, textvariable=self.protocol_label_var).grid(row=1, column=4, columnspan=2)

        # Option: auto-delete originals after compression+upload
        self.auto_delete_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(conn_frame, text='Auto-delete originals after compression', variable=self.auto_delete_var).grid(row=1, column=2, columnspan=3, sticky='w')

        # Local files frame
        local_frame = ttk.LabelFrame(self, text='Local files')
        local_frame.pack(fill='both', expand=True, side='left', padx=10, pady=5)

        self.file_listbox = tk.Listbox(local_frame, selectmode='extended')
        self.file_listbox.pack(fill='both', expand=True, padx=5, pady=5)

        btn_frame = ttk.Frame(local_frame)
        btn_frame.pack(fill='x')
        ttk.Button(btn_frame, text='Add files', command=self.add_files).pack(side='left')
        ttk.Button(btn_frame, text='Add folder', command=self.add_folder).pack(side='left', padx=4)
        ttk.Button(btn_frame, text='New folder', command=self.create_local_dir).pack(side='left', padx=4)
        ttk.Button(btn_frame, text='Delete', command=self.delete_local_selected).pack(side='left', padx=4)
        ttk.Button(btn_frame, text='Unzip Selected', command=self.unzip_selected).pack(side='left', padx=4)
        ttk.Button(btn_frame, text='Clear', command=lambda: self.file_listbox.delete(0, tk.END)).pack(side='left')

        # Unzip options: persistent target entry + overwrite option
        unzip_frame = ttk.Frame(local_frame)
        unzip_frame.pack(fill='x', pady=(6,0))
        ttk.Label(unzip_frame, text='Unzip target:').pack(side='left')
        self.unzip_target_var = tk.StringVar(value='')
        ttk.Entry(unzip_frame, textvariable=self.unzip_target_var, width=40).pack(side='left', padx=4)
        def _browse_unzip_target():
            d = filedialog.askdirectory(title='Select default unzip target')
            if d:
                self.unzip_target_var.set(d)
                try:
                    self._save_settings()
                except Exception:
                    pass
        ttk.Button(unzip_frame, text='Browse', command=_browse_unzip_target).pack(side='left', padx=4)
        self.unzip_overwrite_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(unzip_frame, text='Overwrite existing files', variable=self.unzip_overwrite_var).pack(side='left', padx=6)
        self.unzip_open_after_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(unzip_frame, text='Open folder when done', variable=self.unzip_open_after_var).pack(side='left', padx=6)

        # load settings (if any)
        try:
            self._load_settings()
        except Exception:
            pass

        # Remote listing
        remote_frame = ttk.LabelFrame(self, text='Remote')
        remote_frame.pack(fill='both', expand=True, side='right', padx=10, pady=5)

        self.remote_listbox = tk.Listbox(remote_frame)
        self.remote_listbox.pack(fill='both', expand=True, padx=5, pady=5)

        nav_frame = ttk.Frame(remote_frame)
        nav_frame.pack(fill='x')
        ttk.Button(nav_frame, text='Up', command=self.go_up).pack(side='left', padx=2)
        ttk.Button(nav_frame, text='Refresh', command=self.refresh_remote).pack(side='left', padx=2)
        ttk.Button(nav_frame, text='New dir', command=self.create_remote_dir).pack(side='right', padx=2)
        ttk.Button(nav_frame, text='Delete', command=self.delete_remote_selected).pack(side='right', padx=2)
        ttk.Button(nav_frame, text='Upload Selected', command=self.upload_selected).pack(side='right', padx=2)
        ttk.Button(nav_frame, text='Download', command=self.download_selected).pack(side='right', padx=2)

        # Bind double-click on remote list to navigate into directories
        self.remote_listbox.bind('<Double-Button-1>', self._on_remote_double)

        # Transfer status and logs (bottom)
        bottom_frame = ttk.LabelFrame(self, text='Transfers & Logs')
        bottom_frame.pack(fill='both', expand=False, side='bottom', padx=10, pady=5)

        status_frame = ttk.Frame(bottom_frame)
        status_frame.pack(fill='both', expand=True)

        self.status_tree = ttk.Treeview(status_frame, columns=('status','size','time','progress','speed'), show='headings', height=6)
        self.status_tree.heading('status', text='Status')
        self.status_tree.heading('size', text='Size')
        self.status_tree.heading('time', text='Elapsed')
        self.status_tree.heading('progress', text='Progress')
        self.status_tree.heading('speed', text='Speed')
        self.status_tree.pack(fill='both', expand=True, side='left')

        log_frame = ttk.Frame(bottom_frame)
        log_frame.pack(fill='both', expand=True, side='right')
        self.log_text = tk.Text(log_frame, height=8)
        self.log_text.pack(fill='both', expand=True)
        ttk.Button(log_frame, text='Save log', command=self._save_log).pack(fill='x', pady=(4,0))

        # Track current remote path
        self.cwd = '.'

        self.ftp = None
        # track last logged percent per transfer node to avoid log flooding
        self._node_progress = {}
        # per-node byte counters and start times
        self._node_bytes_done = {}
        self._node_total_bytes = {}
        self._node_start_time = {}

    def add_files(self):
        files = filedialog.askopenfilenames()
        for f in files:
            self.file_listbox.insert(tk.END, f)

    def _save_log(self):
        p = filedialog.asksaveasfilename(title='Save log', defaultextension='.log', filetypes=[('Log files','*.log'),('All files','*.*')])
        if not p:
            return
        try:
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(self.log_text.get('1.0', 'end'))
            messagebox.showinfo('Saved', f'Log saved to {p}')
        except Exception as e:
            messagebox.showerror('Error', f'Could not save log: {e}')

    def connect(self):
        host = self.host_var.get()
        user = self.user_var.get()
        password = self.pass_var.get()
        # Probe server capabilities in background to avoid blocking the UI
        def _probe_and_update():
            try:
                caps = probe_protocols(host)
                hints = []
                if caps.get('sftp'):
                    hints.append('SFTP')
                if caps.get('ftps'):
                    hints.append('FTPS')
                if caps.get('ftp'):
                    hints.append('FTP')
                hint = ' / '.join(hints) if hints else 'unknown'
                self.after(0, lambda: self.protocol_label_var.set(f'Protocols: {hint}'))
            except Exception:
                pass

        threading.Thread(target=_probe_and_update, daemon=True).start()

        # Try the most secure protocol supported by the server: SFTP -> FTPS -> FTP
        # SFTP (paramiko) first
        self.protocol = None
        try:
            if connect_sftp:
                try:
                    sftp, transport = connect_sftp(host, 22, user, password)
                    self.protocol = 'sftp'
                    self.sftp = sftp
                    self.sftp_transport = transport
                    self.ftp = None
                    self._log(f'Connected to {host} using SFTP')
                    messagebox.showinfo('Connected', f'Connected to {host} (SFTP)')
                    self.refresh_remote()
                    return
                except Exception:
                    # SFTP not available or failed; fall through
                    pass
        except Exception:
            pass

        # Try FTPS (FTP over TLS)
        try:
            try:
                ftp = connect_ftp(host, user, password, ftps=True)
                self.protocol = 'ftps'
                self.ftp = ftp
                self._log(f'Connected to {host} using FTPS')
                messagebox.showinfo('Connected', f'Connected to {host} (FTPS)')
                self.refresh_remote()
                return
            except Exception:
                # try plain FTP
                ftp = connect_ftp(host, user, password, ftps=False)
                self.protocol = 'ftp'
                self.ftp = ftp
                self._log(f'Connected to {host} using FTP')
                messagebox.showinfo('Connected', f'Connected to {host} (FTP)')
                self.refresh_remote()
                return
        except Exception as e:
            messagebox.showerror('Error', f'Could not connect: {e}')

    def refresh_remote(self):
        if not self.ftp:
            messagebox.showwarning('Not connected', 'Connect first')
            return
        
        # helper formatting functions are module-level
        try:
            self.remote_listbox.delete(0, tk.END)
            # use cwd stored to list that directory
            try:
                entries = self.ftp.nlst(self.cwd)
            except Exception:
                # fallback to default
                entries = self.ftp.nlst()
            # Annotate directories with a trailing '/'
            for item in entries:
                try:
                    # Check if item is a directory by trying to cwd then back
                    cur = self.ftp.pwd()
                    try:
                        self.ftp.cwd(item)
                        is_dir = True
                    except Exception:
                        is_dir = False
                    try:
                        self.ftp.cwd(cur)
                    except Exception:
                        pass
                except Exception:
                    is_dir = False
                display = item + ('/' if is_dir else '')
                self.remote_listbox.insert(tk.END, display)
        except Exception as e:
            messagebox.showerror('Error', f'Could not list remote: {e}')

    def upload_selected(self):
        if not self.ftp:
            messagebox.showwarning('Not connected', 'Connect first')
            return
        sel = self.file_listbox.curselection()
        if not sel:
            messagebox.showwarning('No files', 'Select files to upload')
            return
        files = [self.file_listbox.get(i) for i in sel]
        # ensure remote target
        remote_target = self.remote_target_var.get() or '/'
        threading.Thread(target=self._upload_thread, args=(files, remote_target), daemon=True).start()

    def download_selected(self):
        if not self.ftp:
            messagebox.showwarning('Not connected', 'Connect first')
            return
        sel = self.remote_listbox.curselection()
        if not sel:
            messagebox.showwarning('No selection', 'Select remote files/directories to download')
            return
        local_target = filedialog.askdirectory(title='Select local target folder')
        if not local_target:
            return
        items = [self.remote_listbox.get(i) for i in sel]
        threading.Thread(target=self._download_thread, args=(items, local_target), daemon=True).start()

    def add_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            # mark folder entries with trailing os.sep so we can detect them
            self.file_listbox.insert(tk.END, folder + os.sep)

    def unzip_selected(self):
        sel = self.file_listbox.curselection()
        if not sel:
            messagebox.showwarning('No selection', 'Select local zip files to unzip')
            return
        # collect only files that look like zip (ignore directories)
        files = []
        for i in sel:
            p = self.file_listbox.get(i)
            if p.endswith(os.sep):
                continue
            if p.lower().endswith('.zip'):
                files.append(p)
        if not files:
            messagebox.showwarning('No zip files', 'No zip files selected')
            return
        target = filedialog.askdirectory(title='Select target folder for extraction')
        if not target:
            return
        threading.Thread(target=self._unzip_thread, args=(files, target), daemon=True).start()

    def _unzip_thread(self, files, target):
        # Use the module-level helper to perform byte-level extraction and callbacks
        for f in files:
            try:
                node = self.status_tree.insert('', 'end', values=('queued', os.path.getsize(f) if os.path.exists(f) else 0, '0s', '0%', ''))
                start = time.time()
                self._log(f'Extracting {f} -> {target}')

                events = []
                def _progress_cb(done, total):
                    try:
                        percent = int((done/total)*100) if total else 100
                        speed = ''
                        try:
                            done = self._node_bytes_done.get(node, 0)
                            st = self._node_start_time.get(node, start)
                            speed = _format_speed(done, time.time()-st)
                        except Exception:
                            speed = ''
                        self.status_tree.item(node, values=('extracting', os.path.getsize(f) if os.path.exists(f) else total, f'{time.time()-start:.1f}s', f'{percent}%', speed))
                    except Exception:
                        pass

                def _file_cb(action, path):
                    # action: 'extracted' | 'skipped' | 'error'
                    events.append((action, path))
                    self._log(f'{action.upper()}: {path}')

                from ftp_explorer import unzip_file_with_progress as _unzip_helper
                _unzip_helper(f, target, overwrite=self.unzip_overwrite_var.get(), progress_callback=_progress_cb, file_callback=_file_cb)

                elapsed = time.time() - start
                speed = ''
                try:
                    done = self._node_bytes_done.get(node, 0)
                    speed = _format_speed(done, elapsed)
                except Exception:
                    speed = ''
                self.status_tree.item(node, values=('success', os.path.getsize(f) if os.path.exists(f) else 0, f'{elapsed:.1f}s', '100%', speed))
                self._log(f'Finished extracting {f} -> {target} ({elapsed:.1f}s)')

                # open folder if requested
                if self.unzip_open_after_var.get():
                    try:
                        if platform.system() == 'Windows':
                            os.startfile(target)
                        elif platform.system() == 'Darwin':
                            os.system(f'open "{target}"')
                        else:
                            os.system(f'xdg-open "{target}"')
                    except Exception:
                        pass
            except Exception as e:
                self._log(f'Error extracting {f}: {e}', error=True)

    # Settings persistence for unzip target and options
    def _settings_path(self):
        return os.path.join(os.path.dirname(__file__), 'ftp_explorer_settings.json')

    def _load_settings(self):
        p = self._settings_path()
        if not os.path.exists(p):
            return
        try:
            with open(p, 'r', encoding='utf-8') as fh:
                s = _json.load(fh)
            self.unzip_target_var.set(s.get('unzip_target', ''))
            self.unzip_overwrite_var.set(bool(s.get('unzip_overwrite', False)))
            self.unzip_open_after_var.set(bool(s.get('unzip_open_after', False)))
        except Exception:
            pass

    def _save_settings(self):
        p = self._settings_path()
        try:
            s = {
                'unzip_target': self.unzip_target_var.get() or '',
                'unzip_overwrite': bool(self.unzip_overwrite_var.get()),
                'unzip_open_after': bool(self.unzip_open_after_var.get()),
            }
            with open(p, 'w', encoding='utf-8') as fh:
                _json.dump(s, fh)
        except Exception:
            pass

    def create_local_dir(self):
        parent = filedialog.askdirectory(title='Select parent directory for new folder')
        if not parent:
            return
        name = simpledialog.askstring('Folder name', 'Enter new folder name:')
        if not name:
            return
        path = os.path.join(parent, name)
        try:
            os.makedirs(path, exist_ok=True)
            self.file_listbox.insert(tk.END, path + os.sep)
            self._log(f'Created local folder {path}')
        except Exception as e:
            messagebox.showerror('Error', f'Could not create folder: {e}')

    def delete_local_selected(self):
        sel = self.file_listbox.curselection()
        if not sel:
            messagebox.showwarning('No selection', 'Select local files/folders to delete')
            return
        if not messagebox.askyesno('Confirm', 'Delete selected local items?'):
            return
        for i in reversed(sel):
            path = self.file_listbox.get(i)
            is_dir = path.endswith(os.sep)
            real_path = path.rstrip(os.sep) if is_dir else path
            try:
                if is_dir:
                    shutil.rmtree(real_path)
                    self._log(f'Deleted local directory {real_path}')
                else:
                    os.remove(real_path)
                    self._log(f'Deleted local file {real_path}')
                self.file_listbox.delete(i)
            except Exception as e:
                self._log(f'Failed to delete {real_path}: {e}', error=True)

    def _upload_thread(self, files, remote_target='/'):
        for f in files:
            try:
                # If the entry is a directory (we stored it ending with os.sep), compress it first
                is_dir_entry = f.endswith(os.sep)
                if is_dir_entry:
                    folder_path = f.rstrip(os.sep)
                    base_name = os.path.basename(folder_path)
                    # Create temporary zip
                    tmp_dir = tempfile.mkdtemp()
                    zip_base = os.path.join(tmp_dir, base_name)
                    self._log(f'Compressing folder {folder_path} -> {zip_base}.zip')
                    archive_path = shutil.make_archive(zip_base, 'zip', folder_path)
                    upload_path = archive_path
                    remote_name = os.path.basename(archive_path)
                    size = os.path.getsize(archive_path)
                else:
                    upload_path = f
                    remote_name = os.path.basename(f)
                    size = os.path.getsize(f)

                # Add entry to status tree
                node = self.status_tree.insert('', 'end', values=('queued', size, '0s', '', ''))
                start = time.time()
                # initialize node byte counters
                self._node_bytes_done[node] = 0
                self._node_total_bytes[node] = size or 0
                self._node_start_time[node] = start
                self._log(f'START UPLOAD {remote_name}: {size} bytes')
                # ensure remote target exists and change into it
                try:
                    ensure = True
                    # create and cd into remote target
                    from ftp_upload import ensure_remote_dirs
                    if remote_target and remote_target != '/':
                        ensure_remote_dirs(self.ftp, remote_target)
                        self.ftp.cwd(remote_target)
                except Exception as e:
                    self._log(f'Could not ensure remote target {remote_target}: {e}', error=True)

                self._log(f'Starting upload {upload_path} -> {remote_name} (to {remote_target})')

                def progress_cb(sent, total):
                    # update progress in treeview
                    percent = int((sent/total)*100) if total and total > 0 else 0
                    try:
                        try:
                            done = self._node_bytes_done.get(node, 0)
                            st = self._node_start_time.get(node, start)
                            speed = _format_speed(done, time.time()-st)
                        except Exception:
                            speed = ''
                        self.status_tree.item(node, values=(self.status_tree.item(node)['values'][0], size, f'{time.time()-start:.1f}s', f'{percent}%', speed))
                        # update bytes done for calculations
                        try:
                            self._node_bytes_done[node] = sent
                        except Exception:
                            pass
                        # log progress changes (only when percent changes)
                        last = self._node_progress.get(node)
                        if last is None or percent != last:
                            self._node_progress[node] = percent
                            self._log(f'Upload progress {remote_name}: {percent}%')
                    except Exception:
                        pass

                # Choose protocol-specific upload
                success = False
                try:
                    if getattr(self, 'protocol', None) == 'sftp' and upload_file_sftp:
                        # ensure remote path via sftp helper
                        try:
                            if remote_target and remote_target != '/':
                                sftp_mkdirs(self.sftp, remote_target)
                        except Exception:
                            pass
                        # for files (and archives) upload via SFTP
                        success = upload_file_sftp(self.sftp, upload_path, os.path.join(remote_target, remote_name).replace('\\','/'), retry=2, verbose=True)
                    else:
                        success = upload_file(self.ftp, upload_path, remote_name, retry=2, verbose=True, progress_callback=progress_cb)
                except Exception as e:
                    self._log(f'Upload exception: {e}', error=True)
                elapsed = time.time() - start
                # compute average speed
                done = self._node_bytes_done.get(node, size)
                avg_speed = _format_speed(done, elapsed)
                try:
                    done = self._node_bytes_done.get(node, size)
                    speed = _format_speed(done, elapsed)
                except Exception:
                    speed = ''
                self.status_tree.item(node, values=('success' if success else 'failed', size, f'{elapsed:.1f}s', '100%', speed))
                self._log(f'END UPLOAD {remote_name}: {"OK" if success else "FAILED"} elapsed={elapsed:.1f}s avg={avg_speed}')
                # cleanup node tracking
                try:
                    del self._node_bytes_done[node]
                    del self._node_total_bytes[node]
                    del self._node_start_time[node]
                except Exception:
                    pass
                if not success:
                    # keep going but notify
                    self._log(f'Upload failed for {upload_path}', error=True)

                # Cleanup any temporary archive
                if is_dir_entry:
                    try:
                        os.remove(archive_path)
                        os.rmdir(tmp_dir)
                        self._log(f'Removed temporary archive {archive_path}')
                    except Exception:
                        pass

                    # If requested, remove the original folder after successful compression+upload
                    if is_dir_entry and success and self.auto_delete_var.get():
                        try:
                            shutil.rmtree(folder_path)
                            # remove from the local listbox if present
                            try:
                                # entries for folders were stored with a trailing sep
                                stored = folder_path + os.sep
                                items = list(self.file_listbox.get(0, tk.END))
                                if stored in items:
                                    idx = items.index(stored)
                                    self.file_listbox.delete(idx)
                            except Exception:
                                pass
                            self._log(f'Auto-deleted original folder {folder_path} after successful upload')
                        except Exception as ex:
                            self._log(f'Failed to auto-delete {folder_path}: {ex}', error=True)
            except Exception as e:
                self._log(f'Error during upload {f}: {e}', error=True)
    def _download_thread(self, items, local_target):
        for item in items:
            try:
                is_dir = item.endswith('/')
                name = item.rstrip('/') if is_dir else item
                node = self.status_tree.insert('', 'end', values=('queued', '0', '0s', '0%', ''))
                start = time.time()
                # Download file
                if not is_dir:
                    local_path = os.path.join(local_target, name)
                    # ensure directory exists
                    os.makedirs(os.path.dirname(local_path) or local_target, exist_ok=True)
                    sent = 0
                    total = None
                    try:
                        total = self.ftp.size(name)
                    except Exception:
                        total = None

                    def cb(data):
                        nonlocal sent
                        try:
                            with open(local_path, 'ab') as lf:
                                lf.write(data)
                        except Exception:
                            pass
                        sent += len(data)
                        try:
                            self._node_bytes_done[node] = sent
                        except Exception:
                            pass
                        if total:
                            percent = int((sent/total)*100) if total and total > 0 else 0
                            try:
                                try:
                                    done = self._node_bytes_done.get(node, 0)
                                    st = self._node_start_time.get(node, start)
                                    speed = _format_speed(done, time.time()-st)
                                except Exception:
                                    speed = ''
                                self.status_tree.item(node, values=('downloading', total, f'{time.time()-start:.1f}s', f'{percent}%', speed))
                                # log percent changes
                                last = self._node_progress.get(node)
                                if last is None or percent != last:
                                    self._node_progress[node] = percent
                                    self._log(f'Download progress {name}: {percent}%')
                            except Exception:
                                pass

                    # remove existing partial file
                    try:
                        if os.path.exists(local_path):
                            os.remove(local_path)
                    except Exception:
                        pass

                    try:
                        self.ftp.retrbinary(f'RETR {name}', cb)
                        elapsed = time.time() - start
                        size = os.path.getsize(local_path) if os.path.exists(local_path) else 0
                        try:
                            done = self._node_bytes_done.get(node, size)
                            speed = _format_speed(done, elapsed)
                        except Exception:
                            speed = ''
                        self.status_tree.item(node, values=('success', size, f'{elapsed:.1f}s', '100%', speed))
                        avg_speed = _format_speed(size, elapsed)
                        self._log(f'END DOWNLOAD {name}: OK elapsed={elapsed:.1f}s avg={avg_speed} -> {local_path}')
                        try:
                            del self._node_bytes_done[node]
                            del self._node_total_bytes[node]
                            del self._node_start_time[node]
                        except Exception:
                            pass
                    except Exception as e:
                        self.status_tree.item(node, values=('failed', 0, '0s', '0%', ''))
                        self._log(f'END DOWNLOAD {name}: FAILED {e}', error=True)
                        try:
                            del self._node_bytes_done[node]
                            del self._node_total_bytes[node]
                            del self._node_start_time[node]
                        except Exception:
                            pass
                else:
                    # Recursive download for directories
                    local_dir = os.path.join(local_target, name)
                    try:
                        os.makedirs(local_dir, exist_ok=True)
                        self._download_remote_recursive(name, local_dir, node, start)
                        elapsed = time.time() - start
                        self.status_tree.item(node, values=('success', 0, f'{elapsed:.1f}s', '100%', ''))
                        self._log(f'Downloaded directory {name} -> {local_dir} ({elapsed:.1f}s)')
                    except Exception as e:
                        self.status_tree.item(node, values=('failed', 0, '0s', '0%', ''))
                        self._log(f'Failed to download directory {name}: {e}', error=True)
            except Exception as e:
                self._log(f'Error during download {item}: {e}', error=True)

    def _download_remote_recursive(self, remote_dir, local_dir, node, start):
        """Recursively download a remote directory into local_dir."""
        try:
            cur = self.ftp.pwd()
        except Exception:
            cur = None
        try:
            self.ftp.cwd(remote_dir)
        except Exception:
            # Not a directory; try downloading as file
            local_path = os.path.join(local_dir, remote_dir)
            try:
                with open(local_path, 'wb') as lf:
                    def cb(data):
                        lf.write(data)
                    self.ftp.retrbinary(f'RETR {remote_dir}', cb)
                return
            except Exception:
                raise

        try:
            entries = self.ftp.nlst()
        except Exception:
            entries = []
        for e in entries:
            if e in ('.', '..'):
                continue
            # detect if entry is dir
            is_dir = False
            try:
                cur2 = self.ftp.pwd()
                try:
                    self.ftp.cwd(e)
                    is_dir = True
                except Exception:
                    is_dir = False
                try:
                    self.ftp.cwd(cur2)
                except Exception:
                    pass
            except Exception:
                is_dir = False

            if is_dir:
                sub_local = os.path.join(local_dir, e)
                os.makedirs(sub_local, exist_ok=True)
                self._download_remote_recursive(e, sub_local, node, start)
            else:
                local_path = os.path.join(local_dir, e)
                sent = 0
                total = None
                try:
                    total = self.ftp.size(e)
                except Exception:
                    total = None

                try:
                    with open(local_path, 'wb') as lf:
                        def cb(data):
                            nonlocal sent
                            lf.write(data)
                            sent += len(data)
                            if total:
                                percent = int((sent/total)*100) if total and total > 0 else 0
                                try:
                                    try:
                                        done = self._node_bytes_done.get(node, 0)
                                        st = self._node_start_time.get(node, start)
                                        speed = _format_speed(done, time.time()-st)
                                    except Exception:
                                        speed = ''
                                    self.status_tree.item(node, values=('downloading', total, f'{time.time()-start:.1f}s', f'{percent}%', speed))
                                except Exception:
                                    pass
                        self.ftp.retrbinary(f'RETR {e}', cb)
                except Exception as ex:
                    self._log(f'Failed to download remote file {e}: {ex}', error=True)
        # return to original cwd
        try:
            if cur:
                self.ftp.cwd(cur)
        except Exception:
            pass

    # Remote navigation helpers
    def _on_remote_double(self, event):
        sel = self.remote_listbox.curselection()
        if not sel: return
        item = self.remote_listbox.get(sel[0])
        # strip trailing /
        if item.endswith('/'):
            target = item.rstrip('/')
            try:
                # change cwd and refresh
                self.ftp.cwd(target)
                self.cwd = self.ftp.pwd()
                self._log(f'Changed directory to {self.cwd}')
                self.refresh_remote()
            except Exception as e:
                self._log(f'Could not enter directory {target}: {e}', error=True)

    def create_remote_dir(self):
        if not self.ftp:
            messagebox.showwarning('Not connected', 'Connect first')
            return
        name = simpledialog.askstring('Remote dir', 'Enter new remote directory name:')
        if not name:
            return
        try:
            # ensure we're in cwd
            self.ftp.cwd(self.cwd)
            self.ftp.mkd(name)
            self._log(f'Created remote directory {name} in {self.cwd}')
            self.refresh_remote()
        except Exception as e:
            self._log(f'Could not create remote dir {name}: {e}', error=True)

    def delete_remote_selected(self):
        if not self.ftp:
            messagebox.showwarning('Not connected', 'Connect first')
            return
        sel = self.remote_listbox.curselection()
        if not sel:
            messagebox.showwarning('No selection', 'Select remote items to delete')
            return
        # Dry-run: build a list of items that would be deleted and present to the user
        dry_list = []
        for i in sel:
            item = self.remote_listbox.get(i)
            is_dir = item.endswith('/')
            name = item.rstrip('/') if is_dir else item
            try:
                if is_dir:
                    # collect recursive listing
                    cur = self.ftp.pwd()
                    try:
                        self.ftp.cwd(name)
                        entries = self.ftp.nlst()
                        # for dry-run we won't recurse deeply; just note the directory
                        dry_list.append(f'{name}/ (dir)')
                    except Exception:
                        dry_list.append(f'{name} (unknown)')
                    finally:
                        try:
                            self.ftp.cwd(cur)
                        except Exception:
                            pass
                else:
                    dry_list.append(f'{name} (file)')
            except Exception:
                dry_list.append(f'{name} (unknown)')

        preview = '\n'.join(dry_list)
        if not messagebox.askyesno('Confirm delete (dry-run)', f'This will delete the following items on remote:\n\n{preview}\n\nProceed?'):
            return
        try:
            # ensure we're in cwd
            self.ftp.cwd(self.cwd)
        except Exception:
            pass
        for i in reversed(sel):
            item = self.remote_listbox.get(i)
            is_dir = item.endswith('/')
            name = item.rstrip('/') if is_dir else item
            try:
                if is_dir:
                    # recursive remote delete
                    self._remote_remove_recursive(name)
                    self._log(f'Deleted remote directory {name}')
                else:
                    self.ftp.delete(name)
                    self._log(f'Deleted remote file {name}')
                self.remote_listbox.delete(i)
            except Exception as e:
                self._log(f'Failed to delete remote {name}: {e}', error=True)

    def _remote_remove_recursive(self, name):
        """Recursively remove a remote directory and its contents."""
        # Try to change into the name; if it fails, assume it's a file and delete
        try:
            cur = self.ftp.pwd()
        except Exception:
            cur = None
        try:
            # try changing into it
            self.ftp.cwd(name)
        except Exception:
            # not a directory, try delete as file
            try:
                self.ftp.delete(name)
            except Exception as e:
                raise
            return
        # now in the directory
        try:
            entries = self.ftp.nlst()
        except Exception:
            entries = []
        for e in entries:
            if e in ('.', '..'):
                continue
            # recursive call works because current dir is the target dir
            self._remote_remove_recursive(e)
        # go up and remove the empty dir
        try:
            self.ftp.cwd('..')
            self.ftp.rmd(name)
        except Exception as ex:
            raise
        finally:
            if cur:
                try:
                    self.ftp.cwd(cur)
                except Exception:
                    pass

    def go_up(self):
        try:
            self.ftp.cwd('..')
            self.cwd = self.ftp.pwd()
            self._log(f'Went up to {self.cwd}')
            self.refresh_remote()
        except Exception as e:
            self._log(f'Could not go up: {e}', error=True)

    # Thread-safe logging helper
    def _log(self, msg, error=False):
        timestamp = time.strftime('%H:%M:%S')
        full = f'[{timestamp}] {msg}\n'
        def append():
            try:
                if error:
                    self.log_text.insert('end', full)
                    self.log_text.tag_add('error', 'end-1l linestart', 'end-1l lineend')
                    self.log_text.tag_config('error', foreground='red')
                else:
                    self.log_text.insert('end', full)
                self.log_text.see('end')
            except Exception:
                pass
        self.after(0, append)


if __name__ == '__main__':
    app = FTPExplorer()
    app.mainloop()
