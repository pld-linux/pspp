#
# Conditional build:
%bcond_without	glade	# Glade extensions for PSPP development
%bcond_without	perl	# Perl module

%include	/usr/lib/rpm/macros.perl
Summary:	GNU PSPP - program for statistical analysis of sampled data
Summary(pl.UTF-8):	GNU PSPP - program do analizy statystycznej danych próbkowanych
Name:		pspp
Version:	1.2.0
Release:	5
License:	GPL v3+
Group:		Applications/Science
Source0:	http://ftp.gnu.org/gnu/pspp/%{name}-%{version}.tar.gz
# Source0-md5:	e940d666b586f5bd2f17a2b305fac71f
Patch0:		%{name}-info.patch
Patch1:		%{name}-perl.patch
Patch2:		%{name}-glade.patch
URL:		http://www.gnu.org/software/pspp/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.5
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.44
BuildRequires:	gsl-devel >= 1.13
BuildRequires:	gtk+3-devel >= 3.18.0
BuildRequires:	gtksourceview3-devel >= 3.4.2
%{?with_glade:BuildRequires:	glade-devel >= 3.0}
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	openssl-devel
BuildRequires:	pango-devel >= 1:1.22
BuildRequires:	perl-base >= 5.005_03
%{?with_perl:BuildRequires:	perl-devel >= 1:5.8}
BuildRequires:	pkgconfig
BuildRequires:	postgresql-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	spread-sheet-widget-devel >= 0.3
BuildRequires:	texinfo
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	cairo >= 1.5
Requires:	glib2 >= 1:2.32
Requires:	gtk+3 >= 3.14.5
Requires:	gtksourceview3 >= 3.4.2
Requires:	pango >= 1:1.22
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNU PSPP is a program for statistical analysis of sampled data. It is
a Free replacement for the proprietary program SPSS, and appears very
similar to it with a few exceptions.

%description -l pl.UTF-8
GNU PSPP to program do analizy statystycznej danych próbkowanych. Jest
to wolnodostępny zamiennik własnościowego programu SPSS; jest do niego
dosyć podobny z kilkoma wyjątkami.

%package libs
Summary:	GNU PSPP libraries and command line tools
Summary(pl.UTF-8):	Biblioteki GNU PSPP i narzędzia linii poleceń
Group:		Applications/Science
Requires:	gsl >= 1.13
Conflicts:	pspp < 0.8.5-1

%description libs
GNU PSP libraries command line tools.

%description libs -l pl.UTF-8
Biblioteki GNU PSPP i narzędzia linii poleceń.

%package -n perl-PSPP
Summary:	PSPP module for Perl
Summary(pl.UTF-8):	Moduł PSPP dla Perla
Group:		Development/Languages/Perl
Requires:	%{name}-libs = %{version}-%{release}

%description -n perl-PSPP
PSPP Perl module provides an interface to the libraries used by pspp
to read and write system files.

%description -n perl-PSPP -l pl.UTF-8
Moduł Perla PSPP udostępnia interfejs do bibliotek wykorzystywanych
przez pspp do odczytu i zapisu plików systemowych.

%package glade
Summary:	Glade extensions for PSPP development
Summary(pl.UTF-8):	Rozszerzenia Glade do rozwijania PSPP
Group:		X11/Development/Libraries
Requires:	glade >= 3.0

%description glade
Glade extensions for PSPP development.

%description glade -l pl.UTF-8
Rozszerzenia Glade do rozwijania PSPP.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I gl/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static \
	%{?with_glade:--with-gui-tools} \
	--with-openssl \
	--with-packager="PLD Linux (http://pld-linux.org/)" \
	%{!?with_perl:--without-perl-module}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with perl}
%{__make} -C perl-module install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

# API not exported
%{__rm} $RPM_BUILD_ROOT%{_libdir}/pspp/lib{pspp,pspp-core}.{la,so}
%if %{with glade}
# loadable module
%{__rm} $RPM_BUILD_ROOT%{_libdir}/glade/modules/*.la
%endif

%find_lang %{name}

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pspp
%attr(755,root,root) %{_bindir}/psppire
%{_datadir}/pspp
%{_datadir}/appdata/pspp.appdata.xml
%{_desktopdir}/pspp.desktop
%{_iconsdir}/hicolor/*/apps/pspp.*
%{_iconsdir}/hicolor/*/mimetypes/application-x-spss-*.png
%{_infodir}/pspp.info*
%{_infodir}/pspp-dev.info*
%{_mandir}/man1/pspp.1*
%{_mandir}/man1/psppire.1*

%files libs
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS ONEWS README THANKS
%attr(755,root,root) %{_bindir}/pspp-convert
%attr(755,root,root) %{_bindir}/pspp-dump-sav
%dir %{_libdir}/pspp
%attr(755,root,root) %{_libdir}/pspp/libpspp-%{version}.so
%attr(755,root,root) %{_libdir}/pspp/libpspp-core-%{version}.so
%{_mandir}/man1/pspp-convert.1*
%{_mandir}/man1/pspp-dump-sav.1*

%if %{with perl}
%files -n perl-PSPP
%defattr(644,root,root,755)
%{perl_vendorarch}/PSPP.pm
%dir %{perl_vendorarch}/auto/PSPP
%attr(755,root,root) %{perl_vendorarch}/auto/PSPP/PSPP.so
%{_mandir}/man3/PSPP.3pm*
%{_mandir}/man3/PSPP::Examples.3pm*
%endif

%if %{with glade}
%files glade
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/glade/modules/libglade-psppire.so
%{_datadir}/glade/catalogs/psppire.xml
%{_datadir}/glade/pixmaps/hicolor/16x16/actions/widget-psppire-psppire-*.png
%{_datadir}/glade/pixmaps/hicolor/22x22/actions/widget-psppire-psppire-*.png
%endif
