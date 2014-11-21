# Tornado-JSON

[![Build Status](https://travis-ci.org/hfaran/Tornado-JSON.png?branch=master)](https://travis-ci.org/hfaran/Tornado-JSON)
[![PyPI version](https://badge.fury.io/py/Tornado-JSON.png)](http://badge.fury.io/py/Tornado-JSON)
[![Coverage Status](https://coveralls.io/repos/hfaran/Tornado-JSON/badge.png)](https://coveralls.io/r/hfaran/Tornado-JSON?branch=master)
[![Stories in Ready](https://badge.waffle.io/hfaran/Tornado-JSON.png?label=In_Progress)](http://waffle.io/hfaran/Tornado-JSON)

## Overview

Tornado-JSON is a small extension of [Tornado](http://www.tornadoweb.org/en/stable/) with the intent of providing the tools necessary to get a JSON API up and running quickly.

Some of the key features the included modules provide:

* Input and output **[JSON Schema](http://json-schema.org/) validation** by decorating RequestHandlers with `@schema.validate`
* **Automated route generation** with `routes.get_routes(package)`
* **Automated [GFM](https://help.github.com/articles/github-flavored-markdown)-formatted API documentation** using schemas and provided descriptions
* **Standardized JSON output** using the **[JSend](http://labs.omniti.com/labs/jsend)** specification

## Getting Started/FAQ

**How do I use this thing?**

* Check out the [Hello World demo](https://github.com/hfaran/Tornado-JSON/tree/master/demos/helloworld) for a quick example and the [accompanying walkthrough](http://tornado-json.readthedocs.org/en/latest/using_tornado_json.html) in the documentation. And then [**explore Tornado-JSON on readthedocs for the rest!**](http://tornado-json.readthedocs.org/en/latest/index.html#)

**Okay, but how do I install it?**

* For the possibly stable

```
pip install Tornado-JSON
```

* For the latest and greatest

```
git clone https://github.com/hfaran/Tornado-JSON.git
cd Tornado-JSON
sudo python setup.py install
```

**Neat, but `x` sucks, `y` is ugly, and `z` could be better.**

* You would be awesome for [opening an issue about it](https://github.com/hfaran/Tornado-JSON/issues/new), and I'll promise my best to take a look.
 
**You completely changed the interface in a recent update; what gives?**

* But newer is so much better! Seriously though, `Tornado-JSON` is, at the moment, still very much a work in progress. Updates will be made that will break the existing interface (and replace it with a shiny, new, much better one). All in the name of making it better! (And progress etc.)


## Dependencies

*Python{2.7, 3.3, 3.4} are supported.*

These dependencies can be satisfied by running `pip install -r requirements.txt`

* [tornado](http://www.tornadoweb.org/en/stable/)
* [jsonschema](https://python-jsonschema.readthedocs.org/en/latest/)


## Running Tests

```bash
sudo pip2 install tox
sudo pip3 install tox
sudo tox  # Will run test matrix
```
