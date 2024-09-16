# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.12
%global python3_pkgversion 3.12
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

%global sum Integrate more support into Python's distutils
%global srcname distutils-extra

Name:           python-%{srcname}
Version:        2.39
Release:        27%{?dist}
Summary:        %{sum}

License:        GPLv2+
URL:            https://launchpad.net/python-distutils-extra
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description
Enables you to easily integrate gettext support, themed icons and
scrollkeeper based documentation into Python's distutils. 

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{sum}
Requires:       intltool
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname}
Enables you to easily integrate gettext support, themed icons and
scrollkeeper based documentation into Python's distutils. 

%prep
%autosetup -n %{name}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python%{python3_pkgversion}-%{srcname}
%doc doc/*
%license LICENSE
%{python3_sitelib}/DistUtilsExtra/
%{python3_sitelib}/python_distutils_extra*.egg-info

%changelog
* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.39-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.39-26
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.39-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.39-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.39-23
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.39-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.39-21
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.39-20
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.39-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.39-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.39-17
- Rebuilt for Python 3.9

* Sat Feb 22 2020 Orion Poplawski <orion@nwra.com> - 2.39-16
- Add Requires on intltool (bz#1651404)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.39-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 28 2019 Miro Hrončok <mhroncok@redhat.com> - 2.39-14
- Subpackage python2-distutils-extra has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.39-13
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.39-12
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.39-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.39-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.39-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.39-8
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.39-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.39-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.39-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.39-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.39-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Fabian Affolter <mail@fabian-affolter.ch> - 2.39-1
- Updated to new upstream version 2.39 (rhbz#1304361)

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.38-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.38-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 2.38-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Jul 31 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.38-1
- Updated to new upstream version 2.38

* Wed Jun 26 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.37-3
- Spec file updated
- Python 3 support added

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 20 2012 Fabian Affolter <mail@fabian-affolter.ch> - 2.37-1
- Updated to new upstream version 2.37

* Mon Aug 06 2012 Fabian Affolter <mail@fabian-affolter.ch> - 2.35-1
- Updated to new upstream version 2.35

* Sun Aug 05 2012 Fabian Affolter <mail@fabian-affolter.ch> - 2.34-1
- Updated to new upstream version 2.34

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Fabian Affolter <mail@fabian-affolter.ch> - 2.33-1
- Updated to new upstream version 2.33

* Tue Mar 13 2012 Fabian Affolter <mail@fabian-affolter.ch> - 2.32-1
- Updated to new upstream version 2.32

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 13 2011 Fabian Affolter <mail@fabian-affolter.ch> - 2.31-1
- Updated to new upstream version 2.31

* Wed Aug 31 2011 Fabian Affolter <mail@fabian-affolter.ch> - 2.29-1
- Updated to new upstream version 2.29

* Sun Jun 19 2011 Fabian Affolter <mail@fabian-affolter.ch> - 2.28-1
- Updated to new upstream version 2.28

* Thu Jun 02 2011 Fabian Affolter <mail@fabian-affolter.ch> - 2.27-1
- Updated to new upstream version 2.27

* Wed Mar 16 2011 Fabian Affolter <mail@fabian-affolter.ch> - 2.26-1
- Added patch for DISPLAY support
- Updated to new upstream version 2.26

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 12 2010 Fabian Affolter <mail@fabian-affolter.ch> - 2.22-1
- Remove archive_name from 2010-06-04, this was useless and wrong
- Updated to new upstream version 2.22

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.19-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jun 04 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 2.19-1
- Update to new upstream version 2.19.  Resolves rhbz#600307
- Update spec to match latest guidelines

* Thu Feb 04 2010 Fabian Affolter <mail@fabian-affolter.ch> - 2.15-1
- Updated to new upstream version 2.15

* Sun Dec 20 2009 Fabian Affolter <mail@fabian-affolter.ch> - 2.12-2
- Bumped release

* Mon Dec 14 2009 Fabian Affolter <mail@fabian-affolter.ch> - 2.12-1
- Updated to new upstream version 2.12

* Sat Aug 01 2009 Fabian Affolter <mail@fabian-affolter.ch> - 2.6-2
- Bump release

* Sat Aug 01 2009 Fabian Affolter <mail@fabian-affolter.ch> - 2.6-1
- Minor spec file changes
- Changed source to launchpad
- Updated to new upstream version 2.6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.91.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.91.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 24 2009 Fabian Affolter <mail@fabian-affolter.ch> - 1.91.2-2
- Changed license to GPLv2+ 

* Tue Nov 18 2008 Fabian Affolter <mail@fabian-affolter.ch> - 1.91.2-1
- Initial package for Fedora

