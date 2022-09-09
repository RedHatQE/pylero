Summary: Python SDK for Polarion
Name: pylero
Version: 0.0.3
Release: 1%{?dist}
License: MIT

URL: https://github.com/RedHatQE/pylero
Source0: %{url}/archive/%{version}/pylero-%{version}.tar.gz

Requires: python3-%{name} == %{version}-%{release}

BuildArch: noarch
BuildRequires: python3-devel
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
# setuptools-scm is needed to build the source distribution, but not
# for packaging, which *starts* from the source distribution
sed -i -e 's., "setuptools_scm"..g' pyproject.toml

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
rm -f %{buildroot}%{_bindir}/pylero

%files -n python3-%{name}
%doc README.md
%license LICENSE
%{python3_sitelib}/%{name}*
%{_bindir}/%{name}-cmd

%changelog
* Tue Aug 02 2022 Wayne Sun <gsun@redhat.com> 0.0.3-1
- new package built with tito
- Switch from suds-py3 to suds
- Downgrade to 201x python rpm build spec
- Remove rpm build action
- Add Fedora rpm build section

* Mon May 23 2022 Wayne Sun <gsun@redhat.com> - 0.0.2-1
- Initial packaging
