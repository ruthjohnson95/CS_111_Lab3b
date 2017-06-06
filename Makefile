
dist:
	tar -czvf lab3b-304682182.tar.gz lab3b.py Makefile 

check:	dist
	./P3B_check.sh 304682182