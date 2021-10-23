# Created by pyp2rpm-3.3.7
%global pypi_name commentjson
%global pypi_version 0.9.0

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        0.1%{?dist}
Summary:        Add Python and JavaScript style comments in your JSON files

License:        None
URL:            https://github.com/vaidik/commentjson
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-lark-parser < 0.8
BuildRequires:  python%{python3_pkgversion}-lark-parser >= 0.7.1
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-six

%description
 commentjson commentjson (Comment JSON) is a Python package that helps you
create JSON files with Python and JavaScript style inline comments. Its API is
very similar to the Python standard library's json_ module... _json:
Installation pip install commentjsonBasic Usage .. code-block:: python >>>
import commentjson >>> json_string """{ ... "name": "Vaidik Kapoor", Person's
name ... "location":...

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

Requires:       python%{python3_pkgversion}-lark-parser < 0.8
Requires:       python%{python3_pkgversion}-lark-parser >= 0.7.1
%description -n python%{python3_pkgversion}-%{pypi_name}
 commentjson commentjson (Comment JSON) is a Python package that helps you
create JSON files with Python and JavaScript style inline comments. Its API is
very similar to the Python standard library's json_ module... _json:
Installation pip install commentjsonBasic Usage .. code-block:: python >>>
import commentjson >>> json_string """{ ... "name": "Vaidik Kapoor", Person's
name ... "location":...


%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
# Must do the default python version install last because
# the scripts in /usr/bin are overwritten with every setup.py install.
%py3_install

%check
echo "Skipping checks"
#%{__python3} setup.py test

%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE.rst
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Tue Aug 31 2021 Nico Kadel-Garcia - 0.9.0-0.1
- Initial package.
- Disable %%check untiol test.json can be ironed out
