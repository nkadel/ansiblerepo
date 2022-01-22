%global collection_namespace community
%global collection_name general

Name:           ansible-collection-%{collection_namespace}-%{collection_name}
Version:        4.0.0
Release:        0%{?dist}
Summary:        Modules and plugins supported by Ansible community

# plugins/module_utils/_mount.py: Python Software Foundation License version 2
# plugins/module_utils/_netapp.py: BSD 2-clause "Simplified" License
# plugins/module_utils/compat/ipaddress.py: Python Software Foundation License version 2
# plugins/module_utils/identity/keycloak/keycloak.py: BSD 2-clause "Simplified" License
License:        GPLv3+ and BSD and Python
URL:            %{ansible_collection_url}
Source:         https://github.com/ansible-collections/community.general/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  ansible-core >= 2.11.0

BuildArch:      noarch
# Manually added for RHEL
BuildRequires:  python%{python3_pkgversion}-jinja2
BuildRequires:  python%{python3_pkgversion}-yaml

%description
%{summary}.

%prep
%autosetup -n community.general-%{version}
rm -vr .github .azure-pipelines
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
rm -vr %{buildroot}%{ansible_collection_files}/%{collection_name}/tests

%files
%license COPYING
%doc README.md CHANGELOG.rst
%{ansible_collection_files}

%changelog
* Wed Nov 03 2021 Sagi Shnaidman (@sshnaidm) <sshnaidm@redhat.com> - 4.0.0-1
- Update to 4.0.0

* Tue Oct 12 2021 Maxwell G (@gotmax23) <gotmax@e.email - 3.8.0-1
- Update to 3.8.0. Fixes rhbz#2013282

* Sat Sep 25 2021 Kevin Fenzi <kevin@scrye.com> - 3.7.0-1
- Update to 3.7.0. Fixes rhbz#1999899

* Thu Sep 23 2021 Alfredo Moralejo <amoralej@redhat.com> - 3.5.0-2
- Use ansible or ansible-core as BuildRequires

* Wed Aug 11 2021 Kevin Fenzi <kevin@scrye.com> - 3.5.0-1
- Update to 3.5.0. Fixes rhbz#1992481

* Wed Aug 4 2021 Maxwell G <gotmax@e.email> - 3.4.0-1
- Update to 3.4.0. Fixes rhbz#1983969 .

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 10 2021 Kevin Fenzi <kevin@scrye.com> - 3.3.2-1
- Update to 3.3.2. Fixes rhbz#1977438

* Tue Jun 08 2021 Kevin Fenzi <kevin@scrye.com> - 3.2.0-1
- Update to 3.2.0. Fixes rhbz#1969570

* Sat May 29 2021 Kevin Fenzi <kevin@scrye.com> - 3.1.0-2
- Fix sed issue that caused python33 to be required.

* Sat May 29 2021 Kevin Fenzi <kevin@scrye.com> - 3.1.0-1
- Update to 3.1.0. Fixes rhbz#1957092

* Tue May 11 2021 Kevin Fenzi <kevin@scrye.com> - 3.0.2-1
- Update to 3.0.2. Fixes rhbz#1957092

* Wed May 05 2021 Kevin Fenzi <kevin@scrye.com> - 3.0.1-1
- Update to 3.0.1. Fixes rhbz#1957092

* Tue Apr 27 2021 Kevin Fenzi <kevin@scrye.com> - 3.0.0-1
- Update to 3.0.0. Fixes rhbz#1953895

* Sat Apr 24 2021 Kevin Fenzi <kevin@scrye.com> - 2.5.1-1
- Update to 2.5.1.

* Thu Feb 04 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 2021 Kevin Fenzi <kevin@scrye.com> - 1.3.1-2
- Rebuild against new ansible-generator and allow usage by ansible-base-2.10.x

* Tue Dec 29 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1

* Sun Aug 09 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.0.0-1
- Initial package
