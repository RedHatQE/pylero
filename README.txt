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

Download and Installation:
**************************
Pylarion is located in a git repository and can be cloned from::

    $ git clone https://code.engineering.redhat.com/gerrit/pylarion

From the root of the project, run::

    $ pip install .

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
with the following values:

    [webservice]
    url=https://polarion.engineering.redhat.com/polarion
    svn_repo=https://polarion.engineering.redhat.com/repo
    user={your username}
    password={your password}
    default_project={your default project}
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
    POLARION_CERT_PATH

Requirements:
*************
The install_requires attribute in setup.py installs the following requirements
suds-py3 if python_version>="3"
suds if python_version<="2.7"
click
requests>=2.6.0'

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

Examples:
**********
    Please see https://mojo.redhat.com/docs/DOC-1016728/ for examples
