## START: Set by rpmautospec
## (rpmautospec version 0.3.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

Name:           xsimd
Version:        11.1.0
Release:        %autorelease
Summary:        C++ wrappers for SIMD intrinsics
License:        BSD-3-Clause
URL:            https://xsimd.readthedocs.io/
%global github  https://github.com/xtensor-stack/xsimd
Source:         %{github}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  doctest-devel >= 2.4.9

# there is no actual arched content - this is a header only library
%global debug_package %{nil}

%global _description \
SIMD (Single Instruction, Multiple Data) is a feature of microprocessors that \
has been available for many years. SIMD instructions perform a single operation \
on a batch of values at once, and thus provide a way to significantly \
accelerate code execution. However, these instructions differ between \
microprocessor vendors and compilers. \
 \
xsimd provides a unified means for using these features for library authors. \
Namely, it enables manipulation of batches of numbers with the same arithmetic \
operators as for single values. It also provides accelerated implementation \
of common mathematical functions operating on batches. \

%description %_description

%package devel
Summary:        %{summary}
Provides:       %{name} = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}

%description devel %_description

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTS=ON
%cmake_build

%install
%cmake_install

%check
# Explicitly not supported upstream for simd mode. Still valuable for scalar mode layer.
%ifnarch ppc64le s390x
%cmake_build -- xtest
%endif

%files devel
%doc README.md
%license LICENSE
%{_includedir}/%{name}/
%{_libdir}/cmake/%{name}/
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 11.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 24 2023 sergesanspaille <sguelton@redhat.com> - 11.1.0-1
- Update to 11.1.0
- Fixes: rhbz#2207683

* Fri Apr 07 2023 Miro Hrončok <miro@hroncok.cz> - 11.0.0-2
- Update the License tag to SPDX

* Fri Apr 07 2023 Miro Hrončok <miro@hroncok.cz> - 11.0.0-1
- Update to 11.0.0
- Fixes: rhbz#2185154

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 2 2022 sguelton@redhat.com - 10.0.0-1
- Update to 10.0.0

* Tue Aug 30 2022 sguelton@redhat.com - 9.0.1-1
- Update to 9.0.1
- Fixes: rhbz#2120851

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 11 2022 sguelton@redhat.com - 8.1.0-1
- Update to 8.1.0

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 08 2021 Miro Hrončok <mhroncok@redhat.com> - 8.0.5-1
- Update to 8.0.5
- Fixes rhbz#1997274

* Wed Dec 08 2021 Miro Hrončok <mhroncok@redhat.com> - 8.0.4-1
- Update to 8.0.4

* Mon Aug 09 2021 Miro Hrončok <mhroncok@redhat.com> - 7.6.0-1
- Update to 7.6.0
- Fixes rhbz#1988647

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Apr 23 2021 sguelton@redhat.com - 7.5.0-1
- Update to latest version

* Tue Apr 6 2021 sguelton@redhat.com - 7.4.10-1
- Update to latest version

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 26 2020 sguelton@redhat.com - 7.4.9-1
- Update to latest version

* Sat Oct 17 2020 sguelton@redhat.com - 7.4.8-2
- Fix missing #include for gcc-11

* Sat Oct 3 2020 sguelton@redhat.com - 7.4.8-1
- Update to latest version

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 16 2020 sguelton@redhat.com - 7.4.6-1
- Update to latest version

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 04 2019 Miro Hrončok <mhroncok@redhat.com> - 7.2.3-3
- Allow all architectures

* Wed Jul 03 2019 Miro Hrončok <mhroncok@redhat.com> - 7.2.3-2
- Apply upstream workaround for armv7
- Reenable tests (commented out by mistake)

* Fri Jun 28 2019 Miro Hrončok <mhroncok@redhat.com> - 7.2.3-1
- Initial package

