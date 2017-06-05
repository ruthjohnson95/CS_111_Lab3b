import csv
import sys
import os.path

block_freelist=[]
inode_freelist=[]
inode_list=[]

def block_consistency_audits(row):
    print("checking for block consistency...")

def inode_allocation_audits():
    print("checking for inode allocations...")

    # check for inodes on FREELIST but have links
    # loop through indoes on FREELIST; save in temp list
    # loop through to see if any have links > 0

    for free_inode in inode_freelist: # loop through all of free inodes
        for inode in inode_list: # compare with inodes on list
            if free_inode == inode[1]: # if inode from summary is on free list
                # check for link number
                link_count = inode[6] # check to see if link count is 0
                if link_count > 0:
                    # allocated inode on freelist
                    print("ALLOCATED INODE {0} ON FREELIST".format(inode[1]))

    # look for unallocated inodes NOT on the freelist
    for inode in inode_list:
        inode_number = inode[1]
        link_count = inode[6]
        if link_count == 0 and inode_number not in inode_freelist:
            print("UNALLOCATED INODE {0} NOT ON FREELIST".format(inode_number))

                # discrepency

    # check for inodes with 0 links but not on FREELIST

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
            for i, field in enumerate(row):
                #print row[i]
                if i == 1:
                    row[i]=int(row[i])
                elif i >=3 and i <=6:
                    row[i]=int(row[i])
                elif i >=10:
                    row[i]=int(row[i])


        # fill in block freelist
        if row[0] == 'BFREE':
            block_freelist.append(int(row[1]))

        # fill in inode freelist
        if row[0] == 'IFREE':
            inode_freelist.append(int(row[1]))

        # inodes
        if row[0] == 'INODE':
            inode_list.append(row)



    #print block_freelist
    print inode_freelist
    #print inode_list


    block_consistency_audits(row)

    inode_allocation_audits()

    directory_consistency_audits(row)

    f.close()

if __name__ == "__main__":
    main()
