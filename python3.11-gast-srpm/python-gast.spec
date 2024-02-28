%if 0%{?el8} || 0%{?el9}
%global python3_version 3.11
%global python3_pkgversion 3.11
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

Name:           python-gast
Version:        0.5.3
#Release:        8%%{?dist}
Release:        0.8%{?dist}
Summary:        Python AST that abstracts the underlying Python version
License:        BSD-3-Clause
URL:            https://github.com/serge-sans-paille/gast/
Source0:        %{url}/archive/%{version}/gast-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pytest


%global _description %{expand:
A generic AST to represent Python2 and Python%{Python3_Pkgversion}'s Abstract Syntax Tree (AST).
GAST provides a compatibility layer between the AST of various Python versions,
as produced by ast.parse from the standard ast module.}
%description %_description


%package -n     python%{python3_pkgversion}-gast
Summary:        %{summary}

%description -n python%{python3_pkgversion}-gast %_description


%prep
%autosetup -p1 -n gast-%{version}


%generate_buildrequires
# Don't use tox options to avoid an unwanted dependency in RHEL
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files gast


%check
%pytest -v


%files -n python%{python3_pkgversion}-gast -f %{pyproject_files}
%doc README.rst


%changelog
* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.5.3-7
- Rebuilt for Python 3.12

* Wed May 24 2023 Miro Hrončok <mhroncok@redhat.com> - 0.5.3-6
- Update the license tag to SPDX

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.5.3-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 30 2021 Tomáš Hrnčiar <thrnciar@redhat.com> - 0.5.3-1
- Update to 0.5.3

* Thu Jul 29 2021 Tomas Hrnciar <thrnciar@redhat.com> - 0.5.2-1
- Update to 0.5.1

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 28 2021 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-1
- Update to 0.5.0
- Fixes rhbz#1977051
- Fixes rhbz#1968986

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.4.0-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 11 2020 Miro Hrončok <mhroncok@redhat.com> - 0.4.0-1
- Update to 0.4.0
- Fixes rhbz#1878159

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 07 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.3-1
- Update to 0.3.3 (#1844892)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 12 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.2-1
- Update to 0.3.2

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jan 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.2-1
- Initial package
