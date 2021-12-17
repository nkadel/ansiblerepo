# Created by pyp2rpm-3.3.7
%global pypi_name ansible
%global pypi_version 5.0.1

#
# If we should enable checks
# Currently we cannot until we get a stack of needed packages added and a few bugs fixed
#
%bcond_with checks

# Disable debugionfo package, the submodule generation mishandles this
%define debug_package %{nil}

Name:           %{pypi_name}
Version:        %{pypi_version}
Release:        0.3%{?dist}
Summary:        Radically simple IT automation

License:        GPLv3+
URL:            https://ansible.com/
Source0:        https://files.pythonhosted.org/packages/source/a/%{pypi_name}/%{pypi_name}-%{pypi_version}.tar.gz

BuildRequires:  ansible-core < 2.13
# roll back demand for 2.12, for python 3.6 compatibility
#BuildRequires:  ansible-core >= 2.12
BuildRequires:  ansible-core >= 2.11.6

BuildRequires:  rsync

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-sphinx
# manually added
BuildRequires:  python%{python3_pkgversion}-cryptography
BuildRequires:  python%{python3_pkgversion}-resolvelib
BuildRequires:  python%{python3_pkgversion}-sphinx_rtd_theme

Requires:       ansible-core < 2.13
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

# Prevent build failures on ambigues python
grep -rl '#!/usr/bin/env python$' . | grep '\.py$' | while read name; do
    echo Disambiguationg bare '#!/usr/bin/env python' in: $name
    sed -i "s|#!/usr/bin/env python$|#!/usr/bin/env python3|g" "$name"
done

find ansible_collections \
    -name '*.swp$' -o \
    -name .DS_Store -o \
    -name .ansible-lint -o \
    -name .azure-pipelines -o \
    -name .circleci -o \
    -name .flake8 -o \
    -name .gitattributes -o \
    -name .github -o \
    -name .github -o \
    -name .gitignore -o \
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

find ansible_collections -type d | grep -E "tests/unit|tests/integration|tests/utils|tests/sanity|tests/runner|tests/regression" | \
    while read tests; do
    echo Flushing tests: $tests
    rm -rf "$tests"
done

%build
%{py3_build}

%install
%{py3_install}

# Pre-stage licenses and docs into local dirs, to avoud path stripping
rsync -a --prune-empty-dirs ansible_collections/ \
    --exclude=docs/ \
    --include=*/ \
    --include=*README* \
    --include=*readme* \
    --exclude=* \
    docs/

rsync -a --prune-empty-dirs ansible_collections/ \
    --exclude=licenses/ \
    --exclude=*license.py \
    --include=*/ \
    --include=*LICENSE* \
    --include=*license* \
    --exclude=* \
    licenses/

%if %{with checks}
%check
%{__python3} setup.py test
%endif

%files
%doc porting_guide_5.rst CHANGELOG-v5.rst
%doc COPYING README.rst
%license licenses

%{python3_sitelib}/ansible_collections
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%files -n %{pypi_name}-doc
%doc docs

%changelog
* Thu Dec 16 2021 Nico Kadel-Garcia - 5.0.1-0.3
- Update to 5.0.1

* Thu Dec 2 2021 Nico Kadel-Garcia - 4.9.0
- Update to 4.9.0
- Use find more consistently to flush unwelcome files
- Use rsync to ro put licenses and READMEs into local staging dirs to avoid path stripping

* Sat Nov 6 2021 Nico Kadel-Garcia - 4.8.0
- Initial package.
- Split up excessively long %%doc and %%license lines
- Add more BuildRequires
- Add 'with docs' and 'with checks' to enable only after bugs resolved
