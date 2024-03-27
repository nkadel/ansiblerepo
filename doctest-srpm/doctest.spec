## START: Set by rpmautospec
## (rpmautospec version 0.3.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 4;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%undefine __cmake3_in_source_build
%global debug_package %{nil}

Name: doctest
Version: 2.4.11
Release: %autorelease
Summary: Feature-rich header-only C++ testing framework
License: MIT
URL: https://github.com/doctest/%{name}
Source0: %{url}/archive/refs/tags/v%{version}.tar.gz
# https://github.com/doctest/doctest/pull/699
#Patch100: %{name}-pointers-compare-fix.patch

BuildRequires: gcc-c++
BuildRequires: cmake3
BuildRequires: git

%description
A fast (both in compile times and runtime) C++ testing framework, with the
ability to write tests directly along production source (or in their own
source, if you prefer).

%package devel
Summary: Development files for %{name}
Provides: %{name}-static = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: libstdc++-devel%{?_isa}

%description devel
%{summary}.

%prep
%autosetup -p1

%build
%cmake3 \
  -DCMAKE_BUILD_TYPE=Release \
  -DDOCTEST_WITH_MAIN_IN_STATIC_LIB:BOOL=OFF \
  -DDOCTEST_WITH_TESTS:BOOL=ON \
  %{nil}
%cmake3_build

%check
%ctest3

%install
%cmake3_install

%files devel
%doc README.md CHANGELOG.md CONTRIBUTING.md
%license LICENSE.txt
%{_includedir}/%{name}/
%{_libdir}/cmake/%{name}/

%changelog
* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 03 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 2.4.9-2
- Backported upstream patch with pointer compare fixes.

* Mon Sep 12 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 2.4.9-1
- Updated to version 2.4.9.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Nick Black <dankamongmen@gmail.com> - 2.4.8-1
- new upstream 2.4.8

* Fri Dec 10 2021 Nick Black <dankamongmen@gmail.com> - 2.4.7-2
- RPMAUTOSPEC: unresolvable merge
