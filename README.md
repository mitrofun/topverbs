Counting the frequency of using verbs in function names
=====
[![Build Status](https://travis-ci.org/mitrofun/topverbs.svg?branch=master)](https://travis-ci.org/mitrofun/topverbs) [![Coverage Status](https://coveralls.io/repos/github/mitrofun/topverbs/badge.svg?branch=master)](https://coveralls.io/github/mitrofun/topverbs?branch=master) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/mitrofun/topverbs/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/mitrofun/topverbs/?branch=master) [![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/mitrofun/topverbs/blob/master/LICENSE)

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

In console print command *topverbs*:
```bash
topverbs -d ~/Projects/o-tech.io -t 7

============================== top 7 verbs ==============================
| total 2618 words, 45 unique                                           |
=========================================================================
| get : 1602                                                            |
| add : 297                                                             |
| run : 105                                                             |
| find : 101                                                            |
| make : 91                                                             |
| save : 91                                                             |
| remove : 64                                                           |
=========================================================================
```

For analyze an external repository, run the --repo command with the url to the repository

```bash
topverbs --repo https://github.com/gitpython-developers/GitPython -t 2

Repository cloned to path: /var/folders/zl/jwb5sj6n6bx_52tlh6kpdhjc0000gn/T/tmpwdnxg4k7/
============================== top 2 verbs ==============================
| total 82 words, 13 unique                                             |
=========================================================================
| get : 27                                                              |
| add : 17                                                              |
=========================================================================
Remove temporary dir: /var/folders/zl/jwb5sj6n6bx_52tlh6kpdhjc0000gn/T/tmpwdnxg4k7
```

Requirements
=====
- python 3.6+
- nltk 3.3+

Contributors
=====
- [mitri4](https://github.com/mitrofun)


License
=====
topverbs is released under the MIT License. See the LICENSE file for more details.
