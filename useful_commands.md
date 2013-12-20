* Update README.rst

    ```$ pandoc -s -t rst --toc README.md -o README.rst```

* Install project with files.txt record

    ```$ sudo python setup.py install --record files.txt```

* "uninstall" package installed with files.txt record

    ```$ cat files.txt | sudo xargs rm -rf```

* Generate/update base docs/ folder with Sphinx

    ```$ sphinx-apidoc -F -o docs tornado_json```
