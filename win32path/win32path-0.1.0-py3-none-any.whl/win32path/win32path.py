import json
import os


class Win32Path:
    def __init__(self):
        """
            Initialize the class and create the paths file if it doesn't exist.
        """
        self.paths_file = os.path.expandvars(
            '%APPDATA%/Local/win32path/paths.json'
        )
        if not os.path.exists(self.paths_file):
            os.makedirs(os.path.dirname(self.paths_file), exist_ok=True)
            with open(self.paths_file, 'w') as f:
                json.dump({}, f)

    def list_paths(self) -> dict:
        """Returns a dict of all the registered paths."""
        try:
            with open(self.paths_file, 'r') as f:
                return json.load(f)
        except json.decoder.JSONDecodeError as e:
            print(f'Error decoding JSON: {e}')
            return {}

    def get_path(self, key) -> str:
        """Returns the path associated with the specified key."""
        try:
            with open(self.paths_file, 'r') as f:
                paths = json.load(f)
                return paths.get(key)
        except json.decoder.JSONDecodeError as e:
            print(f'Error decoding JSON: {e}')
            return None

    def set_path(self, key, value) -> None:
        """Save the specified path for the specified key."""
        try:
            with open(self.paths_file, 'r') as f:
                paths = json.load(f)
        except json.decoder.JSONDecodeError as e:
            print(f'Error decoding JSON: {e}')
            paths = {}
            
        paths[key] = value
        try:
            with open(self.paths_file, 'w') as f:
                json.dump(paths, f)
        except json.decoder.JSONDecodeError as e:
            print(f'Error encoding JSON: {e}')

    def update_path(self, key, value) -> None:
        """Updates the path associated with the specified key."""
        self.set_path(key, value)

    def delete_path(self, key) -> None:
        """Removes the path associated with the specified key."""
        try:
            with open(self.paths_file, 'r') as f:
                paths = json.load(f)
        except json.decoder.JSONDecodeError as e:
            print(f'Error decoding JSON: {e}')
            paths = {}
        
        paths.pop(key, None)
        try:
            with open(self.paths_file, 'w') as f:
                json.dump(paths, f)
        except json.decoder.JSONDecodeError as e:
            print(f'Error decoding JSON: {e}')
