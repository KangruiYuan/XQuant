from pathlib import Path


class BufferManager:
    def __init__(self, root_folder):
        self.root_folder = Path(root_folder)
        self.file_tree = {}

    def _build_file_tree(self, folder):
        file_tree = {'name': folder.name, 'size': 0, 'subfolders': [], 'files': []}

        for item in folder.iterdir():
            if item.is_dir():
                subfolder_tree = self._build_file_tree(item)
                file_tree['subfolders'].append(subfolder_tree)
                file_tree['size'] += subfolder_tree['size']
            elif item.is_file():
                file_size = item.stat().st_size
                file_tree['files'].append({'name': item.name, 'size': file_size})
                file_tree['size'] += file_size

        return file_tree

    def display_file_tree(self):
        self.file_tree = self._build_file_tree(self.root_folder)
        self._display_tree(self.file_tree, 0)

    def _display_tree(self, tree, depth):
        print("  " * depth + tree['name'] + " (" + self._human_readable_size(tree['size']) + ")")

        for subfolder in tree['subfolders']:
            self._display_tree(subfolder, depth + 1)

        for file in tree['files']:
            print("  " * (depth + 1) + file['name'] + " (" + self._human_readable_size(file['size']) + ")")

    def _human_readable_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0

    def calculate_total_size(self):
        self.file_tree = self._build_file_tree(self.root_folder)
        return self._human_readable_size(self.file_tree['size'])

    def delete_files(self):
        if self.file_tree == {}:
            self.file_tree = self._build_file_tree(self.root_folder)
        self._delete_files_recursive(self.file_tree)

    def _delete_files_recursive(self, tree):
        for subfolder in tree['subfolders']:
            self._delete_files_recursive(subfolder)

        for file in tree['files']:
            file_path = self.root_folder / tree['name'] / file['name']
            try:
                file_path.unlink()
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
