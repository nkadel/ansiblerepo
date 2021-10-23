%global pypi_name lark-parser

Name:           python-%{pypi_name}
Version:        0.7.1
#Release:        1%%{?dist}
Release:        0.1%{?dist}
Summary:        Lark is a modern general-purpose parsing library for Python
License:        MIT
Group:          Development/Languages/Python
Url:            https://github.com/lark-parser/lark
Source:         https://files.pythonhosted.org/packages/source/l/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildRequires:  fdupes
BuildArch:      noarch

%description
Lark is a modern general-purpose parsing library for Python.

Lark focuses on simplicity and power. It lets you choose between
two parsing algorithms:

Earley : Parses all context-free grammars (even ambiguous ones)!
It is the default.

LALR(1): Only LR grammars. Outperforms PLY and most if not all
other pure-python parsing libraries.

Both algorithms are written in Python and can be used interchangeably
with the same grammar (aside for algorithmic restrictions).
See "Comparison to other parsers" for more details.

Lark can auto magically build an AST from your grammar, without any
more code on your part.

Features:

- EBNF grammar with a little extra
- Earley & LALR(1)
- Builds an AST auto magically based on the grammar
- Automatic line & column tracking
- Automatic token collision resolution (unless both tokens are regexps)
- Python 2 & 3 compatible
- Unicode fully supported

%package -n python2-%{pypi_name}
Summary:        Lark is a modern general-purpose parsing library for Python
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
Lark is a modern general-purpose parsing library for Python.

Lark focuses on simplicity and power. It lets you choose between
two parsing algorithms:

Earley : Parses all context-free grammars (even ambiguous ones)!
It is the default.

LALR(1): Only LR grammars. Outperforms PLY and most if not all
other pure-python parsing libraries.

Both algorithms are written in Python and can be used interchangeably
with the same grammar (aside for algorithmic restrictions).
See "Comparison to other parsers" for more details.

Lark can auto magically build an AST from your grammar, without any
more code on your part.

Features:

- EBNF grammar with a little extra
- Earley & LALR(1)
- Builds an AST auto magically based on the grammar
- Automatic line & column tracking
- Automatic token collision resolution (unless both tokens are regexps)
- Python 2 & 3 compatible
- Unicode fully supported

%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:        Lark is a modern general-purpose parsing library for Python
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
Lark is a modern general-purpose parsing library for Python.

Lark focuses on simplicity and power. It lets you choose between
two parsing algorithms:

Earley : Parses all context-free grammars (even ambiguous ones)!
It is the default.

LALR(1): Only LR grammars. Outperforms PLY and most if not all
other pure-python parsing libraries.

Both algorithms are written in Python and can be used interchangeably
with the same grammar (aside for algorithmic restrictions).
See "Comparison to other parsers" for more details.

Lark can auto magically build an AST from your grammar, without any
more code on your part.

Features:

- EBNF grammar with a little extra
- Earley & LALR(1)
- Builds an AST auto magically based on the grammar
- Automatic line & column tracking
- Automatic token collision resolution (unless both tokens are regexps)
- Python 2 & 3 compatible
- Unicode fully supported

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

%files -n python2-%{pypi_name}
%license LICENSE
%doc README.md examples
%{python2_sitelib}/lark_parser-*.egg-info
%{python2_sitelib}/lark/

%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE
%doc README.md examples
%{python3_sitelib}/lark_parser-*.egg-info
%{python3_sitelib}/lark/

%changelog
* Thu Sep 16 2021 Nico Kadel-Garcia <nico.kadel-garcia@gmail.com>
- Simplify Requires statements for python2- compatibility

* Mon May 20 2019 Scott K Logan <logans@cottsay.net> - 0.7.1-1
- Update to 0.7.1

* Fri Mar 08 2019 Troy Dawson <tdawson@redhat.com> - 0.6.4-6
- Rebuilt to change main python from 3.4 to 3.6

* Wed Jan 23 2019 Scott K Logan <logans@cottsay.net> - 0.6.4-5
- Add Python 3.6 package for EPEL 7

* Fri Jan 11 2019 Thomas Andrejak <thomas.andrejak@gmail.com> - 0.6.4-4
- Re-fix the packages names

* Wed Oct 24 2018 Thomas Andrejak <thomas.andrejak@gmail.com> - 0.6.4-3
- Fix python 2 and 3 packages name

* Thu Oct 18 2018 Thomas Andrejak <thomas.andrejak@gmail.com> - 0.6.4-2
- Add python2 support

* Mon Sep 24 2018 Thomas Andrejak <thomas.andrejak@gmail.com> - 0.6.4-1
- Initial package
