# TODO
# - Split DB packages for mysql/pgsql
# - fill brr and add autodeps bcond
%include	/usr/lib/rpm/macros.perl
Summary:	Bug tracking system
Summary(pl.UTF-8):	System śledzenia błędów
Name:		bugzilla
Version:	2.22.1
Release:	0.32
License:	GPL
Group:		Applications/WWW
Source0:	http://ftp.mozilla.org/pub/mozilla.org/webtools/%{name}-%{version}.tar.gz
# Source0-md5:	d52e2818441f3c2a5caeddf6c40b9f00
Source1:	%{name}.conf
Source2:	%{name}-localconfig.pl
Source3:	%{name}.cron
Patch0:		%{name}-pld.patch
URL:		http://www.bugzilla.org/
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	perl-DBD-mysql
Requires:	perl-DBI >= 1.36
Requires:	perl-MailTools >= 1.67
Requires:	smtpdaemon
Requires:	webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}
# Don't enforce DBD driver and exclude optional packages according to release notes
%define		_noautoreq		'perl(DBD::*)' perl(Chart::Base) perl(GD) perl(GD::Graph) perl(GD::Text::Align) perl(Net::LDAP) perl(PatchReader) perl(XML::Twig) perl(Image::Magick)

%description
Bugzilla is the Bug-Tracking System from the Mozilla project.

%description -l pl.UTF-8
System śledzenia błędów.

%prep
%setup -q
%patch0 -p1

sed -i -e '
s,use lib ".",use lib "%{_appdir}",
s,use lib qw(.),use lib "%{_appdir}",
' *.cgi

find -name CVS -type d | xargs rm -rf
find '(' -name '*~' -o -name '*.orig' -o -name '.cvsignore' ')' | xargs -r rm -v

# won't package tests
rm -f runtests.pl

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/htdocs,/var/lib/%{name}/{data,graphs}} \
	$RPM_BUILD_ROOT%{perl_vendorlib}

install *.pl $RPM_BUILD_ROOT%{_appdir}
cp -a template $RPM_BUILD_ROOT%{_appdir}
cp -a Bugzilla{,.pm} $RPM_BUILD_ROOT%{perl_vendorlib}

install *.{cgi,js,txt,dtd,xul} $RPM_BUILD_ROOT%{_appdir}/htdocs
cp -a images js skins $RPM_BUILD_ROOT%{_appdir}/htdocs

ln -s /var/lib/%{name}/graphs $RPM_BUILD_ROOT%{_appdir}/htdocs

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/localconfig.pl
install -D %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.daily/bugzilla

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
# shamelessly stolen from gentoo
%banner -e %{name} <<'EOF'
0. Bugzilla has been installed into %{_appdir}

1. To finish the installation, please read
   http://www.bugzilla.org/docs/%{version}/html/installation.html
   You will need to run %{_appdir}/checksetup.pl

   IMPORTANT: If you have customized the values in your
   Status/Resolution field, you must edit checksetup.pl BEFORE YOU RUN
   IT. Please see the Release Notes for more details.

2. Please read the Release Notes, especially if you are upgrading:
   http://www.bugzilla.org/releases/%{version}/release-notes.html
EOF
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc QUICKSTART README UPGRADING* docs/rel_notes.txt docs/txt/Bugzilla-Guide.txt
%doc contrib docs/html
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.pl

%attr(755,root,root) /etc/cron.daily/bugzilla

%{perl_vendorlib}/Bugzilla
%{perl_vendorlib}/Bugzilla.pm

%dir %{_appdir}
%{_appdir}/template
%attr(755,root,root) %{_appdir}/*.pl

%dir %{_appdir}/htdocs
%{_appdir}/htdocs/*.dtd
%{_appdir}/htdocs/*.js
%{_appdir}/htdocs/*.txt
%{_appdir}/htdocs/*.xul
%{_appdir}/htdocs/graphs
%{_appdir}/htdocs/images
%{_appdir}/htdocs/js
%{_appdir}/htdocs/skins
%attr(755,root,root) %{_appdir}/htdocs/*.cgi

%dir /var/lib/%{name}
%attr(770,root,http) /var/lib/%{name}/data
%attr(770,root,http) /var/lib/%{name}/graphs
