# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.11
%global python3_pkgversion 3.11
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

%global pypi_name Pallets-Sphinx-Themes

Name:           python-%{pypi_name}
Version:        2.0.2
#Release:        5%%{?dist}
Release:        0.5%{?dist}
Summary:        Sphinx themes for Pallets and related projects

License:        BSD
URL:            https://github.com/pallets/pallets-sphinx-themes/
Source0:        https://files.pythonhosted.org/packages/source/P/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description
Pallets Sphinx Themes Themes for the Pallets projects.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3-sphinx
Requires:       python3-setuptools
%description -n python3-%{pypi_name}
Pallets Sphinx Themes Themes for the Pallets projects.


%prep
%autosetup -n %{pypi_name}-%{version} -p1
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%license LICENSE.rst
%doc README.rst CHANGES.rst
%{python3_sitelib}/pallets_sphinx_themes
%{python3_sitelib}/Pallets_Sphinx_Themes-*.egg-info/

%changelog
* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.0.2-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 10 2021 Frantisek Zatloukal <fzatlouk@redhat.com> - 2.0.2-1
- Update to 2.0.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 1.2.2-8
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1.2.2-5
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 11 2019 Rick Elrod <relrod@redhat.com> - 1.2.2-3
- Fix dependency issue for python >=3.8

* Mon Nov 4 2019 Rick Elrod <relrod@redhat.com> - 1.2.2-2
- Fix files section for python >=3.10

* Mon Nov 4 2019 Rick Elrod <relrod@redhat.com> - 1.2.2-1
- Latest upstream
- Remove python 2 stuff, to follow Fedora packaging guidelines

* Sat Apr 28 2018 Rick Elrod <rick@elrod.me> - 1.0.0-1
- Initial package.
