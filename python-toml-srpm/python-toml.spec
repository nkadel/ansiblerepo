# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.12
%global python3_pkgversion 3.12
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

# Created by pyp2rpm-3.3.9
%global pypi_name toml
%global pypi_version 0.10.2

Name:           python-%{pypi_name}
Version:        %{pypi_version}
#Release:        1%%{?dist}
Release:        0.1%{?dist}
Summary:        Python Library for Tom's Obvious, Minimal Language

License:        MIT
URL:            https://github.com/uiri/toml
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-pytest

%description
TOML A Python library for parsing and creating TOML < module passes the TOML
test suite < also:* The TOML Standard < * The currently supported TOML
specification <

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        Python Library for Tom's Obvious, Minimal Language

%description -n python%{python3_pkgversion}-%{pypi_name}
TOML A Python library for parsing and creating TOML < module passes the TOML
test suite < also:* The TOML Standard < * The currently supported TOML
specification <


%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --skip-build --root %{buildroot}

%check
%{__python3} setup.py test

%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Sat Apr 22 2023 Nico Kadel-Garcia <ikadel-garcia@statestreet.com> - 0.10.2-1
- Initial package.
