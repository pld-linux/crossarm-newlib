Summary:	A C library intended for use on embedded systems
Name:		crossarm-newlib
Version:	1.12.0
Release:	0.1
License:	several free software licenses
Group:		Libraries
Source0:	ftp://sources.redhat.com/pub/newlib/newlib-%{version}.tar.gz
# Source0-md5:	c3f1fbb52a4864cf8356c124584bae72
Patch0:		%{name}-configure.patch
URL:		http://sources.redhat.com/newlib/
BuildRequires:	crossarm-gcc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		arm-pld-linux
%define		arch		%{_prefix}/%{target}
%define		_noautostrip	.*/lib.*\\.a

%description
Newlib is a C library intended for use on embedded systems. It is a
conglomeration of several library parts, all under free software
licenses that make them easily usable on embedded products.

%prep
%setup -q -n newlib-%{version}
%patch0 -p1

%build
rm -rf build && mkdir build && cd build
../configure \
	--prefix=%{_prefix} \
	--disable-shared \
	--enable-static \
	--enable-multilib \
	--enable-target-optspace \
	--disable-newlib-iconv \
	--disable-newlib-multithread \
	--disable-newlib-io-float \
	--disable-newlib-hw-fp \
	--disable-newlib-supplied-syscalls \
	--target=%{target}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
#install -d $RPM_BUILD_ROOT

cd build
%{__make} install-target-newlib \
	DESTDIR=$RPM_BUILD_ROOT

%{target}-strip -g $RPM_BUILD_ROOT%{arch}/lib/libc.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING* ChangeLog README
%{arch}/include
%{arch}/lib/libc.a
