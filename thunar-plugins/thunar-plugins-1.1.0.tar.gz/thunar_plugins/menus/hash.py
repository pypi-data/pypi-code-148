# system modules
import threading
import time
import pkg_resources
import logging
import hashlib
import os

# internal modules
from thunar_plugins import l10n

# external modules
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import GObject, GLib, Gtk, Gdk, Thunarx

logger = logging.getLogger(__name__)


class HashSubmenu(GObject.GObject, Thunarx.MenuProvider):
    name = _("Hash Context-Menu")

    description = _("This plugin adds a context menu to hash files.")

    def __init__(self):
        pass

    @property
    def ui(self):
        try:
            return self._ui
        except AttributeError:
            self._ui = Gtk.Builder()
            self._ui.set_translation_domain(l10n.GETTEXT_DOMAIN)
            self._ui.add_from_file(
                pkg_resources.resource_filename(
                    "thunar_plugins.ui", "hash.glade"
                )
            )

            handlers = {}
            self._ui.connect_signals(handlers)
        return self._ui

    def get_file_menu_items(self, window, files):
        if any(f.is_directory() for f in files):
            return

        hash_menuitem = Thunarx.MenuItem(
            name="ContextMenu::Hash",
            label=_("Checksums"),
            tooltip=_("Calculate several checksums for the selected files."),
            icon="emblem-information",
        )

        hash_menuitem.connect("activate", self.hash_files, files)

        return (hash_menuitem,)

    @property
    def simple_hashes(self):
        for alg in hashlib.algorithms_available:
            try:
                h = hashlib.new(alg)
                h.hexdigest()
                yield h
            except BaseException:
                pass

    def hash_files(self, item, files):
        dialog = self.ui.get_object("hash-dialog")
        treestore = self.ui.get_object("hash-treestore")
        treeview = self.ui.get_object("hash-treeview")

        treestore.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        stopthread = threading.Event()

        def fill_treestore():
            for f in files:
                f_path = f.get_location().get_path()
                file_iter = treestore.append(
                    None, (os.path.basename(f_path), None, None, 0, True)
                )
                hashers = {h.name: {"hasher": h} for h in self.simple_hashes}
                for name, h in hashers.items():
                    h["iter"] = treestore.append(
                        file_iter, (None, name, None, None, False)
                    )
                total_bytes = os.path.getsize(f_path)
                time_before = time.time()
                with open(f_path, "rb") as fh:
                    bytes_read = 0
                    last_percentage = 0
                    while True:
                        chunk = fh.read(128000)
                        if stopthread.is_set():
                            return
                        if not chunk:
                            break
                        bytes_read += len(chunk)
                        fraction_read = bytes_read / total_bytes
                        for name, h in hashers.items():
                            h["hasher"].update(chunk)
                        percentage_read = int(fraction_read * 100)
                        if percentage_read != last_percentage:
                            # print(f"{f_path}: {fraction_read*100:4.1f}%")
                            treestore.set_value(file_iter, 3, percentage_read)
                            last_percentage = percentage_read
                for name, h in hashers.items():
                    treestore.set_value(h["iter"], 2, h["hasher"].hexdigest())
                treeview.expand_row(treestore.get_path(file_iter), True)

        thread = threading.Thread(target=fill_treestore)
        thread.daemon = True
        thread.start()

        dialog.run()
        stopthread.set()
        dialog.destroy()

        del self._ui
