# TODO
# - Split DB packages for mysql/pgsql
# - fill brr and add autodeps bcond
%include	/usr/lib/rpm/macros.perl
Summary:	Bug tracking system
Summary(pl):	System ¶ledzenia b³êdów
Name:		bugzilla
Version:	2.20
Release:	0.4
License:	GPL
Group:		Applications/WWW
Source0:	http://ftp.mozilla.org/pub/mozilla.org/webtools/%{name}-%{version}.tar.gz
# Source0-md5:	bd8638501bc3f6ce93499ae0227d1ec2
Source1:	%{name}.conf
Patch0:		%{name}-httpd_user.patch
Patch1:		%{name}-chdir.patch
URL:		http://www.bugzilla.org/
Requires:	webserver = apache
Requires:	mysql >= 3.23.41
Requires:	perl-DBD-mysql
Requires:	perl-DBI >= 1.36
Requires:	smtpdaemon
Conflicts:	apache < 1.3.33-2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# see TODO
%define		_noautoreq		'perl(DBD::Pg)'
%define		_bugzilladir	%{_datadir}/bugzilla
%define		_sysconfdir		/etc/%{name}

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
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_bugzilladir}/Bugzilla,/var/lib/%{name}/{data,graphs}}

install *.{cgi,html,jpg,js,pl,pm,txt,dtd,xul} $RPM_BUILD_ROOT%{_bugzilladir}
cp -a Bugzilla $RPM_BUILD_ROOT%{_bugzilladir}
cp -a images js skins template $RPM_BUILD_ROOT%{_bugzilladir}

ln -s /var/lib/%{name}/data $RPM_BUILD_ROOT%{_bugzilladir}
ln -s /var/lib/%{name}/graphs $RPM_BUILD_ROOT%{_bugzilladir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- %{name} < 2.20
# migrate from old config location (only apache2, as there was no apache1 support)
if [ -f /etc/httpd/%{name}.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/apache.conf{,.rpmnew}
	mv -f /etc/httpd/%{name}.conf.rpmsave %{_sysconfdir}/apache.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd reload 1>&2
	fi
fi

# nuke very-old config location (this mostly for Ra)
if [ ! -d /etc/httpd/httpd.conf ]; then
	sed -i -e "/^Include.*%{name}.conf/d" /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd reload 1>&2
	fi
fi

# place new config location, as trigger puts config only on first install, do it here.
# apache1
if [ -d /etc/apache/conf.d ]; then
	ln -sf %{_sysconfdir}/apache.conf /etc/apache/conf.d/99_%{name}.conf
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache reload 1>&2
	fi
fi
# apache2
if [ -d /etc/httpd/httpd.conf ]; then
	ln -sf %{_sysconfdir}/apache.conf /etc/httpd/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd reload 1>&2
	fi
fi

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%files
%defattr(644,root,root,755)
%doc QUICKSTART README UPGRADING UPGRADING-pre-2.8 docs/rel_notes.txt docs/txt/Bugzilla-Guide.txt
%doc contrib docs/html
%attr(750,root,http) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf

%dir %{_bugzilladir}
%{_bugzilladir}/Bugzilla
%{_bugzilladir}/data
%{_bugzilladir}/graphs
%{_bugzilladir}/images
%{_bugzilladir}/js
%{_bugzilladir}/skins
%{_bugzilladir}/template
%attr(755,root,root) %{_bugzilladir}/*.cgi
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_bugzilladir}/globals.pl
%{_bugzilladir}/[!g]*.pl
%{_bugzilladir}/*.dtd
%{_bugzilladir}/*.html
%{_bugzilladir}/*.js
%{_bugzilladir}/*.jpg
%{_bugzilladir}/*.pm
%{_bugzilladir}/*.txt
%{_bugzilladir}/*.xul
%dir /var/lib/%{name}
%attr(770,root,http) /var/lib/%{name}/data
%attr(775,root,http) /var/lib/%{name}/graphs
