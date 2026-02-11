class Block:
    def __init__(self, block_id):
        self.block_id = block_id
        self.data = b""

    def write(self, data):
        self.data = data

    def read(self):
        return self.data


class StorageManager:
    def __init__(self, total_blocks=256, block_size=4096):
        self.total_blocks = total_blocks
        self.block_size = block_size
        self.blocks = {}
        self.free_block_ids = list(range(total_blocks))

    # -------------------------
    # Allocation
    # -------------------------
    def allocate_blocks(self, data):
        blocks_needed = (len(data) // self.block_size) + 1
        if blocks_needed > len(self.free_block_ids):
            raise MemoryError("Not enough storage")

        allocated = []
        for i in range(blocks_needed):
            block_id = self.free_block_ids.pop(0)
            block = Block(block_id)
            start = i * self.block_size
            end = start + self.block_size
            block.write(data[start:end])
            self.blocks[block_id] = block
            allocated.append(block_id)

        return allocated

    def free_blocks(self, block_ids):
        for block_id in block_ids:
            if block_id in self.blocks:
                del self.blocks[block_id]
                self.free_block_ids.append(block_id)

    # -------------------------
    # Persistence helpers ✅
    # -------------------------
    def to_dict(self):
        return {
            "total_blocks": self.total_blocks,
            "block_size": self.block_size,
            "blocks": {
                str(bid): self.blocks[bid].data.decode(errors="ignore")
                for bid in self.blocks
            },
            "free_block_ids": self.free_block_ids,
        }

    def from_dict(self, data):
        self.total_blocks = data["total_blocks"]
        self.block_size = data["block_size"]
        self.blocks = {}
        for bid, content in data["blocks"].items():
            block = Block(int(bid))
            block.write(content.encode())
            self.blocks[int(bid)] = block
        self.free_block_ids = data["free_block_ids"]
