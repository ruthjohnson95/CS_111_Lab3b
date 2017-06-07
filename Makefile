.SILENT:

default:
	chmod u+x lab3b.py
	chmod 755 lab3b
dist:
	tar -czvf lab3b-704275412.tar.gz lab3b.py lab3b README Makefile
clean:
	rm -rf lab3b-704275412.tar.gz

check:	dist
	./P3B_check.sh 704275412