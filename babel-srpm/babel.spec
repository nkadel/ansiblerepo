# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.12
%global python3_pkgversion 3.12
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

# There is some bootstrapping involved when upgrading Python 3
# First of all we need babel (this package) to use sphinx
# And pytest is at this point not yet ready
%if 0%{?el8} || 0%{?el9}
%bcond_without bootstrap
%else
%bcond_with bootstrap
%endif

# Since babel 2.12, the pytz dependency is optional.
# However, pytz is preferred when installed.
# Running tests with pytz is optional as well.
# We don't want to pull pytz into ELN/RHEL just to test integration with it,
# but we don't want to ship babel in Fedora with an untested default,
# so we make the dependency conditional.
# Ideally, the dependency would be conditional on pytz availability in the repo,
# but that's not possible in 2023 yet.
# Additionally, the date/time tests require freezegun, which is unwanted in RHEL.
%bcond_without datetime_tests %{undefined rhel}

Name:           babel
Version:        2.13.1
Release:        3%{?dist}
Summary:        Tools for internationalizing Python applications

License:        BSD-3-Clause
URL:            https://babel.pocoo.org/
Source:         %{pypi_source Babel}

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel

%if %{without bootstrap}
BuildRequires:  coreutils
# The Python test dependencies are not generated from tox.ini,
# because it would require complex patching to be usable
# and becasue we want to avoid the tox dependency in ELN/RHEL.
BuildRequires:  python%{python3_pkgversion}-pytest
%if %{with datetime_tests}
BuildRequires:  python%{python3_pkgversion}-freezegun
# The pytz tests are skipped when pytz is missing
BuildRequires:  python%{python3_pkgversion}-pytz
%endif
# build the documentation
BuildRequires:  make
BuildRequires:  python%{python3_pkgversion}-sphinx
%endif
Requires:       python%{python3_pkgversion}-babel = %{?epoch:%{epoch}:}%{version}-%{release}


%description
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.


%package -n python%{python3_pkgversion}-babel
Summary:        Library for internationalizing Python applications

%description -n python%{python3_pkgversion}-babel
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.

%if %{without bootstrap}
%package doc
Summary:        Documentation for Babel
%py_provides    python%{python3_pkgversion}-babel-doc

%description doc
Documentation for Babel
%endif

%prep
%autosetup -p1 -n Babel-%{version}

# Requires EL9 or later
%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

BUILDDIR="$PWD/built-docs"
rm -rf "$BUILDDIR"

%if %{without bootstrap}
pushd docs
make \
    SPHINXBUILD=sphinx-build-3 \
    BUILDDIR="$BUILDDIR" \
    html man
popd
rm -f "$BUILDDIR/html/.buildinfo"
%endif

%install
%pyproject_install
%pyproject_save_files babel

%if %{without bootstrap}
install -D -m 0644 built-docs/man/babel.1 %{buildroot}%{_mandir}/man1/pybabel.1
%endif

%check
export TZ=UTC
%pyproject_check_import
%if %{without bootstrap}
# The deselected doctests fail without pytz when run during Eastern Daylight Time
# https://github.com/python-babel/babel/issues/988
# The ignored files use freezegun
%pytest %{!?with_datetime_tests:\
  -k "not (babel.dates.format_time or babel.dates.get_timezone_name)" \
  --ignore tests/test_dates.py --ignore tests/messages/test_frontend.py}
%endif

%files
%doc CHANGES.rst AUTHORS
%{_bindir}/pybabel

%if %{without bootstrap}
%{_mandir}/man1/pybabel.1*
%endif

%files -n python%{python3_pkgversion}-babel -f %{pyproject_files}

%if %{without bootstrap}
%files doc
%license LICENSE
%doc built-docs/html/*
%endif

%changelog
* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 2.12.1-5
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.12.1-4
- Bootstrap for Python 3.12

* Mon Jun 05 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 2.12.1-3
- Avoid libfaketime and python-freezegun deps in RHEL builds

* Mon Apr 10 2023 Miro Hrončok <mhroncok@redhat.com> - 2.12.1-2
- Fix DST-related test failures

* Wed Mar 01 2023 Miro Hrončok <mhroncok@redhat.com> - 2.12.1-1
- Update to 2.12.1

* Tue Feb 28 2023 Miro Hrončok <mhroncok@redhat.com> - 2.12.0-1
- Update to 2.12.0
- No longer depends on pytz
- No longer depends on setuptools
- Update the License tag to SPDX

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan 01 2023 Felix Schwarz <fschwarz@fedoraproject.org> - 2.11.0-1
- update to 2.11.0

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 20 2022 Felix Schwarz <fschwarz@fedoraproject.org> - 2.10.3-2
- backport patch to remove usage of cgi module (rhbz #2083956)

* Mon Jun 20 2022 Felix Schwarz <fschwarz@fedoraproject.org> - 2.10.3-1
- update to 2.10.3

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.10.1-4
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.10.1-3
- Bootstrap for Python 3.11

* Mon May 16 2022 Nils Philippsen <nils@redhat.com> - 2.10.1-2
- Build and distribute man page for pybabel (#1611174)

* Fri Apr 22 2022 Felix Schwarz <fschwarz@fedoraproject.org> - 2.10.1-1
- update to 2.10.1

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 2.9.1-3
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 2.9.1-2
- Bootstrap for Python 3.10

* Wed Apr 28 2021 Felix Schwarz <fschwarz@fedoraproject.org> - 2.9.1-1
- update to 2.9.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 21 2020 Miro Hrončok <mhroncok@redhat.com> - 2.9.0-3
- Disable Python 2 build entirely

* Tue Nov 24 2020 Miro Hrončok <mhroncok@redhat.com>
- Disable Python 2 build on RHEL 9+

* Mon Nov 16 22:22:25 CET 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 2.9.0-1
- update to 2.9.0

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 2.8.0-6
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 2.8.0-5
- Bootstrap for Python 3.9

* Fri May 08 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 2.8.0-4
- reenable Python 2 subpackage for Fedora 33+ (rhbz #1737930)

* Tue May 05 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 2.8.0-3
- add patch for compatibility with Python 3.9a6

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 02 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 2.8.0-1
- update to upstream version 2.8.0

* Thu Oct 31 2019 Nils Philippsen <nils@tiptoe.de> - 2.7.0-7
- drop python2-babel only from F33 on as it is needed for trac (for the time
  being, #1737930)

* Thu Oct 31 2019 Nils Philippsen <nils@tiptoe.de> - 2.7.0-6
- drop python2-babel from F32 on

* Fri Sep 13 2019 Miro Hrončok <mhroncok@redhat.com> - 2.7.0-5
- Reduce Python 2 build dependencies on Fedora 32

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 2.7.0-4
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 2.7.0-3
- Bootstrap for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 27 2019 Felix Schwarz <fschwarz@fedoraproject.org> - 2.7.0-1
- update to upstream version 2.7.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-4
- Rebuilt for Python 3.7

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-3
- Rebuilt for Python 3.7

* Fri Jun 29 2018 Felix Schwarz <fschwarz@fedoraproject.org> - 2.6.0-2
- add setting to build without Python 2 support

* Fri Jun 29 2018 Felix Schwarz <fschwarz@fedoraproject.org> - 2.6.0-1
- update to upstream version 2.6.0

* Mon Jun 18 2018 Tomas Orsava <torsava@redhat.com> - 2.5.1-5
- Run tests in pytest (as declared in BuildRequires)

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 2.5.1-4
- Rebuilt for Python 3.7

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 2.5.1-3
- Bootstrap for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 15 2017 Felix Schwarz <fschwarz@fedoraproject.org> - 2.5.1-1
- update to upstream version 2.5.1

* Fri Dec 15 2017 Iryna Shcherbina <ishcherb@redhat.com> - 2.3.4-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Miro Hrončok <mhroncok@redhat.com> - 2.3.4-4
- Finish bootstrapping for Python 3.6

* Tue Dec 13 2016 Miro Hrončok <mhroncok@redhat.com> - 2.3.4-3
- Rebuild for Python 3.6
- Add "bootstrap" conditions

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue May 31 2016 Nils Philippsen <nils@redhat.com>
- fix source URL

* Mon Apr 25 2016 Nils Philippsen <nils@redhat.com> - 2.3.4-1
- version 2.3.4
- always build Python3 subpackages
- remove obsolete packaging constructs
- update to current Python packaging guidelines
- build docs non-destructively
- tag license file as %%license
- use %%python_provide macro only if present
- update remove-pytz-version patch
- fix build dependencies
- set TZ in %%check

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-11
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Nov  6 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3-10
- Also make sure that the babel package that has pybabel depends on the correct
  packages (python2 packages on F23 or less and python3 packages on F24 and
  greater.)

* Wed Nov  4 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3-9
- Install the python3 version of pybabel on Fedora 24+ to match with Fedora's
  default python version

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Dec 17 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3-7
- Remove pytz version requirement in egginfo as it confuses newer setuptools

* Mon Jun 30 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3-6
- Change python-setuptools-devel BR into python-setuptools

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Apr 02 2014 Nils Philippsen <nils@redhat.com> - 1.3-3
- fix dependencies (#1083470)

* Sun Oct 06 2013 Felix Schwarz <fschwarz@fedoraproject.org> - 1.3-2
- enable python3 subpackage

* Wed Oct 02 2013 Felix Schwarz <fschwarz@fedoraproject.org> - 1.3-1
- update to Babel 1.3
- disabled %%check as it tries to download the CLDR

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 26 2013 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.6-8
- split documentation off to a separate subpackage

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 18 2012 Nils Philippsen <nils@redhat.com> - 0.9.6-6
- run tests in %%check
- add pytz build requirement for tests

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 0.9.6-5
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Wed Aug 01 2012 Felix Schwarz <felix.schwarz@oss.schwarz.eu> - 0.9.6-4
- disable building of non-functional python3 subpackage (#761583)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 07 2011 Nils Philippsen <nils@redhat.com> - 0.9.6-1
- version 0.9.6:
  * Backport r493-494: documentation typo fixes.
  * Make the CLDR import script work with Python 2.7.
  * Fix various typos.
  * Fixed Python 2.3 compatibility (ticket #146, #233).
  * Sort output of list-locales.
  * Make the POT-Creation-Date of the catalog being updated equal to
    POT-Creation-Date of the template used to update (ticket #148).
  * Use a more explicit error message if no option or argument (command) is
    passed to pybabel (ticket #81).
  * Keep the PO-Revision-Date if it is not the default value (ticket #148).
  * Make --no-wrap work by reworking --width's default and mimic xgettext's
    behaviour of always wrapping comments (ticket #145).
  * Fixed negative offset handling of Catalog._set_mime_headers (ticket #165).
  * Add --project and --version options for commandline (ticket #173).
  * Add a __ne__() method to the Local class.
  * Explicitly sort instead of using sorted() and don't assume ordering
    (Python 2.3 and Jython compatibility).
  * Removed ValueError raising for string formatting message checkers if the
    string does not contain any string formattings (ticket #150).
  * Fix Serbian plural forms (ticket #213).
  * Small speed improvement in format_date() (ticket #216).
  * Fix number formatting for locales where CLDR specifies alt or draft
    items (ticket #217)
  * Fix bad check in format_time (ticket #257, reported with patch and tests by
    jomae)
  * Fix so frontend.CommandLineInterface.run does not accumulate logging
    handlers (#227, reported with initial patch by dfraser)
  * Fix exception if environment contains an invalid locale setting (#200)
- install python2 rather than python3 executable (#710880)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug 26 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.5-3
- Add python3 subpackage

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Apr  7 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.5-1
- This release contains a small number of bugfixes over the 0.9.4
- release.
-
- What's New:
- -----------
- * Fixed the case where messages containing square brackets would break
-  with an unpack error
- * Fuzzy matching regarding plurals should *NOT* be checked against
-  len(message.id) because this is always 2, instead, it's should be
-  checked against catalog.num_plurals (ticket #212).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Mar 28 2009 Robert Scheck <robert@fedoraproject.org> - 0.9.4-4
- Added missing requires to python-setuptools for pkg_resources

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.9.4-2
- Rebuild for Python 2.6

* Mon Aug 25 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.4-1
- Update to 0.9.4

* Thu Jul 10 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.3-1
- Update to 0.9.3

* Sun Dec 16 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.1-1
- Update to 0.9.1

* Tue Aug 28 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9-2
- BR python-setuptools-devel

* Mon Aug 27 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9-1
- Update to 0.9

* Mon Jul  2 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8.1-1
- Update to 0.8.1
- Remove upstreamed patch.

* Fri Jun 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8-3
- Replace patch with one that actually applies.

* Fri Jun 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8-2
- Apply upstream patch to rename command line script to "pybabel" - BZ#246208

* Thu Jun 21 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8-1
- First version for Fedora

