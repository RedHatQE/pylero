======================
Contribution Guideline
======================


Welcome to the contribution guideline page!

Setting up the environment
==========================

-----------------
Installing pip
-----------------
This project uses `pip <https://pip.pypa.io/en/stable/>`_ as a package manager. To install, simply run the follow command:

.. code-block:: bash

    $ python -m pip install

------------------------
Installing pre-commit
------------------------
`pre-commit <https://pre-commit.com/>`_ is a multi-language package manager for pre-commit hooks. It is used to check code before it makes it to commit. A list of hooks is specified in `.pre-commit-config.yaml` in the root directory of the project.
To install `pre-commit`, simply run the following command:

.. code-block:: bash

    $ pip install pre-commit


-----------------
Before you commit
-----------------

In order to ensure you are able to pass the GitHub CI build, it is recommended that you run the following commands in the base of your pylero directory

.. code-block:: python

    $ pre-commit autoupdate && pre-commit run -a



Pre-commit will ensure that the changes you made are not in violation of PEP8 standards and automatically apply black fixes.

We recommend `black` to automatically fix any pre-commit failures.

.. code-block:: python

    $ pip install black
    $ black <edited_file.py>


-----------------------------------
Fork the project and clone the repo
-----------------------------------

.. code-block:: bash

    $ git clone https://github.com/<your-username>/pylero.git

`You can add upstream as a remote repo and origin as your fork repo`

-----------------------
Installing dependencies
-----------------------

All the project dependencies are listed in `requirements.txt` file located in the root directory. To install all the dependencies of the project, simply run:

.. code-block:: bash

    $ pip install -r requirements.txt



-----------------------------
Setting up configuration file
-----------------------------
You will need to setup config values, for that you need to get some values from Polarion and provide it to the config file. For more detail, check out project's `README.md <https://github.com/RedHatQE/pylero/blob/main/README.md#configuration>`_

----------------------------
Install the project with pip
----------------------------
`Pylero` supports command line interface. Simply run `pylero` on you terminal, it will prompt to the command line interface. However, before you can do that you will have to install the project by running:

.. code-block:: bash

    $ pip install .

in your project root directory. With that, you're ready to submit your first contribution.


How to contribute to Pylero
===========================
There are many ways to contribute to `Pylero`. You can start from reporting issues, raising discussion, submitting bug fixes, adding new features, or updating the documentation. You can also browse through `list of issues <https://github.com/RedHatQE/pylero/issues>`_ and look for any issues with the label of `good first issue` or `help wanted`.

---------------
Create an issue
---------------

To report any bug, please open a new issue `here <https://github.com/RedHatQE/pylero/issues>`_. Remember to provide as much detail as you can including running environment, version of `Pylero` or snippet of the code.

-------------------------
Create a discussion topic
-------------------------

In addition, you can create a `discussion topic <https://github.com/RedHatQE/pylero/discussions>`_. It can be general topics, new ideas, polls, Q&As or awareness raising.

--------------------------
Adding new feature/bug fix
--------------------------

Before adding new feature, it's recommended to create a discussion topic first. Then you can create a pull request for your new feature linked to the discussion topic. That way it is easier for the maintainer to track what the change is about.

New proposed features must be conform to coding style/standard (passing pre-commit checks) and must include at least unit tests. You should create a pull request from your fork against an upstream project. A pull request must be properly rebased from upstream `main` branch, include a precise commit messages, and a brief description.

If you're pushing a bug fix, please link it to the issue related.

Note: The project uses GitHub action to run the CI/CD, you should be able to check whether the CI passes or fails. Then, you can wait for code reviews from maintainers or fix any errors that do not pass in the pipeline.

--------------------
Update documentation
--------------------

The other way to contribute to the project is to look for any outdated documentation and submit an update version to reflect the current status.
New added features should also include documentation and a brief how-to.
