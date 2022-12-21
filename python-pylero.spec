Name:           python-pylero
Version:        0.0.5
Release:        1%{?dist}
Summary:        Python SDK for Polarion

License:        MIT
URL:            https://github.com/RedHatQE/pylero
Source:         %{url}/archive/%{version}/pylero-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
This is Pylero, the Python wrapper for the Polarion WSDL API. The Pylero
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

%package -n python3-pylero
Summary:        %{summary}

%description -n python3-pylero %_description


%prep
%autosetup -p1 -n pylero-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install

%pyproject_save_files pylero


%global _pylero_import_exclude %{expand:
-e pylero.build -e pylero.build_linked_work_item -e pylero.cli.cmd -e pylero.document
-e pylero.plan -e pylero.plan_record -e pylero.test_record -e pylero.test_run
-e pylero.work_item
}

%check
# If the Polarion server URL is not specified in config some libraries will
# fail to import, so exclude the modules which require the server url
%pyproject_check_import %_pylero_import_exclude


%files -n python3-pylero -f %{pyproject_files}
%doc README.md
%{_bindir}/pylero
%{_bindir}/pylero-cmd


%changelog
* Wed Dec 21 2022 Wayne Sun <gsun@redhat.com> 0.0.5-1
- Rename spec to python-pylero
- Bug fixes

* Tue Sep 13 2022 Wayne Sun <gsun@redhat.com> 0.0.4-1
- Fix EPEL9 yum suds package (gsun@redhat.com)
- Switch back to modern rpm spec (gsun@redhat.com)
- Using modern pypi package build system interface (gsun@redhat.com)
- Fix the config file path (gsun@redhat.com)
- Update contact and copyright info (gsun@redhat.com)
- Code style update (gsun@redhat.com)
- Remove the sample config file in data_files (gsun@redhat.com)
- Update spec with improvement (gsun@redhat.com)
- use cft.multi while parsing array custom fields (lgangava@redhat.com)
- Fix testrun search method params with limit (gsun@redhat.com)

* Tue Aug 02 2022 Wayne Sun <gsun@redhat.com> 0.0.3-1
- new package built with tito
- Switch from suds-py3 to suds
- Downgrade to 201x python rpm build spec
- Remove rpm build action
- Add Fedora rpm build section

* Mon May 23 2022 Wayne Sun <gsun@redhat.com> - 0.0.2-1
- Initial packaging
