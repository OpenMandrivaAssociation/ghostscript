# libgs is used by libspectre, libspectre is used by cairo,
# cairo is used by gtk-3.0, gtk-3.0 is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

%bcond_without ijs
%bcond_with crosscompile
%bcond_with bootstrap
%bcond_without GSx11SVGAmodule
%bcond_with debug

%define _disable_ld_no_undefined 1

%define gsver 9.56.0
%define ijsver 0.35
# (tpg) BUMP THIS EVERY UPDATE, RESET WHEN IJSVER INCREASES
%define ijsreloffset 107
%define ijsrel %(echo $((%(echo %{release} |cut -d. -f1) + %{ijsreloffset})))
%define nodot_ver %(echo %{gsver} |sed -e 's,\\.,,g')

%define ijsmajor 1
%define libijs %mklibname ijs %{ijsmajor}
%define libijs_devel %mklibname -d ijs

%define gsmajor 9
%define libgs %mklibname gs %{gsmajor}
%define libgs_devel %mklibname -d gs
%define libgxps %mklibname gxps %{gsmajor}
%define libgpdl %mklibname gpdl %{gsmajor}
%define libgpcl6 %mklibname gpcl6 %{gsmajor}
%define lib32gs %mklib32name gs %{gsmajor}
%define lib32gs_devel %mklib32name -d gs
%define lib32gxps %mklib32name gxps %{gsmajor}
%define lib32gpdl %mklib32name gpdl %{gsmajor}
%define lib32gpcl6 %mklib32name gpcl6 %{gsmajor}

#define pre rc2

Summary:	PostScript/PDF interpreter and renderer (Main executable)
Name:		ghostscript
Version:	%{gsver}
Release:	%{-pre:0.%{pre}.}1
License:	AGPLv3
Group:		Publishing
URL:		http://www.ghostscript.com/awki/Index
Source0:	https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs%{nodot_ver}%{?pre:%{pre}}/ghostpdl-%{version}%{?pre:%{pre}}.tar.xz
Source2:	ps2pdfpress.bz2
Source3:	http://www.linuxprinting.org/download/printing/sipixa6.upp.bz2
Source4:	ghostscript.rpmlintrc

#Patch300:	ghostscript-9.05-x11_shared.diff
# Fix some shell scripts
Patch2:		ghostscript-scripts.patch
Patch3:		ghostpdl-9.56.0rc2-compile.patch
# Fix ./autgen.sh in ijs sub-project
# See http://bugs.ghostscript.com/show_bug.cgi?id=692040 for details.
#Patch4:		ghostscript-ijs-automake-ver.patch
# Define .runlibfileifexists.
Patch5:		ghostscript-runlibfileifexists.patch
# Restored Fontmap.local patch, incorrectly dropped after
# ghostscript-8.15.4-3 (bug #610301).
# Note: don't use -b here to avoid the backup file ending up in the
# package manifest.
Patch27:	ghostscript-Fontmap.local.patch
# Don't assume %%rom%% device is available for initial ICC profile dir.
#Patch28: ghostscript-iccprofiles-initdir.patch
# gdevcups: don't use uninitialized variables in debugging output.
#Patch29:	ghostscript-gdevcups-debug-uninit.patch
Patch31:	objarch-aarch64.patch
Patch32:	ghostscript-9.14-system-zlib.patch
Patch33:	ghostpdl-9.51-dprintf.patch
Patch34:	ghostpdl-9.52-system-jpeg-buildfix.patch

%if !%{with bootstrap}
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(fontconfig)
%endif
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	unzip
BuildRequires:	gettext-devel
BuildRequires:	glibc-devel
BuildRequires:	pkgconfig(jbig2dec)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	libpaper-devel
BuildRequires:	netpbm-devel
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(jasper)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(libidn2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libopenjp2)
BuildRequires:	pkgconfig(com_err)
BuildRequires:	pkgconfig(krb5)
BuildRequires:	cups-devel

Requires:	ghostscript-common
Requires:	update-alternatives
%if !%{with GSx11SVGAmodule}
%rename	ghostscript-module-X
%rename ghostscript-module-SVGALIB
%endif

%if %{with compat32}
BUildRequires:	devel(libjpeg)
BuildRequires:	devel(libjbig2dec)
BuildRequires:	devel(libopenjp2)
BuildRequires:	devel(libxml2)
BuildRequires:	devel(libtiff)
BuildRequires:	devel(libfreetype)
BuildRequires:	devel(libICE)
BuildRequires:	devel(liblcms2)
BuildRequires:	devel(libidn2)
BuildRequires:	devel(libpng16)
BuildRequires:	devel(libcom_err)
BuildRequires:	devel(libkrb5)
BuildRequires:	devel(libdbus-1)
BuildRequires:	devel(libz)
BuildRequires:	devel(libbz2)
BuildRequires:	devel(libcups)
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

%package pcl6
Summary:	PCL6 interpreter and renderer
Group:		Publishing
Requires:	ghostscript-common

%description pcl6
GhostPDL is a PCL6 interpreter. It can render PCL6
files to devices which include X window, many
printer formats, and popular graphics file formats.

%package xps
Summary:	XPS interpreter and renderer
Group:		Publishing
Requires:	ghostscript-common

%description xps
GhostPDL is an XPS interpreter. It can render XPS
files to devices which include X window, many
printer formats, and popular graphics file formats.

%package pdl
Summary:	PDL interpreter and renderer
Group:		Publishing
Requires:	ghostscript-common

%description pdl
GhostPDL is a PDL interpreter. It can render PDL
files to devices which include X window, many
printer formats, and popular graphics file formats.

%if %{with GSx11SVGAmodule}
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
Requires:	%{libgs} >= %{EVRD}
Requires:	ghostscript = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{_lib}gs9-devel < %{EVRD}
Obsoletes:	%{_lib}gs8-devel < %{EVRD}

%description -n %{libgs_devel}
This package contains the static library and the header files needed
to compile applications using the GhostScript shared library.

%package -n %{libgxps}
Summary:	XPS interpreter and renderer (GhostScript shared library)
Group:		Publishing

%description -n %{libgxps}
This is the API library for programs which use the XPS
interpreter of GhostScript.

%package -n %{libgpdl}
Summary:	PDL interpreter and renderer (GhostScript shared library)
Group:		Publishing

%description -n %{libgpdl}
This is the API library for programs which use the XPS
interpreter of GhostScript.

%package -n %{libgpcl6}
Summary:	PCL6 interpreter and renderer (GhostScript shared library)
Group:		Publishing

%description -n %{libgpcl6}
This is the API library for programs which use the PCL6
interpreters of GhostScript.

%package doc
Summary:	Documentation for GhostScript
Group:		Publishing
Requires:	ghostscript

%description doc
This package contains documentation for GhostScript.

%if %{with compat32}
%package -n %{lib32gs}
Summary:	PostScript/PDF interpreter and renderer (GhostScript shared library) (32-bit)
Group:		Publishing

%description -n %{lib32gs}
This is the API library for programs which use the PostScript and/or
PDF interpreters of GhostScript.

%package -n %{lib32gs_devel}
Summary:	Headers and links to compile against the "%{libgs}" library (32-bit)
Group:		Development/C
Requires:	%{libgs_devel} = %{EVRD}
Requires:	%{lib32gs} >= %{EVRD}

%description -n %{lib32gs_devel}
This package contains the static library and the header files needed
to compile applications using the GhostScript shared library.

%package -n %{lib32gxps}
Summary:	XPS interpreter and renderer (GhostScript shared library)
Group:		Publishing

%description -n %{lib32gxps}
This is the API library for programs which use the XPS
interpreter of GhostScript.

%package -n %{lib32gpdl}
Summary:	PDL interpreter and renderer (GhostScript shared library)
Group:		Publishing

%description -n %{lib32gpdl}
This is the API library for programs which use the PDL
interpreter of GhostScript.

%package -n %{lib32gpcl6}
Summary:	PCL6 interpreter and renderer (GhostScript shared library)
Group:		Publishing

%description -n %{lib32gpcl6}
This is the API library for programs which use the PCL6
interpreters of GhostScript.
%endif

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
Provides:	libijs-devel = %{ijsver}-%{ijsrel}
Provides:	ijs-devel = %{ijsver}-%{ijsrel}
Obsoletes:	%{_lib}ijs1-devel < %{ijsver}-%{ijsrel}

%description -n %{libijs_devel}
This package contains the static library and the header files needed
to compile applications using the IJS library.


%prep
%autosetup -p1 -n ghostpdl-%{gsver}%{?pre:%pre}
%config_update
[ -e autogen.sh ] && ./autogen.sh

#backup files not needed
find . -name "*.*~" |xargs rm -f
# prevent building and using bundled libs
rm -rf jbig2dec libpng jpeg tiff zlib lcms2 freetype cups/libs openjpeg

# Convert manual pages to UTF-8
from8859_1() {
        iconv -f iso-8859-1 -t utf-8 < "$1" > "${1}_"
        mv "${1}_" "$1"
}
for i in man/de/*.1; do from8859_1 "$i"; done

# Stuff for shared library support to ghostscript.
%if %{with GSx11SVGAmodule}
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

export CONFIGURE_TOP="$(pwd)"
%if %{with compat32}
mkdir build32
cd build32
%configure32 \
	--without-x \
	--disable-gtk \
	--enable-shared \
	--disable-static \
	--enable-dynamic \
	--enable-fontconfig \
	--enable-dbus
sed -i -e 's,include base,include ../base,g' Makefile
ln -s ../tesseract .
ln -s ../leptonica .
%make_build so
%endif

%build
%if %{with crosscompile}
export ac_cv_c_bigendian=yes
%endif
# Change compiler flags for debugging when in debug mode
%if %{with debug}
export DONT_STRIP=1
export CFLAGS="$(echo %{optflags} |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/')"
export CXXFLAGS="$(echo %{optflags} |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/')"
export RPM_OPT_FLAGS="$(echo %{optflags} |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/')"
%endif

%if %{with ijs}
pushd ijs*
# Rebuild broken build infrastructure
# Needed by patch4.
./autogen.sh
%configure \
%ifarch %{ix86}
	--disable-sse2 \
%endif
	--enable-shared \
	--disable-static

%make_build
popd
%endif

# We have a Subversion version, so we must re-generate "configure"
#./autogen.sh
%configure \
	--enable-dynamic \
%if !%{with bootstrap}
	--enable-fontconfig \
%endif
%ifarch %{ix86}
	--disable-sse2 \
%endif
	--with-drivers=ALL,opvp \
	--with-fontpath="/usr/share/fonts/default/ghostscript:/usr/share/fonts/default/type1:/usr/share/ghostscript/fonts:/usr/share/ghostscript/%{gsver}/Resource:/usr/share/ghostscript/Resource:/usr/share/ghostscript/CIDFont:/usr/share/fonts/ttf:/usr/share/fonts/type1:/usr/share/fonts/default/Type1" \
%if %{with ijs}
	--with-ijs \
%endif
	--without-omni \
	--with-x \
	--disable-compile-inits \
	--with-system-libtiff \
	--enable-dbus \
	--enable-dynamic

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
%if %{with GSx11SVGAmodule}
#make STDDIRS
%make_build obj/X11.so
%endif
%make_build so
#make pcl3opts
%make_build cups

%install
# Change compiler flags for debugging when in debug mode
%if %{with debug}
export DONT_STRIP=1
export CFLAGS="$(echo %{optflags} |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/')"
export CXXFLAGS="$(echo %{optflags} |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/')"
export RPM_OPT_FLAGS="$(echo %{optflags} |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/')"
%endif

# Make directories
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_mandir}/man1

pushd ijs*
%configure \
	--enable-shared \
	--prefix=%{buildroot}%{_prefix} \
	--libdir=%{buildroot}%{_libdir}

# Work around bug in "configure" script
perl -p -i -e 's/\@OBJEXT\@/o/g' Makefile
perl -p -i -e 's/\@EXEEXT\@//g' Makefile
%makeinstall
# Fix prefixes in scripts
perl -p -i -e "s:%{buildroot}::g" %{buildroot}%{_libdir}/pkgconfig/ijs.pc
popd

##### GHOSTSCRIPT
mkdir -p %{buildroot}%{_docdir}/ghostscript-doc-%{gsver}

%if %{with compat32}
cd build32
make \
	prefix=%{_prefix} \
	DESTDIR=%{buildroot} \
	gssharedir=%{_libdir}/ghostscript/%{gsver} \
	docdir=%{_docdir}/ghostscript-doc-%{gsver} \
	bindir=%{_bindir} \
	libdir=%{_prefix}/lib \
	mandir=%{_mandir} \
	soinstall
cd ..
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

%if %{with GSx11SVGAmodule}
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

# GhostPDL and GhostXPS
cp -a sobin/gpcl* sobin/gxps* %{buildroot}%{_bindir}
#cp -a sobin/libgpcl* sobin/libgxps* %{buildroot}%{_libdir}

# Add backward compatibility link to not break printerdrake in Mandriva
# 2006 and older
ln -s %{_bindir}/gsc %{buildroot}%{_bindir}/gs-common
ln -s %{_bindir}/gsc %{buildroot}%{_bindir}/ghostscript

# Correct permissions for all documentation files
chmod -R a+rX %{buildroot}%{_docdir}
chmod -R go-w %{buildroot}%{_docdir}
chmod -R u+w %{buildroot}%{_docdir}

# Fix symlink to buildroot
rm -f %{buildroot}%{_datadir}/ghostscript/%{gsver}/doc
ln -s %{_docdir}/ghostscript-doc-%{gsver} %{buildroot}%{_datadir}/ghostscript/%{gsver}/doc

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

%files pcl6
%{_bindir}/gpcl6c

%files xps
%{_bindir}/gxpsc

%files pdl
%{_bindir}/gpdlc

%files common
%dir %{_datadir}/ghostscript
%{_datadir}/ghostscript/%{gsver}
%doc %{_mandir}/man1/*
%lang(de) %{_mandir}/de/man1/*
#%{_bindir}/[a-c]*
#{_bindir}/dumphint
%{_bindir}/[e-f]*
#{_bindir}/gs-common
%{_bindir}/gs[a-b]*
%{_bindir}/gs[d-n]*
%{_bindir}/[j-l]*
%{_bindir}/[n-z]*

%files doc
%doc %{_docdir}/ghostscript-doc-%{gsver}

%files dvipdf
%{_bindir}/dvipdf

%if %{with GSx11SVGAmodule}
%files module-X
%doc README.shared.mandrivalinux
%dir %{_libdir}/ghostscript/%{gsver}
%{_libdir}/ghostscript/%{gsver}/X11.so
%endif

%files -n %{libgs}
%{_libdir}/libgs.so.*%{gsmajor}*

%files -n %{libgs_devel}
%{_libdir}/libgs.so
%{_libdir}/libgxps.so
%{_libdir}/libgpdl.so
%{_libdir}/libgpcl6.so
%{_includedir}/ghostscript

%files -n %{libgxps}
%{_libdir}/libgxps.so.*%{gsmajor}*

%files -n %{libgpdl}
%{_libdir}/libgpdl.so.*%{gsmajor}*

%files -n %{libgpcl6}
%{_libdir}/libgpcl6.so.*%{gsmajor}*

%files -n %{libijs}
%{_libdir}/libijs-%{ijsver}.so

%files -n %{libijs_devel}
%doc ijs/README
%{_libdir}/libijs.so
%{_libdir}/pkgconfig/ijs.pc
%{_includedir}/ijs
%{_bindir}/ijs_client_example
%{_bindir}/ijs_server_example

%if %{with compat32}
%files -n %{lib32gs}
%{_prefix}/lib/libgs.so.*%{gsmajor}*

%files -n %{lib32gpcl6}
%{_prefix}/lib/libgpcl6.so.*%{gsmajor}*

%files -n %{lib32gpdl}
%{_prefix}/lib/libgpdl.so.*%{gsmajor}*

%files -n %{lib32gxps}
%{_prefix}/lib/libgxps.so.*%{gsmajor}*

%files -n %{lib32gs_devel}
%{_prefix}/lib/libgs.so
%{_prefix}/lib/libgpcl6.so
%{_prefix}/lib/libgpdl.so
%{_prefix}/lib/libgxps.so
%endif
