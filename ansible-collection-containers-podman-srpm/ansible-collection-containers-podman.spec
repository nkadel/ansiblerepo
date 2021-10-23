%global collection_namespace containers
%global collection_name podman

Name:           ansible-collection-%{collection_namespace}-%{collection_name}
Version:        1.6.1
Release:        0.3%{?dist}
Summary:        Podman Ansible collection for Podman containers

License:        GPLv3+
URL:            %{ansible_collection_url}
Source:         https://github.com/containers/ansible-podman-collections/archive/%{version}.tar.gz

BuildRequires:  ansible-core >= 2.11.0
# Manually added
BuildRequires:  python%{python3_pkgversion}-jinja2
BuildRequires:  python%{python3_pkgversion}-yaml

BuildArch:      noarch

%description
%{summary}.

%prep
%autosetup -n ansible-podman-collections-%{version}
sed -i -e 's/version:.*/version: %{version}/' galaxy.yml
find -type f ! -executable -name '*.py' -print -exec sed -i -e '1{\@^#!.*@d}' '{}' +
rm -vr changelogs/ ci/ contrib/ tests/ ./galaxy.yml.in .github/ .gitignore

%build
%ansible_collection_build

%install
%ansible_collection_install

%files
%license COPYING
%doc README.md
%{ansible_collection_files}

%changelog
* Thu Oct 14 2021 Sagi Shnaidman <sshnaidm@redhat.com> - 1.6.1-3
- Use ansible or ansible-core as BuildRequires

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 08 2021 Sagi Shnaidman <sshnaidm@redhat.com> - 1.6.1-1
- Bump to 1.6.1-1

* Sun Feb 21 2021 Sagi Shnaidman <sshnaidm@redhat.com> - 1.4.1-2
- Resolving RPM issues

* Tue Feb 09 2021 Sagi Shnaidman <sshnaidm@redhat.com> - 1.4.1-1
- Initial package
