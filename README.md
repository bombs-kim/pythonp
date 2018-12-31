# What is pythonp?

`pythonp` is a simple utility script that helps you using python on the
command line. Basically, it's a `python -c` command with a handy print
function `p`. See examples below to see how convenient it can be.


## How to install

You can install it via pip
```bash
python -m pip install pythonp
```

or you can simply download this repository and copy `__main__.py` to
one of your `$PATH` locations
```bash
cp pythonp/__main__.py ...../pythonp
```


## Handy global variables defined

#### `p`
A handy print function with commandline usage in mind. It has the
same interface as the default `print` function except that it specially
handles a single iterable as an argument, in which case it prints as many
times as the number of elements in the iterable. Giving extra positional
arguments along with an iterable is not allowed.

#### `lines`
Standard input lines where each line ends with a newline
character. You can think of it as `sys.stdin` except that it's
subscriptable and allows a one-time random access, which means you
can do something `lines[3], lines[10:]`.


#### `_lines`
Lazy evaluted non-stream-like version of `lines`.
Becuase it's a `collections.abc.Sequence`, you can access its 
lines multiple times, reverse it, do inclusion test on it,
and so forth. The lines are not prepared until you actually
use it to save up memory.


## Examples

Print numbers
```bash
$ pythonp 'p(range(3))'
0
1
2
```

Get files whose names are longer than 5  
```bash
$ ls | pythonp "p((l for l in lines if len(l)>5), end='')"
LICENSE
README.md
pythonp
setup.py
```

Concatenate filenames  
```bash
$ ls | pythonp "p((l.strip() for l in lines if not 'bombs' in l), end=',')"
LICENSE,README.md,pythonp,setup.py,
```

Get the 4th column of the processs status  
```bash
$ ps | pythonp 'p(l.split()[3] for l in lines[1:])'
/usr/local/bin/fish
-fish
python3
ssh
```

You can also do some crazy stuffs becuase pythonp can do anything
that python can do  
```bash
$ ls | pythonp 'from random import sample; p(sample(_lines, 2))'
$ ls | pythonp 'p(sum(len(l) for l in lines))'
$ cat urls.txt | pythonp 'from requests import get; p(get(url.strip()) for url in lines)'
```


## Misc

* Both python2 and python3 are supported.

* Refer to python officials docs to learn useful string manipulating functions  
https://docs.python.org/3/library/string.html

* It is a good idea to use generator expressions or list comprehensions
with pythonp
https://docs.python.org/3/howto/functional.html

* If you want some other features, you are always welcome to make an issue,
at the issue tab on the top menu.

