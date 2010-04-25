%define name            cryptsetup
%define version         1.1.0
%define release         %mkrel 2
%define subver          %{nil}
%define major		1
%define libname		%mklibname cryptsetup %major
%define dlibname	%mklibname cryptsetup -d

%bcond_without compatible

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Utility for setting up encrypted filesystems
License:	GPLv2
Group:		System/Base
URL:		http://code.google.com/p/cryptsetup/
Source0:	http://cryptsetup.googlecode.com/files/%{name}-%{version}%{subver}.tar.bz2
Source1:	http://cryptsetup.googlecode.com/files/%{name}-%{version}%{subver}.tar.bz2.asc
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	libgcrypt-devel >= 1.1.42
BuildRequires:	libgpg-error-devel
BuildRequires:	libdevmapper-devel
BuildRequires:	libuuid-devel
BuildRequires:	libpopt-devel
BuildRequires:	glibc-static-devel
Obsoletes:	cryptsetup-luks < 1.0.5
Provides:	cryptsetup-luks = %{version}-%{release}

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

%package -n	%libname
Summary:	Library for setting up encrypted filesystems
Group:		System/Libraries

%description -n %libname
LUKS is the upcoming standard for Linux hard disk encryption.
By providing a standard on-disk-format, it does not only facilitate
compatibility among distributions, but also provide secure management
of multiple user passwords. In contrast to existing solution, LUKS stores
all setup necessary setup information in the partition header, enabling
the user to transport or migrate his data seamlessly.

This package contains the shared libraries required for running
programs which use cryptsetup-luks.


%package -n	%dlibname
Summary:	Development library for setting up encrypted filesystems
Group:		Development/C
Requires:	libgcrypt-devel >= 1.1.42
Requires:	libgpg-error-devel
Requires:	libdevmapper-devel
Requires:	libext2fs-devel
Requires:	libpopt-devel
Requires:	pkgconfig
Requires:	%libname = %{version}-%{release}
Obsoletes:	%mklibname -d cryptsetup 0

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
%setup -q -n %{name}-%{version}%{subver}

%build
# static build for security reasons, and disable selinux
%configure2_5x --disable-selinux --enable-static --sbindir=/sbin \
%if %{with compatible}
	--with-plain-mode=cbc-plain --with-luks1-keybits=128 \
%endif
# end of configure
%make

%install
rm -rf %{buildroot}
%makeinstall_std

# disabled since libgcrypt is under usr
# move shared libraries in /%{_lib}
# pushd %{buildroot}/%{_libdir}
# mkdir -p ../../%{_lib}
# mv lib*.so.* ../../%{_lib}
# ln -s -f ../../%{_lib}/libcryptsetup.so.%{major}.* libcryptsetup.so
# popd

%find_lang %{name}

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig
%endif

%files -f %name.lang
%defattr(-,root,root)
%doc ChangeLog AUTHORS INSTALL NEWS README TODO
%{_mandir}/man8/cryptsetup.8*
/sbin/cryptsetup

%files -n %dlibname
%{_includedir}/libcryptsetup.h
%{_libdir}/libcryptsetup.a
%{_libdir}/libcryptsetup.la
%{_libdir}/libcryptsetup.so
%{_libdir}/pkgconfig/libcryptsetup.pc

%files -n %libname
/%{_libdir}/libcryptsetup.so.%{major}*
