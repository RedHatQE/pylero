%define name pylero
%define version 0.0.2
%define unmangled_version 0.0.2
%define release 1
%define _unpackaged_files_terminate_build 0

Summary: Python SDK for Polarion
Name: %{name}
Version: %{version}
Release: %{release}
License: MIT
Group: Development/Libraries
Prefix: %{_prefix}
Vendor: pylero Developers <gsun@redhat.com>

URL: https://github.com/RedHatQE/pylero
SOURCE: %{url}/archive/%{version}/%{name}-%{version}.tar.gz

Requires: python3-%{name} == %{version}-%{release}
Requires: python3-suds python3-click

BuildArch: noarch
BuildRequires: python3-devel
BuildRequires: python3-suds
BuildRequires: python3-click
BuildRequires: python3-setuptools

%global _description %{expand:
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
downloads the list of workitems and creates them.}

%description %_description

%package -n python3-%{name}
Summary:        %{summary}

%description -n python3-%{name} %_description

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{name}
%{python3_sitelib}/%{name}-*.egg-info/
%{python3_sitelib}/%{name}/
%license LICENSE
%doc README.md
%{_bindir}/%{name}-cmd
%exclude %{_bindir}/%{name}

%changelog
* Mon May 23 2022 Wayne Sun <gsun@redhat.com> - 0.0.2-1
- Initial packaging
