%define	major	4
%define	libname	%mklibname cryptsetup %{major}
%define	devname	%mklibname cryptsetup -d

%bcond_with	compatible
%bcond_with	static
%bcond_without	uclibc

Name:		cryptsetup
Version:	1.5.1
Release:	5
Summary:	Utility for setting up encrypted filesystems
License:	GPLv2
Group:		System/Base
URL:		http://code.google.com/p/cryptsetup/
Source0:	http://cryptsetup.googlecode.com/files/%{name}-%{version}.tar.bz2
Source1:	http://cryptsetup.googlecode.com/files/%{name}-%{version}.tar.bz2.asc
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(gpg-error)
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(python2)
%if %{with static}
BuildRequires:	glibc-static-devel
%endif
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-15
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

%package -n	uclibc-%{name}
Summary:	Utility for setting up encrypted filesystems (uClibc build)
Group:		System/Base

%description -n	uclibc-%{name}
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

%package -n	uclibc-%{libname}
Summary:	Library for setting up encrypted filesystems (uClibc build)
Group:		System/Libraries

%description -n uclibc-%{libname}
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
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{version}-%{release}
%endif
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d cryptsetup 0

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

%build
CONFIGURE_TOP="$PWD"
%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%uclibc_configure \
		--disable-selinux \
		--sbindir=%{uclibc_root}/sbin \
		--enable-cryptsetup-reencrypt
%make
popd
%endif

mkdir -p system
pushd system
%configure2_5x	--disable-selinux \
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

%make
popd

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
mkdir -p %{buildroot}%{uclibc_root}/%{_lib}
mv %{buildroot}%{uclibc_root}%{_libdir}/libcryptsetup.so.%{major}* %{buildroot}%{uclibc_root}/%{_lib}
ln -srf %{buildroot}%{uclibc_root}/%{_lib}/libcryptsetup.so.%{major}.* %{buildroot}%{uclibc_root}%{_libdir}/libcryptsetup.so

rm -r %{buildroot}%{uclibc_root}%{_libdir}/pkgconfig
%endif

%makeinstall_std -C system

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

%if %{with uclibc}
%files -n uclibc-%{name}
%{uclibc_root}/sbin/cryptsetup
%{uclibc_root}/sbin/cryptsetup-reencrypt
%{uclibc_root}/sbin/veritysetup
%endif

%files -n %{libname}
/%{_lib}/libcryptsetup.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}/%{_lib}/libcryptsetup.so.%{major}*
%endif

%files -n %{devname}
%{_includedir}/libcryptsetup.h
%if %{with static}
%{_libdir}/libcryptsetup.a
%endif
%{_libdir}/libcryptsetup.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libcryptsetup.so
%endif
%{_libdir}/pkgconfig/libcryptsetup.pc

%files -n python-%{name}
%{python_sitearch}/pycryptsetup.so

%changelog
* Thu Dec 13 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.5.1-2
- rebuild on ABF

* Mon Oct 29 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.5.1-2
+ Revision: 820552
- build python bindings
- enable build of cryptsetup-reencrypt
- do uClibc build

* Mon Oct 29 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.5.1-1
+ Revision: 820292
- drop useless 'INSTALL' file
- move library to /%%{_lib} (moving libgcrypt as well will also come)
- cleanups
- new version

* Thu Jun 07 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.4.3-1
+ Revision: 803080
- version update 1.4.3

* Fri May 11 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.4.2-1
+ Revision: 798276
- version update 1.4.2

* Fri Mar 16 2012 Oden Eriksson <oeriksson@mandriva.com> 1.4.1-2
+ Revision: 785343
- fix deps
- various fixes

  + Bernhard Rosenkraenzer <bero@bero.eu>
    - Update to 1.4.1
    - Clean up spec file

* Tue Jul 26 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1.3.1-1
+ Revision: 691659
- 1.3.1

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2.0-3
+ Revision: 663428
- mass rebuild

* Thu Dec 23 2010 Luca Berra <bluca@mandriva.org> 1.2.0-2mdv2011.0
+ Revision: 623997
- add FAQ to docs

* Thu Dec 23 2010 Luca Berra <bluca@mandriva.org> 1.2.0-1mdv2011.0
+ Revision: 623996
- update to 1.2.0
- disable backwards compatible plain-mode cipher
- disable static build, since it requires static libgpg-error

* Wed Jul 28 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.3-1mdv2011.0
+ Revision: 562795
- update to new version 1.1.3

* Mon Apr 26 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.0-3mdv2010.1
+ Revision: 538984
- arch-independant virtual devel package

  + Funda Wang <fwang@mandriva.org>
    - provides %%name-devel
    - drop unused requires on devel package (corresponding requires already produced by file deps)

* Sun Apr 25 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.0-2mdv2010.1
+ Revision: 538749
- ensure devel package requires runtime package

  + Sandro Cazzaniga <kharec@mandriva.org>
    - Fix license
    - Fix mixed of spaces and tabs

* Sun Jan 31 2010 Luca Berra <bluca@mandriva.org> 1.1.0-1mdv2010.1
+ Revision: 498763
- updated to version 1.1.0
- new version 1.1.0-rc2

* Tue Aug 04 2009 Eugeni Dodonov <eugeni@mandriva.com> 1.0.7-2mdv2010.0
+ Revision: 409019
- Updated buildrequires for libuuid.
- rebuild with new libuuid

* Sat Jul 25 2009 Frederik Himpe <fhimpe@mandriva.org> 1.0.7-1mdv2010.0
+ Revision: 399843
- Update to new version 1.0.7
- Fix URL and SOURCE location
- Use new --disable-selinux ./configure option to disable selinux
- Remove udevsettle patch: 1.0.7 does not call udevsettle anymore now

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 1.0.6-4mdv2009.1
+ Revision: 350751
- rebuild

* Mon Sep 01 2008 Olivier Blin <blino@mandriva.org> 1.0.6-3mdv2009.0
+ Revision: 278110
- use udevadm to settle for udev events (#43350, patch from upstream SVN)
- remove udevsettle patch (merged upstream)

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 1.0.6-2mdv2009.0
+ Revision: 264381
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Jun 01 2008 Funda Wang <fwang@mandriva.org> 1.0.6-1mdv2009.0
+ Revision: 214094
- there is no use remove .so.major, as it is the soname
- New version 1.0.6

* Wed Jan 16 2008 Andreas Hasenack <andreas@mandriva.com> 1.0.5-5mdv2008.1
+ Revision: 153759
- fix race condition with udev by calling udevsettle (patch from ubuntu/debian/suse)

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 1.0.5-4mdv2008.1
+ Revision: 149141
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Tue Sep 25 2007 Frederic Crozat <fcrozat@mandriva.com> 1.0.5-3mdv2008.0
+ Revision: 92837
- Patch0 (Fedora): add support for LUKS encrypted CD/DVD

* Tue May 08 2007 Andreas Hasenack <andreas@mandriva.com> 1.0.5-2mdv2008.0
+ Revision: 25051
- upstream re-released 1.0.5 with a fix, no need for
  "odd" patch anymore

* Mon May 07 2007 Andreas Hasenack <andreas@mandriva.com> 1.0.5-1mdv2008.0
+ Revision: 24624
- updated to version 1.0.5
- cryptsetup-luks was merged with cryptsetup (upstream rename). There Is Only One now.

* Tue Apr 24 2007 Frederic Crozat <fcrozat@mandriva.com> 1.0.3-2mdv2008.0
+ Revision: 17886
- Rebuild for 2008.0
- use new macro
