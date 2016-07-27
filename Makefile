html:
	pelican content

github: cd output
	git add -A
	git commit -m $1
	git push origin master
