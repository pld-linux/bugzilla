# TODO
# - Split DB packages for mysql/pgsql
# - fill brr and add autodeps bcond
%include	/usr/lib/rpm/macros.perl
Summary:	Bug tracking system
Summary(pl.UTF-8):	System śledzenia błędów
Name:		bugzilla
Version:	3.3.3
Release:	0.1
License:	GPL
Group:		Applications/WWW
Source0:	http://ftp.mozilla.org/pub/mozilla.org/webtools/%{name}-%{version}.tar.gz
# Source0-md5:	893273266255f15e5b253719e8abcb50
Source1:	%{name}-skins.tar.bz2
# Source1-md5:	4e6e8c2b65cab635975eff5ab318057b
Source2:	%{name}.conf
Source3:	%{name}-localconfig.pl
Source4:	%{name}.cron
Patch0:		%{name}-pld.patch
URL:		http://www.bugzilla.org/
# http://www.bugzilla.org/security/3.2.2/
BuildRequires:	security(3.2.2)
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	perl(Email::MIME::Modifier)
Requires:	perl(Email::Send) >= 2.00
Requires:	perl-DBD-mysql
Requires:	perl-DBI >= 1.41
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
%define		_noautoreq		'perl(DBD::.*)' perl(Chart::Base) perl(GD) perl(GD::Graph) perl(GD::Text::Align) perl(Net::LDAP) perl(PatchReader) perl(XML::Twig) perl(Image::Magick)

#D perl-Apache-DBI-1.01-1, perl-AppConfig-1.56-2, perl-BSD-Resource-1.28-1, perl-Class-Inspector-1.16-1,
#D perl-DBD-Pg-1.49-1, perl-Data-Flow-0.09-2, perl-Email-Abstract-2.13-1, perl-Email-Address-1.86-1,
#D perl-Email-MIME-1.85-1, perl-Email-MIME-Attachment-Stripper-1.3-1, perl-Email-MIME-ContentType-1.0-1,
#D perl-Email-MIME-Creator-1.45-1, perl-Email-MIME-Encodings-1.3-2, perl-Email-MIME-Modifier-1.43-1,
#D perl-Email-MessageID-1.35-1, perl-Email-Reply-1.1-1, perl-Email-Send-1.46-1, perl-Email-Simple-1.96-1,
#D perl-Email-Simple-Creator-1.41-1, perl-IO-All-0.33-2, perl-IO-String-1.08-1, perl-Module-Pluggable-3.1-4,
#D perl-Return-Value-1.28-1, perl-Spiffy-0.30-1, perl-Template-Toolkit-2.15-1, perl-mixin-0.04-1, perl-mod_perl-2.0.3-2


%description
Bugzilla is the Bug-Tracking System from the Mozilla project.

%description -l pl.UTF-8
System śledzenia błędów.

%prep
%setup -q %{?_rc:-n %{name}-%{version}%{_rc}} -a1
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

install *.{cgi,txt,dtd} js/*.js $RPM_BUILD_ROOT%{_appdir}/htdocs
cp -a images js skins $RPM_BUILD_ROOT%{_appdir}/htdocs

ln -s /var/lib/%{name}/graphs $RPM_BUILD_ROOT%{_appdir}/htdocs

install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/localconfig.pl
install -D %{SOURCE4} $RPM_BUILD_ROOT/etc/cron.daily/bugzilla

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
%doc QUICKSTART README UPGRADING* docs/en/rel_notes.txt docs/en/txt/Bugzilla-Guide.txt
%doc contrib docs/en/html
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.pl

%attr(755,root,root) /etc/cron.daily/bugzilla

%{perl_vendorlib}/Bugzilla
%{perl_vendorlib}/Bugzilla.pm

%dir %{_appdir}
%{_appdir}/template
%attr(700,root,root) %{_appdir}/checksetup.pl
%attr(755,root,root) %{_appdir}/collectstats.pl
%attr(755,root,root) %{_appdir}/email_in.pl
%attr(755,root,root) %{_appdir}/importxml.pl
%attr(755,root,root) %{_appdir}/install-module.pl
%attr(755,root,root) %{_appdir}/jobqueue.pl
%attr(755,root,root) %{_appdir}/mod_perl.pl
%attr(755,root,root) %{_appdir}/sanitycheck.pl
%attr(755,root,root) %{_appdir}/testserver.pl
%attr(755,root,root) %{_appdir}/whine.pl
%attr(755,root,root) %{_appdir}/whineatnews.pl

%dir %{_appdir}/htdocs
%attr(755,root,root) %{_appdir}/htdocs/*.cgi
%{_appdir}/htdocs/*.dtd
%{_appdir}/htdocs/*.js
%{_appdir}/htdocs/*.txt
%{_appdir}/htdocs/graphs
%{_appdir}/htdocs/images
%{_appdir}/htdocs/js
%dir %{_appdir}/htdocs/skins
%dir %{_appdir}/htdocs/skins/contrib
%dir %{_appdir}/htdocs/skins/contrib/Dusk
%dir %{_appdir}/htdocs/skins/custom
%{_appdir}/htdocs/skins/standard
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_appdir}/htdocs/skins/custom/*.css
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_appdir}/htdocs/skins/contrib/Dusk/*.css

%dir /var/lib/%{name}
%attr(770,root,http) /var/lib/%{name}/data
%attr(770,root,http) /var/lib/%{name}/graphs
