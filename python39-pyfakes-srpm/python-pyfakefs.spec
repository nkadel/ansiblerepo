# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8}
%global python3_version 3.9
%global python3_pkgversion 39
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

%global package_name pyfakefs

Name:           python-%{package_name}
Version:        4.5.6
#Release:        3%%{?dist}
Release:        0.3%{?dist}
Summary:        pyfakefs implements a fake file system that mocks the Python file system modules.
License:        ASL 2.0
URL:            http://pyfakefs.org
Source0:        https://pypi.io/packages/source/p/%{package_name}/%{package_name}-%{version}.tar.gz
BuildArch:      noarch


%description
pyfakefs implements a fake file system that mocks the Python file system
modules.
Using pyfakefs, your tests operate on a fake file system in memory without
touching the real disk. The software under test requires no modification to
work with pyfakefs.

%package -n python%{python3_pkgversion}-%{package_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{package_name}}

BuildRequires:  git
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

Requires:       python%{python3_pkgversion}-pytest >= 2.8.6

%description -n python%{python3_pkgversion}-%{package_name}
pyfakefs implements a fake file system that mocks the Python file system
modules.
Using pyfakefs, your tests operate on a fake file system in memory without
touching the real disk. The software under test requires no modification to
work with pyfakefs.

%prep
%autosetup -n %{package_name}-%{version} -S git

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%py3_build

%install
%py3_install

%files -n python%{python3_pkgversion}-%{package_name}
%license COPYING
%doc README.md
%{python3_sitelib}/%{package_name}
%{python3_sitelib}/*.egg-info

%changelog
* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.5.6-2
- Rebuilt for Python 3.11

* Sat May 21 2022 Orion Poplawski <orion@nwra.com> - 4.5.6-1
- Update to 4.5.6

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.4.0-2
- Rebuilt for Python 3.10

* Mon Mar 15 2021 Orion Poplawski <orion@nwra.com> - 4.4.0-1
- Update to 4.4.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.5.8-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.5.8-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.5.8-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat May 11 2019 Orion Poplawski <orion@nwra.com> - 3.5.8-1
- Update to 3.5.8

* Sat Apr 27 2019 Miro Hrončok <mhroncok@redhat.com> - 3.1-7
- Subpackage python2-pyfakefs has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.1-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 1 2017 David Moreau Simard <dmsimard@redhat.com> - 3.1-1
- First packaged version of pyfakefs
