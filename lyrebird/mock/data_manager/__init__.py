from pathlib import Path
import json
from .group import Group
from .exceptions import DataRootDirNotExistsError, ActivateFailed
from .mock_router import MockRouter


class DataManager:

    def __init__(self):
        self._root_path = None
        self.activated_group_id = None
        self.groups = {}
        self.router = MockRouter()

    @property
    def root(self):
        return self._root_path

    @root.setter
    def root(self, root_path):
        new_path = Path(root_path).expanduser()
        if not new_path.exists():
            raise DataRootDirNotExistsError(root_path)
        self._root_path = new_path
        self.scan()

    def activate(self, group_id):
        if group_id in self.groups:
            self.activated_group_id = group_id
            group = self.groups.get(group_id)
            self.router.switch_group(group)
        else:
            raise ActivateFailed(f'Group id not found {group_id}')

    def deactivate(self, group_id):
        pass

    def create_group(self):
        group = Group.new_group(self.root)
        self.groups[group.id] = group
        return group

    def delete_group(self, group_id):
        group = self.groups.pop(group_id)
        if group:
            group.delete()

    def copy_croup(self):
        pass
    
    def scan(self):
        for sub_file in self.root.iterdir():
            if not sub_file.is_dir():
                continue
            group = Group.createify(sub_file)
            if group:
                self.groups[group.id] = group
    