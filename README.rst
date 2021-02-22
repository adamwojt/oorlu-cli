=========
oorlu CLI
=========

.. image:: https://oor.lu/static/images/fb.png

.. image:: https://img.shields.io/pypi/v/oorlu-cli.svg
        :target: https://pypi.python.org/pypi/oorlu-cli

.. image:: https://github.com/adamwojt/oorlu-cli/workflows/ci/badge.svg?branch=master&event=push
        :target: https://github.com/adamwojt/oorlu-cli/actions

.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
        :target: https://timothycrosley.github.io/isort/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :target: https://github.com/psf/black


Simple URL shortener CLI written in Python. Uses free API from https://oor.lu

Installation
------------

.. code-block:: text

    pip install oorlu-cli

    ... or manually

    pip install .

    ... or if you just to play with code in dev-env:

    git clone https://github.com/adamwojt/yee-cli.git
    cd yee-cli
    poetry install
    poetry shell
    oorlu https://google.com

Config
------

No config needed.
    
Usage
-----
``Usage: oorlu [OPTIONS] [LONG_URL*]```

--limit=int          Set click limit for URL (default: no limit)
-h, --help           Show this message and exit.

*\* url max length: 500.*

**Example Usage:**

.. code-block:: text

    oorlu google.com
    oorlu www.clicklimit2.com -l 2

Troubleshooting
---------------

Connection Issues (make sure):
    * You have internet connection.
    * https://oor.lu is alive.
Other:
    * For more debug ideas visit https://github.com/adamwojt/ur_l - API source code

Credits
-------

* Uses `click <https://click.palletsprojects.com/en/7.x/>`_
* Uses `requests <https://requests.readthedocs.io/en/master/>`_
* Created with Cookiecutter_ and the `johanvergeer/cookiecutter-poetry`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`johanvergeer/cookiecutter-poetry`: https://github.com/johanvergeer/cookiecutter-poetry
