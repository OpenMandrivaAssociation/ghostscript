%define _disable_ld_no_undefined 1
%define rel	1

%define gsver 9.07
%define ijsver 0.35
# (tpg) BUMP THIS EVERY UPDATE
%define ijsreloffset 81
%define ijsrel %(echo $((%{rel} + %{ijsreloffset})))

%define ijsmajor 1
%define libijs %mklibname ijs %{ijsmajor}
%define libijs_devel %mklibname -d ijs

%define gsmajor 9
%define libgs %mklibname gs %{gsmajor}
%define libgs_devel %mklibname -d gs

%define bootstrap 1

%define GSx11SVGAmodule 1
%define withcupsfilters 1
%define debug 0
%if %{bootstrap}
%global withcupsfilters 0
%endif

Summary:	PostScript/PDF interpreter and renderer (Main executable)
Name:		ghostscript
Version:	%{gsver}
Release:	%{rel}
License:	GPLv2+
Group:		Publishing
URL:		http://www.ghostscript.com/awki/Index
Source0:	http://downloads.ghostscript.com/public/%{name}-%{gsver}.tar.gz
Source2:	ps2pdfpress.bz2
Source3:	http://www.linuxprinting.org/download/printing/sipixa6.upp.bz2
Source4:	ghostscript.rpmlintrc

Patch300:	ghostscript-9.05-x11_shared.diff
# Fedora patches
# Fix ijs-config not to have multilib conflicts (bug #192672)
Patch1:		ghostscript-multilib.patch
# Fix some shell scripts
Patch2:		ghostscript-scripts.patch
# Build igcref.c with -O0 to work around bug #150771.
Patch3:		ghostscript-noopt.patch
# Fix ./autgen.sh in ijs sub-project
# See http://bugs.ghostscript.com/show_bug.cgi?id=692040 for details.
#Patch4:		ghostscript-ijs-automake-ver.patch
# Define .runlibfileifexists.
Patch5:		ghostscript-runlibfileifexists.patch
# Install CUPS filter convs files in the correct place.
Patch10:	ghostscript-cups-filters.patch
# Restored Fontmap.local patch, incorrectly dropped after
# ghostscript-8.15.4-3 (bug #610301).
# Note: don't use -b here to avoid the backup file ending up in the
# package manifest.
Patch27:	ghostscript-Fontmap.local.patch
# Don't assume %%rom%% device is available for initial ICC profile dir.
#Patch28: ghostscript-iccprofiles-initdir.patch
# gdevcups: don't use uninitialized variables in debugging output.
#Patch29:	ghostscript-gdevcups-debug-uninit.patch
Patch30:	ghostscript-9.06-automake-1.13.patch

%if !%{bootstrap}
BuildRequires:	gtk+2-devel
BuildRequires:	cups-devel
BuildRequires:	fontconfig-devel
%endif
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	unzip
BuildRequires:	gettext-devel
BuildRequires:	glibc-devel
BuildRequires:	jbig2dec-devel
BuildRequires:	jpeg-devel
BuildRequires:	libpaper-devel
BuildRequires:	netpbm-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(jasper)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(libidn)
BuildRequires:	pkgconfig(libpng15)
BuildRequires:	pkgconfig(libxml)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libopenjpeg1)

Requires:	ghostscript-common
Requires:	update-alternatives
%if !%{GSx11SVGAmodule}
%rename	ghostscript-module-X ghostscript-module-SVGALIB
%endif

%description
Ghostscript is a set of software tools that provide a PostScript(TM)
interpreter, a set of C procedures (the Ghostscript library, which
implements the graphics capabilities in the PostScript language) and
an interpreter for Portable Document Format (PDF) files. Ghostscript
translates PostScript code into many common, bitmapped and vector
formats, like those understood by your printer or screen. Ghostscript
is normally used to display PostScript files and to print PostScript
files to non-PostScript printers.

You should install ghostscript if you need to display PostScript or
PDF files, or if you have a non-PostScript printer.

%package dvipdf
Summary:	PostScript/PDF interpreter and renderer (DVI-to-PDF converter)
Group:		Publishing
Requires:	ghostscript
Requires:	coreutils
Requires:	tetex-dvips

%description dvipdf
Tool to convert the DVI format of TeX into the PDF format. There are
more such tools (for different quality levels) in the tetex-dvipdfm
package. All these tools use dvips of TeX to convert the DVI file to
PostScript, then they use GhostScript to generate the PDF file.

%package common
Summary:	PostScript/PDF interpreter and renderer (Common files)
Group:		Publishing
Requires:	urw-fonts >= 1.1
Requires:	ghostscript-fonts
Requires:	perl

%description common
Ghostscript is a PostScript/PDF interpreter. It can render both
PostScript and PDF files to devices which include X window, many
printer formats, and popular graphics file formats.

This package contains the common data files needed by GhostScript.

%package X
Summary:	PostScript/PDF interpreter and renderer (GTK-based executable)
Group:		Publishing
Requires:	ghostscript-common
Requires:	update-alternatives

%description X
Ghostscript is a PostScript/PDF interpreter. It can render both
PostScript and PDF files to devices which include X window, many
printer formats, and popular graphics file formats.

This package contains a GhostScript executable with GTK-based X
display support ("display" device, default, so it displays files by
simply entering "gs <file>" on the command line). It makes use of the
GhostScript shared library.

%if %{GSx11SVGAmodule}
%package module-X
Summary:	PostScript/PDF interpreter and renderer (Additional support for X)
Group:		Publishing
Requires:	ghostscript-common

%description module-X
Ghostscript is a PostScript/PDF interpreter. It can render both
PostScript and PDF files to devices which include X window, many
printer formats, and popular graphics file formats.

This package enhances Ghostscript with X window support
%endif

%package -n %{libgs}
Summary:	PostScript/PDF interpreter and renderer (GhostScript shared library)
Group:		Publishing

%description -n %{libgs}
This is the API library for programs which use the PostScript and/or
PDF interpreters of GhostScript.

%package -n %{libgs_devel}
Summary:	Headers and links to compile against the "%{libgs}" library
Group:		Development/C
Requires:	%{libgs} >= %{gsver}
Provides:	%{name}-devel = %{gsver}
Provides:	libgs-devel = %{gsver}
Obsoletes:	%{_lib}gs9-devel < %{gsver}
Obsoletes:	%{_lib}gs8-devel < %{gsver}

%description -n %{libgs_devel}
This package contains the static library and the header files needed
to compile applications using the GhostScript shared library.

%package -n %{libijs}
Version:	%{ijsver}
Release:	%{ijsrel}
Summary:	Dynamic library for the IJS printer driver plug-in interface
Group:		Publishing
URL:		http://www.linuxprinting.org/ijs/
Provides:	libijs = %{ijsver}-%{ijsrel}

%description -n %{libijs}
This is the API library for programs using the IJS printer driver
plug-in interface. Printer drivers using this interface can be added
to GhostScript (6.53 or newer) without needing to rebuild
GhostScript. Application programs providing an IJS interface can make
use of IJS printer drivers directly, without needing GhostScript.

%package -n %{libijs_devel}
Version:	%{ijsver}
Release:	%{ijsrel}
Summary:	Headers and links for compiling against the "%{libijs}" library
Group:		Development/C
URL:		http://www.linuxprinting.org/ijs/
Requires:	%{libijs} >= %{ijsver}
Requires:	multiarch-utils
Provides:	libijs-devel = %{ijsver}-%{ijsrel}
Provides:	ijs-devel = %{ijsver}-%{ijsrel}
Obsoletes:	%{_lib}ijs1-devel < %{ijsver}-%{ijsrel}

%description -n %{libijs_devel}
This package contains the static library and the header files needed
to compile applications using the IJS library.

%package doc
Summary:	Documentation for GhostScript
Group:		Publishing
Requires:	ghostscript

%description doc
This package contains documentation for GhostScript.

%prep
%setup -q
%apply_patches

#backup files not needed
find . -name "*.*~" |xargs rm -f
# prevent building and using bundled libs
rm -rf jasper jbig2dec libpng jpeg tiff expat zlib lcms* freetype openjpeg

# Convert manual pages to UTF-8
from8859_1() {
        iconv -f iso-8859-1 -t utf-8 < "$1" > "${1}_"
        mv "${1}_" "$1"
}
for i in man/de/*.1; do from8859_1 "$i"; done

# Stuff for shared library support to ghostscript.
%if %{GSx11SVGAmodule}
# build a small README describing the features available.
cat <<EOF >README.shared.mandrivalinux
This version of ghostscript support shared modules dynamically loaded
at run time.

There are currently two modules compiled with the Mandriva Linux version of
ghostscript, one to support all X11 devices (typically used by gv) and
another to support the svgalib devices. Look at the
ghostscript-module-??? packages.

There is no configuration needed, just can add (or remove) the package
to add (or remove) the devices concerned in ghostscript.
EOF
%endif

# ps2pdfpress
bzcat %{SOURCE2} > ps2pdfpress

# UPP file for SiPix Pocket Printer A6
bzcat %{SOURCE3} > sipixa6.upp

%build

# Change compiler flags for debugging when in debug mode
%if %debug
export DONT_STRIP=1
export CFLAGS="`echo %optflags |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/'`"
export CXXFLAGS="`echo %optflags |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/'`"
export RPM_OPT_FLAGS="`echo %optflags |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/'`"
%endif

pushd ijs*
# Rebuild broken build infrastructure
# Needed by patch4.
./autogen.sh
%configure2_5x \
%ifarch %{ix86}
	--disable-sse2 \
%endif
    --enable-shared \
    --disable-static

%make
popd

# We have a Subversion version, so we must re-generate "configure"
./autogen.sh

%configure2_5x \
	--enable-dynamic \
%if !%{bootstrap}
    --enable-fontconfig \
%endif
%ifarch %{ix86}
    --disable-sse2 \
%endif
    --with-drivers=ALL,opvp \
    --with-fontpath="/usr/share/fonts/default/ghostscript:/usr/share/fonts/default/type1:/usr/share/ghostscript/fonts:/usr/share/ghostscript/%{gsver}/Resource:/usr/share/ghostscript/Resource:/usr/share/ghostscript/CIDFont:/usr/share/fonts/ttf:/usr/share/fonts/type1:/usr/share/fonts/default/Type1" \
    --with-ijs \
    --without-omni \
    --with-x \
    --disable-compile-inits \
    --with-system-libtiff \
    --with-libidn \
    --enable-dbus \
    --enable-dynamic \
    --with-install-cups

# Drivers which do not compile:
# Needs newsiop/lbp.h: nwp533
# Needs sys/ioccom.h: sparc
# Needs unbdev/lpviio.h: sparc

# Set documentation dir
perl -p -i -e 's|^(docdir=).*$|$1\$\(datadir\)/doc/%{name}-doc-%{gsver}|' Makefile

# Fix references to X11 libraries
perl -p -i -e "s|(/usr/X11R6)/lib\b|\1/%{_lib}|g" Makefile base/*.mak

# Correct paths for CJK fonts
perl -p -i -e "s:/usr/share/ghostscript/:/usr/share/ghostscript/Resource/:g" Resource/Init/gs_res.ps
perl -p -i -e "s:ghostscript/Resource/fonts:ghostscript/Resource/Font:g" Resource/Init/gs_res.ps

# Do not use "-ansi" in gcc calls
perl -p -i -e "s:-ansi::g" Makefile

# bork
perl -p -i -e "s|^EXTRALIBS=|EXTRALIBS=-L/%{_lib} -lz |g" Makefile

# The RPM macro for make is not used here, as parallelization of the build 
# process does not work.
%if %{GSx11SVGAmodule}
#make STDDIRS
make obj/X11.so
%endif
make so
#make pcl3opts
make cups

%install
rm -rf %{buildroot}

# Change compiler flags for debugging when in debug mode
%if %debug
export DONT_STRIP=1
export CFLAGS="`echo %optflags |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/'`"
export CXXFLAGS="`echo %optflags |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/'`"
export RPM_OPT_FLAGS="`echo %optflags |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/'`"
%endif

# Make directories
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_mandir}/man1
%if !%{bootstrap}
install -d %{buildroot}%{_prefix}/lib/cups
install -d %{buildroot}%{_datadir}/cups/model
install -d %{buildroot}%{_sysconfdir}/cups
%endif

pushd ijs*
%configure2_5x \
	--enable-shared \
	--prefix=%{buildroot}%{_prefix} \
	--libdir=%{buildroot}%{_libdir}

# Work around bug in "configure" script
perl -p -i -e 's/\@OBJEXT\@/o/g' Makefile
perl -p -i -e 's/\@EXEEXT\@//g' Makefile
%makeinstall
# Fix prefixes in scripts
perl -p -i -e "s:%{buildroot}::g" %{buildroot}%{_bindir}/ijs-config
perl -p -i -e "s:%{buildroot}::g" %{buildroot}%{_libdir}/pkgconfig/ijs.pc
popd

##### GHOSTSCRIPT
mkdir -p %{buildroot}%{_docdir}/ghostscript-doc-%{gsver}

%if !%{bootstrap}
make \
	prefix=%{_prefix} \
	DESTDIR=%{buildroot} \
	gssharedir=%{_libdir}/ghostscript/%{gsver} \
	docdir=%{_docdir}/ghostscript-doc-%{gsver} \
	bindir=%{_bindir} \
	mandir=%{_mandir} \
	install-cups
%endif

make \
	prefix=%{_prefix} \
	DESTDIR=%{buildroot} \
	gssharedir=%{_libdir}/ghostscript/%{gsver} \
	docdir=%{_docdir}/ghostscript-doc-%{gsver} \
	bindir=%{_bindir} \
	libdir=%{_libdir} \
	mandir=%{_mandir} \
	soinstall

%if %{GSx11SVGAmodule}
make \
	prefix=%{_prefix} \
	DESTDIR=%{buildroot} \
	gssharedir=%{_libdir}/ghostscript/%{gsver} \
	docdir=%{_docdir}/ghostscript-doc-%{gsver} \
	bindir=%{_bindir} \
	libdir=%{_libdir} \
	mandir=%{_mandir} \
	install-shared
%endif

ln -sf gs.1%{_extension} %{buildroot}%{_mandir}/man1/ghostscript.1%{_extension}

# ps2pdfpress
install -m 755 ps2pdfpress %{buildroot}%{_bindir}

# UPP file for SiPix Pocket Printer A6
#mkdir -p %{buildroot}%{_datadir}/ghostscript/%{gsver}/lib
install -m 644 sipixa6.upp %{buildroot}%{_datadir}/ghostscript/%{gsver}/lib/

# Add backward compatibility link to not break printerdrake in Mandriva
# 2006 and older
ln -s %{_bindir}/gsc %{buildroot}%{_bindir}/gs-common
ln -s %{_bindir}/gsc %{buildroot}%{_bindir}/ghostscript

%if !%{bootstrap}
# why?
mv %{buildroot}%{_datadir}/cups/mime/gstoraster.convs %{buildroot}%{_sysconfdir}/cups/gstoraster.convs
%endif

# Correct permissions for all documentation files
chmod -R a+rX %{buildroot}%{_docdir}
chmod -R go-w %{buildroot}%{_docdir}
chmod -R u+w %{buildroot}%{_docdir}

%post
# Set up update-alternatives entries
%{_sbindir}/update-alternatives --install %{_bindir}/gs gs %{_bindir}/gsc 200

%post X
# Set up update-alternatives entries
%{_sbindir}/update-alternatives --install %{_bindir}/gs gs %{_bindir}/gsx 100

%post common
# Initialize japanese fonts
if test -f /usr/share/fonts/ttf/japanese/cidinst; then
    sh /usr/share/fonts/ttf/japanese/cidinst
fi

%preun
if [ "$1" = 0 ]; then
  # Remove update-alternatives entry
  %{_sbindir}/update-alternatives --remove gs %{_bindir}/gsc
fi

%preun X
if [ "$1" = 0 ]; then
  # Remove update-alternatives entry
  %{_sbindir}/update-alternatives --remove gs %{_bindir}/gsx
fi

%files
%{_bindir}/gsc
%{_bindir}/gs-common
%{_bindir}/ghostscript

%files X
%{_bindir}/gsx

%files common
%dir %{_datadir}/ghostscript
%{_datadir}/ghostscript/%{gsver}
%{_mandir}/man1/*
%lang(de) %{_mandir}/de/man1/*
#%{_bindir}/[a-c]*
#{_bindir}/dumphint
%{_bindir}/[e-f]*
#{_bindir}/gs-common
%{_bindir}/gs[a-b]*
%{_bindir}/gs[d-n]*
%{_bindir}/[j-l]*
%{_bindir}/[n-z]*
%if %{withcupsfilters}
# "pstoraster" wrapper script to make GhostScript being used as the
# cups-internal RIP
%attr(0755,root,root) %{_prefix}/lib*/cups/filter/*
%{_datadir}/cups/model/*
%config(noreplace) %{_sysconfdir}/cups/gstoraster.convs
%endif

%files doc
%doc %{_docdir}/ghostscript-doc-%{gsver}

%files dvipdf
%{_bindir}/dvipdf

%if %{GSx11SVGAmodule}
%files module-X
%doc README.shared.mandrivalinux
%dir %{_libdir}/ghostscript/%{gsver}
%{_libdir}/ghostscript/%{gsver}/X11.so
%endif

%files -n %{libgs}
%{_libdir}/libgs.so.*%{gsmajor}*

%files -n %{libgs_devel}
%{_libdir}/libgs.so
%{_includedir}/ghostscript

%files -n %{libijs}
%{_libdir}/libijs-%{ijsver}.so

%files -n %{libijs_devel}
%doc ijs/README
%{_libdir}/libijs.so
%{_libdir}/pkgconfig/ijs.pc
%{_includedir}/ijs
%{_bindir}/ijs_client_example
%{_bindir}/ijs_server_example
%{_bindir}/ijs-config


%changelog
* Tue Jul 31 2012 Andrey Bondrov <andrey.bondrov@rosalab.ru> 9.05-2
- Rebuild without bootstrap

* Tue Jul 31 2012 Andrey Bondrov <andrey.bondrov@rosalab.ru> 9.05-1
- New version 9.05
- Drop some no longer needed patches (applied in upstream), re-diff some needed
- Use bootstrap build

* Thu Dec 22 2011 Matthew Dawkins <mattydaw@mandriva.org> 9.04-4
+ Revision: 744600
- bump release
- major clean up
- removed pre 200900 junk
- removed pre 200700 build optionsA
- organized descriptions with packages
- converted BRs to pkgconfig provides
- employed apply_patches

* Sun Oct 30 2011 Alexander Barakin <abarakin@mandriva.org> 9.04-3
+ Revision: 707842
- move "make install-shared" after "make soinstall"
  see http://lists.mandriva.com/cooker/2011-10/msg00288.php
  and next letter

* Tue Oct 04 2011 Oden Eriksson <oeriksson@mandriva.com> 9.04-2
+ Revision: 702671
- stupid release magic...
- 9.04
- sync with patches from fedora
- nuked remaining bundled libs, full list of system libs is: jasper, jbig2dec, libpng, jpeg, tiff, zlib, lcms, freetype
- attempt to relink against libpng15.so.15

* Fri Apr 01 2011 Funda Wang <fwang@mandriva.org> 9.02-1
+ Revision: 649540
- update file list
- update file list
- real 9.02
- update to new version 9.02

* Thu Feb 10 2011 Funda Wang <fwang@mandriva.org> 9.01-1
+ Revision: 637122
- New version 9.01
- drop system jasper patch (merged upstream)
- use new devel package policy

* Fri Sep 24 2010 Oden Eriksson <oeriksson@mandriva.com> 9.00-1mdv2011.0
+ Revision: 580940
- 9.00
- drop redundant patches
- rediff some patches
- fix build deps

  + Funda Wang <fwang@mandriva.org>
    - add archlinux patch to build with png14

* Fri Jul 16 2010 Oden Eriksson <oeriksson@mandriva.com> 8.71-72mdv2011.0
+ Revision: 554181
- P108: CVE-2010-1628 (ubuntu)
- link against system libpng jpeg libs

* Wed Mar 24 2010 Tiago Salem <salem@mandriva.com.br> 8.71-71mdv2010.1
+ Revision: 527273
- add patch to fix some ldflags (fix for #58347)
- remove deprecated "--with-cups"
- bump release

* Mon Mar 22 2010 Tiago Salem <salem@mandriva.com.br> 8.71-70mdv2010.1
+ Revision: 526638
- bump release or it will be reject, even when bumping the version
- update to 8.71
- drop deprecated patches

* Tue Oct 27 2009 Oden Eriksson <oeriksson@mandriva.com> 8.64-69mdv2010.0
+ Revision: 459488
- build against system jbig2dec libs (CVE-2009-0196 is fixed there,
  so no need to patch the bundled jbig2dec libs)

* Thu Sep 24 2009 Olivier Blin <blino@mandriva.org> 8.64-68mdv2010.0
+ Revision: 448394
- add bootstrap flag to be able to break build-dep loop (from Arnaud Patard)

* Sun May 17 2009 Funda Wang <fwang@mandriva.org> 8.64-67mdv2010.0
+ Revision: 376541
- fix link order
- fix linkage of cups module

* Thu May 14 2009 Oden Eriksson <oeriksson@mandriva.com> 8.64-66mdv2010.0
+ Revision: 375676
- bump release
- whoops!, only nuke jasper source
- really link against system jasper libs

* Sat Apr 18 2009 Frederik Himpe <fhimpe@mandriva.org> 8.64-65mdv2009.1
+ Revision: 368001
- Add Fedora patches to fix CVE-2009-0196 and CVE-2009-0792

* Wed Mar 25 2009 Frederik Himpe <fhimpe@mandriva.org> 8.64-64mdv2009.1
+ Revision: 361163
- Sync with Fedora:
  * Add patch fixing CVE-2009-0583 and CVE-2009-0584
  * Add patch fixing bitcmyk driver

* Sun Feb 08 2009 Frederik Himpe <fhimpe@mandriva.org> 8.64-63mdv2009.1
+ Revision: 338500
- Update to new version 8.64
- Rediff windev compatibility patch
- Rediff x11_shared patch
- Add patch to fix format string errors
- Sync with Fedora:
  * Patch to use system libjasper
  * Fix some scripts
  * Fix pksmraw (RH bug #308211)
  * Define .runlibfileifexists patch

* Tue Sep 16 2008 Tiago Salem <salem@mandriva.com.br> 8.63-62mdv2009.0
+ Revision: 285304
- reenabling windev patch (#28960)
- bump release

* Sun Aug 03 2008 Frederik Himpe <fhimpe@mandriva.org> 8.63-61mdv2009.0
+ Revision: 262181
- Update to ghostscript 8.63

* Mon Jun 09 2008 Pixel <pixel@mandriva.com> 8.61-60mdv2009.0
+ Revision: 217185
- do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Funda Wang <fwang@mandriva.org>
    - mark lang properties

* Fri Feb 29 2008 Tiago Salem <salem@mandriva.com.br> 8.61-60mdv2008.1
+ Revision: 176876
- Added security patch for CVE-2008-0411

* Tue Jan 29 2008 Marcelo Ricardo Leitner <mrl@mandriva.com> 8.61-59mdv2008.1
+ Revision: 159691
- Make use of %%mkrel -d
- Includes libgs devel header files. Closes: #37295

* Wed Jan 23 2008 Funda Wang <fwang@mandriva.org> 8.61-58mdv2008.1
+ Revision: 156937
- rebuild against latest gnutls

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Nov 23 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 8.61-57mdv2008.1
+ Revision: 111478
- New upstream: 8.60
- Removed patches CVE-2007-2721 and lib64: already included
- Disabled pcl3opts building, as it's broken.
- Do not ship ghostscript-devel for now.

* Tue Nov 06 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 8.60-56mdv2008.1
+ Revision: 106352
- Added patch jasper-CVE-2007-2721. Closes: #35332

* Mon Sep 24 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 8.60-55mdv2008.0
+ Revision: 92687
- add /usr/share/fonts/default/Type1 as font-path (Type1/ was moved to
  type1/ but some applications have hardcoded references to Type1/, so
  fonts are being put back in Type1 and both paths may be valid for a
  while). See #34054 and #32883.

* Wed Sep 12 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 8.60-54mdv2008.0
+ Revision: 84782
- Bumped release.

* Tue Sep 04 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 8.60-53mdv2008.0
+ Revision: 79363
- Added patch lib64: fix pkgconfig file place.
- Added patch x11_shared, with fixes for x86_64 arch. (-fPIC stuff)
- New upstream: 8.60

* Mon Aug 27 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 8.15.4-52mdv2008.0
+ Revision: 72021
- Fix type1 fonts path. Closes: #32883

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 8.15.4-51mdv2008.0
+ Revision: 70248
- fileutils, sh-utils & textutils have been obsoleted by coreutils a long time ago
- kill file require on update-alternatives

* Sun Jun 17 2007 Helio Chissini de Castro <helio@mandriva.com> 8.15.4-50mdv2008.0
+ Revision: 40565
- Right provides for libgs

* Mon May 28 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 8.15.4-49mdv2008.0
+ Revision: 31973
- Release bump to 49 due to bug #31047.

* Wed May 16 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 8.15.4-1mdv2008.0
+ Revision: 27317
- Specfile cleanup
- Expose upstream minor version in our version too. (use full version on version)
- Update buildrequires.
- New upstream: 8.15.4


* Tue Jan 30 2007 Olivier Blin <oblin@mandriva.com> 8.15-48mdv2007.1
+ Revision: 115348
- move doc in sub-package

  + Marcelo Ricardo Leitner <mrl@mandriva.com>
    - New upstream: 8.15.3
    - Minor specfile cleanup.
    --This line, and those below, will be ignored--
      D    SOURCES/espgs-8.15.2-rev183.tar.bz2
      A    SOURCES/espgs-8.15.3-source.tar.bz2
      M    SPECS/ghostscript.spec
    - Import ghostscript

* Mon Aug 28 2006 Till Kamppeter <till@mandriva.com> 8.15-47mdv2007.0
- Updated to subversion revision 182 (Several bug fixes).
- Removed patch 1 and 4 (merged upstream).

* Sat Aug 19 2006 Till Kamppeter <till@mandriva.com> 8.15-46mdv2007.0
- Updated to subversion revision 172 (Translated comments in OpenPrinting
  Vector header file to english, merged fixes for building /usr/bin/gsc
  and /usr/bin/gsx upstream).
- Added UPP file for the SiPix Pocket Printer A6.
- Removed patch 3 (merged upstream).

* Fri Jul 14 2006 Till Kamppeter <till@mandriva.com> 8.15-45mdv2007.0
- GhostScript was not able to display some PDFs (bug 21493, GhostScript bug
  688736 with proposed patch, applied as patch 4).

* Thu Jul 13 2006 Till Kamppeter <till@mandriva.com> 8.15-44mdv2007.0
- Updated to subversion revision 169 (fontconfig support, fixes on "ps2epsi",
  CJKV patch from GS 8, KRGB 1.3 from HP).
- New patch 1, as GTK presence is checked by ./configure now.
- Fixed Makefile rules for /usr/bin/gsx and /usr/bin/gsc, they got messed
  up by the most recent changes on SVN (patch 3).
- Dropped ghostscript-static package (it only wastes space and no problems
  on the dynamically linked GhostScript were reported).
- Uncompressed patches.

* Fri Jun 30 2006 Oden Eriksson <oeriksson@mandriva.com> 8.15-43mdv2007.0
- rebuilt against gnutls-1.4.0
- remove the tetex-dvips build dep as it is not needed and it leads to 
  circular build deps hell

* Wed May 03 2006 Till Kamppeter <till@mandriva.com> 8.15-42mdk
- Added "BuildRequires: cups" to assure that CUPS drivers get installed.

* Thu Apr 27 2006 Till Kamppeter <till@mandriva.com> 8.15-41mdk
- Updated to subversion revision 145 (ESP GhostScript 8.15.2 release).

* Tue Apr 25 2006 Till Kamppeter <till@mandriva.com> 8.15-40mdk
- Added workaround for compatibility with PDF files generated by
  Windev (bug 15678).

* Mon Apr 24 2006 Till Kamppeter <till@mandriva.com> 8.15-39mdk
- Updated to subversion revision 141 (Tons of bug fixes, especially
  interpreter thingies like "I cannot display xyz.pdf", added CUPS
  1.2 features to "cups" raster device).
- Removed patch 0 (merged upstream).

* Tue Apr 04 2006 Till Kamppeter <till@mandriva.com> 8.15-38mdk
- Conflict against too old CUPS versions must be done with "cups"
  and not with "cups-common".

* Tue Apr 04 2006 Till Kamppeter <till@mandriva.com> 8.15-37mdk
- Moved CUPS filter directory from /usr/lib64/cups/filter to
  /usr/lib/cups/filter on 64-bit systems.

* Thu Mar 30 2006 Till Kamppeter <till@mandriva.com> 8.15-36mdk
- Updated to subversion revision 133 (Fixed bug in the
  OpenPrinting vector driver interface "opvp", updated Epson
  Avasys laser printer driver).

* Tue Mar 07 2006 Till Kamppeter <till@mandriva.com> 8.15-35mdk
- Let /usr/bin/gsx be built against GTK 2 and not against GTK 1
  (bug 21473).

* Wed Mar 01 2006 Till Kamppeter <till@mandriva.com> 8.15-34mdk
- Updated to subversion revision 130 (Fixed non-standard glyph
  rendering in PDF files generated by GhostScript).

* Mon Feb 27 2006 Till Kamppeter <till@mandriva.com> 8.15-33mdk
- Added link /usr/bin/gs-common for backward compatibility with
  printerdrake in Mandriva Linux 2006.

* Mon Feb 27 2006 Till Kamppeter <till@mandriva.com> 8.15-32mdk
- Made automatic release number generation with %%mkrel really working.

* Fri Feb 24 2006 Till Kamppeter <till@mandriva.com> 8.15-31mdk
- Updated to subversion revision 129 (Update to version 1.2 of
  HP's KRGB patch in the "ijs" device, fixes several buffer overflows
  and other segfault sources, especially important for full-bleed
  printing with HPIJS, thanks to David Suffield from HP).

* Fri Feb 24 2006 Till Kamppeter <till@mandriva.com> 8.15-30mdk
- Added "Provides: ghostscript" to ghostscript-static, as this one
  is also a fully functional GhostScript executable.

* Tue Feb 21 2006 Till Kamppeter <till@mandriva.com> 8.15-29mdk
- Changed priorities of update-alternatives to the "gsc" executable,
  it has no working "display" default device, but at least with this
  one everything which worked in the old static GhostScript works as
  before. "gsx" has problems with gv (bug 21131) and ps2pdf (bug 21150).
- Removed the "Requires: ghostscript-X-executable" from the
  "ghostscript-module-X" package. It is not needed.
- Updated package descriptions.

* Mon Feb 13 2006 Till Kamppeter <till@mandriva.com> 8.15-28mdk
- Added "Conflicts: ghostscript < 8.15-27mdk" to make updates
  correctly working (thanks to Frederic Crozat).
- Fixed %%postun script of libgs8 package.

* Fri Feb 03 2006 Till Kamppeter <till@mandriva.com> 8.15-27mdk
- New package splitting to avoid duplicate disk occupation by the same
  code in libgs and the static GhostScript executable
- Improved and cleaned up the package descriptions.
- %%mkrel also for libijs.
- Some spec file clean-up.

* Mon Jan 30 2006 Helio Chissini de Castro <helio@mandriva.com> 8.15-26mdk
- Introduced libgs package.
- Added patch to fix lack of right flags on compilation

* Mon Jan 23 2006 Till Kamppeter <till@mandriva.com> 8.15-25mdk
- Split off the dvipdf tool into its own package to avoid tetex
  dependency.
- Added "Required: tetex-dvips" to the newly defined ghostscript-dvipdf
  package (bug 20330).
- Introduced %%mkrel.

* Sat Jan 14 2006 Till Kamppeter <till@mandriva.com> 8.15-24mdk
- Updated to subversion revision 128 (Patch from Werner Fink from SuSE: 
  Fixed rendering of images when converting PostScript to PDF with 
  "ps2pdf" (bug 19437), fixed also a crash when generating PDF files with 
  the "pdfwrite" device).

* Mon Nov 14 2005 Oden Eriksson <oeriksson@mandriva.com> 8.15-23mdk
- rebuilt against openssl-0.9.8a

* Sat Sep 24 2005 Till Kamppeter <till@mandriva.com> 8.15-22mdk
- Updated to subversion revision 127 (Release 8.15.1 plus assorted
  fixes from Werner Fink from SuSE: Several segfaults, color model
  adaptations to GS 8.15 in some drivers, vertical japanese text
  fix, applied patches 0, 100, and 101 upstream).
- Removed patches 0, 100, and 101 (merged upstream). Now we have the
  first patch-free GhostScript package in a Linux distribution!
- There was still a Mandrake inside, Mandrivized it.

* Wed Aug 17 2005 Till Kamppeter <till@mandriva.com> 8.15-21mdk
- Updated to subversion revision 119 (Fixed bugs in the "pxlmono" and
  "pxlcolor" drivers, once on the Legal paper size definition, and second
  a missing PJL command telling whether the job is grayscale or color).

* Sun Aug 14 2005 Till Kamppeter <till@mandriva.com> 8.15-20mdk
- Updated to subversion revision 118 (Fixed a FreeType bug on 64-bit
  platforms, STR 1235; fixed multiple media selection bugs, STR 1172,
  STR 1204, Foomatic bug 1222120 on Sourceforge; merged in fixes from
  GPL GhostScript repository).

* Sat Jul 16 2005 Till Kamppeter <till@mandrakesoft.com> 8.15-19mdk
- Updated to subversion revision 106 (Fixed GhostScript crashing with
  some PostScript files on 64-bit platforms, STR 1168, bug 16694).

* Thu Jun 16 2005 Till Kamppeter <till@mandrakesoft.com> 8.15-18mdk
- Updated to subversion revision 105 (More bug fixes, especially several
  contributed by Werner Fink from SuSE).

* Thu Apr 21 2005 Till Kamppeter <till@mandrakesoft.com> 8.15-17mdk
- Updated to subversion revision 99/release 8.15.1rc3 (Tons of bug fixes,
  especially broken "ps2epsi", 16-bit/color support for "cups" device/native
  CUPS drivers).

* Wed Mar 30 2005 Till Kamppeter <till@mandrakesoft.com> 8.15-16mdk
- Updated to subversion revision 79 (Several bug fixes, especially
  crashes of "imagen" and "lx5000" drivers, output into a pipe not
  possible for some drivers, ...).

* Thu Mar 17 2005 Till Kamppeter <till@mandrakesoft.com> 8.15-15mdk
- Updated to subversion revision 78 (Several bug fixes, improvement of
  antialiased screen output when using gv or ghostview).
- Added "Conflicts: printer-filters <= 10.1" (bug 14710).

* Tue Mar 08 2005 Till Kamppeter <till@mandrakesoft.com> 8.15-14mdk
- Updated to subversion revision 70 (Deactivated "dmprt", it breaks
  GhostScript completely).

* Mon Mar 07 2005 Till Kamppeter <till@mandrakesoft.com> 8.15-13mdk
- Updated to subversion revision 68 (Added remaining japanese printer
  drivers: "dmprt", "escpage", "lp2000", "npdl", "rpdl").

* Fri Mar 04 2005 Till Kamppeter <till@mandrakesoft.com> 8.15-12mdk
- Updated to subversion revision 67 (Fixed segfaults in "opvp" and "lips4v";
  fixed color handling in "opvp").

* Wed Mar 02 2005 Till Kamppeter <till@mandrakesoft.com> 8.15-11mdk
- Updated to subversion revision 63 (Made PNG devices being compiled).

* Thu Feb 24 2005 Till Kamppeter <till@mandrakesoft.com> 8.15-10mdk
- Updated to subversion revision 62 (Epson Kowa laser printer driver
  added upstream, CUPS driver for PCL-XL improved).

* Mon Feb 21 2005 Till Kamppeter <till@mandrakesoft.com> 8.15-9mdk
- Updated to subversion revision 51 (Fixed segfault of Epson EPL-xxxxL
  driver with KRGB patch).
- Reactivated KRGB.

* Fri Feb 18 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 8.15-8mdk
- drop patch1: fixed upstream

* Thu Feb 17 2005 Till Kamppeter <till@mandrakesoft.com> 8.15-7mdk
- Updated to subversion revision 50 (Added old japanese drivers).

* Wed Feb 16 2005 Till Kamppeter <till@mandrakesoft.com> 8.15-6mdk
- Updated to subversion revision 49 (Many bug fixes, especially "pxlmono"
  driver).
- Temporarily reverted to the original IJS driver from GPL GhostScript, 
  without KRGB, but does not segfault with Epson EPL-xxxxL driver.

* Tue Feb 15 2005 Till Kamppeter <till@mandrakesoft.com> 8.15-5mdk
- Updated to subversion revision 46 (shortly after 8.15.1rc1).
- Added Epson Kowa laser printer drivers (alpha version).
- Cleaned up spec file somewhat.

* Sun Feb 13 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 8.15-4mdk
- Patch1: fix segfault at startup on ppc

* Wed Feb 09 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 8.15-3mdk
- lib64 fixes
- build DSO with PIC

* Sat Jan 29 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 8.15-2mdk
- add BuildRequires: XFree86-devel

* Fri Jan 28 2005 Till Kamppeter <till@mandrakesoft.com> 8.15-1mdk
- Updated to ESP GhostScript 8.15.

