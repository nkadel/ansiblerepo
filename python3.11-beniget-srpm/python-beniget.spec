# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.11
%global python3_pkgversion 3.11
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

Name:           python-beniget
Version:        0.4.1
#Release:        8%{?dist}
Release:        0.8%{?dist}
Summary:        Extract semantic information about static Python code
License:        BSD-3-Clause
URL:            https://github.com/serge-sans-paille/beniget/
Source0:        %{url}/archive/%{version}/beniget-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pytest


%global _description %{expand:
A static analyzer for Python2 and Python%{Python3_Pkgversion} code.Beniget provides a static over-
approximation of the global and local definitions inside Python
Module/Class/Function. It can also compute def-use chains from each definition.}
%description %_description


%package -n     python%{python3_pkgversion}-beniget
Summary:        %{summary}

%description -n python%{python3_pkgversion}-beniget %_description


%prep
%autosetup -n beniget-%{version}


%generate_buildrequires
# Don't use tox options to avoid an unwanted dependency in RHEL
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files beniget


%check
# tox.ini has setup.py test, but that's deprecated
# use pytest, but beware the tests are not named test*.py
%pytest -v tests/*.py


%files -n python%{python3_pkgversion}-beniget -f %{pyproject_files}
%doc README.rst


%changelog
* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.4.1-7
- Rebuilt for Python 3.12

* Wed May 24 2023 Miro Hrončok <mhroncok@redhat.com> - 0.4.1-6
- Update the license tag to SPDX

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.4.1-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 04 2021 Tomas Hrnciar <thrnciar@redhat.com> - 0.4.1-1
- Update to 0.4.1

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 29 2021 Miro Hrončok <mhroncok@redhat.com> - 0.4.0-1
- Update to 0.4.0
- Fixes rhbz#1977164

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.3.0-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 14 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-1
- Update to 0.3.0
- Fixes rhbz#1878161

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 12 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-1
- Update to 0.2.0

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Miro Hrončok <mhroncok@redhat.com> - 0.1.0-1
- Initial package
