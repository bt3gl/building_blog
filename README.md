# Building the Blog

0. Source your virtual environment:

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

1. Create the blog most as a ```md``` file inside ```./content``.

2. ```Makefile``` has the commands to generate the final page:

```
make html
```

3. The content will be generate in ```output```, which can be copied to the website's repo with:

```
yes | cp -r output/* ../bt3gl.github.io/
```

