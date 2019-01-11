# What is pythonp?

**pythonp** is a simple utility script that helps you using python on the
command line. Basically, it's a **python -c** command with a handy print
function **p**. See examples below to see how convenient it can be.  
By design, it avoids adding much sugar to the goold old
**python -c**. It introduces no magic except
for a few preprocessings and handy global variables.
The goal of this project is to deliver seamless experience to
python users and become a part of some major python
implementations in the end, without remaining as a standalone package.


# Disclaimer

There are already several projects that have
smilar goals with this project such as
[pyp](https://code.google.com/archive/p/pyp/),
[pythonpy](https://github.com/Russell91/pythonpy) and others.
Particularly [pythonpy](https://github.com/Russell91/pythonpy) is super
popular. I think they are all amazing projects and I don't mean to assert that
every aspect of **pythonp** is breakingly new.  
But there are fundamental differences between **pythonp**
and others. Notably, **pythonp** has been designed
to be able to run *any python programs*, not just
single statements. Any
valid python code should be able to be run with **pythonp** and only
(almost valid) python code should.


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
can do something like `lines[3], lines[10:]`.

#### `l`
`l` is a line from the standard input. It also doesn't end with a new
line character.
Without `-e` option, `l` is the first line from the standard input.
With `-e` option, it represents each line
of the standard input. See the feature explanation below to learn `-e` option.

#### `_lines`
Lazy evaluted non-stream-like version of `lines`.
Becuase it's a `collections.abc.Sequence`, you can access its 
lines multiple times, reverse it, do inclusion test on it,
and so forth. The lines are not prepared until you actually
use it to save up memory.


## Features
* The last expression is automatically printed with `p` function if your
code dind't write anything to `sys.stdout` and the last expression does
not evalute to `None`. If you don't want this feature you can put
something like `;pass` or `;None` in the end of your code.

* If `-e` option is given, your code is applied to each line `l` of the
stanard input, not the
entire lines `lines` or `_lines`. The names `lines` and `_lines` will
disappear and can not be used. Note that in the current implementation,
globals are shared during continued executions of the code
 and there could be some side effects.
This is an intended behavior but can change in the future.


* Automatic importing is supported. `pythonp` automatically tries to
import a name for you when it encounters an unseen one.

* Backtick(\`) in code is replaced with `"""` so that you can have
one more way to make string literals. In python 3.6 or above `f` prefix
is also added to make the enclosed section a **f-string**.
For example, you can do
something like this.
```bash
$ echo 91/seoul/bombs | pythonp "`name='{l.split('/')[2]}'`"  # python3.6+
name='bombs'
```


## Examples

Make commands that you want on the fly and and run them with your shell
```bash
# Remove extensions of .txt files
$ ls | pythonp -e "if l.endswith('.txt'): p('mv', l, l[:-4])" | sh
```

Randomly sample N lines from a large number of lines
``` bash
# choose n files randomly
ls | pythonp "random.sample(_lines, 3)"
item_1443
item_6360
item_7285
```

Concatenate lines
```bash
$ ls | pythonp "','.join(l.strip() for l in lines if not 'bombs' in l)"
LICENSE,README.md,pythonp,setup.py
```

Do something for **e**ach line
```bash
# A web crawler one-liner
$ cat urls.txt | pythonp -e 'p(requests.get(l)); time.sleep(1)' > output
```

Split a long line and output the nth chunk 
```bash
# Get the 4th column from the current processs status 
$ ps | tail -n+1 | pythonp -e "l.split()[3]"
/usr/local/bin/fish
-fish
python3
ssh

# Only using only pythonp
$ ps | pythonp "lines[1:]" | pythonp -e "l.split()[3]"
```

Others
```bash
# Use it to solve some weird quiz
$ pythonp "now=datetime.datetime.now();(now.year+now.day)%10"

# Make at most 5 random names
$ pythonp "'\n'*(5-1)" | pythonp -e "''.join(random.sample(string.ascii_letters, 7))" | xargs touch
```


## Misc

* If you want a shorter name for `pythonp` you can do something like this.  
```bash
mv $(which pythonp) $(dirname $(which pythonp))/py  # rename pythonp to py
```

* Both python2 and python3 are supported.

* Refer to python official docs to learn useful string manipulating functions
https://docs.python.org/3/library/string.html

* It is a good idea to use generator expressions or list comprehensions
with pythonp
https://docs.python.org/3/howto/functional.html

* If you want some other features, you are always welcome to make an issue
at the issue tab on the top menu.
