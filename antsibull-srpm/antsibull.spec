# Created by pyp2rpm-3.3.8
%global pypi_name antsibull
%global pypi_version 0.47.0

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        Tools for building the Ansible Distribution

License:        None
URL:            https://github.com/ansible-community/antsibull
Source0:        https://files.pythonhosted.org/packages/source/a/%{pypi_name}/%{pypi_name}-%{pypi_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-asyncio-pool
BuildRequires:  python%{python3_pkgversion}-jinja2
BuildRequires:  python%{python3_pkgversion}-setuptools

#BuildRequires:  python%%{python3_pkgversion}-antsibull-changelog >= 0.14
#BuildRequires:  python%%{python3_pkgversion}-antsibull-core < 2~~
#BuildRequires:  python%%{python3_pkgversion}-antsibull-core >= 1
#BuildRequires:  python%%{python3_pkgversion}-antsibull-docs < 2~~
#BuildRequires:  python%%{python3_pkgversion}-antsibull-docs >= 1


%description
 antsibull -- Ansible Build Scripts [![Python linting badge]( [![Python testing
badge]( [![dumb PyPI on GH pages badge](

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        Tools for building the Ansible Distribution

Requires:       python%{python3_pkgversion}-antsibull-changelog >= 0.14
Requires:       python%{python3_pkgversion}-antsibull-core < 2~~
Requires:       python%{python3_pkgversion}-antsibull-core >= 1
Requires:       python%{python3_pkgversion}-antsibull-docs < 2~~
Requires:       python%{python3_pkgversion}-antsibull-docs >= 1
Requires:       python%{python3_pkgversion}-asyncio-pool
Requires:       python%{python3_pkgversion}-jinja2
Requires:       python%{python3_pkgversion}-setuptools
%description -n python%{python3_pkgversion}-%{pypi_name}
 antsibull -- Ansible Build Scripts [![Python linting badge]( [![Python testing
badge]( [![dumb PyPI on GH pages badge](


%prep
%autosetup -n %{pypi_name}-%{pypi_version}

# Prevnt setup.py from choking on src/tests
install -d src/tests

%build
%{__python3} setup.py build

%install
# Must do the default python version install last because
# the scripts in /usr/bin are overwritten with every setup.py install.
%{__python3} setup.py install --skip-build --root %{buildroot}
for name in %{buildroot}/%{_bindir}/*; do
    mv $name ${name}-%{python3_version}
    ln -s $(basename ${name}-%{python3_version}) ${name}
done

#%%check
#%%{__python3} setup.py test

%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.md src/antsibull/data/README_md.txt src/antsibull/data/ansible-readme.rst src/antsibull/data/collection-readme.j2
%{python3_sitelib}/%{pypi_name}
#%%{python3_sitelib}/tests
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info
%{_bindir}/*

%changelog
* Wed Jun 15 2022 Nico Kadel-Garcia <nkadel@gmail.com> - 0.47.0-1
- Initial package.
