import csv
import sys
import os.path

block_freelist=[]
inode_freelist=[]
inode_list=[]
inode_num_list=[]

class Superblock:
    def __init__(self, num_blocks, num_inodes,block_size, inode_size,block_per_group, i_node_per_group, first_free_inode):
        self.num_blocks = num_blocks
        self.num_inodes = num_inodes
        self.block_size = block_size
        self.inode_size = inode_size
        self.block_per_group = block_per_group
        self.i_node_per_group = i_node_per_group
        self.first_free_inode = first_free_inode

class Inode:
    def __init__ (self, inode_number, file_type, mode,link_count,num_blocks, block_pointers):
        self.m_inode_num = inode_number
        self.m_file_type = file_type
        self.m_mode = mode
        self.m_link_count = link_count
        self.m_num_blocks = num_blocks
        self.m_block_pointers = block_pointers # 15 pointers to data blocks


#    def __str__(self):
        #return "Inode Number: %s, File Type: %s, Mode: %s, Link Count: %s a is %s, b is %s" % (self.a, self.b)

superblock = Superblock(0,0,0,0,0,0,0)

def ifDataBlock(block_num):
    if block_num < 0  or block_num > superblock.num_blocks:
        # TODO: ask if 0 is invalid or reserved
        return False

    if block_num in block_freelist:
        return False

    return True

def ifReservedBlock(block_num):
    # TODO
    return True

def block_consistency_audits(row):
    print("checking for block consistency...")

    for inode in inode_list:

        for i in range(0,11):
            # check if invalid
            if not ifDataBlock(inode.m_block_pointers[i]):
                print("INVALID BLOCK {0} IN INODE {1} AT OFFSET".format(inode.m_block_pointers[i], inode.m_inode_num, i))

        for i in range(12,14):
            if not ifDataBlock(inode.m_block_pointers[i]):
                print("INVALID INDIRECT BLOCK {0} IN INODE {1} AT OFFSET".format(inode.m_block_pointers[i], inode.m_inode_num, i))




def inode_allocation_audits():
    print("checking for inode allocations...")
    # loop through inode


    for i in range(superblock.first_free_inode,  superblock.i_node_per_group):
        # check if inode is on freelist
        if i in inode_freelist:
            # check if has a summary entry in inode list
            # TODO: check if inode on summary means not free (without checking link count)
            if i in inode_num_list:
                #if inode.m_link_count > 0:
                print("ALLOCATED INODE {0} ON FREELIST".format(i))


        else: # if i is not on the freelist
            # check if it is on summary list (it should)
            if i not in inode_num_list:
                #if inode.m_link_count == 0:
                print("UNALLOCATED INODE {0} NOT ON FREELIST".format(i))


def directory_consistency_audits(row):
    print("checking for directory consistency")

def main():

    file = sys.argv[1]

    # check if file exists
    if not os.path.exists(file):
        sys.stderr.write("Error: File does not exist")
        sys.exit(1)

    # check if file is readable
    try:
        f = open(file,'rb')

    except IOError as err:
        sys.stderr.write("Error: File is unreadable")
        sys.exit(1)


    reader = csv.reader(f)

    for row in reader:
        #print row

        # convert ints in rows
        if row[0] == 'INODE':
            inode_list.append(Inode(int(row[1]),row[2], int(row[3]), int(row[6]),int(row[11]), map(int, row[12:26])))
            inode_num_list.append(int(row[1]))

        if row[0] == 'SUPERBLOCK':
            superblock.num_blocks = int(row[1])
            superblock.num_inodes = int(row[2])
            superblock.block_size = int(row[3])
            superblock.inode_size = int(row[4])
            superblock.block_per_group= int(row[5])
            superblock.i_node_per_group= int(row[6])
            superblock.first_free_inode= int(row[7])


        # fill in block freelist
        if row[0] == 'BFREE':
            block_freelist.append(int(row[1]))

        # fill in inode freelist
        if row[0] == 'IFREE':
            inode_freelist.append(int(row[1]))



    block_consistency_audits(row)
    inode_allocation_audits()

    #directory_consistency_audits(row)

    f.close()

if __name__ == "__main__":
    main()
