# TODO
# - Split DB packages for mysql/pgsql
# - fill brr and add autodeps bcond
%include	/usr/lib/rpm/macros.perl
Summary:	Bug tracking system
Summary(pl):	System ¶ledzenia b³êdów
Name:		bugzilla
Version:	2.20
Release:	0.5
License:	GPL
Group:		Applications/WWW
Source0:	http://ftp.mozilla.org/pub/mozilla.org/webtools/%{name}-%{version}.tar.gz
# Source0-md5:	bd8638501bc3f6ce93499ae0227d1ec2
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
# see TODO
%define		_noautoreq		'perl(DBD::Pg)'

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

install *.{cgi,html,jpg,js,pl,pm,txt,dtd,xul} $RPM_BUILD_ROOT%{_appdir}
cp -a Bugzilla $RPM_BUILD_ROOT%{_appdir}
cp -a images js skins template $RPM_BUILD_ROOT%{_appdir}

ln -s /var/lib/%{name}/data $RPM_BUILD_ROOT%{_appdir}
ln -s /var/lib/%{name}/graphs $RPM_BUILD_ROOT%{_appdir}

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
%doc QUICKSTART README UPGRADING UPGRADING-pre-2.8 docs/rel_notes.txt docs/txt/Bugzilla-Guide.txt
%doc contrib docs/html
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf

%dir %{_appdir}
%{_appdir}/Bugzilla
%{_appdir}/data
%{_appdir}/graphs
%{_appdir}/images
%{_appdir}/js
%{_appdir}/skins
%{_appdir}/template
%attr(755,root,root) %{_appdir}/*.cgi
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_appdir}/globals.pl
%{_appdir}/[!g]*.pl
%{_appdir}/*.dtd
%{_appdir}/*.html
%{_appdir}/*.js
%{_appdir}/*.jpg
%{_appdir}/*.pm
%{_appdir}/*.txt
%{_appdir}/*.xul
%dir /var/lib/%{name}
%attr(770,root,http) /var/lib/%{name}/data
%attr(775,root,http) /var/lib/%{name}/graphs
