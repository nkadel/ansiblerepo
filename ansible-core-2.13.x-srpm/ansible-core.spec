%global pypi_name ansible-core
%global pypi_version 2.12.4

# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8}
%global python3_version 3.8
%global python3_pkgversion 38
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

# We need this because we are no longer noarch, since our bundled deps might
# conceivably need to compile arch-specific things. But we currently have no
# useful debuginfo stuff.
%global debug_package %{nil}

# Disable shebang munging for specific paths.  These files are data files.
# ansible-core-test munges the shebangs itself.
%global __brp_mangle_shebangs_exclude_from_file %{SOURCE1}

# NOTE(pabelanger): Don't auto add pwsh as Requires for ansible-test. We do
# not wish to package it.
%global __requires_exclude ^/usr/bin/pwsh$

# RHEL and Fedora add -s to the shebang line.  We do *not* use -s -E -S or -I
# with ansible because it has many optional features which users need to
# install libraries on their own to use.  For instance, paramiko for the
# network connection plugins or winrm to talk to windows hosts.
# Set this to nil to remove -s
%define py_shbang_opts %{nil}
%define py2_shbang_opts %{nil}
%define py3_shbang_opts %{nil}

#%%define vendor_path %%{buildroot}%%{python3_sitelib}/ansible/_vendor/
#%%define vendor_pip /usr/bin/python3.8 -m pip install --no-deps -v --no-use-pep517 --no-binary :all: -t %%{vendor_path}

# These control which bundled dep versions we pin against
#%%global packaging_version 20.4
#%%global pyparsing_version 2.4.7
#%%global straightplugin_version 1.4.1

Name: ansible-core
Summary: SSH-based configuration management, deployment, and task execution system
Version: %{pypi_version}
Release: 0%{?dist}
ExcludeArch: i686

Group: Development/Libraries
License: GPLv3+
Source0: https://pypi.python.org/packages/source/a/ansible-core/ansible-core-%{version}.tar.gz
Source1: ansible-test-data-files.txt
Source2: ansible.attr
Source3: ansible-generator
Source4: macros.ansible

URL: http://ansible.com

# We conflict old ansible, and any version of ansible-base.
Conflicts: ansible < 2.10.0
Conflicts: ansible-base

# ... and provide 'ansible' so that old packages still work without updated
# spec files.
# Provides: ansible

# Bundled provides that are sprinkled throughout the codebase.
Provides: bundled(python-backports-ssl_match_hostname) = 3.7.0.1
Provides: bundled(python-distro) = 1.5.0
Provides: bundled(python-selectors2) = 1.1.1
Provides: bundled(python-six) = 1.13.0

BuildRequires: python%{python3_pkgversion}-devel
# BuildRequires: python%%{python3_pkgversion}-docutils
BuildRequires: python%{python3_pkgversion}-jinja2
BuildRequires: python%{python3_pkgversion}-pip
BuildRequires: python%{python3_pkgversion}-packaging
BuildRequires: python%{python3_pkgversion}-pyparsing
BuildRequires: python%{python3_pkgversion}-pyyaml
BuildRequires: python%{python3_pkgversion}-resolvelib
BuildRequires: python%{python3_pkgversion}-rpm-macros
BuildRequires: python%{python3_pkgversion}-setuptools
BuildRequires: python%{python3_pkgversion}-straight-plugin
BuildRequires: python%{python3_pkgversion}-wheel

Requires: git
Requires: python%{python3_pkgversion}
Requires: python%{python3_pkgversion}-jinja2
Requires: python%{python3_pkgversion}-PyYAML
Requires: python%{python3_pkgversion}-cryptography
Requires: python%{python3_pkgversion}-resolvelib
Requires: python%{python3_pkgversion}-six
Requires: sshpass

%description
Ansible is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.

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

%prep
%setup -q -n %{pypi_name}-%{version}
cp -a %{S:2} %{S:3} %{S:4} .

# Fix all Python shebangs recursively in ansible-test
# -p preserves timestamps
# -n prevents creating ~backup files
# -i specifies the interpreter for the shebang
pathfix%{python3_version}.py -pni "%{__python3} %{py3_shbang_opts}" test/lib/ansible_test

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --root %{buildroot}

# Create system directories that Ansible defines as default locations in
# ansible/config/base.yml
DATADIR_LOCATIONS='%{_datadir}/ansible/collections
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

UPSTREAM_DATADIR_LOCATIONS=$(grep -ri default lib/ansible/config/base.yml | tr ':' '\n' | grep '/usr/share/ansible')

if [ "$SYSTEM_LOCATIONS" != "$UPSTREAM_SYSTEM_LOCATIONS" ] ; then
	echo "The upstream Ansible datadir locations have changed.  Spec file needs to be updated"
	exit 1
fi

mkdir -p %{buildroot}%{_datadir}/ansible/plugins/
for location in $DATADIR_LOCATIONS ; do
	mkdir %{buildroot}"$location"
done
mkdir -p %{buildroot}%{_sysconfdir}/ansible/
mkdir -p %{buildroot}%{_sysconfdir}/ansible/roles/

cp examples/hosts %{buildroot}%{_sysconfdir}/ansible/
cp examples/ansible.cfg %{buildroot}%{_sysconfdir}/ansible/

install -Dpm0644 -t %{buildroot}%{_fileattrsdir} ansible.attr
install -Dpm0644 -t %{buildroot}%{_rpmmacrodir} macros.ansible
install -Dpm0755 -t %{buildroot}%{_rpmconfigdir} ansible-generator

mkdir -p %{buildroot}/%{_mandir}/man1/
## Build man pages
#
#mkdir /tmp/_vendor
#
## Remove plugins not needed, they bring in more dependencies
#find hacking/build_library/build_ansible/command_plugins ! -name 'generate_man.py' -type f -exec rm -f {} +
#
#PYTHON=python3.8 PYTHONPATH=%{vendor_path}:/tmp/_vendor make docs
#cp -v docs/man/man1/*.1 %%{buildroot}/%%{_mandir}/man1/
#
#cp -pr docs/docsite/rst .
cp -p lib/ansible_core.egg-info/PKG-INFO .

%files
%defattr(-,root,root)
%{_bindir}/ansible*
%exclude %{_bindir}/ansible-test
%config(noreplace) %{_sysconfdir}/ansible/
%doc README.rst PKG-INFO COPYING
%doc changelogs/CHANGELOG-v2.*.rst
# %%doc %%{_mandir}/man1/ansible*
%{_datadir}/ansible/
%{python3_sitelib}/ansible*
%exclude %{python3_sitelib}/ansible_test
%{_fileattrsdir}/ansible.attr
%{_rpmmacrodir}/macros.ansible
%{_rpmconfigdir}/ansible-generator


%files -n ansible-test
%{_bindir}/ansible-test
%{python3_sitelib}/ansible_test

%changelog
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
