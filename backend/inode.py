import time


class Inode:
    def __init__(self, name, inode_type="file"):
        self.name = name
        self.type = inode_type  # "file" or "dir"

        # File-specific
        self.size = 0
        self.blocks = []

        # Directory-specific
        self.children = {} if inode_type == "dir" else None

        # Metadata
        now = time.time()
        self.created_at = now
        self.modified_at = now
        self.accessed_at = now

        # Permissions (simple)
        self.permissions = "rw"

    def is_file(self):
        return self.type == "file"

    def is_dir(self):
        return self.type == "dir"

    def update_size(self, size):
        self.size = size
        self.modified_at = time.time()

    def access(self):
        self.accessed_at = time.time()

    def to_dict(self):
        """Used for persistence"""
        return {
            "name": self.name,
            "type": self.type,
            "size": self.size,
            "blocks": self.blocks,
            "permissions": self.permissions,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "accessed_at": self.accessed_at,
            "children": {
                k: v.to_dict() for k, v in self.children.items()
            } if self.children is not None else None,
        }

    @staticmethod
    def from_dict(data):
        inode = Inode(data["name"], data["type"])
        inode.size = data["size"]
        inode.blocks = data["blocks"]
        inode.permissions = data["permissions"]
        inode.created_at = data["created_at"]
        inode.modified_at = data["modified_at"]
        inode.accessed_at = data["accessed_at"]

        if data["children"] is not None:
            inode.children = {
                k: Inode.from_dict(v) for k, v in data["children"].items()
            }

        return inode
