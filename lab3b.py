import csv
import sys
import os.path


def block_consistency_audits(row):
    print("checking for block consistency...")

def inode_allocation_audits(row):
    print("checking for inode allocations...")

def directory_consistency_audits(row):
    print("checking for directory consistency")

def main():

    file = sys.argv[1]

    # check if file exists
    if(!os.path.exists(if)):
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
        print row

    block_consistency_audits(row)

    inode_allocation_audits(row)

    directory_consistency_audits(row)

    f.close()

if __name__ == "__main__":
    main()
