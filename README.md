# Pylero

Welcome to Pylero, the Python wrapper for the Polarion WSDL API. The Pylero
wrapper enables native python access to Polarion objects and functionality
using object oriented structure and functionality. This allows the developers to
use Pylero in a natural fashion without being concerned about the Polarion
details.

All Pylero objects inherit from BasePolarion. The objects used in the library
are all generated from the SOAP factory class, using the python-suds library.
The Pylero class attributes are generated dynamically as properties, based on
a mapping dict between the pylero naming convention and the Polarion attribute
names.

The use of properties allows the pylero object attributes to be virtual with no
need for syncing between them and the Polarion objects they are based on.

The Polarion WSDL API does not implement validation/verification of data passed
in, so the Pylero library takes care of this itself. All enums are validated
before being sent to the server and raise an error if not using a valid value.
A number of workflow implementations are also included, for example when
creating a Document, it automatically creates the Heading work item at the same
time.

Polarion Work Items are configured per installation, to give native workitem
objects (such as TestCase), the library connects to the Polarion server,
downloads the list of workitems and creates them.

## Installation
-----------------------------

### Install from Pypi

Pylero package have been published to Pypi:

`https://pypi.org/project/pylero/`

Install Pylero Pypi package with:

`$ pip install pylero`

By default the latest package and dependencies will be installed.

### Install from repo

Pylero is located in a git repository and can be cloned from:

`$ git clone https://github.com/RedHatQE/pylero.git`

From the root of the project, run:

`$ pip install .`

### Build pip package

After cloned the repo and in the dir:

`$ python -m build`

both wheel and bdist format will be built and the package could be found under
dist directory.

Then both files could be used to install the package with pip install locally.

Pylero must be configured (see next section) before it can be used.

## Configuration
-----------------

A configuration file must be filled out, which must be located either in the
current dir (the dir where the script is executed from) named **.pylero** or in
the user's home dir **~/.pylero**

Default settings are stored in **LIBDIR/pylero.cfg**. This file should not
be modified, as it will be overwritten with any future updates.  Certificates
should be verified automatically, but if they aren't, you can add the path to
your CA to the cert_path config option.  These are the configurable values:

```
    [webservice]
    url=https://{your polarion web URL}/polarion
    svn_repo=https://{your polarion web URL}/repo
    user={your username}
    password={your password}
    default_project={your default project}
    #cert_path=/dir/with/certs
    #disable_manual_auth=False
```

If the password value is blank, it will prompt you for a password when you try
to access any of the pylero objects.

These can also be overridden with the following environment variables:
```
    POLARION_URL
    POLARION_REPO
    POLARION_USERNAME
    POLARION_PASSWORD
    POLARION_TIMEOUT
    POLARION_PROJECT
    POLARION_CERT_PATH
    POLARION_DISABLE_MANUAL_AUTH
```

## Requirements
----------------
The install_requires attribute in setup.py installs the following requirements:
```
    suds; python_version < '3.0'
    suds-py3; python_version >= '3.0'
    click
    readline; python_version <= '3.6'
```

## Usage
---------
There is a pylero script installed that opens a python shell with all the
objects in the library already loaded:

```
    $ pylero
    >>> tr = TestRun("example", project_id="project_name")
```

Alternatively, you can open a python shell and import the objects that you want
to use:

```
    $ python
    Python 2.6.6 (r266:84292, Nov 21 2013, 10:50:32)
    [GCC 4.4.7 20120313 (Red Hat 4.4.7-4)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from pylero.test_run import TestRun
    >>> tr = TestRun("example", project_id="project_name")
```

## Examples
------------
```python
import datetime
from pylero.test_run import TestRun
from pylero.test_record import TestRecord
from pylero.work_item import TestCase, Requirement
from pylero.document import Document

# Creating a Test Run Template:
tr = TestRun.create_template("myproj",
                             "Static Query Test",
                             parent_template_id="Empty",
                             select_test_cases_by="staticQueryResult",
                             query="type:testcase AND status:approved")

# Creating a Test Run:
tr = TestRun.create("myproj", "My Test Run", "Static Query Test")

# changing status
tr.status = "inprogress"

# getting and changing a custom attribute in TestRun
arch = tr.get_custom_field("arch")
arch = "i386"
tr.set_custom_field("arch", arch)

# saving the data to the server
tr.update()

# Adding a test record
tr.add_test_record_by_fields(test_case_id="MYPROJ-1813",
                             test_result="passed",
                             test_comment="went smoothly",
                             executed_by="user1",
                             executed=datetime.datetime.now(),
                             duration=10.50,
                             defect_work_item_id="MYPROJ-1824")

# Getting specific WorkItems
tc = TestCase(project_id="myproj", work_item_id="MYPROJ-2015")
req = Requirement(project_id="myproj", work_item_id="MYPROJ-2019")

# Getting required custom fields for specific Work Items
reqs = TestCase.custom_fields("myproj")[1]
# returns [u'caseimportance', u'caselevel', u'caseautomation', u'caseposneg']

reqs = Requirement.custom_fields("myproj")[1]
# returns [u'reqtype']

# Getting the valid values for the custom enumerations
tc.get_valid_field_values("caseimportance")
# returns [critical, high, medium, low]

# Creating a specific Work Item
tc = TestCase.create("myproj",
                     "Title",
                     "Description",
                     caseimportance="high",
                     caselevel="component",
                     caseautomation="notautomated",
                     caseposneg="positive")

# Note if the custom required fields are not specified, an exception will be raised
# Custom field for work items are accessed like regular attributes
tc.caseimportance = "critical"

# to save changes
tc.update()

# Creating a document
doc = Document.create("myproj", "Testing", "API doc", "The API Document",
                      ["testcase"])
# Adding a Functional Test Case work item to the document
wi = TestCase()
wi.tcmscaseid = "12345"
wi.title = "[GUI] Host Network QoS-'named'"
wi.author = "user1"
wi.tcmscategory = "Functional"
wi.caseimportance = "critical"
wi.status = "proposed"
wi.setup = "DC/Cluster/Host"
wi.teardown = """
Proceed with the VM Network QoS paradigm, that is creating Network QoS
entities that can be shared between different networks - let's refer to this
as ""named"" QoS. This QoS entities are created via DC> QoS > Host Network"
"""
steps = TestSteps()
steps.keys = ["step", "expectedResult"]
step1 = TestStep()
step1.values = ["This is step 1", "Step 1 expected result"]
step2 = TestStep()
step2.values = ["This is step 2", "Step 2 expected result"]
arr_step = [step1, step2]
steps.steps = arr_step
wi.test_steps = steps
wi.caseautomation = "notautomated"
wi.caseposneg = "positive"
wi.caselevel = "component"
new_wi = doc.create_work_item(None, wi)

# Getting a list of documents in a space.
docs = Document.get_documents(proj="myproj", space="Testing")

# Create template from document
TestRun.create_template("myproj",
                        "tpl_tp_12071",
                        select_test_cases_by="staticLiveDoc",
                        doc_with_space="Testing/tp_12071")

# create a test run based on the template
tr = TestRun.create("myproj", "tp_12071_1", "tpl_tp_12071")

# process a record
rec = tr.records[0]
rec.duration = "10.0"
rec.executed_by = "user1"
rec.executed = datetime.datetime.now()
rec.result = "passed"
wi = _WorkItem(uri=rec.test_case_id)
steps = wi.get_test_steps()
res1 = TestStepResult()
res1.comment = "This is the 1st result"
res1.result = "passed"
res2 = TestStepResult()
res2.comment = "This is the 2nd result"
res2.result = "failed"
rec.test_step_results = [res1, res2]
tr.add_test_record_by_object(rec)

# update the test record status
tr.status = "inprogress"
tr.update()

# Adding a linked Item
# TestCase MYPROJ-2828 verifies Requirement MYPROJ-11
tc = TestCase(project_id="MYPROJ", work_item_id="MYPROJ-2828")
tc.add_linked_item("MYPROJ-11", "verifies")

# Verify it on both objects:
tc = TestCase(project_id="myproj", work_item_id="MYPROJ-2828")
for linked in tc.linked_work_items:
    print "%s - %s" % (linked.work_item_id, linked.role)

req = Requirement(project_id="myproj", work_item_id="MYPROJ-11")
for linked in req.linked_work_items_derived:
    print "%s - %s" % (linked.work_item_id, linked.role)
```

## Before you commit

In order to ensure you are able to pass the GitHub CI build, it is recommended that you run the following commands in the base of your pylero directory

``` python
$ pip install pre-commit
$ pre-commit autoupdate && pre-commit run -a
```

Pre-commit will ensure that the changes you made are not in violation of PEP8 standards and automatically apply black fixes.

We recommend `black` to automatically fix any pre-commit failures.

``` python
$ pip install black
$ black <edited_file.py>
```

## Fedora RPM package build

### Tito

[Tito](https://github.com/rpm-software-management/tito) is a tool for managing RPM based projects using git for their source code repository.

The tito config dir is [.tito](./.tito)

To create a new tag and automaticlly update pylero.spec with all changelog:

`$ tito tag`

After tag need push the tag:

`git push --follow-tags`

After tag been pushed a new Copr build will be automatically triggered.

### Copr

Fedora [Copr](https://copr.fedorainfracloud.org/) Build System help make building and managing third party package repositories easy.

Each pylero new release will trigger new copr build to fedora-all, EPEL8 and EPEL9.

The build is triggered by webhook defined in the project configuration.

The build project on Copr is [pylero](https://copr.fedorainfracloud.org/coprs/waynesun20/pylero/).

Check the target rpm package in the build to test locally.
