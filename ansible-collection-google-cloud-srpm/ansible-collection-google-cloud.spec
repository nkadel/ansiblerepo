%global collection_namespace google
%global collection_name cloud

Name:           ansible-collection-%{collection_namespace}-%{collection_name}
Version:        1.0.1
Release:        0.5%{?dist}
Summary:        Google Cloud Platform collection

# roles/gcloud: MIT
License:        GPLv2+ and MIT
URL:            %{ansible_collection_url}
Source:         https://github.com/ansible-collections/google.cloud/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  ansible-core
BuildRequires:  python%{python3_pkgversion}-jinja2
BuildRequires:  python%{python3_pkgversion}-yaml

BuildArch:      noarch

%description
%{summary}.

%prep
%autosetup -n google.cloud-%{version} -p1
rm -vr molecule .github .ansible-lint .yamllint requirements.txt
find -type f ! -executable -name '*.py' -print -exec sed -i -e '1{\@^#!.*@d}' '{}' +
find -type f -name '.gitignore' -print -delete
find roles -mindepth 2 -type d -name 'molecule' -exec rm -vr '{}' +

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
%license LICENSE
%doc README.md
%{ansible_collection_files}

%changelog
* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 2021 Kevin Fenzi <kevin@scrye.com> - 1.0.1-3
- Rebuild against new ansible-generator and allow to be used by ansible-base-2.10.x

* Wed Dec 30 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.0.1-2
- Drop runtime dependencies

* Tue Dec 29 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Sun Aug 09 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.10.3-1
- Initial package
