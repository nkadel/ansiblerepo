# Created by pyp2rpm-3.3.6
%global pypi_name resolvelib

Name:           python-%{pypi_name}
Version:        0.5.5
Release:        0.3%{?dist}
Summary:        Resolve abstract dependencies into concrete ones

License:        ISC License
URL:            https://github.com/sarugaku/resolvelib
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description
ResolveLib at the highest level provides a Resolver class that
includes dependency resolution logic. You give it some things, and a little
information on how it should interact with them, and it will spit out a
resolution result. Intended Usage :: import resolvelib Things I want to
resolve. requirements [...] Implement logic so the resolver understands the
requirement format. class...

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

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

# Prevent build failures on ambiguouss python
grep -rl '^#!/usr/bin/env python$' */ | \
    while read name; do
        echo "    Disambiguating /usr/bin/env python: $name"
	sed -i -e 's|^#!/usr/bin/env python$|#!/usr/bin/python3|g' $name
done

grep -rl '^#!/usr/bin/python$' */ | \
    while read name; do
        echo "    Disambiguating /usr/bin/python: $name"
	sed -i -e 's|^#!/usr/bin/python$|#!/usr/bin/python3|g' $name
done

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
* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.5.5-2
- Rebuilt for Python 3.10

* Sat Apr 10 2021 Kevin Fenzi <kevin@scrye.com> - 0.5.5-1
- Initial package.
