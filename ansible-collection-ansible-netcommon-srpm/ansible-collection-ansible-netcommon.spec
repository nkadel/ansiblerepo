%global collection_namespace ansible
%global collection_name netcommon

# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}

Name:           ansible-collection-%{collection_namespace}-%{collection_name}
Version:        2.4.0
Release:        0%{?dist}
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

BuildRequires:  ansible-core >= 2.11.0
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
