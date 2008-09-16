##### VERSION NUMBERS

%define gsversion 8.63
%define gsextraversion %{nil}
%define gsreleaseno 62
%define gsrelease %mkrel %gsreleaseno
%define gssvnrevision -rev183
%define ijsver 0.35
%define ijsreloffset 0
%define ijsrelno %(echo $((%{gsreleaseno} + %{ijsreloffset})))
%define ijsrel %mkrel %ijsrelno
%define ijsmajor 1
%define libijs %mklibname ijs %{ijsmajor}
%define libijs_devel %mklibname -d ijs %{ijsmajor}
%define gsmajor 8
%define libgs %mklibname gs %{gsmajor}
%define libgs_devel %mklibname -d gs %{gsmajor}

##### BUILD OPTIONS

%define GSx11SVGAmodule 1
%define withsvgalib 0
%define withcupsfilters 1
%define withstaticgs 0
%define debug 0

##### GENERAL DEFINITIONS

Summary:	PostScript/PDF interpreter and renderer (Main executable)
Name:		ghostscript
Version:	%{gsversion}%{gsextraversion}
Release:	%{gsrelease}
License:	GPLv2+
Group:		Publishing
Requires: 	ghostscript-common
Requires:	update-alternatives
Obsoletes:	ghostscript-PrintOnly
Provides:	ghostscript-PrintOnly
%if !%{GSx11SVGAmodule}
Obsoletes:	ghostscript-module-X ghostscript-module-SVGALIB
Provides:	ghostscript-module-X ghostscript-module-SVGALIB
%endif
%if !%{withstaticgs}
Obsoletes:	ghostscript-static
Provides:	ghostscript-static
%endif
Conflicts:	omni < 0.4 cups <= 1.1.14
Conflicts:	printer-filters <= 10.1
URL:		http://www.ghostscript.com/awki/Index

##### BUILDREQUIRES

BuildRequires: autoconf2.5
BuildRequires: bison
BuildRequires: flex
BuildRequires: freetype-devel
BuildRequires: gettext-devel
BuildRequires: glibc-devel
BuildRequires: gtk+2-devel
BuildRequires: libcups-devel >= 1.2.0-0.5361.0mdk
BuildRequires: libfontconfig-devel
BuildRequires: libice-devel
BuildRequires: libnetpbm-devel
BuildRequires: libpng-devel
BuildRequires: libsm-devel
BuildRequires: libtiff-devel
BuildRequires: libx11-devel
BuildRequires: libxext-devel
BuildRequires: libxml-devel
BuildRequires: libxt-devel
BuildRequires: unzip
BuildRequires: zlib1-devel

%ifarch %ix86
%if %{withsvgalib}
BuildRequires:	svgalib-devel
%endif
%endif

##### GHOSTSCRIPT SOURCES

Source0:	ftp://mirror.cs.wisc.edu/pub/mirrors/ghost/GPL/gs860/ghostscript-%{gsversion}%{gsextraversion}.tar.bz2
Source1:        ftp://ftp.uu.net/graphics/jpeg/jpegsrc.v6b.tar.bz2
Source2:	ps2pdfpress.bz2
Source3:	http://www.linuxprinting.org/download/printing/sipixa6.upp.bz2

##### GHOSTSCRIPT PATCHES

Patch2:	espgs-8.15-windev-pdf-compatibility.patch
Patch3: ghostscript-8.60-x11_shared.patch
Patch4: CVE-2008-0411.patch

##### LIBIJS PATCHES

# Fortunately none currently

##### BUILD ROOT

BuildRoot:	%_tmppath/%name-%gsversion-%gsrelease-root

##### PACKAGE DESCRIPTIONS

##### GHOSTSCRIPT

%package dvipdf
Summary: PostScript/PDF interpreter and renderer (DVI-to-PDF converter)
Group: 		Publishing
Requires: 	ghostscript, coreutils
Requires:	tetex-dvips

%package common
Summary: PostScript/PDF interpreter and renderer (Common files)
Group: 		Publishing
Requires:	urw-fonts >= 1.1, ghostscript-fonts, perl
Conflicts:	ghostscript < 8.15-27mdk
%ifarch x86_64
Conflicts:	cups < 1.2.0-0.5361.0mdk
%endif

%package X
Summary: PostScript/PDF interpreter and renderer (Executable with GTK-based screen display)
Group: 		Publishing
Requires: 	ghostscript-common
Requires:	update-alternatives
# This one is buggy, so do not let it get automatically installed by
# the "Provides: ghostscript"
#Provides:	ghostscript = %{version}-%{release}

%if %withstaticgs
%package static
Summary: PostScript/PDF interpreter and renderer (Static executable)
Group: 		Publishing
Requires: 	ghostscript-common
Requires:	update-alternatives
Provides:	ghostscript = %{version}-%{release}
%endif

%if %{GSx11SVGAmodule}
%package module-X
Summary: PostScript/PDF interpreter and renderer (Additional support for X)
Group: 		Publishing
Requires: 	ghostscript-common
Conflicts: 	ghostscript-X < 8.15
Obsoletes:	ghostscript-Both
Provides: 	ghostscript-Both

%ifarch %ix86
%if %{withsvgalib}
%package module-SVGALIB
Summary: PostScript/PDF interpreter and renderer (Additional support for SVGALIB)
Group: 		Publishing
Requires: 	ghostscript, coreutils
Obsoletes: 	ghostscript-SVGALIB, ghostscript-Both
Provides: 	ghostscript-SVGALIB, ghostscript-Both
%endif
%endif
%endif

%package -n %libgs
Summary: PostScript/PDF interpreter and renderer (GhostScript shared library)
Group: Publishing

%package -n %libgs_devel
Summary: Headers and links to compile against the "%{libgs}" library
Group: Development/C
Requires: %libgs = %version
Provides: libgs-devel

##### IJS

%package -n %{libijs}
Version:	%{ijsver}
Release:	%{ijsrel}
Summary:	Dynamic library for the IJS printer driver plug-in interface
Group:		Publishing
URL:		http://www.linuxprinting.org/ijs/
Provides:       libijs = %{ijsver}-%{ijsrel}

%package -n %{libijs_devel}
Version:	%{ijsver}
Release:	%{ijsrel}
Summary:	Headers and links for compiling against the "%{libijs}" library
Group:		Development/C
URL:		http://www.linuxprinting.org/ijs/
Requires:       %{libijs} = %{ijsver} multiarch-utils
Provides:       libijs-devel = %{ijsver}-%{ijsrel}
Provides:       ijs-devel = %{ijsver}-%{ijsrel}

%package doc
Summary:	Documentation for GhostScript
Group:		Publishing

##### DESCRIPTION TEXTS

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

%description dvipdf
Tool to convert the DVI format of TeX into the PDF format. There are
more such tools (for different quality levels) in the tetex-dvipdfm
package. All these tools use dvips of TeX to convert the DVI file to
PostScript, then they use GhostScript to generate the PDF file.

%description common
Ghostscript is a PostScript/PDF interpreter. It can render both
PostScript and PDF files to devices which include X window, many
printer formats, and popular graphics file formats.

This package contains the common data files needed by GhostScript.

%description X
Ghostscript is a PostScript/PDF interpreter. It can render both
PostScript and PDF files to devices which include X window, many
printer formats, and popular graphics file formats.

This package contains a GhostScript executable with GTK-based X
display support ("display" device, default, so it displays files by
simply entering "gs <file>" on the command line). It makes use of the
GhostScript shared library.

%if %withstaticgs
%description static
Ghostscript is a PostScript/PDF interpreter. It can render both
PostScript and PDF files to devices which include X window, many
printer formats, and popular graphics file formats.

This package contains a GhostScript executable which does not need the
GhostScript shared library. To get simple X display support, the
ghostscript-module-X package must be installed in addition.
%endif

%if %{GSx11SVGAmodule}
%description module-X
Ghostscript is a PostScript/PDF interpreter. It can render both
PostScript and PDF files to devices which include X window, many
printer formats, and popular graphics file formats.

This package enhances Ghostscript with X window support

%ifarch %ix86
%if %{withsvgalib}
%description module-SVGALIB
Ghostscript is a PostScript/PDF interpreter. It can render both
PostScript and PDF files to devices which include X window, many
printer formats, and popular graphics file formats.

This package enhances Ghostscript with console output using SVGALIB.
%endif
%endif
%endif

%description -n %libgs
This is the API library for programs which use the PostScript and/or
PDF interpreters of GhostScript.

%description -n %libgs-devel
This package contains the static library and the header files needed
to compile applications using the GhostScript shared library.

%description -n %{libijs}
This is the API library for programs using the IJS printer driver
plug-in interface. Printer drivers using this interface can be added
to GhostScript (6.53 or newer) without needing to rebuild
GhostScript. Application programs providing an IJS interface can make
use of IJS printer drivers directly, without needing GhostScript.

%description -n %{libijs_devel}
This package contains the static library and the header files needed
to compile applications using the IJS library.

%description doc
This package contains documentation for GhostScript.

%prep
##### GHOSTSCRIPT
%setup -q

# unpack jpeg
%setup -q -T -D -a 1
# For GhostScript, rename jpeg subdirectory
mv jpeg-6b jpeg

cd lib
%patch2 -p0 -b .windev-pdf
cd ..

%patch3 -p1 -b .shared

%patch4 -p0 -b .CVE-2008-0411

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

##### IJS

cd ijs*
# Rebuild broken build infrastructure
# Needed by patch4.
./autogen.sh
%configure --enable-shared
%make
cd ..

##### GHOSTSCRIPT

# We have a Subversion version, so we must re-generate "configure"
# <mrl> 20070827 not anymore
#./autogen.sh

%configure \
	--enable-dynamic \
	--enable-fontconfig \
	--with-cups \
	--with-drivers=ALL,opvp \
	--with-fontpath="/usr/share/fonts/default/ghostscript:/usr/share/fonts/default/type1:/usr/share/ghostscript/fonts:/usr/share/ghostscript/%{gsversion}/Resource:/usr/share/ghostscript/Resource:/usr/share/ghostscript/CIDFont:/usr/share/fonts/ttf:/usr/share/fonts/type1:/usr/share/fonts/default/Type1" \
	--with-ijs \
	--with-omni \
	--with-x

# Drivers which do not compile: 
# Needs newsiop/lbp.h: nwp533
# Needs sys/ioccom.h: sparc
# Needs unbdev/lpviio.h: sparc

# Set documentation dir
perl -p -i -e 's|^(docdir=).*$|$1\$\(datadir\)/doc/%{name}-doc-%{gsversion}|' Makefile

# Fix references to X11 libraries
perl -p -i -e "s|(/usr/X11R6)/lib\b|\1/%{_lib}|g" Makefile src/*.mak

# Correct paths for CJK fonts
perl -p -i -e "s:/usr/share/ghostscript/:/usr/share/ghostscript/Resource/:g" lib/gs_res.ps
perl -p -i -e "s:ghostscript/Resource/fonts:ghostscript/Resource/Font:g" lib/gs_res.ps

# Do not use "-ansi" in gcc calls
perl -p -i -e "s:-ansi::g" Makefile

# The RPM macro for make is not used here, as parallelization of the build 
# process does not work.
%if %withstaticgs
make
%else
%if %GSx11SVGAmodule
make STDDIRS
make obj/X11.so
%endif
%endif
make so
#make pcl3opts

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
install -d %{buildroot}%{_prefix}/lib/cups
install -d %{buildroot}%{_datadir}/cups/model
install -d %{buildroot}%{_sysconfdir}/cups

##### IJS
cd ijs*
./configure --enable-shared --prefix=%buildroot%{_prefix} --libdir=%buildroot%{_libdir}
# Work around bug in "configure" script
perl -p -i -e 's/\@OBJEXT\@/o/g' Makefile
perl -p -i -e 's/\@EXEEXT\@//g' Makefile
%makeinstall
# Fix prefixes in scripts
perl -p -i -e "s:%buildroot::g" %buildroot%{_bindir}/ijs-config
perl -p -i -e "s:%buildroot::g" %buildroot%{_libdir}/pkgconfig/ijs.pc
cd ..

##### GHOSTSCRIPT
mkdir -p %{buildroot}%{_docdir}/ghostscript-doc-%{gsversion}

%if %withstaticgs
make \
	prefix=%{buildroot}/usr \
	DESTDIR=%{buildroot} \
	gssharedir=%{buildroot}%{_libdir}/ghostscript/%{gsversion} \
	docdir=%{_docdir}/ghostscript-doc-%{gsversion} \
	bindir=%{buildroot}%{_bindir} \
	mandir=%{buildroot}%{_mandir} \
	install
%else
make \
	prefix=%{_prefix} \
	DESTDIR=%{buildroot} \
	gssharedir=%{_libdir}/ghostscript/%{gsversion} \
	docdir=%{_docdir}/ghostscript-doc-%{gsversion} \
	bindir=%{_bindir} \
	mandir=%{_mandir} \
	install-cups

%if %GSx11SVGAmodule
make \
	prefix=%{_prefix} \
	DESTDIR=%{buildroot} \
	gssharedir=%{_libdir}/ghostscript/%{gsversion} \
	docdir=%{_docdir}/ghostscript-doc-%{gsversion} \
	bindir=%{_bindir} \
	mandir=%{_mandir} \
	install-shared
%endif
%endif

%if 0
make \
	prefix=%{_prefix} \
	DESTDIR=%{buildroot} \
	gssharedir=%{_libdir}/ghostscript/%{gsversion} \
	docdir=%{_docdir}/ghostscript-doc-%{gsversion} \
	bindir=%{_bindir} \
	mandir=%{_mandir} \
	man1dir=%{_mandir}/man1 \
	pcl3-install
%endif

make \
	prefix=%{_prefix} \
	DESTDIR=%{buildroot} \
	gssharedir=%{_libdir}/ghostscript/%{gsversion} \
	docdir=%{_docdir}/ghostscript-doc-%{gsversion} \
	bindir=%{_bindir} \
	libdir=%{_libdir} \
	mandir=%{_mandir} \
	soinstall

ln -sf gs.1.bz2 %{buildroot}%{_mandir}/man1/ghostscript.1.bz2

%if %withstaticgs
mv %{buildroot}%{_bindir}/gs %{buildroot}%{_bindir}/gs-static
%endif

# ps2pdfpress
install -m 755 ps2pdfpress %{buildroot}%{_bindir}

# UPP file for SiPix Pocket Printer A6
install -m 644 sipixa6.upp %{buildroot}%{_datadir}/ghostscript/%{gsversion}/lib/

%if %{withcupsfilters}
%if 0
# "pstoraster" wrapper script to make GhostScript being used as the
# cups-internal RIP
install -d %{buildroot}%{_libdir}/cups/filter
install -m 755 pstoraster/pstoraster %{buildroot}%{_libdir}/cups/filter
install -m 755 pstoraster/pstopxl %{buildroot}%{_libdir}/cups/filter
install -d %{buildroot}%{_datadir}/cups/model
install -m 755 pstoraster/*.ppd %{buildroot}%{_datadir}/cups/model
install -d %{buildroot}%{_sysconfdir}/cups
install -m 644 pstoraster/pstoraster.convs %{buildroot}%{_sysconfdir}/cups
%endif
%endif

# Add backward compatibility link to not break printerdrake in Mandriva
# 2006 and older
ln -s %{_bindir}/gsc %{buildroot}%{_bindir}/gs-common
ln -s %{_bindir}/gsc %{buildroot}%{_bindir}/ghostscript

##### GENERAL STUFF

# Correct permissions for all documentation files
chmod -R a+rX %{buildroot}%{_docdir}
chmod -R go-w %{buildroot}%{_docdir}
chmod -R u+w %{buildroot}%{_docdir}

##### FILES

%files
%defattr(-,root,root)
%{_bindir}/gsc
%{_bindir}/gs-common
%{_bindir}/ghostscript

%files X
%defattr(-,root,root)
%{_bindir}/gsx

%if %withstaticgs
%files static
%defattr(-,root,root)
%{_bindir}/gs-static
%endif

%files common
%defattr(-,root,root)
%dir %{_datadir}/ghostscript
%{_datadir}/ghostscript/%{gsversion}
#%{_datadir}/ghostscript/Resource
#%{_datadir}/ghostscript/CIDFont
%{_mandir}/man1/*
%lang(de) %{_mandir}/de/man1/*
%{_bindir}/[a-c]*
%{_bindir}/dumphint
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
%config(noreplace) %{_sysconfdir}/cups/pstoraster.convs
%endif

%files doc
%defattr(-,root,root)
%doc %{_docdir}/ghostscript-doc-%{gsversion}

%files dvipdf
%defattr(-,root,root)
%{_bindir}/dvipdf

%if %{GSx11SVGAmodule}
%files module-X
%defattr(-,root,root)
%doc README.shared.mandrivalinux
%dir %{_libdir}/ghostscript/%{gsversion}
%{_libdir}/ghostscript/%{gsversion}/X11.so

%ifarch %ix86
%if %{withsvgalib}
%files module-SVGALIB
%defattr(-,root,root)
%doc README.shared.mandrivalinux
%dir %{_libdir}/ghostscript/%{gsversion}
%{_libdir}/ghostscript/%{gsversion}/lvga256.so
%{_libdir}/ghostscript/%{gsversion}/vgalib.so
%endif
%endif
%endif

%files -n %{libgs}
%defattr(-,root,root)
%{_libdir}/libgs.so.*

%files -n %{libgs_devel}
%defattr(-,root,root)
%{_libdir}/libgs.so
%{_includedir}/ghostscript

%files -n %{libijs}
%defattr(-,root,root)
%{_libdir}/libijs*.so

%files -n %{libijs_devel}
%defattr(-,root,root)
%doc ijs/README
%{_libdir}/libijs.a
%{_libdir}/libijs.la
%{_libdir}/libijs.so
%{_libdir}/pkgconfig/ijs.pc
%{_includedir}/ijs
%{_bindir}/ijs_client_example
%{_bindir}/ijs_server_example
%{_bindir}/ijs-config


##### PRE/POSTINSTALL SCRIPTS

%post
# Set up update-alternatives entries
%{_sbindir}/update-alternatives --install %{_bindir}/gs gs %{_bindir}/gsc 200

%post X
# Set up update-alternatives entries
%{_sbindir}/update-alternatives --install %{_bindir}/gs gs %{_bindir}/gsx 100

%if %withstaticgs
%post static
# Set up update-alternatives entries
%{_sbindir}/update-alternatives --install %{_bindir}/gs gs %{_bindir}/gs-static 10
%endif

%post common
# Initialize japanese fonts
if test -f /usr/share/fonts/ttf/japanese/cidinst; then
    sh /usr/share/fonts/ttf/japanese/cidinst
fi

%if %mdkversion < 200900
%post -n %{libijs} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libgs} -p /sbin/ldconfig
%endif

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

%if %withstaticgs
%preun static
if [ "$1" = 0 ]; then
  # Remove update-alternatives entry
  %{_sbindir}/update-alternatives --remove gs %{_bindir}/gs-static
fi
%endif

%if %mdkversion < 200900
%postun -n %{libijs} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libgs} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}
