html:
	pelican content
clean:
	rm -rf output/*
	rm -rf *pyc
	rm -rf __pycache__/
copy:
	cp -r output/* ../bt3gl.github.io/ 

