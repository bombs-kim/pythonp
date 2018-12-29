# What is pythonc?

`pythonc` is a short utility script that helps you using python on the 
command line. Basically, it does what `python -c` does, but not just that.
See examples below to see how convenient it can be.  
Currently, it focuses on helping string manipulation. If you need other
features, you are welcome to make an issue for it.


## How to install

You can install it via pip
```bash
# test version. will change soon
python -m pip install --index-url https://test.pypi.org/simple/ pythonc-test
```

or you can simply download this repository and mv `__main__.py` to
one of your `$PATH` locations
```bash
# no need for .py at the end
mv pythonc/__main__.py ...../pythonc
```


## Handy global vairables defined

* `p`: A handy print function with commandline usage in mind. It has the
same interface as the default print function except that it specially
handles a single sequence. If it recieves a single sequence as input,
it prints as many times as the number of elements in the sequence.

* `line`: The first input line. `sys.stdin.readline()`.

* `lines`: All input lines including the first one.
`sys.stdin.readlines()`. Note that this should be considered
as a stream. Therefore, you cannot reuse it even though
it's subscriptable and allows a one time random access.

* `_lines` : Lazy evaluted non-stream-like lines. You can access
its element as many times as you want. The actual input lines
are not prepared to save up memory if you don't use it.


## Examples

Print numbers
```bash
pythonc 'p(range(3))'
0
1
2
```

Get files whose names are longer than 5  
```bash
$ ls | pythonc "p((l for l in lines if len(l)>5), end='')"
LICENSE
README.md
pythonc
setup.py
```

Concatenate filenames  
```bash
$ ls | pythonc "p((l.strip() for l in lines), end=',')"
LICENSE,README.md,pythonc,setup.py,
```

Get the 4th column of the processs status  
```bash
$ ps | $pythonc 'p(l.split()[3] for l in lines[1:])'
/usr/local/bin/fish
-fish
python3
-fish
ssh
```

You can also do some crazy stuffs becuase pythonc can do anything
that python can do  
```bash
$ ls | pythonc 'from random import sample; p(sample(_lines, 2))'
$ ls | pythonc 'p(sum(len(l) for l in lines))'
```


## Misc

* Both python2 and python3 are supported

* Refer to python officials docs to learn useful string manipulating functions  
https://docs.python.org/3/library/string.html

* It is a good idea to use generator expressions or list comprehensions
with pythonc  
https://docs.python.org/3/howto/functional.html

* TODO: Adding some useful non-string-manipulating functionalities
