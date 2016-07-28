%define major 4
%define libname %mklibname cryptsetup %{major}
%define devname %mklibname cryptsetup -d

%define _disable_rebuild_configure 1
%bcond_with compatible
%bcond_with static

Summary:	Utility for setting up encrypted filesystems
Name:		cryptsetup
Version:	1.7.2
Release:	2
License:	GPLv2
Group:		System/Base
Url:		https://gitlab.com/cryptsetup/cryptsetup
Source0:	https://www.kernel.org/pub/linux/utils/%{name}/v1.6/%{name}-%{version}.tar.xz
Patch0:		cryptsetup-1.6.4-out-of-source-build.patch

BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	pkgconfig(gpg-error)
BuildRequires:	pkgconfig(libgcrypt) >= 1.7.2
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(uuid)
%if %{with static}
BuildRequires:	glibc-static-devel
%endif
%rename		cryptsetup-luks

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

%package -n	%{libname}
Summary:	Library for setting up encrypted filesystems
Group:		System/Libraries

%description -n %{libname}
LUKS is the upcoming standard for Linux hard disk encryption.
By providing a standard on-disk-format, it does not only facilitate
compatibility among distributions, but also provide secure management
of multiple user passwords. In contrast to existing solution, LUKS stores
all setup necessary setup information in the partition header, enabling
the user to transport or migrate his data seamlessly.

This package contains the shared libraries required for running
programs which use cryptsetup-luks.

%package -n	%{devname}
Summary:	Development library for setting up encrypted filesystems
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
LUKS is the upcoming standard for Linux hard disk encryption.
By providing a standard on-disk-format, it does not only facilitate
compatibility among distributions, but also provide secure management
of multiple user passwords. In contrast to existing solution, LUKS stores
all setup necessary setup information in the partition header, enabling
the user to transport or migrate his data seamlessly.

This package contains the header files and development libraries
for building programs which use cryptsetup-luks.

%package -n	python-%{name}
Summary:	Python bindings for %{name}
Group:		Development/Python

%description -n	python-%{name}
This package provides Python bindings for libcryptsetup, a library
for setting up disk encryption using dm-crypt kernel module.

%prep
%setup -q
%apply_patches
chmod -x python/pycryptsetup-test.py
chmod -x misc/dracut_90reencrypt/*

autoreconf -fiv

%build
%configure \
	--disable-selinux \
	--sbindir=/sbin \
	--enable-python \
	--enable-cryptsetup-reencrypt \
%if %{with static}
	--enable-static-cryptsetup \
%endif
%if %{with compatible}
	--with-plain-mode=cbc-plain \
	--with-luks1-keybits=128
%endif

# remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
%makeinstall_std

mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libcryptsetup.so.%{major}* %{buildroot}/%{_lib}
ln -srf %{buildroot}/%{_lib}/libcryptsetup.so.%{major}.*.* %{buildroot}%{_libdir}/libcryptsetup.so

%find_lang %{name}

%files -f %{name}.lang
%doc ChangeLog AUTHORS FAQ NEWS README TODO
%{_mandir}/man8/cryptsetup.8*
%{_mandir}/man8/cryptsetup-reencrypt.8*
%{_mandir}/man8/veritysetup.8*
/sbin/cryptsetup
/sbin/cryptsetup-reencrypt
/sbin/veritysetup

%files -n %{libname}
/%{_lib}/libcryptsetup.so.%{major}*

%files -n %{devname}
%{_includedir}/libcryptsetup.h
%if %{with static}
%{_libdir}/libcryptsetup.a
%endif
%{_libdir}/libcryptsetup.so
%{_libdir}/pkgconfig/libcryptsetup.pc

%files -n python-%{name}
%{python_sitearch}/pycryptsetup.so
