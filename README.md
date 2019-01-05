# What is pythonp?

`pythonp` is a simple utility script that helps you using python on the
command line. Basically, it's a `python -c` command with a handy print
function `p`. See examples below to see how convenient it can be.
By design, no magic is added in `pythonp` in a hope that
it will be merged into some major python implementations later
and becomes default setting for `python -c`. Therefore, any kind of
valid python code should be able to run with `pythonp` and only
python code can be run.

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
similar interface to the built-in `print` with some exceptions.
- It specially handles a single iterable as an argument,
in which case it prints as many
times as the number of elements in the iterable. Giving extra positional
arguments along with an iterable is not allowed.

#### `lines`
Standard input lines. You can think of it as `sys.stdin` except that
each line of it doesn't end with a newline character. Also note that it's
subscriptable and allows a one-time random access, which means you
can do something `lines[3], lines[10:]`.

#### `_lines`
Lazy evaluted non-stream-like version of `lines`.
Becuase it's a `collections.abc.Sequence`, you can access its 
lines multiple times, reverse it, do inclusion test on it,
and so forth. The lines are not prepared until you actually
use it to save up memory.

#### `l`
Each line of the `sys.stdin` when `-e` option is on. See explanations
with `-e` option below. Note that in the current `pythonp` implementation
globals are shared among
all lines and there could be side effects. This is a inteded behavior
 but can change in the future.


## Features
* The last expression is automatically printed with `p` function if your
code dind't write anything to `sys.stdout` and the last expression does
not evalute to `None`. If you don't want this feature you can put
something like `;pass` or `;None` in the end of your code.

* If `-e` option is given, your code can work on each line `l`, not the
entire lines `lines` or `_lines`. The names `lines` and `_lines` will
disappear and can not be used.

* Automatic importing is supported. `pythonp` automatically tries to
import a name for you when it encounters an unseen one.

* Backtick(\`) in code is replaced with `"""` so that you can have
one more way to make string literals. In python 3.6 or above `f` prefix
is also added to make the enclosed section a f-string.
For example, you can do
something like
```bash
$ echo 91/seoul/bombs | pythonp -e "`name='{l.split('/')[2]}'`"  # python3.6+
name='bombs'
```

## Examples

Print numbers
```bash
$ pythonp 'range(3)'
0
1
2
```

Print time
```bash
$ pythonp 'time.time()'
1546362172.5707405
```

List files whose names are longer than 5
```bash
$ ls | pythonp -e "if len(l)>5: p(l)"
LICENSE
README.md
pythonp
setup.py
```

Randomly sample N files to investigate from a large number of files
``` bash
ls | pythonp "random.sample(_lines, 3)"
item_1443
item_6360
item_7285
```

Concatenate filenames  
```bash
$ ls | pythonp "','.join(l.strip() for l in lines if not 'bombs' in l)"
LICENSE,README.md,pythonp,setup.py
```

Get the 4th column of the processs status  
```bash
$ ps | tail -n+1 | pythonp -e "l.split()[3]"
/usr/local/bin/fish
-fish
python3
ssh

# or, using only pythonp
$ ps | pythonp "lines[1:]" | pythonp -e "l.split()[3]"
```

You can also do some crazy stuffs becuase pythonp can do anything
that python can do  
```bash
# If you have to solve a weird quiz
$ pythonp "now=datetime.datetime.now();(now.year+now.day)%10"

# Make at most 5 random names
$ pythonp "'\n'*5" | pythonp -e "''.join(random.sample(string.ascii_letters, 7))" | xargs touch

# If you want an one-liner crawler
$ cat urls.txt | pythonp -e 'requests.get(l.strip())' > output
```


## Misc

* If you want a shorter name for `pythonp` you can do something like this.  
```bash
mv $(which pythonp) $(dirname $(which pythonp))/p  # rename pythonp to p
```

* Both python2 and python3 are supported.

* Refer to python official docs to learn useful string manipulating functions
https://docs.python.org/3/library/string.html

* It is a good idea to use generator expressions or list comprehensions
with pythonp
https://docs.python.org/3/howto/functional.html

* If you want some other features, you are always welcome to make an issue
at the issue tab on the top menu.
