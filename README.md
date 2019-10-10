# Building the Blog

#### Source your virtual environment:

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Create the blog most as a ```md``` file inside ```./content``.

####```Makefile``` has the commands to generate the final page:

```
make html
```

#### The content will be generate in ```output```, which can be copied to the website's repo with:

```
yes | cp -r output/* ../bt3gl.github.io/
```

