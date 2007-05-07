%define name            cryptsetup-luks
%define version         1.0.3
%define release         %mkrel 2
%define	major		0

%define __libtoolize	%{nil}

%define	_sbindir	/sbin
%define	libname		%mklibname cryptsetup %major
%define	dlibname	%mklibname cryptsetup %major -d

Name: %{name}
Version: %{version}
Release: %{release}
Summary: Utility for setting up encrypted filesystems
License: GPL
Group: System/Base
URL: http://clemens.endorphin.org/LUKS
Source0: %{name}-%{version}.tar.bz2
Source1: %{name}-%{version}.tar.bz2.asc
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: libgcrypt-devel >= 1.1.42
BuildRequires: libgpg-error-devel
BuildRequires: libdevmapper-devel
BuildRequires: libext2fs-devel
BuildRequires: libpopt-devel
BuildRequires: glibc-static-devel
Obsoletes: cryptsetup
Provides: cryptsetup

%description
LUKS is the upcoming standard for Linux hard disk encryption. 
By providing a standard on-disk-format, it does not only facilitate 
compatibility among distributions, but also provide secure management 
of multiple user passwords. In contrast to existing solution, LUKS stores 
all setup necessary setup information in the partition header, enabling 
the user to transport or migrate his data seamlessly.
LUKS for dm-crypt is implemented in cryptsetup. cryptsetup-luks is intended 
as a complete replacement for the original cryptsetup. It provides all the 
functionally of the original version plus all LUKS features, that are 
accessible by luks* action.

%package -n %libname
Summary: Library for setting up encrypted filesystems
Group: System/Libraries

%description -n %libname
LUKS is the upcoming standard for Linux hard disk encryption.
By providing a standard on-disk-format, it does not only facilitate
compatibility among distributions, but also provide secure management
of multiple user passwords. In contrast to existing solution, LUKS stores
all setup necessary setup information in the partition header, enabling
the user to transport or migrate his data seamlessly.

This package contains the shared libraries required for running
programs which use cryptsetup-luks.


%package -n %dlibname
Summary: Development library for setting up encrypted filesystems
Group: Development/C
Requires: libgcrypt-devel >= 1.1.42
Requires: libgpg-error-devel
Requires: libdevmapper-devel
Requires: libext2fs-devel
Requires: libpopt-devel

%description -n %dlibname
LUKS is the upcoming standard for Linux hard disk encryption.
By providing a standard on-disk-format, it does not only facilitate
compatibility among distributions, but also provide secure management
of multiple user passwords. In contrast to existing solution, LUKS stores
all setup necessary setup information in the partition header, enabling
the user to transport or migrate his data seamlessly.

This package contains the header files and development libraries
for building programs which use cryptsetup-luks.

%prep
%setup -q

%build
# static build for security reasons, and disable selinux
export ac_cv_lib_selinux_is_selinux_enabled=no
%configure2_5x --enable-static
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %libname -p /sbin/ldconfig

%postun -n %libname -p /sbin/ldconfig

%files -f %name.lang
%defattr(-,root,root)
%doc COPYING ChangeLog AUTHORS INSTALL NEWS README
%{_mandir}/man8/cryptsetup.8*
%{_sbindir}/cryptsetup

%files -n %dlibname
%{_includedir}/libcryptsetup.h
%{_libdir}/libcryptsetup.a
%{_libdir}/libcryptsetup.la
%{_libdir}/libcryptsetup.so

%files -n %libname
%exclude %{_libdir}/libcryptsetup.so.%{major}
%{_libdir}/libcryptsetup.so.%{major}.*


