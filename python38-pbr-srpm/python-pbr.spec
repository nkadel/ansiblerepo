# Created by pyp2rpm-3.3.8
%global pypi_name pbr
%global pypi_version 5.8.1

#
# If we should enable tests by default
#
%bcond_with tests

#
# If we should enable docs by default
#
%bcond_with docs

# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8}
%global python3_version 3.8
%global python3_pkgversion 38
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        0%{?dist}
Summary:        Python Build Reasonableness

License:        None
URL:            https://docs.openstack.org/pbr/latest/
Source0:        %{pypi_source}
BuildArch:	noarch

%if 0%{?el8}
BuildRequires:  python%{python3_pkgversion}-rpm-macros
BuildRequires:  %{_bindir}/pathfix.py
%endif

BuildRequires:  python%{python3_pkgversion}
BuildRequires:  python%{python3_pkgversion}-devel
# Why is this blocked???
#BuildConflicts: python%{python3_pkgversion}-coverage
BuildRequires:  python%{python3_pkgversion}-mock
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-six
BuildRequires:  python%{python3_pkgversion}-wheel

%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-fixtures
BuildRequires:  python%{python3_pkgversion}-hacking
BuildRequires:  python%{python3_pkgversion}-pre-commit
BuildRequires:  python%{python3_pkgversion}-stestr
BuildRequires:  python%{python3_pkgversion}-testrepository
BuildRequires:  python%{python3_pkgversion}-testresources
BuildRequires:  python%{python3_pkgversion}-testscenarios
BuildRequires:  python%{python3_pkgversion}-testtools
BuildRequires:  python%{python3_pkgversion}-virtualenv
%endif

%description
Introduction PBR is a library that injects some useful and sensible default
behaviors into your setuptools run. It started off life as the chunks of code
that were copied between all of the OpenStack_ projects. Around the time that
OpenStack hit 18 different projects each with at least 3 active branches, it
seemed like a good time to make that code into a proper reusable library.PBR is
only...

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        Python Build Reasonableness

Requires:       python%{python3_pkgversion}-setuptools
%description -n python%{python3_pkgversion}-%{pypi_name}
Introduction PBR is a library that injects some useful and sensible default
behaviors into your setuptools run. It started off life as the chunks of code
that were copied between all of the OpenStack_ projects. Around the time that
OpenStack hit 18 different projects each with at least 3 active branches, it
seemed like a good time to make that code into a proper reusable library.PBR is
only...

%package -n python-%{pypi_name}-doc
Summary:        pbr documentation
%description -n python-%{pypi_name}-doc
Documentation for pbr

%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Prevent build failures on ambiguous python
grep -rl -e '^#!/usr/bin/env python$' -e '^#!/usr/bin/env python $' */ | \
    grep '\.py$' | \
    while read name; do
        echo "    Disambiguating /usr/bin/env python: $name"
	pathfix.py -i %{__python3} $name
done

grep -rl -e '^#!/usr/bin/python$' -e '^#!/usr/bin/python $' */ | \
    grep '\.py$' | \
    while read name; do
        echo "    Disambiguating /usr/bin/python in: $name"
	pathfix.py -i %{__python3} $name
done

if [ "%{__python3}" != "/usr/bin/python3" ]; then
    grep -rl -e '^#!/usr/bin/python3$' -e '^#!/usr/bin/python3 $' */ | \
	grep '\.py$' | \
	while read name; do
            echo "    Disambiguating /usr/bin/python3 in: $name"
	    pathfix.py -i %{__python3} $name
	done
fi

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build

%if %{with docs}
# generate html docs
PYTHONPATH=${PWD} sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
# Must do the default python version install last because
# the scripts in /usr/bin are overwritten with every setup.py install.
%{__python3} setup.py install --skip-build --root %{buildroot}
rm -rf %{buildroot}%{_bindir}/*

%if %{with tests}
%check
%{__python3} setup.py test
%endif

%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.rst pbr/tests/testpackage/README.txt
#%{python3_sitearch}/%{pypi_name}
#%{python3_sitearch}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%files -n python-%{pypi_name}-doc
%license LICENSE pbr/tests/testpackage/LICENSE.txt
%if %{with docs}
%doc html
%endif

%changelog
* Wed Apr 20 2022 Nico Kadel-Garcia <nkadel@gmail.com> - 5.8.1-1
- Initial package.
