# Created by pyp2rpm-3.3.6
%global pypi_name resolvelib

# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8}
%global python3_version 3.8
%global python3_pkgversion 38
%endif

Name:           python-%{pypi_name}
Version:        0.5.5
Release:        0.4%{?dist}
Summary:        Resolve abstract dependencies into concrete ones

License:        ISC License
URL:            https://github.com/sarugaku/resolvelib
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  %{_bindir}/pathfix.py
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%if 0%{?el8}
BuildRequires:  python%{python3_pkgversion}-rpm-macros
%endif

%description
ResolveLib at the highest level provides a Resolver class that
includes dependency resolution logic. You give it some things, and a little
information on how it should interact with them, and it will spit out a
resolution result. Intended Usage :: import resolvelib Things I want to
resolve. requirements [...] Implement logic so the resolver understands the
requirement format. class...

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

#Requires:       python%%{python3_pkgversion}-black
#Requires:       python%%{python3_pkgversion}-commentjson
#Requires:       python%%{python3_pkgversion}-flake8
#Requires:       python%%{python3_pkgversion}-html5lib
#Requires:       python%%{python3_pkgversion}-packaging
#Requires:       python%%{python3_pkgversion}-packaging
#Requires:       python%%{python3_pkgversion}-pygraphviz
#Requires:       python%%{python3_pkgversion}-pytest
#Requires:       python%%{python3_pkgversion}-requests
#Requires:       python%%{python3_pkgversion}-setl
#Requires:       python%%{python3_pkgversion}-towncrier
%description -n python%{python3_pkgversion}-%{pypi_name}
ResolveLib at the highest level provides a Resolver class that
includes dependency resolution logic. You give it some things, and a little
information on how it should interact with them, and it will spit out a
resolution result. Intended Usage :: import resolvelib Things I want to
resolve. requirements [...] Implement logic so the resolver understands the
requirement format. class...


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

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
    grep -rl -e '^#!/usr/bin/python3' -e '^#!/usr/bin/python3 $' */ | \
	grep '\.py$' | \
	while read name; do
            echo "    Disambiguating /usr/bin/python3 in: $name"
	    pathfix.py -i %{__python3} $name
	done
fi

%build
%py3_build

%install
%py3_install

%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%changelog
* Thu Apr 14 2022 Nico Kadel-Garcia - 2.14.4-0.1
- Introduce python38 dependency for RHEL 8

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.5.5-2
- Rebuilt for Python 3.10

* Sat Apr 10 2021 Kevin Fenzi <kevin@scrye.com> - 0.5.5-1
- Initial package.
