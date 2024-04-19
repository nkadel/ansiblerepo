# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.12
%global python3_pkgversion 3.12
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

%global collection_namespace ansible
%global collection_name netcommon

Name:           ansible-collection-%{collection_namespace}-%{collection_name}
Version:        2.4.0
Release:        0.2%{?dist}
Summary:        Ansible Network Collection for Common Code

# plugins/module_utils/compat/ipaddress.py: Python Software Foundation License version 2
# plugins/module_utils/network/common/config.py: BSD 2-clause "Simplified" License
# plugins/module_utils/network/common/netconf.py: BSD 2-clause "Simplified" License
# plugins/module_utils/network/common/network.py: BSD 2-clause "Simplified" License
# plugins/module_utils/network/common/parsing.py: BSD 2-clause "Simplified" License
# plugins/module_utils/network/common/utils.py: BSD 2-clause "Simplified" License
# plugins/module_utils/network/restconf/restconf.py: BSD 2-clause "Simplified" License
License:        GPLv3+ and BSD and Python
URL:            %{ansible_collection_url}
Source:         https://github.com/ansible-collections/ansible.netcommon/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  ansible-packaging
BuildRequires:  ansible-core

%if 0%{?el8}
BuildRequires:  python%{python3_pkgversion}-rpm-macros
BuildRequires:  %{_bindir}/pathfix.py
%endif

# Manually added
BuildRequires:  python%{python3_pkgversion}-jinja2
BuildRequires:  python%{python3_pkgversion}-yaml

BuildArch:      noarch

%description
%{summary}.

%prep
%autosetup -n ansible.netcommon-%{version}
sed -i -e '/version:/s/null/%{version}/' galaxy.yml
find -type f ! -executable -type f -name '*.py' -print -exec sed -i -e '1{\@^#!.*@d}' '{}' +
rm -vr tests/integration bindep.txt .yamllint changelogs/fragments/.keep
find -type f -name '.gitignore' -print -delete

# Prevent build failures on ambiguous python
grep -rl -e '^#!/usr/bin/env python$' -e '^#!/usr/bin/env python $' */ | \
    grep '\.py$' | \
    while read name; do
        echo "    Disambiguating /usr/bin/env python: $name"
	pathfix.py -i %{__python3} $name
done

grep -rl -e '^#!/usr/bin/python$' -e '^#!/usr/bin/python $' */ | \
    grep '\.py$' | \
    while read name; do
        echo "    Disambiguating /usr/bin/python in: $name"
	pathfix.py -i %{__python3} $name
done

if [ "%{__python3}" != "/usr/bin/python3" ]; then
    grep -rl -e '^#!/usr/bin/python3' -e '^#!/usr/bin/python3 $' */ | \
	grep '\.py$' | \
	while read name; do
            echo "    Disambiguating /usr/bin/python3 in: $name"
	    pathfix.py -i %{__python3} $name
	done
fi

%build
%ansible_collection_build

%install
%ansible_collection_install

%files
%license LICENSE
%doc README.md
%{ansible_collection_files}

%changelog
* Wed Oct 13 2021 Sagi Shnaidman <sshnaidm@redhat.com> - 2.2.0-2
- Use ansible or ansible-core as BuildRequires

* Thu Jul 22 2021 Sagi Shnaidman <sshnaidm@redhat.com> - 2.2.0-1
- Update to 2.2.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.5.0-1
- Update to 1.5.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 2021 Kevin Fenzi <kevin@scrye.com> - 1.4.1-2
- Rebuild for new ansible-generator and allow to be used with ansible-base-2.10.x

* Tue Dec 29 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.4.1-1
- Update to 1.4.1

* Sat Aug 08 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.1.2-1
- Initial package
