import base64
import logging
import os
from pathlib import Path
from threading import Lock
from typing import Dict, Optional

from RPA.core.locators import ImageTemplate  # type: ignore
from RPA.core.locators import BrowserDOM, Locator, LocatorsDatabase, sanitize_name

# The types mapping coming in from apiTypes!
DOC_TYPES = [
    "library",
    "keyword",
    "argument",
    "variable",
    "locator",
    "work-item",
]

LOCATOR_TYPES = [
    "browser",
    "windows",
    "image",
    "web-recorder",
]


class DatabaseError(Exception):
    """Common exception for Inspector's database errors."""


class Database:
    """Common interface for locators database."""

    def __init__(
        self, path: Optional[str] = None, load_on_start: Optional[bool] = None
    ):
        self.logger = logging.getLogger(__name__)
        self.cache: Dict[str, Dict] = {}
        self.lock = Lock()

        path = str(Path(path)) if path is not None else path
        self.internal_db = LocatorsDatabase(path)
        if load_on_start:
            self.load()
            if self.error:
                self.logger.warning(*self.error)

    @property
    def path(self):
        return self.internal_db.path

    @property
    def error(self):
        return self.internal_db.error

    @property
    def names(self):
        return list(sorted(self.internal_db.locators.keys()))

    @staticmethod
    def api_type_to_db_locator(api_type):
        if api_type["type"] in DOC_TYPES:
            temp = api_type["type"]
            api_type["type"] = api_type["kind"]
            api_type["kind"] = temp
            return api_type
        return api_type

    def _create_cache(self):
        locators: Dict[str, Dict] = {
            name: locator.to_dict()
            for name, locator in self.internal_db.locators.items()
        }

        def load_image(path) -> Optional[str]:
            root = Path(self.internal_db.path).parent
            try:
                with open(root / path, "rb") as infile:
                    return base64.b64encode(infile.read()).decode()
            except FileNotFoundError:
                self.logger.warning("Failed to read image: %s", path)
                return ""

        for locator in locators.values():
            if locator["type"] == "browser" and locator.get("screenshot"):
                locator["screenshot"] = load_image(locator["screenshot"])
            elif locator["type"] == "image":
                locator["value"] = load_image(locator["path"])

        self.cache = locators

    def load(self):
        with self.lock:
            self.internal_db.load()
            self._create_cache()

    def get(self, name):
        if name not in self.internal_db.locators:
            raise KeyError(f"No locator with name: {name}")
        return self.cache[name]

    def pop(self, name):
        if name not in self.internal_db.locators:
            raise KeyError(f"No locator with name: {name}")

        del self.internal_db.locators[name]
        val = self.cache.pop(name)
        return val

    def save(self):
        # Filter out stored source images, if they exist
        root = Path(self.internal_db.path).parent
        for locator in self.internal_db.locators.values():
            if not isinstance(locator, ImageTemplate):
                continue
            if not getattr(locator, "source", None):
                continue
            try:
                Path(root / str(locator.source)).unlink()
                self.logger.info("Removed source image: %s", locator.source)
                locator.source = None
            except FileNotFoundError:
                pass

        self.internal_db.save()
        self._create_cache()

    def list(self):
        """Convert current database to JSON."""
        if self.internal_db.error:
            message = self.internal_db.error[0] % self.internal_db.error[1]
            raise DatabaseError(message)
        return self.cache

    def update(self, name, fields):  # noqa: C901
        """Update locator entries."""
        with self.lock:
            if not name.strip():
                raise DatabaseError("Empty/missing locator name")

            fields = self.api_type_to_db_locator(fields)

            stored = self.internal_db.locators.get(name, {})
            cached = self.cache.get(name, {})

            def required(src, dst=None):
                dst = dst or src
                path = getattr(stored, dst, None)
                if fields[src] != cached.get(src):
                    fields[dst] = self._save_image(name, dst, fields[src], path)
                else:
                    fields[dst] = path

            def optional(src, dst=None):
                dst = dst or src
                val = fields.get(src)
                path = getattr(stored, dst, None)
                if val:
                    if val != cached.get(src):
                        fields[dst] = self._save_image(name, dst, val, path)
                    else:
                        fields[dst] = path
                elif path:
                    try:
                        Path(path).unlink()
                    except FileNotFoundError:
                        pass

            if fields["type"] == "browser":
                optional("screenshot")
            elif fields["type"] == "image":
                required("value", "path")

            try:
                self.internal_db.locators[name] = Locator.from_dict(fields)
            except ValueError as err:
                raise DatabaseError from err

            self.save()
            return self.list()

    def delete(self, name):
        """Delete locator entries."""
        with self.lock:
            if name not in self.internal_db.locators:
                raise DatabaseError(f"Unknown locator: {name}")

            locator = self.internal_db.locators.pop(name)

            def remove(key):
                path = getattr(locator, key, None)
                if not path:
                    return
                try:
                    Path(path).unlink()
                except FileNotFoundError:
                    pass

            if isinstance(locator, BrowserDOM):
                remove("screenshot")
            elif isinstance(locator, ImageTemplate):
                remove("path")

            self.save()
            return self.list()

    def _save_image(self, name, field, content, path=None):
        """Save base64 image into a file."""
        root = Path(self.internal_db.path).parent
        images = root / ".images"

        if path is not None and str(path).strip():
            path = root / path
        else:
            path = images / f"{sanitize_name(name)}-{field}.png"

        data = base64.b64decode(content)

        os.makedirs(images, exist_ok=True)
        with open(path, "wb") as outfile:
            outfile.write(data)

        return str(path.relative_to(root))
