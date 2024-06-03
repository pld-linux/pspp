#
# Conditional build:
%bcond_with	glade	# Glade extensions for PSPP development (broken in 1.4.1)
%bcond_without	perl	# Perl module

Summary:	GNU PSPP - program for statistical analysis of sampled data
Summary(pl.UTF-8):	GNU PSPP - program do analizy statystycznej danych próbkowanych
Name:		pspp
Version:	2.0.1
Release:	2
License:	GPL v3+
Group:		Applications/Science
Source0:	https://ftp.gnu.org/gnu/pspp/%{name}-%{version}.tar.gz
# Source0-md5:	0933860d7d511dac67277ef4829263ce
Patch0:		%{name}-info.patch
Patch1:		%{name}-perl.patch
URL:		http://www.gnu.org/software/pspp/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.14
BuildRequires:	cairo-devel >= 1.5
BuildRequires:	gettext-tools >= 0.20
BuildRequires:	glib2-devel >= 1:2.44
BuildRequires:	gsl-devel >= 1.13
BuildRequires:	gtk+3-devel >= 3.22.0
BuildRequires:	gtksourceview4-devel >= 4.0
%{?with_glade:BuildRequires:	glade-devel >= 3.0}
BuildRequires:	libtool >= 2:2
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	openssl-devel
BuildRequires:	pango-devel >= 1:1.22
BuildRequires:	perl-base >= 5.005_03
%{?with_perl:BuildRequires:	perl-devel >= 1:5.8}
BuildRequires:	pkgconfig
BuildRequires:	postgresql-devel
BuildRequires:	python3 >= 1:3
BuildRequires:	readline-devel
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.745
BuildRequires:	spread-sheet-widget-devel >= 0.7
BuildRequires:	texinfo
# tex
BuildRequires:	texlive
BuildRequires:	zlib-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name}-libs = %{version}-%{release}
Requires:	cairo >= 1.5
Requires:	glib2 >= 1:2.44
Requires:	gtk+3 >= 3.22.0
Requires:	gtksourceview4 >= 4.0
Requires:	pango >= 1:1.22
Requires:	shared-mime-info
Requires:	spread-sheet-widget >= 0.7
%if %{without glade}
Obsoletes:	pspp-glade < 1.4.1
%endif
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

%build
%{__libtoolize}
%{__aclocal} -I gl/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static \
	%{?with_glade:--with-gui-tools} \
	--with-packager="PLD Linux (http://pld-linux.org/)" \
	%{!?with_perl:--without-perl-module}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# program no longer installed, but manual still is... restore for now
install utilities/pspp-dump-sav $RPM_BUILD_ROOT%{_bindir}

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

%post
%update_desktop_database
%update_icon_cache hicolor
%update_mime_database

%postun
%update_desktop_database
%update_icon_cache hicolor
%update_mime_database

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pspp
%attr(755,root,root) %{_bindir}/pspp-output
%attr(755,root,root) %{_bindir}/psppire
%{_datadir}/pspp
%{_datadir}/metainfo/org.gnu.pspp.metainfo.xml
%{_datadir}/mime/packages/org.gnu.pspp.xml
%{_desktopdir}/org.gnu.pspp.desktop
%{_iconsdir}/hicolor/*/apps/org.gnu.pspp.*
%{_iconsdir}/hicolor/*x*/mimetypes/application-x-spss-*.png
%{_infodir}/pspp.info*
%{_infodir}/pspp-dev.info*
%{_infodir}/pspp-figures
%{_infodir}/screenshots
%{_mandir}/man1/pspp.1*
%{_mandir}/man1/pspp-output.1*
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
