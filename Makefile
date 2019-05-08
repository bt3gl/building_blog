html:
	pelican content
clean:
	$rm -rf output/*
	$rm -rf *pyc
copy:
	cp -r output/* ../bt3gl.github.io/ 

