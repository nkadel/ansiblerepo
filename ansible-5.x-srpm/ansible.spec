# Created by pyp2rpm-3.3.7
# tarball is named ansible at pypi.org, real modules go in ansible_collections
# due to very confusing upsream renaming
%global pypi_name ansible
%global pypi_realname ansible_collections
%global pypi_version 5.10.0

# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8}
%global python3_version 3.9
%global python3_pkgversion 39
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

#
# If we should enable checks
# Currently we cannot until we get a stack of needed packages added and a few bugs fixed
#
%bcond_with checks

# Disable debugionfo package, the submodule generation mishandles this
%define debug_package %{nil}

# Disable '#!/usr/bin/python' and '#!/usr/bin/env python' complaints
%global __brp_mangle_shebangs /usr/bin/true

Name:           %{pypi_name}
Version:        %{pypi_version}
Release:        0.2%{?dist}
Summary:        Radically simple IT automation

License:        GPLv3+
URL:            https://ansible.com/
Source0:        https://files.pythonhosted.org/packages/source/a/%{pypi_name}/%{pypi_name}-%{pypi_version}.tar.gz

BuildRequires:  ansible-core < 2.14.0
# Roll back demand for 2.13, for python 3.6 compatibility
# Use 2.11.9 to avoid accidental published Fedora conflict
#BuildRequires:  ansible-core >= 2.13.0
BuildRequires:  ansible-core

BuildRequires:  rsync

%if 0%{?el8}
BuildRequires:  python%{python3_pkgversion}-rpm-macros
%endif

BuildRequires:  python%{python3_pkgversion}
BuildRequires:  python%{python3_pkgversion}-cryptography
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-resolvelib
BuildRequires:  python%{python3_pkgversion}-setuptools
#BuildRequires:  python%%{python3_pkgversion}-sphinx
#BuildRequires:  python%%{python3_pkgversion}-sphinx_rtd_theme

Requires:       ansible-core < 2.14
Requires:       ansible-core >= 2.11.6

%description
Ansible is a radically simple IT automation system. It handles
configuration management, application deployment, cloud provisioning,
ad-hoc task execution, network automation, and multi-node
orchestration. Ansible makes complex changes like zero-downtime
rolling updates with load...

%package -n %{pypi_name}-doc
Summary:        ansible documentation
%description -n %{pypi_name}-doc
Documentation for ansible

%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

find %{pypi_realname} \
    -name '*.swp$' -o \
    -name .DS_Store -o \
    -name .ansible-lint -o \
    -name .azure-pipelines -o \
    -name .circleci -o \
    -name .flake8 -o \
    -name .gitattributes -o \
    -name .github -o \
    -name .gitignore -o \
    -name .gitkeep -o \
    -name .gitlab-ci.yml -o \
    -name .idea -o \
    -name .keep -o \
    -name .mypy_cache -o \
    -name .orig -o \
    -name .plugin-cache.yaml -o \
    -name .pre-commit-config.yaml -o \
    -name .pytest_cache -o \
    -name .pytest_cache -o \
    -name .settings \
    -name .travis.yml -o \
    -name .vscode -o \
    -name .yamllint -o \
    -name hello -o \
    -name .zuul.yaml | \
    sort | while read hidden; do
    echo Flushing debris file: "$hidden"
    rm -rf "$hidden"
done

find %{pypi_realname} -type d | grep -E "tests/unit|tests/integration|tests/utils|tests/sanity|tests/runner|tests/regression" | \
    while read tests; do
    echo Flushing tests: $tests
    rm -rf "$tests"
done

%build
%{py3_build}

%install
%{py3_install}

# Pre-stage licenses and docs into local dirs, to avoud path stripping
install -d %{buildroot}%{_defaultdocdir}/%{name}-%{version}/%{pypi_realname}/
rsync -a --prune-empty-dirs %{pypi_realname}/ \
    --exclude=docs/ \
    --include=*/ \
    --include=*README* \
    --include=*readme* \
    --exclude=* \
    %{buildroot}%{_defaultdocdir}/%{name}-%{version}/%{pypi_realname}/

install -d %{buildroot}%{_defaultlicensedir}/%{name}-%{version}/%{pypi_realname}/
rsync -a --prune-empty-dirs %{pypi_realname}/ \
    --exclude=licenses/ \
    --exclude=*license.py \
    --include=*/ \
    --include=*LICENSE* \
    --include=*license* \
    --exclude=* \
    %{buildroot}%{_defaultlicensedir}/%{name}-%{version}/%{pypi_realname}/

%if %{with checks}
%check
%{__python3} setup.py test
%endif

%files
%doc porting_guide_*.rst CHANGELOG-*.rst
%doc COPYING README.rst
%exclude %{_defaultdocdir}/%{name}-%{version}/%{pypi_realname}
%license %{_defaultlicensedir}/%{name}-%{version}/%{pypi_realname}

%{python3_sitelib}/%{pypi_realname}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%files -n %{pypi_name}-doc
%doc %{_defaultdocdir}/%{name}-%{version}/%{pypi_realname}

%changelog
* Tue Jun 7 2022 Nico Kadel-Garcia - 5.9.0-0
- Provide a rollback to 5.9.0, just in case

* Wed Jun 1  2022 Nico Kadel-Garcia - 6.0.0b2-0
- Update to beta 6.0.0b2

* Fri May 27 2022 Nico Kadel-Garcia - 6.0.0b1-0
- Update to beta 6.0.0b1

* Mon May 16 2022 Nico Kadel-Garcia - 6.0.0a2-0
- Update to alpha 6.0.0a2, with ansible-core dependency updates

* Wed May 4 2022 Nico Kadel-Garcia - 5.7.1-0
- Update to 5.7.1
- Discard "data_package" repair

* Thu Apr 28 2022 Nico Kadel-Garcia - 5.7.0-0
- Update to 5.7.0
- Repair "data_package -" syntax error in fortios modules

* Wed Apr 6 2022 Nico Kadel-Garcia - 5.6.0-0
- Update to 5.6.0

* Tue Mar 15 2022 Nico Kadel-Garcia - 5.5.0-0
- Update to 5.5.0

* Tue Feb 22 2022 Nico Kadel-Garcia - 5.4.0-0
- Update to 5.4.0

* Tue Feb 1 2022 Nico Kadel-Garcia - 5.3.0-0
- Update to 5.3.0

* Sat Jan 22 2022 Nico Kadel-Garcia - 5.2.0-0.1
- Replace all "shebang python" headers with "#!!/usr/bin/python3" for consistency

* Wed Jan 12 2022 Nico Kadel-Garcia - 5.2.0-0
- Update to 5.2.0

* Wed Dec 22 2021 Nico Kadel-Garcia - 5.1.0-0.1
- Update to 5.1.0
- Simplify and optimize multiple licenses and docs one more step

* Thu Dec 16 2021 Nico Kadel-Garcia - 5.0.1-0.3
- Update to 5.0.1

* Wed Dec 15 2021 Nico Kadel-Garcia - 4.10.0-0.1
- Update to 4.10.0

* Thu Dec 2 2021 Nico Kadel-Garcia - 4.9.0-0.2
- Update to 4.9.0
- Use find more consistently to flush unwelcome files
- Use rsync to ro put licenses and READMEs into local staging dirs to avoid path stripping

* Sat Nov 6 2021 Nico Kadel-Garcia - 4.8.0
- Initial package.
- Split up excessively long %%doc and %%license lines
- Add more BuildRequires
- Add 'with docs' and 'with checks' to enable only after bugs resolved
