# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.12
%global python3_pkgversion 3.12
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

## START: Set by rpmautospec
## (rpmautospec version 0.3.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

Name:           python-py-tes
Version:        0.4.2
Release:        %autorelease
Summary:        Python SDK for the GA4GH Task Execution API

# SPDX
License:        MIT
URL:            https://github.com/ohsu-comp-bio/py-tes
# The PyPI sdist is missing the LICENSE and the tests, so we must use the
# GitHub source archive.
Source:         %{url}/archive/%{version}/py-tes-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel

# Most of the dependencies in tests/requirements.txt pertain to linting and
# coverage analysis. (Plus, the package wants to use the deprecated nose
# package as the test runner.) Rather than working around all of these, it is
# simpler to BR and invoke pytest manually.
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist requests_mock} >= 1.3

%global common_description %{expand:
This is a library for interacting with servers implementing the GA4GH Task
Execution Schema (https://github.com/ga4gh/task-execution-schemas).}

%description %{common_description}


%package -n python%{python3_pkgversion}-py-tes
Summary:        %{summary}

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_provides_for_importable_modules
%py_provides python%{python3_pkgversion}-tes

%description -n python%{python3_pkgversion}-py-tes %{common_description}


%prep
%autosetup -n py-tes-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files tes


%check
%pytest -v


%files -n python%{python3_pkgversion}-py-tes -f %{pyproject_files}
%doc README.md


%changelog
* Sat Jan 13 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.2-2
- Backport to EPEL9

* Sat Jan 13 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.2-1
- Initial package (close RHBZ#2257483)
