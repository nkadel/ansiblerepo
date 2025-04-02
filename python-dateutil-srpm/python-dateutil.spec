# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.12
%global python3_pkgversion 3.12
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

%global modname dateutil

Name:           python-%{modname}
Version:        2.8.1
Release:        7%{?dist}
Epoch:          1
Summary:        Powerful extensions to the standard datetime module

License:        BSD
URL:            https://github.com/dateutil/dateutil
Source:         %{pypi_source}

# Mitigate CVE-2007-4559 (tarfile directory traversal).
# `dateutil.zoneinfo.rebuild` handles "pure data" tarballs,
# here we disable tar features that are potentially unsafe.
# Submitted upstream, but rejected because they're removing this
# code entirely.
# BZ: https://bugzilla.redhat.com/show_bug.cgi?id=2203905
Patch1:         https://github.com/dateutil/dateutil/pull/1295.patch

# Disable tests to avoid pulling in test dependencies on RHEL9
# Specify --with tests to run the tests e.g. on EPEL
%bcond_with tests

BuildArch:      noarch
BuildRequires: make
BuildRequires:  python%{python3_pkgversion}-sphinx
BuildRequires:  python%{python3_pkgversion}-sphinx_rtd_theme

%global _description \
The dateutil module provides powerful extensions to the standard datetime\
module available in Python.

%description %_description

%package -n python%{python3_pkgversion}-%{modname}
Summary:        %summary
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-setuptools_scm
%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-freezegun
BuildRequires:  python%{python3_pkgversion}-hypothesis
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-six
%endif
Requires:       tzdata
%{?python_provide:%python_provide python%{python3_pkgversion}-%{modname}}

%description -n python%{python3_pkgversion}-%{modname}  %_description

%package doc
Summary: API documentation for python-dateutil
%description doc
This package contains %{summary}.

%prep
%autosetup -p1
iconv --from=ISO-8859-1 --to=UTF-8 NEWS > NEWS.new
mv NEWS.new NEWS

%build
%py3_build
make -C docs html

%install
%py3_install

%if %{with tests}
%check
%{__python3} -m pytest -W ignore::pytest.PytestUnknownMarkWarning
%endif

%files -n python%{python3_pkgversion}-%{modname}
%license LICENSE
%doc NEWS README.rst
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/*.egg-info

%files doc
%license LICENSE
%doc docs/_build/html

%changelog
* Wed Jul 12 2023 Petr Viktorin <pviktori@redhat.com> - 1:2.8.1-7
- Mitigate CVE-2007-4559 (tarfile directory traversal).
  Resolves: rhbz#2203905

* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 1:2.8.1-6
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 1:2.8.1-5
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Mon Mar 08 2021 Charalampos Stratakis <cstratak@redhat.com> - 1:2.8.1-4
- Disable tests on RHEL9 to remove the test dependencies

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 31 2020 Gwyn Ciesla <gwync@protonmail.com> - 1:2.8.1-1
- 2.8.1

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 1:2.8.0-10
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 1:2.8.0-9
- Bootstrap for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Miro Hrončok <mhroncok@redhat.com> - 1:2.8.0-7
- Subpackage python2-dateutil has been removed
  See https://fedoraproject.org/wiki/Changes/RetirePython2

* Fri Sep 13 2019 Miro Hrončok <mhroncok@redhat.com> - 1:2.8.0-6
- Reduce Python 2 build dependencies on Fedora 32

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 1:2.8.0-5
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 1:2.8.0-4
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 06 2019 Petr Viktorin <pviktori@redhat.com> - 1:2.8.0-2
- Enable tests (but keep a few skipped on Python 2)
- Add explicit dependency on python3-sphinx_rtd_theme
- Remove test dependency on python2-hypothesis

* Wed Feb 06 2019 Gwyn Ciesla <limburgher@gmail.com> - 1:2.8.0-1
- 2.8.0

* Thu Jan 31 2019 Gwyn Ciesla <limburgher@gmail.com> - 1:2.7.5-1
- 2.7.5

* Sat Sep 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:2.7.3-1
- Update to 2.7.3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 1:2.7.0-2
- Rebuilt for Python 3.7

* Mon Mar 12 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:2.7.0-1
- Fix license tag (should be BSD)
- Update to latest version (#1469314)
  See https://github.com/dateutil/dateutil/blob/master/NEWS for details.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 11 2017 Iryna Shcherbina <ishcherb@redhat.com> - 1:2.6.1-2
- Fix ambiguous Python 2 dependency declarations
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Nov  2 2017 Haïkel Guémar <hguemar@fedoraproject.org> - 1:2.6.1-1
- Upstream 2.6.1

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.6.0-2
- Rebuild for Python 3.6

* Wed Nov 09 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.6.0-1
- Update to 2.6.0 (RHBZ #1393159)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.5.3-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu May  5 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:2.5.3-1
- Update to latest version (#1318828)

* Thu May  5 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:2.5.2-2
- Use separate dirs for docs for py2 and py3 subpackages (#1332623)

* Sat Apr 09 2016 Igor Gnatenko <ignatenko@redhat.com> - 1:2.5.2-1
- Update to 2.5.2
- Adopt for new packaging guidelines

* Mon Feb 29 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 1:2.5.0-1
- Update to latest upstream version
- The patch to make dateutil.zoneinfo.gettz() use the system database is dropped.
  Upstream recommends using dateutil.tz.gettz() instead.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 1:2.4.2-3
- Rebuilt for Python3.5 rebuild
- Add BuildRequires: python3-setuptools

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr  6 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:2.4.2-1
- Update to latest upstream release.

* Tue Mar  3 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:2.4.0-3
- Add patch for string handling in dateutil.tz.tzstr (#1197791)

* Wed Jan 21 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:2.4.0-2
- Add python3 subpackage.
- Conflict with python-vobject <= 0.8.1c-10 (workaround until #1183377
  is fixed one way or another).

* Wed Jan 21 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:2.4.0-1
- Change to new upstream, update to 2.4 (#1126521)
- Build documentation.

* Tue Aug 05 2014 Jon Ciesla <limburgher@gmail.com> - 1:1.5-9
- Reverting to 1.5 pre user feedback and upstream.

* Mon Aug 04 2014 Jon Ciesla <limburgher@gmail.com> - 2.2-1
- Update to 2.2, BZ 1126521.
- Fix bad dates.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 15 2011 Jef Spaleta <jspaleta@fedoraproject.org> - 1.5-3
- Adjust patch to respect systemwide tzdata. Ref bug 729786

* Thu Sep 15 2011 Jef Spaleta <jspaleta@fedoraproject.org> - 1.5-2
- Added a patch to respect systemwide tzdata. Ref bug 729786

* Wed Jul 13 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 1.5-1
- New upstream release
- Fix UTF8 encoding correctly
- Drop buildroot, clean, defattr and use macro for Source

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 1.4.1-2
- small specfile fix

* Fri Feb 20 2009 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 1.4.1-2
- New upstream version

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.4-3
- Rebuild for Python 2.6

* Fri Aug 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.4-2
- fix license tag

* Tue Jul 01 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> 1.4-1
- Latest upstream release

* Fri Jan 04 2008 Jef Spaleta <jspaleta@fedoraproject.org> 1.2-2
- Fix for egg-info file creation

* Thu Jun 28 2007 Orion Poplawski <orion@cora.nwra.com> 1.2-1
- Update to 1.2

* Mon Dec 11 2006 Jef Spaleta <jspaleta@gmail.com> 1.1-5
- Fix python-devel BR, as per discussion in maintainers-list

* Mon Dec 11 2006 Jef Spaleta <jspaleta@gmail.com> 1.1-4
- Release bump for rebuild against python 2.5 in devel tree

* Wed Jul 26 2006 Orion Poplawski <orion@cora.nwra.com> 1.1-3
- Add patch to fix building on x86_64

* Wed Feb 15 2006 Orion Poplawski <orion@cora.nwra.com> 1.1-2
- Rebuild for gcc/glibc changes

* Thu Dec 22 2005 Orion Poplawski <orion@cora.nwra.com> 1.1-1
- Update to 1.1

* Thu Jul 28 2005 Orion Poplawski <orion@cora.nwra.com> 1.0-1
- Update to 1.0

* Tue Jul 05 2005 Orion Poplawski <orion@cora.nwra.com> 0.9-1
- Initial Fedora Extras package
