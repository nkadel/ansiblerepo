# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.12
%global python3_pkgversion 3.12
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

%global collection_namespace netbox
%global collection_name netbox

Name:           ansible-collection-%{collection_namespace}-%{collection_name}
Version:        3.17.0
Release:        0.3%{?dist}
Summary:        Netbox modules for Ansible

License:        GPLv3+
URL:            %{ansible_collection_url}
Source:         https://github.com/netbox-community/ansible_modules/archive/v%{version}/%{name}-%{version}.tar.gz

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
%autosetup -n ansible_modules-%{version}
sed -i -e '1{\@^#!.*@d}' plugins/modules/*.py
rm -vr .{github,gitignore,readthedocs.yml} tests/integration

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
%doc README.md CHANGELOG.rst
%{ansible_collection_files}

%changelog
* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 2021 Kevin Fenzi <kevin@scrye.com> - 1.2.0-3
- Rebuild against new ansible-generator and allow to be used by ansible-base-2.10.x

* Wed Dec 30 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.2.0-2
- Drop runtime dependencies

* Tue Dec 29 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Sun Aug 09 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.3.1-1
- Update to 0.3.1

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 04 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1

* Sun Apr 19 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.1.10-1
- Update to 0.1.10

* Wed Mar 04 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.1.9-1
- Initial package
