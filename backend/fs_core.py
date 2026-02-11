# fs_core.py
# Core File System Structures

BLOCK_SIZE = 4096
TOTAL_BLOCKS = 256

# Simulated disk blocks
data_blocks = [None] * TOTAL_BLOCKS

# Free block list
free_blocks = list(range(TOTAL_BLOCKS))

# Inode table
inode_table = {}

class Inode:
    def __init__(self, name):
        self.name = name
        self.size = 0
        self.blocks = []
