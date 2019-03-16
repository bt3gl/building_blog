# Building the Blog

1. Create the blog most as a ```md``` file inside ```./content``.

2. ```Makefile``` has the commands to generate the final page:

```
$ make html
```

3. The content will be generate in ```output```, which can be copied to the website's repo with:

```
$ yes | cp -r output/* ../bt3gl.github.io/
```

