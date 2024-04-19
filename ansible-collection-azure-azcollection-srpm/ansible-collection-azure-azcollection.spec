# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.12
%global python3_pkgversion 3.12
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

%global _docdir_fmt %{name}

Name:           ansible-collection-azure-azcollections
Version:        2.2.0
Release:        0.1%{?dist}
Summary:        Ansible Network Collection for Azure code
License:        GPLv3
URL:            %{ansible_collection_url ansible azcollections}
Source:         https://github.com/ansible-collections/azure/archive/refs/tags/v%{version}.zip

# https://github.com/ansible-collections/azure/archive/refs/tags/v2.2.0.zip

# Patch galaxy.yml to exclude unnecessary files from the built collection.
# This is a downstream only patch.
BuildRequires:  ansible-packaging

BuildArch:      noarch

%global _description %{expand:
The Ansible ansible.azcollections collection includes common content to help
automate the management of network, security, and cloud devices. This includes
connection plugins, such as network_cli, httpapi, and netconf.}

%description %_description

%prep
%autosetup -n azure-%{version}
sed -i -e '/version:/s/null/%{version}/' galaxy.yml
find -type f -name '*.py' | xargs sed -i 's|^#!/usr/bin/env python$|#!%{__python3}|g'

%build
%ansible_collection_build

%install
%ansible_collection_install

%files -f %{ansible_collection_filelist}
%license LICENSE
%doc README.md CHANGELOG.md

%changelog
* Mon Mar 4 2024 Nico Kadel-Garcia <nkadel@gmail.com>
- Package azure collection as RPM
