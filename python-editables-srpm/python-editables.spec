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
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# Sphinx-generated HTML documentation is not suitable for packaging; see
# RHBZ#2006555 for discussion. Additionally, upstream uses the furo theme,
# which we would have to patch; see RHBZ#1910798.
#
# We could, in theory, generate PDF documentation as a substitute, but this
# would still require it requires python3dist(myst-parser), which is not
# currently packaged–and we are not willing to package it solely for this
# purpose.

Name:           python-editables
Version:        0.5
Release:        %autorelease
Summary:        Editable installations

# SPDX
License:        MIT
URL:            https://github.com/pfmoore/editables
# PyPI source distributions lack tests; use the GitHub archive
Source:         %{url}/archive/%{version}/editables-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel

# Most of the dependencies, and all of the pytest options, in tox.ini are for
# coverage analysis and for installation with pip/virtualenv. Rather than
# working around all of these, it is simpler not to use tox for dependency
# generation or testing.
BuildRequires:  python3dist(pytest)

%global common_description %{expand:
A Python library for creating “editable wheels”

This library supports the building of wheels which, when installed, will expose
packages in a local directory on sys.path in “editable mode”. In other words,
changes to the package source will be reflected in the package visible to
Python, without needing a reinstall.}

%description %{common_description}


%package -n python%{python3_pkgversion}-editables
Summary:        %{summary}

%description -n python%{python3_pkgversion}-editables %{common_description}


%prep
%autosetup -n editables-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files editables


%check
%pytest


%files -n python%{python3_pkgversion}-editables -f %{pyproject_files}
%license LICENSE.txt
%doc CHANGELOG.md
%doc README.md


%changelog
* Tue Jul 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5-1
- Update to 0.5 (close RHBZ#2225249)

* Thu Jul 06 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4-1
- Update to 0.4 (close RHBZ#2220948)
- Upstream switched from setuptools to flit_core: pyproject-rpm-macros no
  longer handles LICENSE.txt

* Thu Jul 06 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3-3
- Confirm License is SPDX MIT

* Mon Apr 11 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3-1
- Update to 0.3 (close RHBZ#2073823)

* Thu Feb 17 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.0-1
- Initial package (close RHBZ#2050876)
