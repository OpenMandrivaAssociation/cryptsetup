%define name            cryptsetup
%define version         1.0.6
%define release         %mkrel 1
%define	major		0
%define	libname		%mklibname cryptsetup %major
%define	dlibname	%mklibname cryptsetup -d

Name: %{name}
Version: %{version}
Release: %{release}
Summary: Utility for setting up encrypted filesystems
License: GPL
Group: System/Base
URL: http://luks.endorphin.org/
Source0: http://luks.endorphin.org/source/%{name}-%{version}.tar.bz2
Source1: http://luks.endorphin.org/source/%{name}-%{version}.tar.bz2.asc
# https://bugs.launchpad.net/ubuntu/+source/udev/+bug/132373
Patch1: cryptsetup-1.0.5-udevsettle.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: libgcrypt-devel >= 1.1.42
BuildRequires: libgpg-error-devel
BuildRequires: libdevmapper-devel
BuildRequires: libext2fs-devel
BuildRequires: libpopt-devel
BuildRequires: glibc-static-devel
Obsoletes: cryptsetup-luks < 1.0.5
Provides: cryptsetup-luks = %{version}-%{release}

%description
LUKS is the upcoming standard for Linux hard disk encryption. 
By providing a standard on-disk-format, it does not only facilitate 
compatibility among distributions, but also provide secure management 
of multiple user passwords. In contrast to existing solution, LUKS stores 
all setup necessary setup information in the partition header, enabling 
the user to transport or migrate his data seamlessly.
LUKS for dm-crypt is implemented in cryptsetup. cryptsetup-luks is
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
Obsoletes: %mklibname -d cryptsetup 0

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
%patch1 -p1 -b .udevsettle

%build
# static build for security reasons, and disable selinux
export ac_cv_lib_selinux_is_selinux_enabled=no
autoconf
%configure2_5x --enable-static --sbindir=/sbin --libdir=/%{_lib}
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# move libcryptsetup.so to %{_libdir}
pushd $RPM_BUILD_ROOT/%{_lib}
rm libcryptsetup.so
mkdir -p $RPM_BUILD_ROOT/%{_libdir}
ln -s ../../%{_lib}/$(ls libcryptsetup.so.?.?.?) $RPM_BUILD_ROOT/%{_libdir}/libcryptsetup.so
mv *.{a,la} %buildroot%_libdir
popd

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %libname -p /sbin/ldconfig

%postun -n %libname -p /sbin/ldconfig

%files -f %name.lang
%defattr(-,root,root)
%doc COPYING ChangeLog AUTHORS INSTALL NEWS README
%{_mandir}/man8/cryptsetup.8*
/sbin/cryptsetup

%files -n %dlibname
%{_includedir}/libcryptsetup.h
%{_libdir}/libcryptsetup.a
%{_libdir}/libcryptsetup.la
%{_libdir}/libcryptsetup.so

%files -n %libname
/%{_lib}/libcryptsetup.so.%{major}*
