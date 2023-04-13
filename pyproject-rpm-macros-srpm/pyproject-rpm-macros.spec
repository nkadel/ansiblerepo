# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8}
%global python3_version 3.9
%global python3_pkgversion 39
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

Name:           pyproject-rpm-macros
Summary:        RPM macros for PEP 517 Python packages
License:        MIT

# Disable tests on RHEL9 as to not pull in the test dependencies
# Specify --with tests to run the tests e.g. on EPEL
%bcond_with tests

# The idea is to follow the spirit of semver
# Given version X.Y.Z:
#   Increment X and reset Y.Z when there is a *major* incompatibility
#   Increment Y and reset Z when new macros or features are added
#   Increment Z when this is a bugfix or a cosmetic change
# Dropping support for EOL Fedoras is *not* considered a breaking change
Version:        1.6.2
#Release:        1%%{?dist}
Release:        0.1%{?dist}

# Macro files
Source001:      macros.pyproject
Source002:      macros.aaa-pyproject-srpm

# Implementation files
Source101:      pyproject_buildrequires.py
Source102:      pyproject_save_files.py
Source103:      pyproject_convert.py
Source104:      pyproject_preprocess_record.py
Source105:      pyproject_construct_toxenv.py
Source106:      pyproject_requirements_txt.py
Source107:      pyproject_wheel.py

# Tests
Source201:      test_pyproject_buildrequires.py
Source202:      test_pyproject_save_files.py
Source203:      test_pyproject_requirements_txt.py
Source204:      compare_mandata.py

# Test data
Source301:      pyproject_buildrequires_testcases.yaml
Source302:      pyproject_save_files_test_data.yaml
Source303:      test_RECORD

# Metadata
Source901:      README.md
Source902:      LICENSE

URL:            https://src.fedoraproject.org/rpms/pyproject-rpm-macros

BuildArch:      noarch

%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-pytest-xdist
BuildRequires:  python%{python3_pkgversion}-pyyaml
BuildRequires:  python%{python3_pkgversion}-packaging
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-tox-current-env >= 0.0.6
BuildRequires:  python%{python3_pkgversion}-wheel
BuildRequires:  (python%{python3_pkgversion}-toml if python%{python3_pkgversion}-devel < 3.11)
%endif

# We build on top of those:
BuildRequires:  python-rpm-macros
BuildRequires:  python-srpm-macros
BuildRequires:  python%{python3_pkgversion}-rpm-macros
Requires:       python-rpm-macros
Requires:       python-srpm-macros
Requires:       python%{python3_pkgversion}-rpm-macros
Requires:       (pyproject-srpm-macros = %{?epoch:%{epoch}:}%{version}-%{release} if pyproject-srpm-macros)

# We use the following tools outside of coreutils
Requires:       /usr/bin/find
Requires:       /usr/bin/sed

%description
These macros allow projects that follow the Python packaging specifications
to be packaged as RPMs.

They work for:

* traditional Setuptools-based projects that use the setup.py file,
* newer Setuptools-based projects that have a setup.cfg file,
* general Python projects that use the PEP 517 pyproject.toml file
  (which allows using any build system, such as setuptools, flit or poetry).

These macros replace %%py3_build and %%py3_install,
which only work with setup.py.


%package -n pyproject-srpm-macros
Summary:        Minimal implementation of %%pyproject_buildrequires
Requires:       (pyproject-rpm-macros = %{?epoch:%{epoch}:}%{version}-%{release} if pyproject-rpm-macros)

%description -n pyproject-srpm-macros
This package contains a minimal implementation of %%pyproject_buildrequires.
When used in %%generate_buildrequires, it will generate BuildRequires
for pyproject-rpm-macros. When both packages are installed, the full version
takes precedence.


%prep
# Not strictly necessary but allows working on file names instead
# of source numbers in install section
%setup -c -T
cp -p %{sources} .

%build
# nothing to do, sources are not buildable

%install
mkdir -p %{buildroot}%{_rpmmacrodir}
mkdir -p %{buildroot}%{_rpmconfigdir}/redhat
install -pm 644 macros.pyproject %{buildroot}%{_rpmmacrodir}/
install -pm 644 macros.aaa-pyproject-srpm %{buildroot}%{_rpmmacrodir}/
install -pm 644 pyproject_buildrequires.py %{buildroot}%{_rpmconfigdir}/redhat/
install -pm 644 pyproject_convert.py %{buildroot}%{_rpmconfigdir}/redhat/
install -pm 644 pyproject_save_files.py  %{buildroot}%{_rpmconfigdir}/redhat/
install -pm 644 pyproject_preprocess_record.py %{buildroot}%{_rpmconfigdir}/redhat/
install -pm 644 pyproject_construct_toxenv.py %{buildroot}%{_rpmconfigdir}/redhat/
install -pm 644 pyproject_requirements_txt.py %{buildroot}%{_rpmconfigdir}/redhat/
install -pm 644 pyproject_wheel.py %{buildroot}%{_rpmconfigdir}/redhat/

%if %{with tests}
%check
export HOSTNAME="rpmbuild"  # to speedup tox in network-less mock, see rhbz#1856356
%pytest -vv --doctest-modules -n auto

# brp-compress is provided as an argument to get the right directory macro expansion
%{python3} compare_mandata.py -f %{_rpmconfigdir}/brp-compress
%endif


%files
%{_rpmmacrodir}/macros.pyproject
%{_rpmconfigdir}/redhat/pyproject_buildrequires.py
%{_rpmconfigdir}/redhat/pyproject_convert.py
%{_rpmconfigdir}/redhat/pyproject_save_files.py
%{_rpmconfigdir}/redhat/pyproject_preprocess_record.py
%{_rpmconfigdir}/redhat/pyproject_construct_toxenv.py
%{_rpmconfigdir}/redhat/pyproject_requirements_txt.py
%{_rpmconfigdir}/redhat/pyproject_wheel.py

%doc README.md
%license LICENSE

%files -n pyproject-srpm-macros
%{_rpmmacrodir}/macros.aaa-pyproject-srpm
%license LICENSE


%changelog
* Wed Feb 08 2023 Lumír Balhar <lbalhar@redhat.com> - 1.6.2-1
- Improve detection of lang files

* Fri Feb 03 2023 Miro Hrončok <mhroncok@redhat.com> - 1.6.1-1
- %%pyproject_buildrequires: Avoid leaking stdout from subprocesses

* Fri Jan 20 2023 Miro Hrončok <miro@hroncok.cz> - 1.6.0-1
- Add pyproject-srpm-macros with a minimal %%pyproject_buildrequires macro

* Fri Jan 13 2023 Miro Hrončok <mhroncok@redhat.com> - 1.5.1-1
- Adjusts %%pyproject_buildrequires tests for tox 4

* Mon Nov 28 2022 Miro Hrončok <mhroncok@redhat.com> - 1.5.0-1
- Use %%py3_test_envvars in %%tox when available

* Mon Sep 19 2022 Python Maint <python-maint@redhat.com> - 1.4.0-1
- %%pyproject_save_files: Support License-Files installed into the *Root License Directory* from PEP 369
- %%pyproject_check_import: Import only the modules whose top-level names
  match any of the globs provided to %%pyproject_save_files

* Tue Aug 30 2022 Otto Liljalaakso <otto.liljalaakso@iki.fi> - 1.3.4-1
- Fix typo in internal function name

* Tue Aug 09 2022 Karolina Surma <ksurma@redhat.com> - 1.3.3-1
- Don't fail %%pyproject_save_files '*' if no modules are detected

* Wed Jun 15 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.3.2-1
- Update %%pyproject_build_lib to support setuptools 62.1.0 and later
- %%pyproject_buildrequires: When extension modules are built,
  support https://fedoraproject.org/wiki/Changes/Package_information_on_ELF_objects

* Fri May 27 2022 Owen Taylor <otaylor@redhat.com> - 1.3.1-1
- %%pyproject_install: pass %%{_prefix} explicitly to pip install

* Thu May 12 2022 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-1
- Use tomllib from the standard library on Python 3.11+

* Wed Apr 27 2022 Miro Hrončok <mhroncok@redhat.com> - 1.2.0-1
- %%pyproject_buildrequires: Add provisional -w flag for build backends without
  prepare_metadata_for_build_wheel hook
  When used, the wheel is built in %%pyproject_buildrequires
  and information about runtime requires and extras is read from that wheel.

* Tue Apr 12 2022 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-1
- %%pyproject_save_files: Support nested directories in dist-info

* Tue Mar 22 2022 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-1
- Prefix paths of intermediate files (such as %%{pyproject_files}) with NVRA

* Tue Mar 01 2022 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-1
- Release final version 1.0.0

* Mon Feb 07 2022 Lumír Balhar <lbalhar@redhat.com> - 1.0.0~rc2-1
- Updated compatibility with tox4

* Tue Jan 25 2022 Miro Hrončok <mhroncok@redhat.com> - 1.0.0~rc1-1
- Release version 1.0.0, first release candidate

* Mon Jan 24 2022 Miro Hrončok <mhroncok@redhat.com> - 0-55
- %%pyproject_buildrequires: Generate BuildRequires for this package
  This package is already installed, but this way, the resulting SRPM explicitly BuildRequires it

* Wed Jan 19 2022 Karolina Surma <ksurma@redhat.com> - 0-54
- Include compressed manpages to the package if flag '+auto' is provided to %%pyproject_save_files

* Fri Jan 14 2022 Miro Hrončok <mhroncok@redhat.com> - 0-53
- %%pyproject_buildrequires: Make -r (include runtime) the default, use -R to opt-out

* Sun Dec 19 2021 Gordon Messmer <gordon.messmer@gmail.com> - 0-52
- Handle legacy version specifiers that would previously raise exceptions.

* Wed Dec 08 2021 Miro Hrončok <mhroncok@redhat.com> - 0-51
- Define provisional %%pyproject_build_lib

* Mon Nov 1 2021 Gordon Messmer <gordon.messmer@gmail.com> - 0-50
- Improve handling of > operator, preventing post-release from satisfying most rpm requirements
- Improve handling of < operator, preventing pre-release from satisfying rpm requirement
- Improve handling of != operator with prefix matching, preventing pre-release from satisfying rpm requirements

* Tue Oct 19 2021 Karolina Surma <ksurma@redhat.com> - 0-49
- %%pyproject_save_files: Save %%_pyproject_modules file with importable module names
- Introduce %%pyproject_check_import which passes %%_pyproject_modules to %%py3_check_import
- Introduce -t, -e filtering options to %%pyproject_check_import

* Sat Oct 16 2021 Miro Hrončok <mhroncok@redhat.com> - 0-48
- %%pyproject_buildrequires: Accept installed pre-releases for all requirements

* Thu Sep 09 2021 Miro Hrončok <mhroncok@redhat.com> - 0-47
- %%pyproject_save_files: Expand the namespace error message, also display it with /
- %%pyproject_save_files: Add a workaround error for spaces and [brackets]

* Fri Jul 23 2021 Miro Hrončok <miro@hroncok.cz> - 0-46
- %%pyproject_buildrequires now fails when it encounters an invalid requirement
- Rename %%_pyproject_ghost_distinfo and %%_pyproject_record to indicate they are private
- Automatically detect LICENSE files and mark them with %%license macro

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 09 2021 Python Maint <python-maint@redhat.com> - 0-44
- Escape weird paths generated by %%pyproject_save_files
- Support x.* versions in %%pyproject_buildrequires
- %%pyproject_buildrequires fallbacks to setuptools only if setup.py exists
- Explicitly require the "basic" Python RPM macros
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Thu Jul 01 2021 Tomas Hrnciar <thrnciar@redhat.com> - 0-43
- Generate BuildRequires from file

* Tue Jun 29 2021 Miro Hrončok <mhroncok@redhat.com> - 0-42
- Don't accidentally treat "~= X.0" requirement as "~= X"
- Fixes rhzb#1977060

* Mon Jun 28 2021 Miro Hrončok <mhroncok@redhat.com> - 0-41
- Don't leak %%{_pyproject_builddir} to pytest collection

* Thu May 27 2021 Miro Hrončok <mhroncok@redhat.com> - 0-40
- Don't leak $TMPDIR outside of pyproject macros
- Set %%_pyproject_wheeldir and %%_pyproject_builddir relative to the source tree, not $PWD

* Thu Apr 22 2021 Miro Hrončok <mhroncok@redhat.com> - 0-39.2
- Handle tox provision (tox.requires / tox.minversion)
- Generate BuildRequires on extras in lower case
- Fixes: rhbz#1947074

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 0-39.1
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Mon Mar 08 2021 Charalampos Stratakis <cstratak@redhat.com> - 0-38.1
- Disable tests on RHEL9 to remove tox dependency

* Sun Feb 07 2021 Miro Hrončok <mhroncok@redhat.com> - 0-38
- Include nested __pycache__ directories in %%pyproject_save_files
- Fixes: rhbz#1925963

* Tue Feb 02 2021 Miro Hrončok <mhroncok@redhat.com> - 0-37
- Remove support for Python 3.7 from %%pyproject_buildrequires
- Generate python3dist(toml) BR with pyproject.toml earlier to avoid extra install round
- Generate python3dist(setutpools/wheel) BR without pyproject.toml earlier as well

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 2021 Miro Hrončok <mhroncok@redhat.com> - 0-35
- Update the description of the package to match the new README content

* Fri Dec 04 2020 Miro Hrončok <miro@hroncok.cz> - 0-34
- List all files in %%pyproject_files explicitly to avoid duplicate %%lang entries
- If you amend the installed files after %%pyproject_install, %%pyproject_files might break

* Fri Nov 27 2020 Miro Hrončok <mhroncok@redhat.com> - 0-33
- Pass PYTHONDONTWRITEBYTECODE=1 to %%tox to avoid packaged PYTEST bytecode

* Tue Nov 03 2020 Miro Hrončok <mhroncok@redhat.com> - 0-32
- Allow multiple -e in %%pyproject_buildrequires
- Fixes: rhbz#1886509

* Mon Oct 05 2020 Miro Hrončok <mhroncok@redhat.com> - 0-31
- Support PEP 517 list based backend-path

* Tue Sep 29 2020 Lumír Balhar <lbalhar@redhat.com> - 0-30
- Process RECORD files in %%pyproject_install and remove them
- Support the extras configuration option of tox in %%pyproject_buildrequires -t
- Support multiple -x options for %%pyproject_buildrequires
- Fixes: rhbz#1877977
- Fixes: rhbz#1877978

* Wed Sep 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0-29
- Check the requirements after installing "requires_for_build_wheel"
- If not checked, installing runtime requirements might fail

* Tue Sep 08 2020 Gordon Messmer <gordon.messmer@gmail.com> - 0-28
- Support more Python version specifiers in generated BuildRequires
- This adds support for the '~=' operator and wildcards

* Fri Sep 04 2020 Miro Hrončok <miro@hroncok.cz> - 0-27
- Make code in $PWD importable from %%pyproject_buildrequires
- Only require toml for projects with pyproject.toml
- Remove a no longer useful warning for unrecognized files in %%pyproject_save_files

* Mon Aug 24 2020 Tomas Hrnciar <thrnciar@redhat.com> - 0-26
- Implement automatic detection of %%lang files in %%pyproject_save_files
  and mark them with %%lang in filelist

* Fri Aug 14 2020 Miro Hrončok <mhroncok@redhat.com> - 0-25
- Handle Python Extras in %%pyproject_buildrequires on Fedora 33+

* Tue Aug 11 2020 Miro Hrončok <mhroncok@redhat.com> - 0-24
- Allow multiple, comma-separated extras in %%pyproject_buildrequires -x

* Mon Aug 10 2020 Lumír Balhar <lbalhar@redhat.com> - 0-23
- Make macros more universal for alternative Python stacks

* Thu Aug 06 2020 Tomas Hrnciar <thrnciar@redhat.com> - 0-22
- Change %%pyproject_save_files +bindir argument to +auto
  to list all unclassified files in filelist

* Tue Aug 04 2020 Miro Hrončok <mhroncok@redhat.com> - 0-21
- Actually implement %%pyproject_extras_subpkg

* Wed Jul 29 2020 Miro Hrončok <mhroncok@redhat.com> - 0-20
- Implement %%pyproject_extras_subpkg

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Miro Hrončok <mhroncok@redhat.com> - 0-18
- %%pyproject_buildrequires -x (extras requires for tests) now implies -r
  (runtime requires) instead of erroring without it for better UX.

* Wed Jul 15 2020 Miro Hrončok <mhroncok@redhat.com> - 0-17
- Set HOSTNAME to prevent tox 3.17+ from a DNS query
- Fixes rhbz#1856356

* Fri Jun 19 2020 Miro Hrončok <mhroncok@redhat.com> - 0-16
- Switch from upstream deprecated pytoml to toml

* Thu May 07 2020 Tomas Hrnciar <thrnciar@redhat.com> - 0-15
- Adapt %%pyproject_install not to create a PEP 610 direct_url.json file

* Wed Apr 15 2020 Patrik Kopkan <pkopkan@redhat.com> - 0-14
- Add %%pyproject_save_file macro for generating file section
- Handle extracting debuginfo from extension modules (#1806625)

* Mon Mar 02 2020 Miro Hrončok <mhroncok@redhat.com> - 0-13
- Tox dependency generator: Handle deps read in from a text file (#1808601)

* Wed Feb 05 2020 Miro Hrončok <mhroncok@redhat.com> - 0-12
- Fallback to setuptools.build_meta:__legacy__ backend instead of setuptools.build_meta
- Properly handle backends with colon
- Preserve existing flags in shebangs of Python files in /usr/bin

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 15 2019 Patrik Kopkan <pkopkan@redhat.com> - 0-10
- Install wheel in '$PWD/pyproject-macros-wheeldir' to have more explicit path from which we install.
- The path can be changed by redefining %%_pyproject_wheeldir.

* Wed Nov 13 2019 Anna Khaitovich <akhaitov@redhat.com> - 0-9
- Remove stray __pycache__ directory from /usr/bin when running %%pyproject_install

* Fri Oct 25 2019 Miro Hrončok <mhroncok@redhat.com> - 0-8
- When tox fails, print tox output before failing

* Tue Oct 08 2019 Miro Hrončok <mhroncok@redhat.com> - 0-7
- Move a verbose line of %%pyproject_buildrequires from stdout to stderr

* Fri Jul 26 2019 Petr Viktorin <pviktori@redhat.com> - 0-6
- Use importlib_metadata rather than pip freeze

* Fri Jul 26 2019 Miro Hrončok <mhroncok@redhat.com> - 0-5
- Allow to fetch test dependencies from tox
- Add %%tox macro to invoke tests

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 02 2019 Miro Hrončok <mhroncok@redhat.com> - 0-3
- Add %%pyproject_buildrequires

* Tue Jul 02 2019 Miro Hrončok <mhroncok@redhat.com> - 0-2
- Fix shell syntax errors in %%pyproject_install
- Drop PATH warning in %%pyproject_install

* Fri Jun 28 2019 Patrik Kopkan <pkopkan@redhat.com> - 0-1
- created package
