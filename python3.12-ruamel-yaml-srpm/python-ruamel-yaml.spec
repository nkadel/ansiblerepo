# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.12
%global python3_pkgversion 3.12
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

%global srcname ruamel-yaml

# Breaks the circular dependency with ruamel.yaml.clib.
%bcond_without bootstrap

Name:           python-ruamel-yaml
Version:        0.18.6
Release:        0.1%{?dist}
Summary:        YAML 1.2 loader/dumper package for Python

# SPDX
License:        MIT
URL:            https://sourceforge.net/projects/ruamel-yaml
# The PyPI sdist does not contain tests, so we use a snapshot from SourceForge
Source:         https://github.com/pycontribs/ruamel-yaml/archive/refs/tags/%{version}.zip

BuildArch:      noarch

%global _description %{expand:
ruamel.yaml is a YAML parser/emitter that supports roundtrip preservation of
comments, seq/map flow style, and map key order.}

%description %{_description}

%package -n     python%{python3_pkgversion}-ruamel-yaml
Summary:        YAML 1.2 loader/dumper package for Python

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pytest

%py_provides python%{python3_pkgversion}-ruamel.yaml

%description -n python%{python3_pkgversion}-ruamel-yaml %{_description}

%prep
%autosetup -n ruamel-yaml-%{version}
# Upstream upper-bounds the Python interpeter versions with which the C
# implementation (ruamel.yaml.clib dependency) may be used. Patch this out.
sed -r -i 's/( and python_version<"[^"]+")(.*ruamel\.yaml\.clib)/\2/' \
    __init__.py
%if %{with bootstrap}
sed -r -i 's/^([[:blank:]]*)(.*ruamel\.yaml\.clib)/\1# \2/' __init__.py
%endif

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
# RFE: Add option for namespace packages to %%pyproject_save_files
# https://bugzilla.redhat.com/show_bug.cgi?id=1935266
%pyproject_save_files ruamel

%check
%if %{with bootstrap}
k="${k-}${k+ and }not test_load_cyaml"
k="${k-}${k+ and }not test_load_cyaml_1_2"
k="${k-}${k+ and }not test_dump_cyaml_1_2"
%endif
%pytest -k "${k-}" _test/test_*.py

%files -n python%{python3_pkgversion}-ruamel-yaml -f %{pyproject_files}
# pyproject_files handles LICENSE; verify with “rpm -qL -p …”
%doc README.md

%changelog
* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Nov 12 2023 Parag Nemade <pnemade AT redhat DOT com> - 0.18.5-1
- Update to 0.18.5

* Thu Oct 26 2023 Joel Capitao <jcapitao@redhat.com> - 0.18.2-1
- Update to 0.18.2 (close RHBZ#2245968)

* Tue Oct 24 2023 Joel Capitao <jcapitao@redhat.com> - 0.18.1-1
- Update to 0.18.1 (close RHBZ#2241174)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 22 2023 Python Maint <python-maint@redhat.com> - 0.17.32-2
- Rebuilt for Python 3.12

* Mon Jun 19 2023 Joel Capitao <jcapitao@redhat.com> - 0.17.32-1
- Update to 0.17.32 (close RHBZ#2210057)

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.17.26-4
- Rebuilt for Python 3.12

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.17.26-3
- Bootstrap for Python 3.12

* Wed May 24 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.17.26-2
- Avoid tox dependency

* Tue May 09 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 0.17.26-1
- Update to 0.17.26 (close RHBZ#2196655)

* Sun May 07 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.17.24-1
- Update to 0.17.24 (close RHBZ#2193478)

* Thu May 04 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.17.22-2
- Confirm License is SPDX MIT
- Reduce macro indirection and drop ancient constructs and conditionals
- Update description from upstream
- Make the package noarch (python-ruamel-yaml-clib contains the compiled code)
- Fix upper-bounded Python interpreter version for ruamel.yaml.clib dependency
- Drop unused manual runtime dependency on setuptools
- Port to pyproject-rpm-macros (“new Python guidelines”)
- Stop numbering the source archive
- Add a bootstrap conditional to break the circular dependency with
  ruamel.yaml.clib
- Fix an obsolete comment referring to bitbucket

* Wed May 03 2023 Maxwell G <maxwell@gtmx.me> - 0.17.22-1
- Update to 0.17.22. Fixes rhbz#2192464.

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.17.21-2
- Rebuilt for Python 3.11

* Tue May 10 2022 Jakub Čajka <jcajka@redhat.com> - 0.17.21-1
- Update to 0.17.21
- Related: BZ#2042422

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.16.6-7
- Rebuilt for Python 3.10

* Mon Feb 22 2021 Joel Capitao <jcapitao@redhat.com> - 0.16.6-6
- Change upstream URL
- Remove obsolete patch

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.16.6-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Jason Montleon <jmontleo@redhat.com> - 0.16.6-1
- Update to 0.16.6

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.16.5-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 30 2019 Chandan Kumar <raukadah@gmail.com> - 0.16.5-2
- Added ruamel-yaml-clib as Requires

* Tue Aug 27 2019 Chedi Toueiti <chedi.toueiti@gmail.com> - 0.16.5-1
- Update to 0.16.5

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.15.41-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.41-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.41-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Miro Hrončok <mhroncok@redhat.com> - 0.15.41-3
- Subpackage python2-ruamel-yaml has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Miro Hrončok <mhroncok@redhat.com> - 0.15.41-1
- Update to 0.15.41
- Add patch not to require ruamel.std.pathlib

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.13.14-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.13.14-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 9 2017 Orion Poplawski <orion@nwra.com> - 0.13.14-1
- Update to 0.13.14

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 13 2017 Jan Chaloupka <jchaloup@redhat.com> - 0.13.13-3
- The ruamel.yaml needs at least typing >= 3.5.2.2
  related: #1386563

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Orion Poplawski <orion@cora.nwra.com> - 0.13.13-1
- Update to 0.13.13

* Tue Jan 31 2017 Orion Poplawski <orion@cora.nwra.com> - 0.12.14-7
- Add patch to support pytest 2.7 in EPEL7

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.12.14-6
- Rebuild for Python 3.6

* Wed Oct 26 2016 Orion Poplawski <orion@cora.nwra.com> - 0.12.14-5
- Require python34-typing on EPEL
- Ignore python2 test failure due to old pytest on EPEL7

* Wed Oct 26 2016 Orion Poplawski <orion@cora.nwra.com> - 0.12.14-4
- Build python3 package
- Run tests

* Tue Oct 25 2016 Chandan Kumar <chkumar@redhat.com> - 0.12.14-3
- Disabling python3 as python3-ruamel-ordereddict not available

* Mon Oct 24 2016 Chandan Kumar <chkumar@redhat.com> - 0.12.14-2
- Fixed python2-typing runtime dependency issue

* Fri Oct 14 2016 Chandan Kumar <chkumar@redhat.com> - 0.12.14-1
- Initial package.
