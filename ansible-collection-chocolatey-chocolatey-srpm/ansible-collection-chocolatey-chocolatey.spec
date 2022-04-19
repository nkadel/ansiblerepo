%global collection_namespace chocolatey
%global collection_name chocolatey

# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}

Name:           ansible-collection-%{collection_namespace}-%{collection_name}
Version:        1.1.0
Release:        0%{?dist}
Summary:        Ansible collection for Chocolatey

License:        GPLv3+
URL:            %{ansible_collection_url}
Source:         https://github.com/chocolatey/chocolatey-ansible/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  ansible-core >= 2.9.10
# Manually added
BuildRequires:  python%{python3_pkgversion}-jinja2
BuildRequires:  python%{python3_pkgversion}-yaml

BuildArch:      noarch

%description
The collection includes the modules required to configure Chocolatey, as well
as manage packages on Windows using Chocolatey.

%prep
%autosetup -n chocolatey-ansible-%{version}
rm -vr azure-pipelines.yml
find -type f ! -executable -name '*.py' -print -exec sed -i -e '1{\@^#!.*@d}' '{}' +
find -type f -name '.gitignore' -print -delete
sed -i -e 's/{{ REPLACE_VERSION }}/%{version}/' chocolatey/galaxy.yml

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
cd chocolatey
%ansible_collection_build

%install
cd chocolatey
%ansible_collection_install
rm -vr %{buildroot}%{ansible_collection_files}/%{collection_name}/tests

%files
%license LICENSE
%doc README.md
%{ansible_collection_files}

%changelog
* Sat Nov 6 2021 Nico Kadel-Garcia <nkadel@gmail.com> - 1.1.0-0
- Update to 1.1.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Mar 12 2021 Orion Poplawski <orion@nwra.com> - 1.0.2-1
- Initial package
