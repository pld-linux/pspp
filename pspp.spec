Summary:	GNU PSPP - program for statistical analysis of sampled data
Summary(pl.UTF-8):	GNU PSPP - program do analizy statystycznej danych próbkowanych
Name:		pspp
Version:	0.8.4
Release:	2
License:	GPL v3+
Group:		Applications/Science
Source0:	http://ftp.gnu.org/gnu/pspp/%{name}-%{version}.tar.gz
# Source0-md5:	85b7729751ebe427fb71a362b71cdfd9
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/pspp/
BuildRequires:	cairo-devel >= 1.5
BuildRequires:	gettext-devel
BuildRequires:	gsl-devel >= 1.13
BuildRequires:	gtk+2-devel >= 2:2.24
BuildRequires:	gtksourceview2-devel >= 2.2
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
Requires:	cairo >= 1.5
Requires:	gsl >= 1.13
Requires:	gtk+2 >= 2:2.24
Requires:	gtksourceview2 >= 2.2
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

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--disable-static
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
%doc AUTHORS ChangeLog NEWS ONEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/pspp
%attr(755,root,root) %{_bindir}/pspp-convert
%attr(755,root,root) %{_bindir}/pspp-dump-sav
%attr(755,root,root) %{_bindir}/psppire
%dir %{_libdir}/pspp
%attr(755,root,root) %{_libdir}/pspp/libpspp-%{version}.so
%attr(755,root,root) %{_libdir}/pspp/libpspp-core-%{version}.so
%{_datadir}/pspp
%{_datadir}/appdata/pspp.appdata.xml
%{_desktopdir}/pspp.desktop
%{_iconsdir}/hicolor/*/apps/pspp.*
%{_iconsdir}/hicolor/*/mimetypes/application-x-spss-*.png
%{_infodir}/pspp.info*
%{_infodir}/pspp-dev.info*
%{_mandir}/man1/pspp-convert.1*
%{_mandir}/man1/pspp-dump-sav.1*
