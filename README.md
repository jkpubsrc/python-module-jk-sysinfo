jk_sysinfo
==========

Introduction
------------

This python module provides ways to retrieve and parse technical system data.

To achieve this goal this module encapsulates various operating system tools by invoking them and parsing their return data. This data can then be processed further by other tools.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/python-module-jk-sysinfo)
* [pypi.python.org](https://pypi.python.org/pypi/jk_sysinfo)

Why this module?
----------------

If you run Linux you will likely have encountered the command line tool `inxi`. This tool is capable of retrieving system information and presenting it in a condensed way.

Unfortunately this tool does not provide the data in a machine readable form. Extending this tool to other output formats than plaintext is not intended by the authors (and would not be easy at all).

This python module bridges this gap: It contains various functions that invoke system routines to provide data which then gets parsed and returned as JSON.

Limitations of this module
--------------------------

Currently this module only supports Ubuntu Linux out of the box.

Other Linuxes might work well but minor changes to the current implementation might be required in order to adapt to subtle differences of other Linux distributions. If you intend to make use of this tool on other Linux systems please contact the author of this module and assist in implementing the necessary changes.

How to use this module
----------------------

### Import this module

Please include this module into your application using the following code:

```python
import jk_sysinfo
```

...

Contact Information
-------------------

This is Open Source code. That not only gives you the possibility of freely using this code it also
allows you to contribute. Feel free to contact the author(s) of this software listed below, either
for comments, collaboration requests, suggestions for improvement or reporting bugs:

* Jürgen Knauth: jknauth@uni-goettingen.de, pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



