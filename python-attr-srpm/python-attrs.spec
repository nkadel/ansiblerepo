# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.12
%global python3_pkgversion 3.12
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

%global modname attrs

%if 0%{?rhel}
# Avoid unwanted/unavailable dependencies in RHEL builds
%bcond_with tests
%else
# Turn the tests off when bootstrapping Python, because pytest requires attrs
%bcond_without tests
%endif

Name:           python-attrs
Version:        23.2.0
Release:        7%{?dist}
Summary:        Python attributes without boilerplate

# SPDX
License:        MIT
URL:            http://www.attrs.org/
BuildArch:      noarch
Source0:        https://github.com/python-attrs/%{modname}/archive/%{version}/%{modname}-%{version}.tar.gz
Patch0:         0001-Remove-hatch-vcs-and-hatch-fancy-pypi-readme-deps.patch

BuildRequires:  python%{python3_pkgversion}-devel

%description
attrs is an MIT-licensed Python package with class decorators that
ease the chores of implementing the most common attribute-related
object protocols.

%package -n python%{python3_pkgversion}-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{modname}}

%description -n python%{python3_pkgversion}-%{modname}
attrs is an MIT-licensed Python package with class decorators that
ease the chores of implementing the most common attribute-related
object protocols.

%prep
%setup -q -n %{modname}-%{version}
%patch -P 0 -p1

# Remove undesired/optional test dependency on pympler
sed -i '/"pympler",/d' pyproject.toml

# Remove tests-mypy extra from tests-no-zope extra
sed -i "/attrs\[tests-mypy\]/d" pyproject.toml

%generate_buildrequires
%pyproject_buildrequires %{?with_tests:-x tests}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files attr attrs

%check
%pyproject_check_import
%if %{with tests}
%pytest
%endif

%files -n python%{python3_pkgversion}-%{modname} -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
* Tue Oct 29 2024 Troy Dawson <tdawson@redhat.com> - 23.2.0-7
- Bump release for October 2024 mass rebuild:
  Resolves: RHEL-64018

* Wed Jun 26 2024 Ondřej Budai <obudai@redhat.com> - 23.2.0-6
- Drop unneeded build dependencies

* Mon Jun 24 2024 Troy Dawson <tdawson@redhat.com> - 23.2.0-5
- Bump release for June 2024 mass rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 15 2024 Miro Hrončok <mhroncok@redhat.com> - 23.2.0-2
- Remove undesired/optional test dependency on pympler

* Tue Jan 02 2024 Lumír Balhar <lbalhar@redhat.com> - 23.2.0-1
- Update to 23.2.0 (rhbz#2256322)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 23.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 04 2023 Python Maint <python-maint@redhat.com> - 23.1.0-3
- Rebuilt for Python 3.12

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 23.1.0-2
- Bootstrap for Python 3.12

* Wed May 17 2023 Lumír Balhar <lbalhar@redhat.com> - 23.1.0-1
- Update to 23.1.0 (rhbz#2187066)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 21 2022 Lumír Balhar <lbalhar@redhat.com> - 22.2.0-1
- Update to 22.2.0 (rhbz#2155469)

* Fri Jul 29 2022 Lumír Balhar <lbalhar@redhat.com> - 22.1.0-1
- Update to 22.1.0
Resolves: rhbz#2112006

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 21.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 24 2022 Lumír Balhar <lbalhar@redhat.com> - 21.4.0-5
- Fixed compatibility with Python 3.11 beta 3
Resolves: rhbz#2039259

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 21.4.0-4
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 21.4.0-3
- Bootstrap for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 21.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 03 2022 Lumír Balhar <lbalhar@redhat.com> - 21.4.0-1
- Update to 21.4.0
Resolves: rhbz#2035864

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 21.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 21.2.0-3
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 21.2.0-2
- Bootstrap for Python 3.10

* Fri May 07 2021 Lumír Balhar <lbalhar@redhat.com> - 21.2.0-1
- Update to 21.2.0
  Resolves: rhbz#1957660

* Wed May 05 2021 Lumír Balhar <lbalhar@redhat.com> - 20.3.0-3
- Fix tests with Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 19 2020 Lumír Balhar <lbalhar@redhat.com> - 20.3.0-1
- Update to 20.3.0 (#1894866)

* Mon Sep 07 2020 Lumír Balhar <lbalhar@redhat.com> - 20.2.0-1
- Update to 20.2.0 (#1876063)

* Thu Aug 27 2020 Lumír Balhar <lbalhar@redhat.com> - 20.1.0-1
- Update to 20.1.0 (#1870794)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 19.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 19.3.0-4
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 19.3.0-3
- Bootstrap for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 19.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 18 2019 Lumír Balhar <lbalhar@redhat.com> - 19.3.0-1
- New upstream version 19.3.0 (#1761701)
- Python 2 subpackage has been removed (#1773236)

* Sun Oct 13 2019 Miro Hrončok <mhroncok@redhat.com> - 19.1.0-6
- Drop Python 2 optional build dependencies

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 19.1.0-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 19.1.0-4
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 19.1.0-3
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 19.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 19 2019 Eric Smith <brouhaha@fedoraproject.org> 19.1.0-1
- Updated to latest upstream.

* Mon Feb 25 2019 Eric Smith <brouhaha@fedoraproject.org> 18.2.0-1
- Updated to latest upstream.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 17.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 17.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 17.4.0-6
- Rebuilt for Python 3.7

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 17.4.0-5
- Bootstrap for Python 3.7

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 17.4.0-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 17.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 17 2018 Eric Smith <brouhaha@fedoraproject.org> 17.4.0-2
- Added BuildRequires for python<n>-six.

* Thu Jan 11 2018 Eric Smith <brouhaha@fedoraproject.org> 17.4.0-1
- Updated to latest upstream.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 14 2016 Eric Smith <brouhaha@fedoraproject.org> 16.3.0-1
- Updated to latest upstream.

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 16.1.0-3
- Enable tests

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 16.1.0-2
- Rebuild for Python 3.6
- Disable python3 tests for now

* Sat Sep 10 2016 Eric Smith <brouhaha@fedoraproject.org> 16.1.0-1
- Updated to latest upstream.
- Removed patch, no longer necessary.
- Removed "with python3" conditionals.

* Thu Aug 18 2016 Eric Smith <brouhaha@fedoraproject.org> 16.0.0-6
- Build for Python 3.4 in EPEL7.

* Thu Aug 18 2016 Eric Smith <brouhaha@fedoraproject.org> 16.0.0-5
- Updated based on Fedora package review (#1366878).
- Fix check section, though tests can not be run for EPEL7.
- Add patch to skip two tests with keyword collisions.

* Tue Aug 16 2016 Eric Smith <brouhaha@fedoraproject.org> 16.0.0-4
- Fix python2 BuildRequires.

* Mon Aug 15 2016 Eric Smith <brouhaha@fedoraproject.org> 16.0.0-3
- Updated based on Fedora package review (#1366878).

* Sun Aug 14 2016 Eric Smith <brouhaha@fedoraproject.org> 16.0.0-2
- Updated based on Fedora package review (#1366878).

* Sat Aug 13 2016 Eric Smith <brouhaha@fedoraproject.org> 16.0.0-1
- Initial version.
