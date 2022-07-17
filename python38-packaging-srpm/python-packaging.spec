# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8}
%global python3_version 3.8
%global python3_pkgversion 38
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

# Created by pyp2rpm-3.3.8
%global pypi_name packaging
%global pypi_version 21.3

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        0.1%{?dist}
Summary:        Core utilities for Python packages

License:        BSD-2-Clause or Apache-2.0
URL:            https://github.com/pypa/packaging
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildConflicts: python%{python3_pkgversion}-pyparsing = 3.0.5
BuildRequires:  python%{python3_pkgversion}-pyparsing >= 2.0.2
BuildRequires:  python%{python3_pkgversion}-setuptools
#BuildRequires:  python%{python3_pkgversion}-sphinx

BuildRequires:  python%{python3_pkgversion}-invoke
BuildRequires:  python%{python3_pkgversion}-pretend
BuildRequires:  python%{python3_pkgversion}-progress
BuildRequires:  python%{python3_pkgversion}-pytest

%description
packaging .. start-introReusable core utilities for various Python Packaging
interoperability specifications < library provides utilities that implement the
interoperability specifications which have clearly one correct behaviour (eg:
:pep:440) or benefit greatly from having a single shared implementation (eg:
:pep:425)... end-introThe packaging project includes the following: version...

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        Core utilities for Python packages

Conflicts:      python%{python3_pkgversion}-pyparsing = 3.0.5
Requires:       python%{python3_pkgversion}-pyparsing >= 2.0.2
%description -n python%{python3_pkgversion}-%{pypi_name}
packaging .. start-introReusable core utilities for various Python Packaging
interoperability specifications < library provides utilities that implement the
interoperability specifications which have clearly one correct behaviour (eg:
:pep:440) or benefit greatly from having a single shared implementation (eg:
:pep:425)... end-introThe packaging project includes the following: version...

%package -n python-%{pypi_name}-doc
Summary:        packaging documentation
%description -n python-%{pypi_name}-doc
Documentation for packaging

%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{__python3} setup.py build

## generate html docs
#PYTHONPATH=${PWD} sphinx-build-3 docs html
## remove the sphinx-build leftovers
#rm -rf html/.{doctrees,buildinfo}

%install
%{__python3} setup.py install --skip-build --root %{buildroot}

%check
%{__python3} setup.py test

%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%files -n python-%{pypi_name}-doc
#%%doc html
%license LICENSE LICENSE.APACHE LICENSE.BSD

%changelog
* Sat Jul 16 2022 Nico Kadel-Garcia <nkadel@gmail.com> - 21.3-1
- Initial package.
