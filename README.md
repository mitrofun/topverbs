Counting the frequency of using verbs in function names
=====
[![Build Status](https://travis-ci.org/mitrofun/topverbs.svg?branch=master)](https://travis-ci.org/mitrofun/topverbs) [![Coverage Status](https://coveralls.io/repos/github/mitrofun/topverbs/badge.svg?branch=master)](https://coveralls.io/github/mitrofun/topverbs?branch=master) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/mitrofun/topverbs/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/mitrofun/topverbs/?branch=master) [![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/mitrofun/topverbs/blob/master/LICENSE)

Script to count the number of verbs used in function names.

Installation
=====
    pip3 install git+https://github.com/mitrofun/topverbs
    
Parameters 
====
The startup parameters of the application are available in help:
```bash
topverbs -h
usage: topverbs [-h] [-d DIRS [DIRS ...]] [-t TOP_SIZE] [--repo REPO]
                [-c {noun,verb}] [-e {var,func}] [-o {console,file}]
                [--format {json,csv}] [--report REPORT_PATH] [--ext EXTENSION]

Top verbs used in function names in the project(s).

optional arguments:
  -h, --help            show this help message and exit
  -d DIRS [DIRS ...], --dirs DIRS [DIRS ...]
                        The path to the project or projects separated by
                        space.
  -t TOP_SIZE, --top TOP_SIZE
                        The size of the top verbs, default is 10.
  --repo REPO           The repository url.
  -c {noun,verb}, --category {noun,verb}
                        Language word category. Possible value: noun - search
                        noun in code, verb - search verb in code.
  -e {var,func}, --element {var,func}
                        The analyzed part of the code.Search for words in
                        function names or local variables. Possible value: var
                        - search in local variables in function, func - search
                        in function names.
  -o {console,file}, --output {console,file}
                        Report output method.Possible value: console - output
                        result script to console, file - output result script
                        to file.
  --format {json,csv}   Report output format.Possible value: json - save
                        report in json format, csv - save report in csv
                        format.
  --report REPORT_PATH  Report path to file.Default is user home dir.
  --ext EXTENSION       Analyze files with the file extension.Default is py.Is
                        mode in develop.
```

Usage
=====
In python code for find top 5 verb:
```python
import topverbs
words = topverbs.get_top_words('/Users/mitri4/Projects/ViewKids', top_size=5, lang_category='verb')
print(words) 
[('get', 69), ('save', 5), ('run', 3), ('add', 2)]
```

In python code with json format find top 5 verb:
```python
import topverbs
words = topverbs.get_top_words('/Users/mitri4/Projects/ViewKids', top_size=5, format_data='json', lang_category='verb')
print(words) 
'{"get": 69, "save": 5, "run": 3, "add": 2}'
```
In python code for find top 2 noun:
```python
import topverbs
words = topverbs.get_top_words('/Users/mitri4/Projects/ViewKids', top_size=2, format_data='json', lang_category='verb')
print(words) 
'{"context": 18, "url": 12}'
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
- GitPython 2.1.11+

Contributors
=====
- [mitri4](https://github.com/mitrofun)


License
=====
topverbs is released under the MIT License. See the LICENSE file for more details.
