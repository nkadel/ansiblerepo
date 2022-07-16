# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8}
%global python3_version 3.8
%global python3_pkgversion 38
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

# Created by pyp2rpm-3.3.8
%global pypi_name invoke
%global pypi_version 1.7.1

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        0.1%{?dist}
Summary:        Pythonic task execution

License:        BSD
URL:            https://pyinvoke.org
Source0:        https://files.pythonhosted.org/packages/source/i/%{pypi_name}/%{pypi_name}-%{pypi_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description
 For a high level introduction, including example code, please see our main
project website <>_; or for detailed API docs, see the versioned API website

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        Pythonic task execution

Requires:       python%{python3_pkgversion}-setuptools
%description -n python%{python3_pkgversion}-%{pypi_name}
 For a high level introduction, including example code, please see our main
project website <>_; or for detailed API docs, see the versioned API website
<>_.

%package -n python-%{pypi_name}-doc
Summary:        invoke documentation
%description -n python-%{pypi_name}-doc
Documentation for invoke

%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{__python3} setup.py build

## generate html docs
#PYTHONPATH=${PWD} sphinx-build sites/docs html
## remove the sphinx-build leftovers
#rm -rf html/.{doctrees,buildinfo}

%install
# Must do the default python version install last because
# the scripts in /usr/bin are overwritten with every setup.py install.
%{__python3} setup.py install --skip-build --root %{buildroot}
rm -rf %{buildroot}%{_bindir}/*

%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%files -n python-%{pypi_name}-doc
#%doc html
%license LICENSE

%changelog
* Sat Jul 16 2022 Nico Kadel-Garcia <nkadel@gmail.com> - 1.7.1-1
- Initial package.
