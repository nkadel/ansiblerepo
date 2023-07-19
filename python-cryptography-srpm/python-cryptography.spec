%bcond_without tests

%{!?python3_pkgversion:%global python3_pkgversion 3}

%global srcname cryptography

Name:           python-%{srcname}
Version:        37.0.2
#Release:        8%%{?dist}
Release:        0.8%{?dist}
Summary:        PyCA's cryptography library

# cryptography is dual licensed under the Apache-2.0 and BSD-3-Clause,
# as well as the Python Software Foundation license for the OS random
# engine derived by CPython.
License:        (Apache-2.0 OR BSD-3-Clause) AND PSF-2.0
URL:            https://cryptography.io/en/latest/
Source0:        https://github.com/pyca/cryptography/archive/%{version}/%{srcname}-%{version}.tar.gz
                # created by ./vendor_rust.py helper script
Source1:        cryptography-%{version}-vendor.tar.bz2
Source2:        conftest-skipper.py

# https://github.com/pyca/cryptography/pull/8230
Patch1:         CVE-2023-23931.patch

ExclusiveArch:  %{rust_arches}

BuildRequires:  openssl-devel
BuildRequires:  gcc
BuildRequires:  gnupg2
%if 0%{?fedora}
BuildRequires:  rust-packaging
%else
BuildRequires:  rust-toolset
%endif

BuildRequires:  python%{python3_pkgversion}-cffi >= 1.7
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-setuptools-rust >= 0.11.3
# Cargo.toml requires asn1 0.6, but package FTBFS with 0.6.1
BuildRequires:  rust-asn1-devel >= 0.6.4

%if %{with tests}
%if 0%{?fedora}
BuildRequires:  python%{python3_pkgversion}-hypothesis >= 1.11.4
BuildRequires:  python%{python3_pkgversion}-iso8601
BuildRequires:  python%{python3_pkgversion}-pretend
BuildRequires:  python%{python3_pkgversion}-pytest-xdist
%endif
BuildRequires:  python%{python3_pkgversion}-pytest >= 6.0
BuildRequires:  python%{python3_pkgversion}-pytest-benchmark
BuildRequires:  python%{python3_pkgversion}-pytest-subtests >= 0.3.2
BuildRequires:  python%{python3_pkgversion}-pytz
%endif

%description
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.

%package -n  python%{python3_pkgversion}-%{srcname}
Summary:        PyCA's cryptography library
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

Requires:       openssl-libs
%if 0%{?fedora} >= 35 || 0%{?rhel} >= 9
# Can be safely removed in Fedora 37
Obsoletes: python%{python3_pkgversion}-cryptography-vectors < 3.4.7
%endif

%description -n python%{python3_pkgversion}-%{srcname}
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%generate_buildrequires

%if 0%{?fedora}
# Fedora: use cargo macros to make use of RPMified crates
%cargo_prep
cd src/rust
rm -f Cargo.lock
%cargo_generate_buildrequires
cd ../..
%else
# RHEL: use vendored Rust crates
%cargo_prep -V 1
%endif

%build
%py3_build

%install
# Actually other *.c and *.h are appropriate
# see https://github.com/pyca/cryptography/issues/1463
find . -name .keep -print -delete
%py3_install

%check
%if %{with tests}
%if 0%{?rhel}
# skip hypothesis tests on RHEL
rm -rf tests/hypothesis
# append skipper to skip iso8601 and pretend tests
cat < %{SOURCE2} >> tests/conftest.py
%endif

%if 0%{?eln}
# enable SHA-1 signatures for RSA tests
# also see https://github.com/pyca/cryptography/pull/6931 and rhbz#2060343
export OPENSSL_ENABLE_SHA1_SIGNATURES=yes
%endif

# see https://github.com/pyca/cryptography/issues/4885 and
# see https://bugzilla.redhat.com/show_bug.cgi?id=1761194 for deselected tests
# see rhbz#2042413 for memleak. It's unstable under Python 3.11 and makes
# not much sense for downstream testing.
# see rhbz#2171661 for test_load_invalid_ec_key_from_pem: error:030000CD:digital envelope routines::keymgmt export failure
PYTHONPATH=${PWD}/vectors:%{buildroot}%{python3_sitearch} \
    %{__python3} -m pytest \
    -k "not (test_buffer_protocol_alternate_modes or test_dh_parameters_supported or test_load_ecdsa_no_named_curve or test_decrypt_invalid_decrypt or test_openssl_memleak or test_load_invalid_ec_key_from_pem)"
%endif

%files -n python%{python3_pkgversion}-%{srcname}
%doc README.rst docs
%license LICENSE LICENSE.APACHE LICENSE.BSD
%{python3_sitearch}/%{srcname}
%{python3_sitearch}/%{srcname}-%{version}-py*.egg-info

%changelog
* Wed Feb 22 2023 Christian Heimes <cheimes@redhat.com> - 37.0.2-8
- Fix CVE-2023-23931: Don't allow update_into to mutate immutable objects, resolves rhbz#2171820
- Fix FTBFS due to failing test_load_invalid_ec_key_from_pem and test_decrypt_invalid_decrypt, resolves rhbz#2171661

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 37.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 09 2022 Christian Heimes <cheimes@redhat.com> - 37.0.2-6
- Enable SHA1 signatures in test suite (ELN-only)

* Wed Aug 17 2022 Miro Hrončok <mhroncok@redhat.com> - 37.0.2-5
- Drop unused requirement of python3-six

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 37.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 37.0.2-3
- Rebuilt for Python 3.11

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 37.0.2-2
- Bootstrap for Python 3.11

* Thu May 05 2022 Christian Heimes <cheimes@redhat.com> - 37.0.2-1
- Update to 37.0.2, resolves rhbz#2078968

* Thu Jan 27 2022 Christian Heimes <cheimes@redhat.com> - 36.0.0-3
- Skip unstable memleak tests, resolves: RHBZ#2042413

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 36.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 22 2021 Christian Heimes <cheimes@redhat.com> - 36.0.0-1
- Update to 36.0.0, fixes RHBZ#2025347

* Thu Sep 30 2021 Christian Heimes <cheimes@redhat.com> - 35.0.0-2
- Require rust-asn1 >= 0.6.4

* Thu Sep 30 2021 Christian Heimes <cheimes@redhat.com> - 35.0-1
- Update to 35.0.0 (#2009117)

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 3.4.7-6
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 10 2021 Stephen Gallagher <sgallagh@redhat.com> - 3.4.7-4
- Don't conditionalize Source: directives

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 3.4.7-3
- Rebuilt for Python 3.10

* Tue May 11 2021 Christian Heimes <cheimes@redhat.com> - 3.4.7-2
- Fix compatibility issue with Python 3.10. Enums now use same
  representation as on Python 3.9. (#1952522)
- Backport OpenSSL 3.0.0 compatibility patches.

* Wed Apr 21 2021 Christian Heimes <cheimes@redhat.com> - 3.4.7-1
- Update to 3.4.7
- Remove dependency on python-cryptography-vectors package and use vectors
  directly from Github source tar ball. (#1952024)

* Wed Mar 03 2021 Christian Heimes <cheimes@redhat.com> - 3.4.6-1
- Update to 3.4.6 (#1927044)

* Mon Feb 15 2021 Christian Heimes <cheimes@redhat.com> - 3.4.5-1
- Update to 3.4.5 (#1927044)

* Fri Feb 12 2021 Christian Heimes <cheimes@redhat.com> - 3.4.4-3
- Skip iso8601 and pretend tests on RHEL

* Fri Feb 12 2021 Christian Heimes <cheimes@redhat.com> - 3.4.4-2
- Provide RHEL build infrastructure

* Wed Feb 10 2021 Christian Heimes <cheimes@redhat.com> - 3.4.4-1
- Update to 3.4.4 (#1927044)

* Mon Feb 08 2021 Christian Heimes <cheimes@redhat.com> - 3.4.2-1
- Update to 3.4.2 (#1926339)
- Package no longer depends on Rust (#1926181)

* Mon Feb 08 2021 Fabio Valentini <decathorpe@gmail.com> - 3.4.1-2
- Use dynamically generated BuildRequires for PyO3 Rust module.
- Drop unnecessary CARGO_NET_OFFLINE environment variable.

* Sun Feb 07 2021 Christian Heimes <cheimes@redhat.com> - 3.4.1-1
- Update to 3.4.1 (#1925953)

* Sun Feb 07 2021 Christian Heimes <cheimes@redhat.com> - 3.4-2
- Add missing abi3 and pytest dependencies

* Sun Feb 07 2021 Christian Heimes <cheimes@redhat.com> - 3.4-1
- Update to 3.4 (#1925953)
- Remove Python 2 support
- Remove unused python-idna dependency
- Add Rust support

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 10 2020 Christian Heimes <cheimes@redhat.com> - 3.3.1-1
- Update to 3.3.1 (#1905756)

* Wed Oct 28 2020 Christian Heimes <cheimes@redhat.com> - 3.2.1-1
- Update to 3.2.1 (#1892153)

* Mon Oct 26 2020 Christian Heimes <cheimes@redhat.com> - 3.2-1
- Update to 3.2 (#1891378)

* Mon Sep 07 2020 Christian Heimes <cheimes@redhat.com> - 3.1-1
- Update to 3.1 (#1872978)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Christian Heimes <cheimes@redhat.com> - 3.0-1
- Update to 3.0 (#185897)

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 2.9-3
- Rebuilt for Python 3.9

* Tue May 12 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 2.9-2
- add source file verification

* Fri Apr 03 2020 Christian Heimes <cheimes@redhat.com> - 2.9-1
- Update to 2.9 (#1820348)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Christian Heimes <cheimes@redhat.com> - 2.8-2
- cryptography 2.8+ no longer depends on python-asn1crypto

* Thu Oct 17 2019 Christian Heimes <cheimes@redhat.com> - 2.8-1
- Update to 2.8
- Resolves: rhbz#1762779

* Sun Oct 13 2019 Christian Heimes <cheimes@redhat.com> - 2.7-3
- Skip unit tests that fail with OpenSSL 1.1.1.d
- Resolves: rhbz#1761194
- Fix and simplify Python 3 packaging

* Sat Oct 12 2019 Christian Heimes <cheimes@redhat.com> - 2.7-2
- Drop Python 2 package
- Resolves: rhbz#1761081

* Tue Sep 03 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 2.7-1
- Update to 2.7 (#1715680).

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 2.6.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 28 2019 Christian Heimes <cheimes@redhat.com> - 2.6.1-1
- New upstream release 2.6.1, resolves RHBZ#1683691

* Wed Feb 13 2019 Alfredo Moralejo <amoralej@redhat.com> - 2.5-1
- Updated to 2.5.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 13 2018 Christian Heimes <cheimes@redhat.com> - 2.3-2
- Use TLSv1.2 in test as workaround for RHBZ#1615143

* Wed Jul 18 2018 Christian Heimes <cheimes@redhat.com> - 2.3-1
- New upstream release 2.3
- Fix AEAD tag truncation bug, RHBZ#1602752

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 2.2.1-2
- Rebuilt for Python 3.7

* Wed Mar 21 2018 Christian Heimes <cheimes@redhat.com> - 2.2.1-1
- New upstream release 2.2.1

* Sun Feb 18 2018 Christian Heimes <cheimes@redhat.com> - 2.1.4-1
- New upstream release 2.1.4

* Sun Feb 18 2018 Christian Heimes <cheimes@redhat.com> - 2.1.3-4
- Build requires gcc

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.1.3-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
