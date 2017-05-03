# This package is part of the Python 3 bootstrapping sequence.
#
# The python3-devel subpackage has a runtime dependency on this package.
# Therefore it needs to be built before Python 3 itself. To facilitate this,
# this package has a bootstrapping mode—triggered by the macro below—that skips
# bytecompilation and therefore no Python is actually needed for building of
# this package. After Python 3 is built, this package can be rebuilt in
# normal mode again.
#
# Note, however, that even the bootstrapping version of this package is fully
# functional as Python will simply bytecompile the Python files when they are
# run. There will be a warning that the bytecompiled file cannot be saved
# (unless Python is run with root privileges), but the script will work.
#
# More info on the Python 3 bootstrapping sequence in the `python3` spec file.
#
%global bootstrapping_python 0


# When bootstrapping Python, disable automatic bytecompilation
# in %%__os_install_post.
%if 0%{?bootstrapping_python}
%undefine py_auto_byte_compile
%endif

%global srcname rpm

# These macros are copied from the `rpm` package so it's trivial to keep
# the two packages on the same upstream version.
%global rpmver 4.13.0.1
#global snapver rc2
%global srcver %{version}%{?snapver:-%{snapver}}
%global srcdir %{?snapver:testing}%{!?snapver:rpm-%(echo %{version} | cut -d'.' -f1-2).x}

Name:           python-rpm-generators
Summary:        The Python RPM dependency and provides generators
Version:        %{rpmver}
Release:        %{?snapver:0.%{snapver}.}1%{?dist}
License:        GPLv2+
Url:            http://www.rpm.org/
Source0:        http://ftp.rpm.org/releases/%{srcdir}/%{srcname}-%{srcver}.tar.bz2

BuildArch:      noarch

%if 0%{?bootstrapping_python} == 0
BuildRequires:  python3-devel
%endif

# Patches already upstream:
Patch0: rpm-4.13.x-pythondistdeps.patch
Patch1: rpm-4.13.x-pythondistdeps-Makefile.patch
Patch2: rpm-4.13.x-pythondistdeps-fileattr.patch
Patch3: rpm-4.13.x-pythondistdeps.py-skip-distribution-metadata-if-ther.patch
Patch4: rpm-4.13.x-pythondistdeps.py-show-warning-if-version-is-not-fou.patch
Patch5: rpm-4.13.x-pythondistdeps.py-skip-.egg-link-files.patch
Patch6: rpm-4.13.x-pythondistdeps.py-add-forgotten-import.patch
Patch7: rpm-4.13.x-pythondistdeps.py-fix-processing-wheels.patch
# Switch the shebang of pythondistdeps.py to Python 3
# Upstream PR: https://github.com/rpm-software-management/rpm/pull/212
Patch8: rpm-4.13.x-pythondistdeps-python3.patch

%description
This package provides scripts that analyse Python binary RPM packages
and add appropriate Provides and Requires tags to them.


%package -n     python3-rpm-generators
Summary:        %{summary}
Requires:       python3-setuptools

%description -n python3-rpm-generators
This package provides scripts that analyse Python binary RPM packages
and add appropriate Provides and Requires tags to them.


%prep
%autosetup -n %{srcname}-%{srcver} -p1


%build
%if 0%{?bootstrapping_python} == 0
%{__python3} -m compileall scripts/
%endif


%install
install -Dm 644 fileattrs/python.attr -t %{buildroot}/%{_fileattrsdir}
install -Dm 755 scripts/pythondeps.sh \
                scripts/pythondistdeps.py \
                -t %{buildroot}/%{_rpmconfigdir}

%if 0%{?bootstrapping_python} == 0
install -Dm 755 scripts/__pycache__/* \
                -t %{buildroot}/%{_rpmconfigdir}/__pycache__
%endif


%files -n python3-rpm-generators
%{_fileattrsdir}/python.attr
%{_rpmconfigdir}/pythondeps.sh
%{_rpmconfigdir}/pythondistdeps.py

%if 0%{?bootstrapping_python} == 0
%{_rpmconfigdir}/__pycache__/*
%endif


%changelog
* Tue May 02 2017 Tomas Orsava <torsava@redhat.com> - 4.13.0.1-1
- Splitting Python RPM generators from the `rpm` package to standalone one
