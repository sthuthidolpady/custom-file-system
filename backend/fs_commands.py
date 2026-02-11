# fs_commands.py
from fs_core import inode_table, free_blocks, data_blocks, Inode

def create_file(filename):
    if filename in inode_table:
        print("File already exists")
        return
    inode_table[filename] = Inode(filename)
    print(f"File '{filename}' created")

def write_file(filename, data):
    if filename not in inode_table:
        print("File not found")
        return

    inode = inode_table[filename]
    blocks_needed = len(data)

    if blocks_needed > len(free_blocks):
        print("Not enough space")
        return

    for char in data:
        block = free_blocks.pop(0)
        data_blocks[block] = char
        inode.blocks.append(block)

    inode.size = len(data)
    print("Write successful")

def read_file(filename):
    if filename not in inode_table:
        print("File not found")
        return

    inode = inode_table[filename]
    content = ""
    for block in inode.blocks:
        content += data_blocks[block]

    print("Content:", content)

def delete_file(filename):
    if filename not in inode_table:
        print("File not found")
        return

    inode = inode_table.pop(filename)
    for block in inode.blocks:
        data_blocks[block] = None
        free_blocks.append(block)

    print("File deleted")
