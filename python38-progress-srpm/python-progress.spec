# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8}
%global python3_version 3.8
%global python3_pkgversion 38
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

%bcond_without python3
%bcond_with    python2

# Created by pyp2rpm-0.5.2
%global pypi_name progress

Name:           python-%{pypi_name}
Version:        1.6
#Release:        4%%{?dist}
Release:        0.4%{?dist}
Summary:        Easy to use progress bars

License:        ISC
URL:            http://github.com/verigak/progress/
Source0:        %pypi_source
BuildArch:      noarch

%if %{with python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif

%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif

Patch1:         0001-fixup-moving-average-window.patch

%global _description\
Collection of easy to use progress bars and spinners.\


%description %_description


%if 0%{with python2}
%package -n python2-%{pypi_name}
Summary: %summary
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name} %_description
%endif # python2


%if 0%{with python3}
%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        Easy to use progress bars

%description -n python%{python3_pkgversion}-%{pypi_name}
Collection of easy to use progress bars and spinners.
%endif # python3


%prep
%autosetup -p1 -n %{pypi_name}-%{version}

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info


%build
%{?with_python2: %py2_build}
%{?with_python3: %py3_build}


%install
%{?with_python2: %py2_install}
%{?with_python3: %py3_install}


%if 0%{with python2}
%files -n python2-%{pypi_name}
%doc README.rst LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%if 0%{with python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.rst LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info
%endif


%changelog
* Sat Jul 02 2022 Pavel Raiskup <praiskup@redhat.com> - 1.6-4
- fix for very frequent next() call, rhbz#2103093

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.6-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.5-9
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.5-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.5-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.5-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 18 2019 Pavel Raiskup <praiskup@redhat.com> - 1.5-1
- the latest upstream release

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 11 2018 Pavel Raiskup <praiskup@redhat.com> - 1.4-2
- followup for previous commit, PR#3

* Wed Dec 05 2018 Gwyn Ciesla <limburgher@gmail.com> - 1.4-1
- 1.4

* Wed Oct 03 2018 Pavel Raiskup <praiskup@redhat.com> - 1.2-19
- no python2 in f30+ (rhbz#1634951)
- fix el6 build (rhbz#1310704)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2-17
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.2-15
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2-14
- Python 2 binary package renamed to python2-progress
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.2-11
- Rebuild for Python 3.6

* Thu Dec 08 2016 Pavel Raiskup <praiskup@redhat.com> - 1.2-10
- keep enabled python3 subpackage only in fedora, and merge into epel7

* Tue Nov 01 2016 Pavel Raiskup <praiskup@redhat.com> - 1.2-9
- fix avg counter for copr-cli (rhbz#1299634)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-8
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Feb 18 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2-2
- Add missing BR: python{,3}-setuptools

* Tue Feb 18 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2-1
- Initial package.
