#
# If we should enable docs building
# Currently we cannot until we get a stack of needed packages added and a few bugs fixed
#
%bcond_with docs

#
# If we should enable tests by default
#
%bcond_with tests

# Set this when there's a beta or rc version
#%%global betaver rc2

Name: ansible-core
Summary: A radically simple IT automation system
Version: 2.12.2
Release: 0.1%{?betaver}%{?dist}

License: GPLv3+
Source0: %pypi_source ansible-core %{version}%{?betaver}

Source1: ansible.attr
Source2: ansible-generator
Source3: macros.ansible
Url: http://ansible.com
BuildArch: noarch
#Provides: ansible = %%{version}-%%{release}
#Obsoletes: ansible <= 2.9.99
# For now conflict with the ansible 'classic' package.
Conflicts: ansible <= 2.9.99
#
# obsoletes/provides for ansible-base
#
Provides: ansible-base = 2.10.7
Obsoletes: ansible-base < 2.10.6-1%{?dist}
# Avoids mixed ansible release dependency wackiness
Obsoletes: ansible-core < 2.12.0

# A 2.10.3 async test uses /usr/bin/python, which we do not have by default.
# Patch the test to use /usr/bin/python3 as we have for our build.
Patch1:  2.10.3-test-patch.patch

%if %{with tests}
#
# For tests
#
# These two exist on both fedora and rhel8
#
BuildRequires: make
BuildRequires: git-core
BuildRequires: python%{python3_pkgversion}-packaging
BuildRequires: python%{python3_pkgversion}-pexpect
BuildRequires: openssl
BuildRequires: python%{python3_pkgversion}-systemd
#
# These only exist on Fedora. RHEL8 will just skip tests that need them.
#
%if 0%{?fedora}
BuildRequires: python%{python3_pkgversion}-paramiko
BuildRequires: python%{python3_pkgversion}-winrm

BuildRequires: python%{python3_pkgversion}-crypto
BuildRequires: python%{python3_pkgversion}-pbkdf2
BuildRequires: python%{python3_pkgversion}-httmock
BuildRequires: python%{python3_pkgversion}-gitlab
BuildRequires: python%{python3_pkgversion}-boto3
BuildRequires: python%{python3_pkgversion}-botocore
BuildRequires: python%{python3_pkgversion}-coverage
BuildRequires: python%{python3_pkgversion}-passlib
%endif
%endif
%if %{with docs}
BuildRequires: make
BuildRequires: python%{python3_pkgversion}-sphinx
BuildRequires: python%{python3_pkgversion}-sphinx-theme-alabaster
BuildRequires: python%{python3_pkgversion}-sphinx-notfound-page
BuildRequires: asciidoc
BuildRequires: python%{python3_pkgversion}-straight-plugin
BuildRequires: python%{python3_pkgversion}-rstcheck
BuildRequires: python%{python3_pkgversion}-pygments
BuildRequires: antsibull
%endif

#
# main buildrequires to build
#
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-setuptools
BuildRequires: python%{python3_pkgversion}-six
BuildRequires: python%{python3_pkgversion}-nose
BuildRequires: python%{python3_pkgversion}-pytest
BuildRequires: python%{python3_pkgversion}-pytest-xdist
BuildRequires: python%{python3_pkgversion}-pytest-mock
BuildRequires: python%{python3_pkgversion}-requests
BuildRequires: python%{python3_pkgversion}-mock
BuildRequires: python%{python3_pkgversion}-jinja2
%if 0%{?fedora}
BuildRequires: python%{python3_pkgversion}-pyyaml
%else
BuildRequires: python%{python3_pkgversion}-PyYAML
%endif
BuildRequires: python%{python3_pkgversion}-cryptography
BuildRequires: python%{python3_pkgversion}-pyvmomi

# RHEL8 does not have python%%{python3_pkgversion}-paramiko or python%%{python3_pkgversion}-winrm (yet), but Fedora does
%if 0%{?fedora}
Recommends: python%{python3_pkgversion}-paramiko
Recommends: python%{python3_pkgversion}-winrm
%endif

Requires: python%{python3_pkgversion}-jinja2
# needed for json_query filter
Requires: python%{python3_pkgversion}-jmespath
# needed for galaxy
Requires: python%{python3_pkgversion}-resolvelib
# needed

%if 0%{?fedora}
BuildRequires: python%{python3_pkgversion}-pyyaml
%else
BuildRequires: python%{python3_pkgversion}-PyYAML
%endif

%description
Ansible is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.

This is the base part of ansible (the engine).

%package -n ansible-core-doc
Summary: Documentation for Ansible Base
Provides: ansible-base-doc = 2.10.7
Obsoletes: ansible-base-doc < 2.10.6-1%{?dist}

%description -n ansible-core-doc

Ansible is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.

This package installs extensive documentation for ansible-core

%prep
%autosetup -p1 -n %{name}-%{version}%{?betaver}
cp -a %{S:1} %{S:2} %{S:3} .

grep -rl '^#!/usr/bin/env python$' */ | \
    grep '\.py$' | \
    while read name; do
        echo "    Disambiguating /usr/bin/env python: $name"
	sed -i -e 's|^#!/usr/bin/env python$|#!/usr/bin/python3|' $name
done

grep -rl '^#!/usr/bin/python$' */ | \
    grep '\.py$' | \
    while read name; do
        echo "    Disambiguating /usr/bin/python in: $name"
	sed -i -e 's|^#!/usr/bin/python$|#!/usr/bin/python3|' $name
done

sed -i -s 's|/usr/bin/env python|/usr/bin/python3|' \
    test/lib/ansible_test/_util/target/cli/ansible_test_cli_stub.py

%build
# disable the python -s shbang flag as we want to be able to find non system modules
%global py3_shbang_opts %(echo %{py3_shbang_opts} | sed 's/-s//')
%py3_build

%if %{with docs}
  make PYTHON=%{__python3} SPHINXBUILD=sphinx-build-%{python3_version} webdocs
%else
  # we still need things to build these minimal docs too.
  # make PYTHON=%{__python3} -Cdocs/docsite config cli keywords modules plugins testing
%endif

%install
%py3_install

# Create system directories that Ansible defines as default locations in
# ansible/config/base.yml
DATADIR_LOCATIONS='%{_datadir}/ansible/collections
%{_datadir}/ansible/collections/ansible_collections
%{_datadir}/ansible/plugins/doc_fragments
%{_datadir}/ansible/plugins/action
%{_datadir}/ansible/plugins/become
%{_datadir}/ansible/plugins/cache
%{_datadir}/ansible/plugins/callback
%{_datadir}/ansible/plugins/cliconf
%{_datadir}/ansible/plugins/connection
%{_datadir}/ansible/plugins/filter
%{_datadir}/ansible/plugins/httpapi
%{_datadir}/ansible/plugins/inventory
%{_datadir}/ansible/plugins/lookup
%{_datadir}/ansible/plugins/modules
%{_datadir}/ansible/plugins/module_utils
%{_datadir}/ansible/plugins/netconf
%{_datadir}/ansible/roles
%{_datadir}/ansible/plugins/strategy
%{_datadir}/ansible/plugins/terminal
%{_datadir}/ansible/plugins/test
%{_datadir}/ansible/plugins/vars'

UPSTREAM_DATADIR_LOCATIONS=$(grep -ri default lib/ansible/config/base.yml| tr ':' '\n' | grep '/usr/share/ansible')

if [ "$SYSTEM_LOCATIONS" != "$UPSTREAM_SYSTEM_LOCATIONS" ] ; then
  echo "The upstream Ansible datadir locations have changed.  Spec file needs to be updated"
  exit 1
fi

mkdir -p %{buildroot}%{_datadir}/ansible/plugins/
for location in $DATADIR_LOCATIONS ; do
	mkdir %{buildroot}"$location"
done
mkdir -p %{buildroot}/etc/ansible/
mkdir -p %{buildroot}/etc/ansible/roles/

cp examples/hosts %{buildroot}/etc/ansible/
cp examples/ansible.cfg %{buildroot}/etc/ansible/
mkdir -p %{buildroot}/%{_mandir}/man1
cp -v docs/man/man1/*.1 %{buildroot}/%{_mandir}/man1/

install -Dpm0644 -t %{buildroot}%{_fileattrsdir} ansible.attr
install -Dpm0644 -t %{buildroot}%{_rpmmacrodir} macros.ansible
install -Dpm0755 -t %{buildroot}%{_rpmconfigdir} ansible-generator

# no need to ship zero length files
find %{buildroot}/%{python3_sitelib} -name .git_keep -exec rm -f {} \;
find %{buildroot}/%{python3_sitelib} -name .travis.yml -exec rm -f {} \;

%check
%if %{with tests}
ln -s /usr/bin/pytest-%{python3_version} bin/pytest
pathfix.py -i %{__python3} -p test/lib/ansible_test/_data/cli/ansible_test_cli_stub.py
# This test needs a module not packaged in Fedora so disable it.
#rm -f test/units/modules/cloud/cloudstack/test_cs_traffic_type.py
# These tests are failing with pytest 6
rm -f test/units/galaxy/test_collection_install.py
rm -f test/units/module_utils/urls/test_prepare_multipart.py
make PYTHON=/usr/bin/python3 tests-py3
%endif

%files
%license COPYING
%doc README.rst PKG-INFO changelogs/CHANGELOG-v2.12.rst
%dir %{_sysconfdir}/ansible/
%config(noreplace) %{_sysconfdir}/ansible/*
%{_mandir}/man1/ansible*
%{_bindir}/ansible*
%{_datadir}/ansible/
%{python3_sitelib}/ansible
%{python3_sitelib}/ansible_test
%{python3_sitelib}/*egg-info
%{_fileattrsdir}/ansible.attr
%{_rpmmacrodir}/macros.ansible
%{_rpmconfigdir}/ansible-generator

%files -n ansible-core-doc
%doc docs/docsite/rst
%if %{with docs}
%doc docs/docsite/_build/html
%endif

%changelog
* Tue Feb 1 2022 Nico Kadel-Garcia - 2.12.2-0.1
- Update to 2.12.2

* Sat Jan 22 2022 Nico Kadel-Garcia - 2.12.1-0.2
- Replace all "shebang python" headers with "#!!/usr/bin/python3" for consistency

* Thu Dec 16 2021 Nico Kadel-Garcia - 2.12.1-0.1
- Update to 2.12.1

* Thu Dec  2 2021 Nico Kadel-Garcia
- Add Requires for pyyaml and jinja2

* Mon Nov 08 2021 Kevin Fenzi <kevin@scrye.com> - 2.12.0-1
- Update to 2.12.0. Fixes rhbz#2022533

* Thu Oct 14 2021 Maxwell G <gotmax@e.email> - 2.11.6-1
- Update to 2.11.6.

* Tue Sep 14 2021 Kevin Fenzi <kevin@scrye.com> - 2.11.5-1
- Update to 2.11.5. Fixes rhbz#2002393

* Thu Aug 19 2021 Kevin Fenzi <kevin@scrye.com> - 2.11.4-1
- Update to 2.11.4. Fixes rhbz#1994107

* Sun Jul 25 2021 Kevin Fenzi <kevin@scrye.com> - 2.11.3-1
- Update to 2.11.3. Fixes rhbz#1983836

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Kevin Fenzi <kevin@scrye.com> - 2.11.2-1
- Update to 2.11.2. Fixed rhbz#1974593

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.11.1-2
- Rebuilt for Python 3.10

* Mon May 24 2021 Kevin Fenzi <kevin@scrye.com> - 2.11.1-1
- Update to 2.11.1. Fixes rhbz#1964172

* Tue Apr 27 2021 Kevin Fenzi <kevin@scrye.com> - 2.11.0-1
- Update to 2.11.0 final.

* Sat Apr 24 2021 Kevin Fenzi <kevin@scrye.com> - 2.11.0-0.3.rc2
- Update to 2.11.0rc2.

* Sat Apr 03 2021 Kevin Fenzi <kevin@scrye.com> - 2.11.0-0.1.b4
- Rename to ansible-base, update to b4 beta version.

* Sat Feb 20 2021 Kevin Fenzi <kevin@scrye.com> - 2.10.6-1
- Update to 2.10.6.
- Fixes CVE-2021-20228

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 24 2021 Kevin Fenzi <kevin@scrye.com> - 2.10.5-1
- Update to 2.10.5.

* Sat Dec 19 2020 Kevin Fenzi <kevin@scrye.com> - 2.10.4-1
- Update to 2.10.4

* Sat Nov 07 2020 Kevin Fenzi <kevin@scrye.com> - 2.10.3-2
- Various review fixes

* Tue Nov 03 2020 Kevin Fenzi <kevin@scrye.com> - 2.10.3-1
- Update to 2.10.3

* Sat Oct 10 2020 Kevin Fenzi <kevin@scrye.com> - 2.10.2-1
- Update to 2.10.2

* Sat Sep 26 2020 Kevin Fenzi <kevin@scrye.com> - 2.10.1-1
- Initial version for review.
