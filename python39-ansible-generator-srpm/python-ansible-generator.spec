# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8}
%global python3_version 3.9
%global python3_pkgversion 39
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

%global pypi_name ansible-generator
%global pypi_modulename ansible_generator
%global pypi_version 2.1.4

Name: python-%{pypi_name}
Version: %{pypi_version}
Release: 0.1
Summary: simplify creating a new ansible playbook
License: Apache
URL:     https://github.com/kkirsche/ansible-generator

Source: https://github.com/kkirsche/ansible-generator/archive/refs/tags/v2.1.4.zip

BuildArch: noarch

%description
Ansible Generator is a python program designed to simplify creating a
new ansible playbook by creating the necessary directory structure for
the user based on ansible's best practices, as outlined in content
organization best practices.

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        The new features in unittest backported to Python 2.4+
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description -n python%{python3_pkgversion}-%{pypi_name}
Ansible Generator is a python program designed to simplify creating a
new ansible playbook by creating the necessary directory structure for
the user based on ansible's best practices, as outlined in content
organization best practices.

%prep
%autosetup -n %{pypi_name}-%{pypi_version}

%build
%{py3_build}

%{py3_install}
mv %{buildroot}%{_bindir}/ansible-generate %{buildroot}%{_bindir}/ansible-generate-%{python3_version}
ln -s ansible-generate-%{python3_version} %{buildroot}%{_bindir}/ansible-generate

%files -n     python%{python3_pkgversion}-%{pypi_name}
%license LICENSE.txt
%doc README.md
%{python3_sitelib}/%{pypi_modulename}
%{python3_sitelib}/%{pypi_modulename}-%{version}-py%{python3_version}.egg-info
%{_bindir}/ansible-generate
%{_bindir}/ansible-generate-%{python3_version}

%changelog
