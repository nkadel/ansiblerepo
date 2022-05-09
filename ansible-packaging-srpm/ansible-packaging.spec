Name:           ansible-packaging
Version:        1
#Release:        3%%{?dist}
Release:        0.3%{?dist}
Summary:        RPM packaging macros and generators for Ansible collections

License:        GPLv3+

Source0:        ansible-generator
Source1:        ansible.attr
Source2:        macros.ansible
Source3:        COPYING

# Packages which ormerly required ansible-core now require ansible-packagingg
# Add Requires ansible-packaging to ansible-core instead
#Requires:       ansible-core

# More logical name this rpm
Provides:       ansible-rpm-macros = %{version}-%{release}

# Conflict with anything providing its own copies of these files
#Conflicts:      ansible-core < 2.12.1-3
Conflicts:      ansible-core < 2.11.0
Conflicts:      ansible-base < 2.11.0
Conflicts:      ansible <= 2.9.99

BuildArch:      noarch

%description
%{summary}.

%prep
%autosetup -T -c
cp -a %{sources} .

%build
# Nothing to build

%install
install -Dpm0644 -t %{buildroot}%{_fileattrsdir} ansible.attr
install -Dpm0644 -t %{buildroot}%{_rpmmacrodir} macros.ansible
install -Dpm0755 -t %{buildroot}%{_rpmconfigdir} ansible-generator

%files
%license COPYING
%{_fileattrsdir}/ansible.attr
%{_rpmmacrodir}/macros.ansible
%{_rpmconfigdir}/ansible-generator

%changelog
* Sun May 8 2022 Nico Kadel-Garcia <nkadel@gmai.com> - 1-0.3
- Permit RHEL 7 installation with ansible-core 2.11

* Mon Jan 31 2022 Neal Gompa <ngompa@fedoraproject.org> - 1-3
- Drop vestigial support for the legacy ansible package
- Make compatibile with RHEL 8.6+

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Neal Gompa <ngompa@fedoraproject.org> - 1-1
- Initial packaging split out of ansible-core (#2038591)
