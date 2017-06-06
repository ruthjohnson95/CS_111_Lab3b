import csv
import sys
import os.path

block_freelist=[]
inode_freelist=[]
inode_list=[]
inode_num_list=[]
indirect_list = []
allocated_list = []
dirent_list = []


single_offset = 12
double_offset = 268
triple_offset = 65804


level = ["BLOCK","INDIRECT" , "DOUBLE INDIRECT", "TRIPPLE INDIRECT"]

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

class Indirect:
    def __init__ (self, inode_number, level, block_offset, parent, block_num):
        self.m_inode_number = int(inode_number)
        self.m_level = int(level)
        self.m_block_offset = int(block_offset)
        self.m_parent = int(parent)
        self.m_block_num = int(block_num)

class Dirent:
    def __init__ (self, parent, inode_number,name):
        self.m_parent = int(parent)
        self.m_inode_number = int(inode_number)
        self.m_name = name
    
superblock = Superblock(0,0,0,0,0,0,0)

def ifDataBlock(block_num):
    if block_num < 0  or block_num > superblock.num_blocks:
        # TODO: ask if 0 is invalid or reserved
        return False

    if block_num in block_freelist:
        return False

    return True

def ifReservedBlock(block_num):
    # TODO check range with TA
    if block_num < 8 and block_num > 0:
        return True
    #elif block_num not in block_freelist and block_num > 0  and block_num < superblock.num_blocks:
    #    return True
    else:
        return False

def isValidInode (inode_num):
    if inode_num in range(0, superblock.i_node_per_group+1):
        return True
    return False

def isAllocatedInode (inode_num):
    for inode in inode_list:
        if (inode.m_inode_num == inode_num):
            if (inode.m_mode > 0) and (inode.m_link_count > 0):
                return True
            return False
    return False

def block_consistency_audits():
    print("checking for block consistency...")

    block_list = [0] * (superblock.num_blocks +1)

    for inode in inode_list:
        #print (inode.m_inode_num)
        for i in range(0,12): # NOTE: not inclusive range
            # check if invalid
            block_num = inode.m_block_pointers[i]
            if not ifDataBlock(block_num):
                print("INVALID BLOCK {0} IN INODE {1} AT OFFSET {2}".format(inode.m_block_pointers[i], inode.m_inode_num, i))

            if ifReservedBlock(block_num):
                print("RESERVED BLOCK {0} IN INODE {1} AT OFFSET {2}".format(inode.m_block_pointers[i], inode.m_inode_num, i))

        for i in range(12,15):
            # TODO: change offset for indirect blocks
            #print i
            #print inode.m_block_pointers[i]
            if not ifDataBlock(inode.m_block_pointers[i]):
                # indirect
                if i == 12:
                    print("INVALID {0} BLOCK {1} IN INODE {2} AT OFFSET {3}".format(level[i-11],inode.m_block_pointers[i], inode.m_inode_num, single_offset))
                if i == 13:
                    print("INVALID {0} BLOCK {1} IN INODE {2} AT OFFSET {3}".format(level[i-11],inode.m_block_pointers[i], inode.m_inode_num, double_offset))
                if i == 14:
                    print("INVALID {0} BLOCK {1} IN INODE {2} AT OFFSET {3}".format(level[i-11],inode.m_block_pointers[i], inode.m_inode_num, triple_offset))



    # print("INVALID {0} BLOCK {1} IN INODE {2} AT OFFSET {3}".format(level[i-12],inode.m_block_pointers[i], inode.m_inode_num, i))

            if ifReservedBlock(block_num):
                if i == 12:
                    print("RESERVED {0} BLOCK {1} IN INODE {2} AT OFFSET {3}".format(level[i-11],inode.m_block_pointers[i], inode.m_inode_num, single_offset))
                if i == 13:
                    print("RESERVED {0} BLOCK {1} IN INODE {2} AT OFFSET {3}".format(level[i-11],inode.m_block_pointers[i], inode.m_inode_num, double_offset))
                if i == 14:
                    print("RESERVED {0} BLOCK {1} IN INODE {2} AT OFFSET {3}".format(level[i-11],inode.m_block_pointers[i], inode.m_inode_num, triple_offset))

    for i in range(8, superblock.num_blocks ):
        # if not on the free list and not in the allocated list
        if (i not in block_freelist) and (i not in allocated_list):
            # unfreferenced
            print("UNREFERENCED BLOCK {0}".format(i))

        elif(i in block_freelist) and (i in allocated_list):
            print("ALLOCATED BLOCK {0} ON FREELIST".format(i))

    for j in range (0, len(allocated_list)):
        if (allocated_list[j] not in block_freelist):
            # check number of times referenced
            block_list[allocated_list[j]] = block_list[allocated_list[j]] + 1

    #print block_list
    for i in range(8,superblock.num_blocks+1):

        if block_list[i] > 1:
            # find the duplicates
            # loop through inodes
            for inode in inode_list:
                # direct
                for j in range(0,12):
                    if inode.m_block_pointers[j] == i:
                        print("DUPLICATE BLOCK {0} IN INODE {1} AT OFFSET {2}".format(i, inode.m_inode_num, j))
                # indirect
                if inode.m_block_pointers[12] == i:
                    print("DUPLICATE INDIRECT BLOCK {0} IN INODE {1} AT OFFSET {2}".format(i, inode.m_inode_num, single_offset))
                if inode.m_block_pointers[13] == i:
                    print("DUPLICATE DOUBLE INDIRECT BLOCK {0} IN INODE {1} AT OFFSET {2}".format(i, inode.m_inode_num, double_offset))
                if inode.m_block_pointers[14] == i:
                    print("DUPLICATE TRIPPLE INDIRECT BLOCK {0} IN INODE {1} AT OFFSET {2}".format(i, inode.m_inode_num, triple_offset))

            # loop through indirect list
            for indirect in indirect_list:
                if i == indirect.m_block_num:
                    # it's a duplicates
                    print("DUPLICATE {0} BLOCK {1} IN INODE {2} AT OFFSET {3}".format(level[indirect.m_level], i, inode.m_inode_num, indirect.m_block_offset))

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

def directory_consistency_audits():
    print("checking for directory consistency")
    link_count_list = [0] * (superblock.num_inodes +1)
    parent_inode_list = [0] * (superblock.num_inodes +1) #index is the referenced inode number and the stored value is the parent inode number 
   
    #TODO: CHECK IF NEED THIS STEP. IF NOT REFERENCED DO WE ASSUME IT LINKS TO ITSELF
    for i in range (0,superblock.num_inodes +1):
        parent_inode_list[i] = i

    #loop through each dirent object
    for dirent in dirent_list:
        #check if the referenced inode is valid 
        if not (isValidInode(dirent.m_inode_number)):
            print ("DIRECTORY INODE {0} NAME {1} INVALID INODE {2}".format(dirent.m_parent,dirent.m_name,dirent.m_inode_number))
        elif not (isAllocatedInode (dirent.m_inode_number)):
            print ("DIRECTORY INODE {0} NAME {1} UNALLOCATED INODE {2}".format(dirent.m_parent,dirent.m_name,dirent.m_inode_number))
        else:
            link_count_list[dirent.m_inode_number] = link_count_list[dirent.m_inode_number] +1
            
            if (dirent.m_name != "'.'") and (dirent.m_name != "'..'") : 
                parent_inode_list[dirent.m_inode_number] = dirent.m_parent
    #check link consistancy
    for inode in inode_list:
        if inode.m_link_count != link_count_list[inode.m_inode_num]:
            sys.stdout.write ("INODE {0} HAS {1} LINKS BUT LINKCOUNT IS {2}".format(inode.m_inode_num,link_count_list[inode.m_inode_num],inode.m_link_count))

    #check parent child consistency 
    #check if current directory points to itself
    for dirent in dirent_list:
        if dirent.m_name == "'.'": 
            if dirent.m_parent != dirent.m_inode_number:
                sys.stdout.write ("DIRECTORY INODE {0} NAME '.' LINK TO INODE {1} SHOULD BE {1}".format(dirent.m_parent,dirent.m_inode_number))

    #print parent_inode_list
    
    for dirent in dirent_list:
        if dirent.m_name == "'..'":
            if dirent.m_inode_number != parent_inode_list[dirent.m_parent]:
                sys.stdout.write("DIRECTORY INODE {0} NAME '..' LINK TO INODE {1} SHOULD BE {2}".format(dirent.m_parent,dirent.m_inode_number, parent_inode_list[dirent.m_parent]))

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
            inode_list.append(Inode(int(row[1]),row[2], int(row[3]), int(row[6]),int(row[11]), map(int, row[12:27])))
            for i in range(12,27):
                allocated_list.append(int(row[i]))

            inode_num_list.append(int(row[1]))

        if row[0] == 'SUPERBLOCK':
            superblock.num_blocks = int(row[1])
            superblock.num_inodes = int(row[2])
            superblock.block_size = int(row[3])
            superblock.inode_size = int(row[4])
            superblock.block_per_group= int(row[5])
            superblock.i_node_per_group= int(row[6])
            superblock.first_free_inode= int(row[7])

        if row[0] == 'INDIRECT':
            indirect_list.append(Indirect(row[1], row[2], row[3], row[4], row[5]))
            allocated_list.append(int(row[5]))

        # fill in block freelist
        if row[0] == 'BFREE':
            block_freelist.append(int(row[1]))

        # fill in inode freelist
        if row[0] == 'IFREE':
            inode_freelist.append(int(row[1]))

        if row[0] == "DIRENT":
            dirent_list.append(Dirent(int(row[1]), int(row[3]), row[6]))



    block_consistency_audits()
    inode_allocation_audits()
    #print allocated_list

    directory_consistency_audits()

    f.close()

if __name__ == "__main__":
    main()
