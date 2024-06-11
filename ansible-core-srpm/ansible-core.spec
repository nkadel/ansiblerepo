# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.12
%global python3_pkgversion 3.12
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

#
# If we should enable docs building
# Currently we cannot until we get a stack of needed packages added and a few bugs fixed
#
%bcond_with docs

#
# If we should enable tests by default
#
#%%if 0%%{?rhel}
%bcond_with tests
#%%%else
#%%bcond_without tests
#%%endif

# Set this when there's a beta or rc version
%global betaver %{nil}

# Differing names since upstream split
%global pypi_name ansible-core
%global srcname ansible

Name: %{pypi_name}
Summary: A radically simple IT automation system
Version: 2.17.0
Release: 0.1%{?betaver}%{?dist}

License: GPLv3+
Epoch: 1

#Source0: %%pypi_source %%{pypi_name} %%{version}%%{?betaver}
Source0: https://github.com/ansible/%{srcname}/archive/refs/tags/v%{version}%{betaver}.zip

Url: https://ansible.com
BuildArch: noarch

# This makes the transition seamless for other packages
# Not all rpm versions support if statements
#Requires: (ansible-packaging if rpm-build)
Requires: ansible-packaging

#Provides: ansible = %%{version}-%%{release}
# For now conflict with the ansible 'classic' package.
Conflicts: ansible < 2.11.0
#
# obsoletes/provides for ansible-base
#
Obsoletes: ansible-base < 2.11.0

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
BuildRequires: python%{python3_pkgversion}-pytz
BuildRequires: glibc-all-langpacks
BuildRequires: python%{python3_pkgversion}-resolvelib >= 0.5.3
BuildRequires: python%{python3_pkgversion}-resolvelib < 1.1.0
BuildRequires: python%{python3_pkgversion}-rpm-macros
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
#BuildRequires: antsibull
%endif

#
# main buildrequires to build
#
BuildRequires: python%{python3_pkgversion}
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-setuptools
BuildRequires: python%{python3_pkgversion}-six
BuildRequires: python%{python3_pkgversion}-requests
BuildRequires: python%{python3_pkgversion}-mock
BuildRequires: python%{python3_pkgversion}-jinja2 >= 3.0.0
BuildRequires: python%{python3_pkgversion}-pyyaml >= 5.1
BuildRequires: python%{python3_pkgversion}-cryptography

%if %{with tests}
BuildRequires: python%{python3_pkgversion}-pytest
BuildRequires: python%{python3_pkgversion}-pytest-xdist
BuildRequires: python%{python3_pkgversion}-pytest-mock
BuildRequires: python%{python3_pkgversion}-pyvmomi
BuildRequires: unzip

# Some tests have awkward "#!/usr/bin/env python"
BuildRequires: /usr/bin/python
BuildRequires: /usr/bin/pip
%endif

# RHEL8 doesn't have python3-paramiko or python3-winrm (yet), but Fedora does
%if 0%{?el} > 8 || 0%{?fedora}
Recommends: python%{python3_pkgversion}-paramiko
Recommends: python%{python3_pkgversion}-winrm
%endif

# needed for json_query filter
Requires: python%{python3_pkgversion}-jmespath
# needed for galaxy
Requires: python%{python3_pkgversion}-resolvelib >= 0.5.3
Requires: python%{python3_pkgversion}-resolvelib < 1.1.0
# avoid module wackiness
Requires: python%{python3_pkgversion}-packaging

# needed for ansible galaxy
Requires: python%{python3_pkgversion}-jinja2 >= 3.0.0

%description
Ansible is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.

This is the base part of ansible (the engine).

%package -n ansible-test
Summary: Tool for testing ansible plugin and module code
Requires: %{name} = %{version}-%{release}

%description -n ansible-test
Ansible is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.

This package installs the ansible-test command for testing modules and plugins
developed for ansible.

%package -n %{pypi_name}-doc
Summary: Documentation for Ansible Base
Obsoletes: ansible-base-doc < 2.10.6-1%{?dist}

%description -n %{pypi_name}-doc

Ansible is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.

This package installs extensive documentation for %{pypi_name}

%prep
%autosetup -p1 -n %{srcname}-%{version}%{?betaver}

# RPM dependency generation confused by dependencies on RHEL 8,
# python 3.11 has this module built in
%if 0%{?el8}
sed -i.bak 's/^importlib_resources /#importlib_resources /g' requirements.txt
%endif

# pytest in Fedora 38 does not support --forked opton
%if 0%{?fc38}
sed -i.bak '/--forked/d' test/lib/ansible_test/_internal/commands/units/__init__.py
%endif

# Set /usr/bin/python consistently for tests
#grep -rl "'/usr/bin/python'" tests/ | \
#grep '.py$' | \
#while reead name; do
#      sed -i.bak "s|'/usr/bin/python'|'/usr/bin/python3'|g" $name
#done

%build
sed -i -s 's|/usr/bin/env python$|%{__python3}|g' test/lib/ansible_test/_util/target/cli/ansible_test_cli_stub.py

# disable the python -s shbang flag as we want to be able to find non system modules
%global py3_shbang_opts %(echo %{py3_shbang_opts} | sed 's/-s//')
%py3_build

%if %{with docs}
  make PYTHON=%{__python3} SPHINXBUILD=sphinx-build-3 -Cdocs/docsite webdocs
%else
  # we still need things to build these minimal docs too.
  #make PYTHON=%{__python3} -Cdocs/docsite config cli keywords modules plugins testing
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

# no need to ship zero length files
find %{buildroot}/%{python3_sitelib} -name .git_keep -exec rm -f {} \;
find %{buildroot}/%{python3_sitelib} -name .travis.yml -exec rm -f {} \;

%check
%if %{with tests}
ln -s /usr/bin/pytest-%{python3_version} bin/pytest
# This test needs a module not packaged in Fedora so disable it.
#rm -f test/units/modules/cloud/cloudstack/test_cs_traffic_type.py
# These tests are failing with pytest 6
rm -f test/units/galaxy/test_collection_install.py
rm -f test/units/module_utils/urls/test_prepare_multipart.py
# requires perms to read/manipulate iptables rules
rm -f test/units/modules/test_iptables.py
# This seems sunos specific
rm -f test/units/modules/test_service.py
make PYTHON=%{__python3} tests-py3
%endif

%files
%license COPYING
%doc README.md
%doc changelogs/CHANGELOG-*.rst
%dir %{_sysconfdir}/ansible/
%config(noreplace) %{_sysconfdir}/ansible/*
%{_bindir}/ansible*
%exclude %{_bindir}/ansible-test
%{_datadir}/ansible/
%{python3_sitelib}/ansible*
%exclude %{python3_sitelib}/ansible_test

%files -n ansible-test
%{_bindir}/ansible-test
%{python3_sitelib}/ansible_test

%files -n %{pypi_name}-doc
%if %{with docs}
%doc docs/docsite/_build/html
%endif

%changelog
* Tue Mar 26 2024 Nico Kadel-Garcia - 2.16.5-0.1
- Update to 2.16.5

* Sun Mar 10 2024 Nico Kadel-Garcia - 2.16.4-0.1
- Update to 2.16.5
- Add Epoch to avoid conflicts on RHEL deployment

* Tue Jul 18 2023 Nico Kadel-Garcia - 2.15.2-0.1
- Update to 2.25.2

* Mon Jul 17 2023 Nico Kadel-Garcia - 2.15.2-0.1rc1
- Update to 2.15.2rc1

* Mon May 15 2023 Nico Kadel-Garcia - 2.15.0-0.1
- Update to 2.15.0

* Wed May 3 2023 Nico Kadel-Garcia - 2.15.0rc2-0.1
- Update to 2.15.0rc2

* Tue Apr 25 2023 Nico Kadel-Garcia - 2.15.0b3-0.1
- Update to 2.15.0b2

* Sun Apr 23 2023 Nico Kadel-Garcia - 2.15.0b2-0.1
- Update to 2.15.0b2
- Disable conditional importlib-resources from requirements.txt on RHEL 8

* Mon Mar 27 2023 Nico Kadel-Garcia - 2.14.4-0.1
- Update to 2.14.4

* Tue Feb 28 2023 Nico Kadel-Garcia - 2.14.3-0.1
- Update to 2.14.3

* Wed Feb 1 2023 Nico Kadel-Garcia - 2.14.2-0.1
- Update to 2.14.2
- Discard obsolete patches

* Sat Nov 05 2022 Nico Kadel-Garcia - 2.14.0rc2-0.1
- Update to 2.14.0rc2

* Fri Oct 14 2022 Nico Kadel-Garcia - 2.13.5-0.2
- Split away ansible-test

* Tue Oct 11 2022 Nico Kadel-Garcia - 2.13.5-0.1
- Update

* Mon Sep 12 2022 Nico Kadel-Garcia - 2.13.4-0.1
- Update resolvelib dependencies

* Mon Aug 15 2022 James Marshall <jamarsha@redhat.com> - 2.13.3-1
- ansible-core 2.13.3 release (rhbz#2118475)

* Wed Jul 20 2022 James Marshall <jamarsha@redhat.com> - 2.13.2-1
- ansible-core 2.13.2 release (rhbz#2109192)

* Mon Jul 04 2022 Dimitri Savineau <dsavinea@redhat.com> - 2.13.1-1
- ansible-core 2.13.1 release (rhbz#2103699)
- add bundled version of jinja2, markupsafe and resolvelib
- rebuild with python 3.9

* Mon Jun 20 2022 Dimitri Savineau <dsavinea@redhat.com> - 2.12.7-1
- ansible-core 2.12.7 release (rhbz#2099323)

* Thu Jun 09 2022 Dimitri Savineau <dsavinea@redhat.com> - 2.12.6-3
- Build manpages (rhbz#2032809)
- Remove legacy files

* Tue Jun 07 2022 Dimitri Savineau <dsavinea@redhat.com> - 2.12.6-2
- switch from git to git-core dependency (rhbz#2094549)

* Tue May 24 2022 James Marshall <jamarsha@redhat.com> - 2.12.6-1
- ansible-core 2.12.6 release

* Mon May 09 2022 Dimitri Savineau <dsavinea@redhat.com> - 2.12.5-1
- ansible-core 2.12.5 release

* Mon Apr 11 2022 James Marshall <jamarsha@redhat.com> - 2.12.4-1
- ansible-core 2.12.4 release

* Mon Mar 14 2022 Dimitri Savineau <dsavinea@redhat.com> - 2.12.3-1
- ansible-core 2.12.3 release
- re-enable changelog and manpages

* Mon Mar 07 2022 Dimitri Savineau <dsavinea@redhat.com> - 2.12.2-3
- replace Obsolete to Conflicts

* Wed Feb 02 2022 Dimitri Savineau <dsavinea@redhat.com> - 2.12.2-2
- fix ansible tarball setup

* Wed Feb 02 2022 Dimitri Savineau <dsavinea@redhat.com> - 2.12.2-1
- ansible-core 2.12.2 release
- add gating and test files

* Wed Jan 19 2022 Dimitri Savineau <dsavinea@redhat.com> - 2.12.1-2
- Remove Provides on ansible

* Thu Dec 16 2021 Yanis Guenane <yguenane@redhat.com> - 2.12.1-1
- ansible-core 2.12.1-1

* Wed Jul 21 2021 Paul Belanger <pabelanger@redhat.com> - 2.11.3-2
- Add git dependency for ansible-galaxy CLI command.

* Tue Jul 20 2021 Yanis Guenane <yguenane@redhat.com> - 2.11.3-1
- ansible-core 2.11.3-1

* Fri Jul 02 2021 Satoe Imaishi <simaishi@redhat.com> - 2.11.2-2
- Add man pages

* Tue Jun 29 2021 Paul Belanger <pabelanger@redhat.com> - 2.11.2-1
- ansible-core 2.11.2 released.
- Drop bundled version of resolvelib in favor of
  python38-resolvelib.

* Wed Mar 31 2021 Rick Elrod <relrod@redhat.com> - 2.11.0b4-1
- ansible-core 2.11.0 beta 4

* Thu Mar 18 2021 Rick Elrod <relrod@redhat.com> - 2.11.0b2-3
- Try adding a Provides for old ansible.

* Thu Mar 18 2021 Rick Elrod <relrod@redhat.com> - 2.11.0b2-2
- Try Obsoletes instead of Conflicts.

* Thu Mar 18 2021 Rick Elrod <relrod@redhat.com> - 2.11.0b2-1
- ansible-core 2.11.0 beta 2
- Conflict with old ansible and ansible-base.

* Thu Mar 11 2021 Rick Elrod <relrod@redhat.com> - 2.11.0b1-1
- ansible-core 2.11.0 beta 1

* Mon Nov 30 2020 Rick Elrod <relrod@redhat.com> - 2.11.0-1
- ansible-core, beta

* Wed Jun 10 2020 Rick Elrod <relrod@redhat.com> - 2.10.0-1
- ansible-base, beta
