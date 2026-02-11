class Block:
    BLOCK_SIZE = 4096  # 4KB per block

    def __init__(self, block_id):
        self.block_id = block_id
        self.data = b""        # raw bytes
        self.is_free = True    # block availability

    def write(self, data: bytes):
        if len(data) > self.BLOCK_SIZE:
            raise ValueError("Data exceeds block size")
        self.data = data
        self.is_free = False

    def read(self) -> bytes:
        return self.data

    def clear(self):
        self.data = b""
        self.is_free = True
