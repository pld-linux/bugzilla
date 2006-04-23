# TODO
# - Split DB packages for mysql/pgsql
# - fill brr and add autodeps bcond
%include	/usr/lib/rpm/macros.perl
Summary:	Bug tracking system
Summary(pl):	System ¶ledzenia b³êdów
Name:		bugzilla
Version:	2.22
Release:	0.1
License:	GPL
Group:		Applications/WWW
Source0:	http://ftp.mozilla.org/pub/mozilla.org/webtools/%{name}-%{version}.tar.gz
# Source0-md5:	bbf2f1ec5607978d39855df104231973
Source1:	%{name}.conf
Patch0:		%{name}-httpd_user.patch
Patch1:		%{name}-chdir.patch
URL:		http://www.bugzilla.org/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	perl-DBD-mysql
Requires:	perl-DBI >= 1.36
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

%description -l pl
System ¶ledzenia b³êdów.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

find -name CVS -type d | xargs rm -rf
find '(' -name '*~' -o -name '*.orig' -o -name '.cvsignore' ')' | xargs -r rm -v

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/Bugzilla,/var/lib/%{name}/{data,graphs}}

install *.{cgi,js,pl,pm,txt,dtd,xul} $RPM_BUILD_ROOT%{_appdir}
cp -a Bugzilla $RPM_BUILD_ROOT%{_appdir}
cp -a images js skins template $RPM_BUILD_ROOT%{_appdir}

ln -s /var/lib/%{name}/data $RPM_BUILD_ROOT%{_appdir}
ln -s /var/lib/%{name}/graphs $RPM_BUILD_ROOT%{_appdir}
mv $RPM_BUILD_ROOT%{_appdir}/globals.pl $RPM_BUILD_ROOT%{_sysconfdir}
ln -s %{_sysconfdir}/globals.pl $RPM_BUILD_ROOT%{_appdir}/globals.pl

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1
%webapp_register apache %{_webapp}

%triggerun -- apache1
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

%dir %{_appdir}
%{_appdir}/Bugzilla
%{_appdir}/data
%{_appdir}/graphs
%{_appdir}/images
%{_appdir}/js
%{_appdir}/skins
%{_appdir}/template
%{_appdir}/*.pl
%{_appdir}/*.dtd
%{_appdir}/*.js
%{_appdir}/*.pm
%{_appdir}/*.txt
%{_appdir}/*.xul
%attr(755,root,root) %{_appdir}/*.cgi
%dir /var/lib/%{name}
%attr(770,root,http) /var/lib/%{name}/data
%attr(775,root,http) /var/lib/%{name}/graphs
