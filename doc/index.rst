.. pylarion documentation master file, created by
   sphinx-quickstart on Mon Mar 16 19:01:11 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pylarion's documentation!
====================================
Welcome to Pylarion, the Python wrapper for the Polarion WSDL API. The
Pylarion wrapper enables native python access to Polarion objects and
functionality using object oriented structure and functionality. This
allows the devlopers to use Pylarion in a natural fashion without being
concerned about the Polarion details.

All Pylarion objects inherit from BasePolarion. The objects used in the
library are all generated from the SOAP factory class, using the python-suds
library. The Pylarion class attributes are generated dynamically as
properties, based on a mapping dict between the pylarion naming convention
and the Polarion attribute names.

The use of properties allows the pylarion object attributes to be virtual with
no need for syncing between them and the Polarion objects they are based on.

The Polarion WSDL API does not implement validation/verification of data
passed in, so the Pylarion library takes care of this itself. All enums are
validated before being sent to the server and raise an error if not using a
valid value. A number of workflow implementations are also included, for
example when creating a Document, it automatically creates the Heading work
item at the same time.

Polarion Work Items are configured per installation, and the library gives 2
options to handle this. Either you can add the list of workitems to the config
file and then it will create them on import of the work_item module, or it
will connect to the Polarion server, download the list of workitems and create
them.

Download and Installation:
**************************
Pylarion is located in a git repository and can be cloned from::

    $ git clone https://gitlab.cee.redhat.com/ccit/pylarion.git

From the root of the project, run::

    $ python setup.py install

If you want to make an rpm out of it::

    $ python setup.py bdist_rpm

Pylarion must be configured (see next section) before it can be used.

Configuration:
**************
A configuration file must be filled out, which must be located either in the
current dir (the dir where the script is executed from) **.pylarion**, in the
user's home dir **~/.pylarion**
Default settings are stored in **LIBDIR/etc/pylarion.cfg**. This file should
not be modified, as it will be overwritten with any future updates.
Certificates should be verified automatically, but if they aren't, you can add
the path to your CA to the cert_path config option.
Workitems is a JSON with the name of the workitem type as the key and the class
name as the value.
These are the configurable values:

    [webservice]
    url=https://polarion.engineering.redhat.com/polarion
    svn_repo=https://polarion.engineering.redhat.com/repo
    user={your username}
    password={your password}
    default_project={your default project}
    workitems={"testcase": "TestCase", "requirement":"Requirement}
    #cert_path=/dir/with/certs

If the password value is blank, it will prompt you for a password when you try
to access any of the pylarion objects.

These can also be overridden with the following environment variables:
    POLARION_URL
    POLARION_REPO
    POLARION_USERNAME
    POLARION_PASSWORD
    POLARION_TIMEOUT
    POLARION_PROJECT
    POLARION_WORKITEMS
    POLARION_CERT_PATH

Requirements:
*************
python-suds
requests

There is a requirements.txt file in the root directory. All requirements can
be installed by:
pip install -r requirements.txt

Usage:
******
There is a pylarion script installed that opens a python shell with all the
objects in the library already loaded::

    $ pylarion
    >>> tr = TestRun("example", project_id="project_name")

Alternatively, you can open a python shell and import the objects that you
want to use::

    $ python
    Python 2.6.6 (r266:84292, Nov 21 2013, 10:50:32)
    [GCC 4.4.7 20120313 (Red Hat 4.4.7-4)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from pylarion.test_run import TestRun
    >>> tr = TestRun("example", project_id="project_name")

To have all the workitems created, you have to import the module itself::
    $ python
    Python 2.6.6 (r266:84292, Nov 21 2013, 10:50:32)
    [GCC 4.4.7 20120313 (Red Hat 4.4.7-4)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import pylarion.work_item
    >>> from pylarion.work_item import TestCase

Examples:
**********
    Please see https://mojo.redhat.com/docs/DOC-1016728/ for examples


Contents:

.. toctree::
   :maxdepth: 4

   pylarion


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

