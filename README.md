Counting the frequency of using verbs in function names
=====
[![Build Status](https://travis-ci.org/mitrofun/topverbs.svg?branch=master)](https://travis-ci.org/mitrofun/topverbs)

Script to count the number of verbs used in function names.

Installation
=====
    pip3 install git+https://github.com/mitrofun/topverbs

Usage
=====
In python code:
```python
import topverbs
words = topverbs.get_top_verbs('/Users/mitri4/Projects/ViewKids', top_size=5)
print(words) 
[('get', 69), ('save', 5), ('run', 3), ('add', 2)]
```

In python code with json format:
```python
import topverbs
words = topverbs.get_top_verbs('/Users/mitri4/Projects/ViewKids', top_size=5, format_data='json')
print(words) 
'{"get": 69, "save": 5, "run": 3, "add": 2}'
```

In console print:
```bash
python3 topverbs.py -d /Users/mitri4/Projects/Google-Business-class -t 10
============================== top 10 verbs ==============================
total 475 words, 13 unique
==========================================================================
get 381
see 29
save 16
add 16
make 11
be 7
serialize 4
sanitize 3
have 3
find 2
==========================================================================
```

Requirements
=====
- python 3.6+
- nltk 3.3+

Contributors
=====
- [mitri4](https://github.com/mitrofun)

TODO
=====
- Run user command, if pkg install from pip
- Not work function get_top_verbs, if pkg install from pip
- Coverage code tests

License
=====
django-bulk-update is released under the MIT License. See the LICENSE file for more details.