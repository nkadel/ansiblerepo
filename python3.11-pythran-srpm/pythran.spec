# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.11
%global python3_pkgversion 3.11
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

Name:           pythran
Version:        0.13.1
Release:        2%{?dist}
Summary:        Ahead of Time Python compiler for numeric kernels

# pythran is BSD
# pythran/graph.py has bits of networkx, also BSD
# pythran/pythonic/patch/complex is MIT or NCSA
License:        BSD and (MIT or NCSA)

# see pythran/pythonic/patch/README.rst
# The version is probably somewhat around 3
Provides:       bundled(libcxx) = 3

# see pythran/graph.py
# Only bundles one function from networkx
Provides:       bundled(python3dist(networkx)) = 2.6.1


%py_provides    python%{python3_pkgversion}-%{name}

URL:            https://github.com/serge-sans-paille/pythran
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

# assertEquals was removed from unittest in Python 3.12
Patch:          https://github.com/serge-sans-paille/pythran/pull/2119.patch

# Introduce pythran/pythonic/include/types/longdouble.hpp et cie
# New numpy version alias np.float128 to np.longdouble, so we need these headers too.
Patch1:          https://github.com/serge-sans-paille/pythran/pull/2120.patch

# Use pythran logger instead of default logger to report absence of spec
# Fixes build with setuptools distutils
Patch2:          https://github.com/serge-sans-paille/pythran/pull/2122.patch

# there is no actual arched content
# yet we want to test on all architectures
# and we also might need to skip some
%global debug_package %{nil}

BuildRequires: make
BuildRequires:  boost-devel
BuildRequires:  flexiblas-devel
BuildRequires:  gcc-c++
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  xsimd-devel >= 8

BuildRequires:	python%{python3_pkgversion}dist(beniget) >= 0.4
BuildRequires: 	python%{python3_pkgversion}dist(gast) >= 0.5

# For docs
# Avoid building the docs by default on RHEL not to drag pandoc into RHEL:
%bcond docs %{undefined rhel}
%if %{with docs}
BuildRequires:  pandoc
%endif

# For tests
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  /usr/bin/python
BuildRequires:  python%{python3_pkgversion}-scipy

# these packages are not included in RHEL
%if %{undefined rhel}
# this is used for supporting -n auto in %%pytest
BuildRequires:  python%{python3_pkgversion}-pytest-xdist
# this is only used to test integration with ipython
BuildRequires:  /usr/bin/ipython
%endif

# This is a package that compiles code, it runtime requires devel packages
Requires:       flexiblas-devel
Requires:       gcc-c++
Requires:       python%{python3_pkgversion}-devel
Requires:       boost-devel
Requires:       xsimd-devel >= 8

%description
Pythran is an ahead of time compiler for a subset of the Python language, with
a focus on scientific computing. It takes a Python module annotated with a few
interface description and turns it into a native Python module with the same
interface, but (hopefully) faster. It is meant to efficiently compile
scientific programs, and takes advantage of multi-cores and SIMD
instruction units.


%prep
%autosetup -p1 -n %{name}-%{version}
find -name '*.hpp' -exec chmod -x {} +
sed -i '1{/#!/d}' pythran/run.py

# Remove bundled header libs and use the ones from system
rm -r third_party/boost third_party/xsimd
cat >> setup.cfg << EOF
[build_py]
no_boost=True
no_xsimd=True
EOF

# Both OpenBLAS and FlexiBLAS are registered as "openblas" in numpy
sed -i 's|blas=blas|blas=openblas|' pythran/pythran-linux*.cfg
sed -i 's|libs=|libs=flexiblas|' pythran/pythran-linux*.cfg
sed -i 's|include_dirs=|include_dirs=/usr/include/flexiblas|' pythran/pythran-linux*.cfg

# not yet available in Fedora
sed -i '/guzzle_sphinx_theme/d' docs/conf.py docs/requirements.txt

# The tests have some cflags in them
# We need to adapt the flags to play nicely with other Fedora's flags
# E.g. fortify source implies at least -O1
sed -i -e 's/-O0/-O1/g' -e 's/-Werror/-w/g' pythran/tests/__init__.py


%generate_buildrequires
%pyproject_buildrequires %{?with_docs:-x doc}


%build
%pyproject_wheel

%if %{with docs}
PYTHONPATH=$PWD make -C docs html
rm -rf docs/_build/html/.{doctrees,buildinfo}
%endif


%install
%pyproject_install
%pyproject_save_files %{name} omp


%check
# https://bugzilla.redhat.com/show_bug.cgi?id=1747029#c12
k="not test_numpy_negative_binomial"
%ifarch %{arm}
# https://github.com/serge-sans-paille/pythran/pull/1946#issuecomment-992458379
k="$k and not test_interp_6c"
%endif
%ifarch aarch64
# the test is so flaky it makes the build fail almost all the time
k="$k and not test_interp_8"
%endif
%ifarch %{power64}
# https://github.com/serge-sans-paille/pythran/pull/1946#issuecomment-992460026
k="$k and not test_setup_bdist_install3"
%endif
%if %{defined rhel}
# this test needs ipython
k="$k and not test_loadext_and_run"
%endif
%pytest %{?!rhel:-n auto} -k "$k"


%files -f %{pyproject_files}
%license LICENSE
%doc README.rst
%if %{with docs}
%doc docs/_build/html
%endif
%{_bindir}/%{name}
%{_bindir}/%{name}-config


%changelog
* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Miro Hrončok <mhroncok@redhat.com> - 0.13.1-1
- Update to 0.13.1

* Mon Jul 03 2023 Python Maint <python-maint@redhat.com> - 0.12.1-4
- Rebuilt for Python 3.12

* Wed Jan 25 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.12.1-3
- Avoid ipython test dependency in RHEL builds

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan 15 2023 Serge Guelton <serge.guelton@telecom-bretagne.eu> - 0.12.1-1
- Update to 0.12.1

* Wed Sep 28 2022 Miro Hrončok <mhroncok@redhat.com> - 0.12.0-1
- Update to 0.12.0
- Fixes: rhbz#2130464

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 0.11.0-5
- Rebuilt for Python 3.11

* Tue Mar 15 2022 Miro Hrončok <mhroncok@redhat.com> - 0.11.0-4
- Add a workaround for setuptools 60+,
  use distutils from the standard library during the tests

* Mon Mar 14 2022 Serge Guelton - 0.11.0-3
- Fix gcc12 build
- Fixes: rhbz#2046923

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 14 2021 Miro Hrončok <mhroncok@redhat.com> - 0.11.0-1
- Update to 0.11.0
- Fixes: rhbz#2032254

* Fri Sep 17 2021 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-1
- Update to 0.10.0
- Fixes: rhbz#2003905

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12.post1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 14 2021 Miro Hrončok <mhroncok@redhat.com> - 0.9.12.post1-1
- Update to 0.9.12.post1
- Fixes: rhbz#1982196

* Wed Jul 14 2021 Miro Hrončok <mhroncok@redhat.com> - 0.9.12-1
- Update to 0.9.12
- Fixes: rhbz#1981981
- Fixes: rhbz#1927172

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.9.11-2
- Rebuilt for Python 3.10

* Sun May 23 2021 sguelton@redhat.com - 0.9.11-1
- Update to 0.9.11

* Sun May 9 2021 sguelton@redhat.com - 0.9.10-1
- Update to 0.9.10

* Wed Mar 31 2021 sguelton@redhat.com - 0.9.9-1
- Update to 0.9.9

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.8^post3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Serge Guelton - 0.9.8^post3-2
- Apply compatibility patch with numpy 1.20

* Sun Dec 13 2020 sguelton@redhat.com - 0.9.8^post3-1
- Update to 0.9.8post3
- No longer recommend SciPy

* Wed Sep 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0.9.7-1
- Update to 0.9.7
- Rebuilt for Python 3.9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager
- Fixes: rhbz#1818006
- Fixes: rhbz#1787813

* Fri Mar 13 2020 Miro Hrončok <mhroncok@redhat.com> - 0.9.5-2
- Fix tests with ipython 7.12+ (#1813075)

* Fri Jan 31 2020 Miro Hrončok <mhroncok@redhat.com> - 0.9.5-1
- Update to 0.9.5 (#1787813)

* Tue Dec 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.4post1-1
- Update to 0.9.4post1 (#1747029)

* Tue Aug 20 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.3-1
- Update to 0.9.3 (#1743187)
- Allow 32bit architectures

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.2-1
- Initial package
