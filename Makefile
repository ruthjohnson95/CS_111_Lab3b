# NAME: Ruth Johnson
# EMAIL: ruthjohnson@ucla.edu
# ID: 704275412

default:
	chmod u+x lab3b.py
	cp lab3b.py lab3b

dist:
	tar -czvf lab3b-704275412.tar.gz lab3b.py Makefile README

clean:
	rm lab3b
