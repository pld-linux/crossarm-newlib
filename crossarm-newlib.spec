Summary:	A C library intended for use on embedded systems
Summary(pl.UTF-8):	Biblioteka C przeznaczona dla systemów wbudowanych
Name:		crossarm-newlib
Version:	1.12.0
Release:	1
License:	several free software licenses
Group:		Libraries
Source0:	ftp://sources.redhat.com/pub/newlib/newlib-%{version}.tar.gz
# Source0-md5:	c3f1fbb52a4864cf8356c124584bae72
Patch0:		%{name}-configure.patch
URL:		http://sources.redhat.com/newlib/
BuildRequires:	crossarm-gcc
Requires:	crossarm-binutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		arm-pld-linux
%define		arch		%{_prefix}/%{target}
%define		_noautostrip	.*/lib.*\\.a

%description
Newlib is a C library intended for use on embedded systems. It is a
conglomeration of several library parts, all under free software
licenses that make them easily usable on embedded products.

%description -l pl.UTF-8
Newlib to biblioteka C przeznaczona dla systemów wbudowanych. Jest to
połączenie różnych części biblioteki, wszystkich na wolnych
licencjach, co czyni je łatwo używalnymi w produktach wbudowanych.

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

%{__make} \
	CFLAGS_FOR_TARGET="-mthumb -mthumb-interwork"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install-target-newlib \
	CFLAGS_FOR_TARGET="-mthumb -mthumb-interwork" \
	DESTDIR=$RPM_BUILD_ROOT

%{target}-strip -g $RPM_BUILD_ROOT%{arch}/lib/libc.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING* ChangeLog README
%{arch}/include
%{arch}/lib/libc.a
