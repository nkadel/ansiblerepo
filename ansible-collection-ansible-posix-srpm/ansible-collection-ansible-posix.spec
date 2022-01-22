%global collection_namespace ansible
%global collection_name posix

Name:           ansible-collection-%{collection_namespace}-%{collection_name}
Version:        1.3.0
Release:        0.2%{?dist}
Summary:        Ansible Collection targeting POSIX and POSIX-ish platforms

# plugins/module_utils/mount.py: Python Software Foundation License version 2
License:        GPLv3+ and Python
URL:            %{ansible_collection_url}
Source:         https://github.com/ansible-collections/ansible.posix/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  ansible-core >= 2.11.0
# Manually added
BuildRequires:  python%{python3_pkgversion}-jinja2
BuildRequires:  python%{python3_pkgversion}-yaml

BuildArch:      noarch

%description
%{summary}.

%prep
%autosetup -n ansible.posix-%{version}
rm -vr tests/{integration,utils} .github changelogs/fragments/.keep {test-,}requirements.txt shippable.yml
rm -vr .azure-pipelines
find -type f ! -executable -name '*.py' -print -exec sed -i -e '1{\@^#!.*@d}' '{}' +
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
%license COPYING
%doc README.md
%{ansible_collection_files}

%changelog
* Thu Oct 14 2021 Sagi Shnaidman <sshnaidm@redhat.com> - 1.3.0-2
- Use ansible or ansible-core as BuildRequires 

* Mon Sep 06 2021 Kevin Fenzi <kevin@scrye.com> - 1.3.0-1
- Update to 1.3.0. Fixes rhbz#1992970

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Apr 24 2021 Kevin Fenzi <kevin@scrye.com> - 1.2.0-1
- Update to 1.2.0.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 2021 Kevin Fenzi <kevin@scrye.com> - 1.1.1-2
- Rebuild against new ansible-generator and allow to be used by ansible-base-2.10.x

* Tue Dec 29 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1

* Sun Aug 09 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.1.0-1
- Initial package
