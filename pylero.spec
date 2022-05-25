%define name pylero
%define version 0.0.2
%define unmangled_version 0.0.2
%define release 1

Summary: Python SDK for Polarion
Name: %{name}
Version: %{version}
Release: %{release}
Source0: https://github.com/RedHatQE/pylero/archive/refs/tags/%{unmangled_version}.tar.gz
License: MIT
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: pylero Developers <gsun@redhat.com>
Url: https://github.com/RedHatQE/pylero

%description
# Pylero

Welcome to Pylero, the Python wrapper for the Polarion WSDL API. The Pylero
wrapper enables native python access to Polarion objects and functionality
using object oriented structure and functionality. This allows the devlopers to
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

%prep
%setup -q -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
python3 setup.py build

%install
python3 setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog
* Mon May 23 2022 Wayne Sun <gsun@redhat.com> - 0.0.2-1
- Initial packaging
