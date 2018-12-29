# What is pythonc?

`pythonc` is a short utility script that helps you using python on the 
command line. Basically it does what `python -c` does and a few more.
See examples below.


## How to install

You can install it via pip
```bash
# test version
python -m pip install --index-url https://test.pypi.org/simple/ pythonc-test
```

or you can simply download this repository and mv `__main__.py` to
one of your `$PATH` locations
```bash
mv pythonc/__main__.py ...../pythonc  # no need for .py at the end
```


## Handy global vairables defined

* `p`: A handy print function with commandline usage in mind. It's has the
same interface as the default print function except that it specially
handles a single sequence. If it recieves a single sequence as input, the
default end characer becomes '' not '\n' and it prints as many times as 
the number of  elements in the sequence

* `line`: First input line

* `lines`: All input lines including the first one. Note that this should
be considered as a stream. Therefore, you cannot reuse it even though
it's subscriptable and allows a one time random access.

* `_lines` : Lazy evaluted non-stream lines. You can access its element
as many times as you want. This is not evaluated until you use it to
save up memory.


## Examples
Refer to python officials docs to learn useful string manipulating functions  
https://docs.python.org/3/library/string.html

It is a good idea to use generator expressions or list comprehensions
with pythonc  
https://docs.python.org/3/howto/functional.html

* Get files whose names are longer than 5  
`ls | pythonc 'p(l for l in lines if len(l)>5)'`
```
LICENSE
README.md
pythonc
setup.py
```

* Concatenate filenames  
`ls | pythonc 'p((l.strip() for l in lines), end=",")'`
```
LICENSE,README.md,pythonc,setup.py,
```

* Get the 4th column of the processs status  
`ps | pythonc 'p((l.split()[3] for l in lines[1:]), end="\n")'`
```
/usr/local/bin/fish
-fish
python3
-fish
ssh
```

* You can also do some crazy stuffs becuase pythonc can do anything
that python can do  
`ls | pythonc 'from random import sample; p(sample(_lines, 2))'`
`ls | pythonc 'p(sum(len(l) for l in lines))'`


## Misc

Both python2 and python3 are supported