# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.12
%global python3_pkgversion 3.12
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

%global collection_namespace community
%global collection_name mysql

Name:           ansible-collection-%{collection_namespace}-%{collection_name}
Version:        3.9.0
Release:        0.1%{?dist}
Summary:        MySQL collection for Ansible

License:        GPLv3+
URL:            %{ansible_collection_url}
Source:         https://github.com/ansible-collections/community.mysql/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  ansible-packaging
BuildRequires:  ansible-core >= 2.10.0


%if 0%{?el8}
BuildRequires:  python%{python3_pkgversion}-rpm-macros
%endif
%if 0%{?el8} || 0%{?el9}
BuildRequires:  %{_bindir}/pathfix.py
%endif

# Manually added
BuildRequires:  python%{python3_pkgversion}-jinja2
BuildRequires:  python%{python3_pkgversion}-yaml

BuildArch:      noarch

%description
%{summary}.

%prep
%autosetup -n community.mysql-%{version}
rm -vr .github
find -type f ! -executable -name '*.py' -print -exec sed -i -e '1{\@^#!.*@d}' '{}' +
find -type f -name '.gitignore' -print -delete

# Prevent build failures on ambiguous python
%if 0%{?el8} || 0%{?el9}
find . -name '*.py' | while read name; do
    pathfix.py -i %{__python3} $name
    rm -f ${name}~
done
%else
find . -name '*.py' | while read name; do
    sed -i 's|#!/usr/bin/env python$|#!%__python3|g' $name
    rm -f ${name}~
done

%endif

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
* Wed Oct 20 2021 Orion Poplawski <orion@nwra.com> - 2.3.1-1
- Update to 2.3.1

* Tue Sep 28 2021 Orion Poplawski <orion@nwra.com> - 2.3.0-1
- Update to 2.3.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 02 2021 Orion Poplawski <orion@nwra.com> - 2.1.0-1
- Update to 2.1.0

* Thu Mar 11 2021 Orion Poplawski <orion@nwra.com> - 1.3.0-1
- Initial package
