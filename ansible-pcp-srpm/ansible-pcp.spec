%bcond_without ansible

%if 0%{?rhel}
%global collection_namespace redhat
%global collection_name rhel_metrics
%else
%global collection_namespace performancecopilot
%global collection_name metrics
%endif

# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8}
%global python3_version 3.9
%global python3_pkgversion 39
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

Name:             ansible-pcp
Version:          2.2.5
#Release:          1%%{?dist}
Release:          0.1%{?dist}
Summary:          Ansible Metric collection for Performance Co-Pilot
License:          MIT
URL:              %{ansible_collection_url}
Source:           https://github.com/performancecopilot/ansible-pcp/archive/v%{version}/%{name}-%{version}.tar.gz

#BuildRequires:    ansible-core >= 2.9.10
BuildRequires:    ansible-packaging
#BuildRequires:    python%{python3_pkgversion}-ansible-lint
BuildRequires:    ansible-lint
BuildArch:        noarch

%description
A collection containing roles for Performance Co-Pilot (PCP) and related
software such as Redis and Grafana.  The collection is made up of several
Ansible roles, including:

%{collection_namespace}.%{collection_name}.pcp
A role for core PCP capabilities, configuring live performance analysis
with a large base set of metrics from the kernel and system services, as
well as data recording and rule inference.

%{collection_namespace}.%{collection_name}.redis
A role for configuring a local Redis server, suitable for use with a
Performance Co-Pilot archive repository (for single or many hosts) and
fast, scalable querying of metrics.

%{collection_namespace}.%{collection_name}.grafana
A role for configuring a local Grafana server, providing web frontend
visuals for Performance Co-Pilot metrics, both live and historically.
Data sources for Vector (live), Redis (historical) and interactive
bpftrace (eBPF) scripts can be configured by this role.  The PCP REST
API service (from the core pcp role) should be configured in order to
use this role.

%{collection_namespace}.%{collection_name}.bpftrace
A role that extends the core PCP role, providing metrics from bpftrace
scripts using Linux eBPF facilities.  Configuring authentication of a
local user capable of running bpftrace scripts via the PCP agent is a
key task of this role.

%{collection_namespace}.%{collection_name}.elasticsearch
A role that extends the core PCP role, providing metrics from a live
ElasticSearch instance for PCP analysis or exporting of PCP metric
values (and metadata) to ElasticSearch for the indexing and querying
of performance data.

%prep
%autosetup
mv .yamllint.yml yamllint.yml
mv .yamllint_defaults.yml yamllint_defaults.yml
%if 0%{?rhel}
rm -vr roles/repository tests/*repository* tests/*/*repository* docs/repository
%endif
rm -vr .github .gitignore .ansible-lint .*.yml
sed -i \
    -e 's/^name: .*/name: %{collection_name}/g' \
    -e 's/^namespace: .*/namespace: %{collection_namespace}/g' \
    galaxy.yml
find . -name \*.yml -o -name \*.md | while read file; do
    sed -i \
        -e 's/performancecopilot.metrics/%{collection_namespace}.%{collection_name}/g' \
    $file
done

# Prevent build failures on ambiguouss python
grep -rl '^#!/usr/bin/env python$' */ | \
    while read name; do
        echo "    Disambiguating /usr/bin/env python: $name"
	sed -i -e 's|^#!/usr/bin/env python$|#!/usr/bin/python3|g' $name
done

grep -rl '^#!/usr/bin/python$' */ | \
    while read name; do
        echo "    Disambiguating /usr/bin/python: $name"
	sed -i -e 's|^#!/usr/bin/python$|#!/usr/bin/python3|g' $name
done

%build
%ansible_collection_build

%install
%ansible_collection_install

%check
mv yamllint.yml .yamllint.yml
mv yamllint_defaults.yml .yamllint_defaults.yml
ansible-lint `find roles -name \*.yml`

%files
%doc README.md
%license LICENSE
%{ansible_collection_files}

%changelog
* Thu Aug 26 2021 Nathan Scott <nathans@redhat.com> 2.2.1-1
- Latest upstream release

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 25 2021 Nathan Scott <nathans@redhat.com> 2.1.4-1
- Latest upstream release

* Thu Jun 03 2021 Nathan Scott <nathans@redhat.com> 2.1.3-1
- Latest upstream release

* Fri Feb 05 2021 Nathan Scott <nathans@redhat.com> 2.1.2-1
- Add RHEL macros to the spec alongside Fedora
- Latest upstream release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 11 2020 Nathan Scott <nathans@redhat.com> 2.0.3-1
- Updated for new version with changed namespace
- Ansible collection macros now used in the spec
- Added ansible-lint checking in %%check section

* Fri Oct 23 2020 Nathan Scott <nathans@redhat.com> 1.0.0-1
- Initial RPM spec build
