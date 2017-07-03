Summary:	GNU PSPP - program for statistical analysis of sampled data
Summary(pl.UTF-8):	GNU PSPP - program do analizy statystycznej danych próbkowanych
Name:		pspp
Version:	0.10.2
Release:	1
License:	GPL v3+
Group:		Applications/Science
Source0:	http://ftp.gnu.org/gnu/pspp/%{name}-%{version}.tar.gz
# Source0-md5:	9c5a3295d59b07a9a4462148371723ae
Patch0:		%{name}-info.patch
Patch1:		perl-no-dot-in-inc.patch
URL:		http://www.gnu.org/software/pspp/
BuildRequires:	cairo-devel >= 1.5
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.32
BuildRequires:	gsl-devel >= 1.13
BuildRequires:	gtk+3-devel >= 3.4.2
BuildRequires:	gtksourceview3-devel >= 3.4.2
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	pango-devel >= 1:1.22
BuildRequires:	perl-base >= 5.005_03
BuildRequires:	pkgconfig
BuildRequires:	postgresql-devel
BuildRequires:	readline-devel
BuildRequires:	texinfo
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	cairo >= 1.5
Requires:	glib2 >= 1:2.32
Requires:	gtk+3 >= 3.4.2
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

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure \
	--disable-static \
	--with-openssl \
	--with-packager="PLD Linux (http://pld-linux.org)"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# API not exported
%{__rm} $RPM_BUILD_ROOT%{_libdir}/pspp/lib{pspp,pspp-core}.{la,so}

%find_lang %{name}

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
%doc AUTHORS ChangeLog NEWS ONEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/pspp-convert
%attr(755,root,root) %{_bindir}/pspp-dump-sav
%dir %{_libdir}/pspp
%attr(755,root,root) %{_libdir}/pspp/libpspp-%{version}.so
%attr(755,root,root) %{_libdir}/pspp/libpspp-core-%{version}.so
%{_mandir}/man1/pspp-convert.1*
%{_mandir}/man1/pspp-dump-sav.1*
