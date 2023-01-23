import os
import shutil
from pathlib import Path
from stat import S_IRWXG, S_IRWXO, S_IRWXU
from zipfile import ZipFile, ZipInfo

from ..logging import Logger, get_logger
from ..utils.text import format_message
from . import ActionType
from .confirm import ConfirmType, confirm

__all__: list[str] = ["extract"]


# https://stackoverflow.com/questions/39296101/python-zipfile-removes-execute-permissions-from-binaries
class MyZipFile(ZipFile):
    def _extract_member(self, member: str | ZipInfo, target_path: str, pwd: str) -> str:
        if isinstance(member, ZipInfo):
            zipinfo = member
        else:
            zipinfo = self.getinfo(member)
        target_path = super()._extract_member(zipinfo, target_path, pwd)  # type: ignore
        attr = (zipinfo.external_attr >> 16) & (S_IRWXU | S_IRWXG | S_IRWXO)
        if attr != 0:
            os.chmod(target_path, attr)
        return target_path


def unzip(src: str | Path, dst: str | Path) -> None:
    with MyZipFile(file=src, mode="r") as zip_file:
        zip_file.extractall(path=dst)


shutil.unregister_unpack_format(name="zip")
shutil.register_unpack_format(name="zip", extensions=[".zip"], function=unzip)


def extract(
    src: str | Path,
    dst: str | Path = Path.cwd(),
    confirm_type: ConfirmType = ConfirmType.DEFAULT,
    default: bool = True,
) -> None:
    logger: Logger = get_logger()
    message: str = format_message(
        action=ActionType.EXTRACT, src=src, dst=dst, markup=True
    )
    if not confirm(
        default=default,
        confirm_type=confirm_type,
        action=ActionType.EXTRACT,
        src=src,
        dst=dst,
    ):
        logger.skipped(message=message)
        return

    dst = Path(dst)
    os.makedirs(name=dst.parent, exist_ok=True)
    shutil.unpack_archive(filename=src, extract_dir=dst)

    logger.success(message=message)
