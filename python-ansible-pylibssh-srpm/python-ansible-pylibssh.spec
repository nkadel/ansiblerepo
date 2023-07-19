# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.11
%global python3_pkgversion 3.11
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

#
Name:           python-ansible-pylibssh
Version:        1.1.0
Release:        %autorelease
Summary:        Python bindings for libssh client specific to Ansible use case

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
License:        LGPL2+
URL:            https://github.com/ansible/pylibssh
Source:         %{pypi_source ansible-pylibssh}

BuildArch:      noarch
BuildRequires:  python%{python3_pkgversion}-devel


# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'ansible-pylibssh' generated automatically by pyp2spec.}


%description %_description

%package -n     python%{python3_pkgversion}-ansible-pylibssh
Summary:        %{summary}

%description -n python%{python3_pkgversion}-ansible-pylibssh %_description


%prep
%autosetup -p1 -n ansible-pylibssh-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
# For official Fedora packages, including files with '*' +auto is not allowed
# Replace it with a list of relevant Python modules/globs and list extra files in %%files
%pyproject_save_files '*' +auto


%check
%pyproject_check_import


%files -n python%{python3_pkgversion}-ansible-pylibssh -f %{pyproject_files}


%changelog
%autochangelog
