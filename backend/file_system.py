import pickle
import time


class Inode:
    def __init__(self, filename, is_dir=False):
        self.filename = filename
        self.is_dir = is_dir
        self.size = 0
        self.blocks = []
        self.created_at = time.time()
        self.modified_at = self.created_at
        self.accessed_at = self.created_at
        self.permissions = "rw"


class StorageManager:
    def __init__(self):
        self.blocks = {}

    def write(self, block_id, data):
        self.blocks[block_id] = data

    def read(self, block_id):
        return self.blocks.get(block_id, b"")

    def free(self, block_ids):
        for b in block_ids:
            self.blocks.pop(b, None)


class FileSystem:
    def __init__(self):
        self.inode_table = {}
        self.storage = StorageManager()
        self.next_block = 0
        self.load()

    # ---------- Persistence ----------
    def save(self):
        with open("fs_state.pkl", "wb") as f:
            pickle.dump((self.inode_table, self.storage, self.next_block), f)

    def load(self):
        try:
            with open("fs_state.pkl", "rb") as f:
                data = pickle.load(f)
                if isinstance(data, tuple) and len(data) == 3:
                    self.inode_table, self.storage, self.next_block = data
                else:
                    self.inode_table = {}
                    self.storage = StorageManager()
                    self.next_block = 0
        except FileNotFoundError:
            self.inode_table = {}
            self.storage = StorageManager()
            self.next_block = 0

    # ---------- Core ----------
    def create_file(self, filename):
        if filename in self.inode_table:
            raise FileExistsError("File already exists")
        self.inode_table[filename] = Inode(filename)
        self.save()

    def delete_file(self, filename):
        inode = self.inode_table.pop(filename)
        self.storage.free(inode.blocks)
        self.save()

    def write_file(self, filename, data):
        inode = self.inode_table[filename]
        self.storage.free(inode.blocks)
        inode.blocks = []

        block_id = self.next_block
        self.next_block += 1
        self.storage.write(block_id, data.encode())
        inode.blocks.append(block_id)
        inode.size = len(data)
        inode.modified_at = time.time()
        self.save()

    def read_file(self, filename):
        inode = self.inode_table[filename]
        inode.accessed_at = time.time()
        content = b"".join(self.storage.read(b) for b in inode.blocks)
        return content.decode()

    def rename_file(self, old, new):
        inode = self.inode_table.pop(old)
        inode.filename = new
        self.inode_table[new] = inode
        self.save()

    def list_files(self):
        return list(self.inode_table.keys())

    def file_info(self, filename):
        i = self.inode_table[filename]
        return {
            "Filename": i.filename,
            "Size (bytes)": i.size,
            "Blocks": i.blocks,
            "Created": time.ctime(i.created_at),
            "Modified": time.ctime(i.modified_at),
            "Accessed": time.ctime(i.accessed_at),
            "Permissions": i.permissions,
        }
