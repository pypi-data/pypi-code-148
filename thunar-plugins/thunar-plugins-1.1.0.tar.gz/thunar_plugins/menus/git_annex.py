# system modules
import logging
import os
import subprocess
import shutil
import shlex
import pathlib

# internal modules
from thunar_plugins import l10n
from thunar_plugins.log import console

# external modules
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import GObject, Gtk, Thunarx

logger = logging.getLogger(__name__)


class GitAnnexSubmenu(GObject.GObject, Thunarx.MenuProvider):
    @classmethod
    def name(cls):
        s = _("Git Annex Context-Menu")
        if not shutil.which("git-annex"):
            s = _("[Unavailable]") + " " + s
        return s

    @classmethod
    def description(cls):
        s = _(
            "This plugin adds a context menu item "
            "for managing Git Annex repositories."
        )
        if not shutil.which("git-annex"):
            s += " " + _(
                "Install Git Annex to use this plugin: "
                "https://git-annex.branchable.com"
            )
        return s

    def __init__(self):
        pass

    @classmethod
    def run_git_annex(
        cls,
        subcmd,
        paths=None,
        reset_before=True,
        args=None,
        cwd=None,
        terminal=True,
        keep_open_on_success=False,
        keep_open_on_failure=True,
        dry_run=False,
    ):
        args = args or []
        paths = paths or []
        cmdparts = ["git", "annex", subcmd] + args + paths
        logger.debug(f"Bare {cmdparts = }")
        if logger.getEffectiveLevel() <= logging.DEBUG:
            console.print(f"📋 Copy-pastable:\n\n{shlex.join(cmdparts)}\n")
        if reset_before:
            cmdparts = [
                "sh",
                "-xc",
                ";".join(
                    shlex.join(p) for p in (["git", "reset"] + paths, cmdparts)
                ),
            ]
            logger.debug(f"With git resetting: {cmdparts = }")
            if logger.getEffectiveLevel() <= logging.DEBUG:
                console.print(f"📋 Copy-pastable:\n\n{shlex.join(cmdparts)}\n")
        if not shutil.which("xfce4-terminal"):
            logger.warning(
                f"xfce4-terminal not found. Currently, "
                f"this is the only terminal our git-annex integration supports. "
                f"Continuing without showing commands in terminal."
            )
            terminal = False
        if terminal:

            def close_cmd(text, timeout=None):
                return ";".join(
                    map(
                        shlex.join,
                        [["echo"], ["echo", text]]
                        + (
                            [
                                ["echo", "This window will auto-close soon."],
                                ["sleep", str(int(timeout))],
                                ["exit"],
                            ]
                            if isinstance(timeout, int)
                            else [
                                ["echo", "You can close this window now."],
                                ["sleep", "infinity"],
                            ]
                        ),
                    )
                )

            cmdparts = [
                "sh",
                "-c",
                f"(set -x;{shlex.join(cmdparts)}) "
                f"&& ({close_cmd('✅ Success!',timeout=None if keep_open_on_success else 10)}) "
                f"|| ({close_cmd('💥 Failure!',timeout=None if keep_open_on_failure else 10)})",
            ]
            logger.debug(f"What the terminal will be given: {cmdparts = }")
            if logger.getEffectiveLevel() <= logging.DEBUG:
                console.print(f"📋 Copy-pastable:\n\n{shlex.join(cmdparts)}\n")
            cmdparts = [
                "xfce4-terminal",  # TODO: Hard-coded terminal emulator is bad
                "--icon",
                "git-annex",
                "--hide-menubar",
                "--hide-toolbar",
                "--command",
                shlex.join(cmdparts),
            ]
        logger.info(f"🚀 Running {cmdparts = }")
        if logger.getEffectiveLevel() <= logging.DEBUG:
            console.print(f"📋 Copy-pastable:\n\n{shlex.join(cmdparts)}\n")
        if dry_run:
            return cmdparts
        else:
            return subprocess.run(cmdparts, cwd=cwd)

    @classmethod
    def get_git_annex_uuid(cls, folder):
        try:
            return subprocess.check_output(
                ["git", "-C", folder, "config", "annex.uuid"],
                encoding="utf-8",
                errors="ignore",
            ).strip()
        except subprocess.CalledProcessError as e:
            logger.info(f"{folder!r} is apparently no git repository: {e}")

    def get_file_menu_items(self, window, items):
        folders = set(
            (
                f.get_location().get_path()
                if f.is_directory()
                else os.path.dirname(f.get_location().get_path())
            )
            for f in items
        )
        folder_uuids = {d: self.get_git_annex_uuid(d) for d in folders}
        uuids = set(folder_uuids.values())
        if not (len(uuids) == 1 and all(uuids)):
            logger.info(
                f"Not exactly ONE unique git-annex repo selected: "
                f"{folder_uuids = }"
            )
            return []
        cwd = next(iter(folder_uuids))
        logger.debug(f"Will operate in {cwd = }")
        repo = subprocess.check_output(
            ["git", "-C", cwd, "rev-parse", "--show-toplevel"],
            encoding="utf-8",
            errors="ignore",
        ).rstrip("\r\n")
        logger.debug(f"{repo = }")

        # Note: Using a relative path to the repo is necessary as git-annex/git
        # doesn't see paths behind symlinks in the repo as tracked. So we need
        # to give it the actual absolute path in the repo
        # (see https://git-annex.branchable.com/bugs/Paths_behind_relative_symlinks_in_repo_don__39__t_work/)
        def path_for_git(path, repo=repo):
            repo = pathlib.Path(repo)
            objects_dir = (repo / ".git" / "annex" / "objects").resolve()
            p = pathlib.Path(path)
            # find the last link in the chain pointing to the actual annex
            while p.is_symlink():
                logger.debug(
                    f"{str(p)!r} is a symlink to {str(p.readlink())!r}"
                )
                if objects_dir in p.resolve().parents:
                    logger.debug(
                        f"{str(p)!r} is a git annex symlink "
                        f"pointing within {str(objects_dir)!r}"
                    )
                    # something dir in the path can still be a link, so we resolve the parent
                    return str(p.parent.resolve() / p.name)
                logger.debug(
                    f"following {str(p)!r} symlink to {str(p.readlink())!r}"
                )
                p = p.readlink()
            logger.debug(
                f"{str(p)!r} is no symlink, resolved path for git is {str(p.resolve())!r}"
            )
            return str(p.resolve())

        paths = [str(path_for_git(f.get_location().get_path())) for f in items]

        notify_flags = ["--notify-start", "--notify-finish"]
        if any(i.is_directory() for i in items) or len(items) > 10:
            logger.debug(
                f"Directory or too many files selected, "
                f"won't show desktop notifications"
            )
            notify_flags = []

        def on_click(menuitem, **kwargs):
            kwargs = {**dict(cwd=cwd), **kwargs}
            menuitem.connect(
                "activate",
                lambda item, *a, **kw: self.run_git_annex(**kwargs),
            )

        # top-level Git Annex context menu entry
        git_annex_menuitem = Thunarx.MenuItem(
            name="ContextMenu::GitAnnex",
            label=_("Git Annex"),
            tooltip=_("Git Annex File Synchronization"),
            icon="git-annex",
        )

        git_annex_sync_menuitem = Thunarx.MenuItem(
            name="ContextMenu::GitAnnexSync",
            label=_("Sync"),
            tooltip=_("Synchronize Git Annex state with other repos")
            + " (git annex sync)",
            icon="emblem-synchronizing",
        )
        on_click(git_annex_sync_menuitem, subcmd="sync")

        git_annex_add_menuitem = Thunarx.MenuItem(
            name="ContextMenu::GitAnnexAdd",
            label=_("Add"),
            tooltip=_("Add untracked files to Git Annex") + " (git annex add)",
            icon="list-add",
        )
        on_click(
            git_annex_add_menuitem,
            subcmd="add",
            paths=paths,
            reset_before=False,
            args=notify_flags,
        )

        git_annex_get_menuitem = Thunarx.MenuItem(
            name="ContextMenu::GitAnnexGet",
            label=_("Get"),
            tooltip=_("Retreve files with Git Annex") + " (git annex get)",
            icon="edit-download",
        )
        on_click(
            git_annex_get_menuitem,
            subcmd="get",
            paths=paths,
            reset_before=True,
            args=notify_flags,
        )

        git_annex_drop_menuitem = Thunarx.MenuItem(
            name="ContextMenu::GitAnnexDrop",
            label=_("Drop"),
            tooltip=_("Drop files safely with Git Annex")
            + " (git annex drop)",
            icon="edit-delete",
        )
        on_click(
            git_annex_drop_menuitem,
            subcmd="drop",
            paths=paths,
            reset_before=True,
            args=notify_flags,
        )

        git_annex_lock_menuitem = Thunarx.MenuItem(
            name="ContextMenu::GitAnnexLock",
            label=_("Lock"),
            tooltip=_(
                "Lock files with Git Annex. "
                "This saves disk space and is faster but makes them read-only."
            )
            + " (git annex lock)",
            icon="object-locked",
        )
        on_click(
            git_annex_lock_menuitem,
            subcmd="lock",
            paths=paths,
            reset_before=True,
        )

        git_annex_unlock_menuitem = Thunarx.MenuItem(
            name="ContextMenu::GitAnnexUnlock",
            label=_("Unlock"),
            tooltip=_(
                "Unlock files with Git Annex to make them editable. "
                "Increases disk usage and is slower."
            )
            + " (git annex unlock)",
            icon="object-unlocked",
        )
        on_click(
            git_annex_unlock_menuitem,
            subcmd="lock",
            paths=paths,
            reset_before=True,
        )

        git_annex_metadata_menuitem = Thunarx.MenuItem(
            name="ContextMenu::GitAnnexMetadata",
            label=_("Metadata"),
            tooltip=_("Show Git Annex Metadata") + " (git annex metadata)",
            icon="dialog-information",
        )
        on_click(
            git_annex_metadata_menuitem,
            subcmd="metadata",
            paths=paths,
            keep_open_on_success=True,
        )

        git_annex_submenu = Thunarx.Menu()
        git_annex_submenu.append_item(git_annex_sync_menuitem)
        git_annex_submenu.append_item(git_annex_add_menuitem)
        git_annex_submenu.append_item(git_annex_get_menuitem)
        git_annex_submenu.append_item(git_annex_drop_menuitem)
        git_annex_submenu.append_item(git_annex_lock_menuitem)
        git_annex_submenu.append_item(git_annex_unlock_menuitem)
        git_annex_submenu.append_item(git_annex_metadata_menuitem)
        git_annex_menuitem.set_menu(git_annex_submenu)

        return (git_annex_menuitem,)

    def get_folder_menu_items(self, window, folder):
        return self.get_file_menu_items(window, [folder])
