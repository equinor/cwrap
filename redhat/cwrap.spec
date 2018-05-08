#
# spec file for package cwrap
#

Name:           cwrap
Version:        1.5.1
Release:        0
Summary:        Write python bindings for C libraries
License:        GPL-3+
Group:          Development/Libraries/C and C++
Url:            http://statoil.no
Source0:        https://github.com/Statoil/cwrap/archive/release/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires: python-devel numpy
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
python-cwrap is a package helping to write python bindings for C libraries

%package -n python-cwrap
Summary:        Simplify ctypes based wrapping of C code.
Group:          Python/Libraries
Requires:	python-six

%description -n python-cwrap
python-cwrap is a package helping to write python bindings for C libraries

%prep
%setup -q -n cwrap-%{version}

%build
python setup.py build

%install
python setup.py install --root=${RPM_BUILD_ROOT} --install-lib=/usr/lib64/python2.7/site-packages

%clean
rm -rf %{buildroot}

%files -n python-cwrap 
%defattr(-,root,root,-)
%{_libdir}/*
