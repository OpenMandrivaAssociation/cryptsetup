%define major 12
%define libname %mklibname cryptsetup %{major}
%define devname %mklibname cryptsetup -d
%global optflags %{optflags} -O3

%define _disable_rebuild_configure 1
%bcond_with compatible
%bcond_with static

Summary:	Utility for setting up encrypted filesystems
Name:		cryptsetup
Version:	2.4.2
Release:	1
License:	GPLv2
Group:		System/Base
Url:		https://gitlab.com/cryptsetup/cryptsetup
Source0:	https://www.kernel.org/pub/linux/utils/%{name}/v%(echo %{version} |cut -d. -f1-2)/%{name}-%{version}.tar.xz

BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(devmapper) >= 1.02.153
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(libargon2)
BuildRequires:	pkgconfig(json-c)
BuildRequires:	pkgconfig(blkid)
BuildRequires:	systemd-macros
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

%package -n %{libname}
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

%package -n %{devname}
Summary:	Development library for setting up encrypted filesystems
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
LUKS is the upcoming standard for Linux hard disk encryption.
By providing a standard on-disk-format, it does not only facilitate
compatibility among distributions, but also provide secure management
of multiple user passwords. In contrast to existing solution, LUKS stores
all setup necessary setup information in the partition header, enabling
the user to transport or migrate his data seamlessly.

This package contains the header files and development libraries
for building programs which use cryptsetup-luks.

%prep
%autosetup -p1

chmod -x misc/dracut_90reencrypt/*

autoreconf -fiv

%build
# (tpg) 2020-03-15 BIG FAT WARNING
# grub and calamares does not support LUKS2
# so stick to LUKS1 until they extend support

%configure \
	--disable-selinux \
	--sbindir=/sbin \
	--with-tmpfilesdir="%{_tmpfilesdir}" \
	--enable-cryptsetup-reencrypt \
	--disable-ssh-token \
	--enable-libargon2 \
%if %{with static}
	--enable-static-cryptsetup \
%endif
%if %{with compatible}
	--with-plain-mode=cbc-plain \
	--with-luks1-keybits=128 \
%endif
	--with-default-luks-format=LUKS1 \
	--with-crypto_backend=kernel
# NOTE: --with-crypto_backend=openssl breaks steam
# https://github.com/ValveSoftware/steam-for-linux/issues/6861
# kernel is safer because it doesn't drag in any extra libraries
# that might clash.

# remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install

mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libcryptsetup.so.%{major}* %{buildroot}/%{_lib}
ln -srf %{buildroot}/%{_lib}/libcryptsetup.so.%{major}.*.* %{buildroot}%{_libdir}/libcryptsetup.so

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS FAQ
%{_tmpfilesdir}/cryptsetup.conf
/sbin/cryptsetup
/sbin/cryptsetup-reencrypt
/sbin/veritysetup
/sbin/integritysetup
%doc %{_mandir}/man8/cryptsetup.8*
%doc %{_mandir}/man8/cryptsetup-reencrypt.8*
%doc %{_mandir}/man8/veritysetup.8*
%doc %{_mandir}/man8/integritysetup.8*

%files -n %{libname}
/%{_lib}/libcryptsetup.so.%{major}*

%files -n %{devname}
%{_includedir}/libcryptsetup.h
%if %{with static}
%{_libdir}/libcryptsetup.a
%endif
%{_libdir}/libcryptsetup.so
%{_libdir}/pkgconfig/libcryptsetup.pc
