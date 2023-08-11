from pathlib import Path
from typing import Union, Any


class BufferManager:
    root_folder: Path = Path(__file__).parent / "Temp"
    file_tree: dict = dict()
    
    @classmethod
    def _build_file_tree(cls, folder: Path):
        file_tree = {"name": folder.name, "size": 0, "subfolders": [], "files": []}

        for item in folder.iterdir():
            if item.is_dir():
                subfolder_tree = cls._build_file_tree(item)
                file_tree["subfolders"].append(subfolder_tree)
                file_tree["size"] += subfolder_tree["size"]
            elif item.is_file():
                file_size = item.stat().st_size
                file_tree["files"].append({"name": item.name, "size": file_size})
                file_tree["size"] += file_size

        return file_tree
    
    @classmethod
    def display_file_tree(cls):
        cls.file_tree = cls._build_file_tree(cls.root_folder)
        cls._display_tree(cls.file_tree, 0)

    @classmethod
    def _display_tree(cls, tree: dict, depth: int):
        print(
            "  " * depth
            + tree["name"]
            + " ("
            + cls._human_readable_size(tree["size"])
            + ")"
        )

        for subfolder in tree["subfolders"]:
            cls._display_tree(subfolder, depth + 1)

        for file in tree["files"]:
            print(
                "  " * (depth + 1)
                + file["name"]
                + " ("
                + cls._human_readable_size(file["size"])
                + ")"
            )

    @classmethod
    def _human_readable_size(cls, size: float):
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0

    @classmethod
    def calculate_total_size(cls):
        cls.file_tree = cls._build_file_tree(cls.root_folder)
        return cls._human_readable_size(cls.file_tree["size"])

    @classmethod
    def delete_files(cls):
        if cls.file_tree == {}:
            cls.file_tree = cls._build_file_tree(cls.root_folder)
        cls._delete_files_recursive(cls.file_tree)

    @classmethod
    def _delete_files_recursive(cls, tree: dict):
        for subfolder in tree["subfolders"]:
            cls._delete_files_recursive(subfolder)

        for file in tree["files"]:
            file_path = cls.root_folder / tree["name"] / file["name"]
            try:
                file_path.unlink()
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
