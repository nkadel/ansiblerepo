# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.12
%global python3_pkgversion 3.12
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

%global pypi_name pep517

Name:           python-%{pypi_name}
Version:        0.12.0
Release:        2%{?dist}
Summary:        Wrappers to build Python packages using PEP 517 hooks

%bcond_without tests

# colorlog.py is "copied from Tornado", Apache licensed
License:        MIT and ASL 2.0
URL:            https://github.com/takluyver/pep517
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  pyproject-rpm-macros


%description
This package contains wrappers around the hooks of standard API
for systems which build Python packages, specified in PEP 517.


%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

# colorlog.py is "copied from Tornado", Apache licensed
Provides:       bundled(python3dist(tornado))

%description -n python%{python3_pkgversion}-%{pypi_name}
This package contains wrappers around the hooks of standard API
for systems which build Python packages, specified in PEP 517.


%prep
%autosetup -n %{pypi_name}-%{version}

# Don't run the linter as part of tests
sed -i '/--flake8$/d' pytest.ini
sed -i '/pytest-flake8/d' dev-requirements.txt

%generate_buildrequires
%pyproject_buildrequires %{?with_tests:-t}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{pypi_name}


%if %{with tests}
%check
# "test_meta" skipped as it creates a venv and tries
# to install to it from PyPI
%tox -- -- -v -k "not test_meta"
%endif


%files -n python%{python3_pkgversion}-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.rst


%changelog
* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Oct 26 2021 Lumír Balhar <lbalhar@redhat.com> - 0.12.0-1
- Update to 0.12.0
Resolves: rhbz#2014930

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 22 2021 Petr Viktorin <pviktori@redhat.com> - 0.11.0-1
- Update to version 0.11.0

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.10.0-2
- Rebuilt for Python 3.10

* Tue Mar 16 2021 Petr Viktorin <pviktori@redhat.com> - 0.10.0-1
- Update to version 0.10.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 13 2020 Petr Viktorin <pviktori@redhat.com> - 0.9.1-1
- Update to version 0.9.1

* Fri Oct 09 2020 Petr Viktorin <pviktori@redhat.com> - 0.8.2-1
- Update to version 0.8.2

* Mon Sep 21 2020 Miro Hrončok <mhroncok@redhat.com> - 0.7.0-6
- Use %%pyproject_buildrequires to bring in all the needed tools (like pip)
- Resolves rhbz#1880983

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.7.0-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 14 2019 Petr Viktorin <pviktori@redhat.com> - 0.7.0-2
- Don't pull in importlib_metadata & zipp backports for Python 3.8+

* Wed Oct 23 2019 Petr Viktorin <pviktori@redhat.com> - 0.7.0-1
- Update to version 0.7.0
- Change dependency from pytoml to toml

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 18 2019 Petr Viktorin <pviktori@redhat.com> - 0.5.0-1
- Initial package
