# TODO:
# - SECURITY: http://securitytracker.com/alerts/2004/Jul/1010681.html

%define _rcver rc2

%include	/usr/lib/rpm/macros.perl
Summary:	Bug tracking system
Summary(pl):	System ¶ledzenia b³êdów
Name:		bugzilla
Version:	2.18
Release:	0.%{_rcver}.3
License:	GPL
Group:		Applications/WWW
Source0:	http://ftp.mozilla.org/pub/mozilla.org/webtools/%{name}-%{version}%{_rcver}.tar.gz
# Source0-md5:	aadd24a0177a7b44ef7b2785c0d6740f
Source1:	%{name}.conf
Patch0:		%{name}-httpd_user.patch
Patch1:		%{name}-chdir.patch
URL:		http://www.bugzilla.org/
BuildRequires:	perl-base
Requires(post,postun):	apache
Requires(post,postun):	grep
Requires(postun):	fileutils
Requires:	apache
Requires:	mysql >= 3.23.41
Requires:	perl-DBD-mysql
Requires:	perl-DBI >= 1.36
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'perl(localconfig)' 'perl(data::params)' 'perl(data::versioncache)'

%define		_bugzilladir	/usr/share/bugzilla

%description
Bug tracking system.

%description -l pl
System ¶ledzenia b³êdów.

%prep
%setup -q -n %{name}-%{version}%{_rcver}
%patch0 -p1
%patch1 -p1

%build
perl -pi -e 's@#\!%{_prefix}/bonsaitools/bin/perl@#\!%{_bindir}/perl@' *cgi *pl Bug.pm processmail syncshadowdb

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/httpd,%{_bugzilladir}/{Bugzilla/{Auth,Template/Plugin},css,docs/{html,images},template},/var/lib/%{name}/{data,graphs}}

install *.{cgi,gif,html,jpg,js,pl,pm,txt} $RPM_BUILD_ROOT%{_bugzilladir}
install Bugzilla/*.pm $RPM_BUILD_ROOT%{_bugzilladir}/Bugzilla
install Bugzilla/Auth/*.pm $RPM_BUILD_ROOT%{_bugzilladir}/Bugzilla/Auth
install Bugzilla/Template/Plugin/*.pm $RPM_BUILD_ROOT%{_bugzilladir}/Bugzilla/Template/Plugin
install css/*.css $RPM_BUILD_ROOT%{_bugzilladir}/css
install docs/html/*.html $RPM_BUILD_ROOT%{_bugzilladir}/docs/html
install docs/images/*.gif $RPM_BUILD_ROOT%{_bugzilladir}/docs/images

cp -r template/en $RPM_BUILD_ROOT%{_bugzilladir}/template
find -name CVS -type d | xargs rm -rf

ln -s /var/lib/%{name}/data $RPM_BUILD_ROOT%{_bugzilladir}
ln -s /var/lib/%{name}/graphs $RPM_BUILD_ROOT%{_bugzilladir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && \
	! grep -q "^Include.*/bugzilla.conf" /etc/httpd/httpd.conf; then
		echo "Include /etc/httpd/bugzilla.conf" >> /etc/httpd/httpd.conf
fi
if [ -d /etc/httpd/httpd.conf ]; then
	mv -f /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl restart 1>&2
fi

%postun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*bugzilla.conf" /etc/httpd/httpd.conf/10_httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
		if [ -f /var/lock/subsys/httpd ]; then
			/usr/sbin/apachectl restart 1>&2
		fi
	fi
fi

%files
%defattr(644,root,root,755)
%doc README UPGRADING UPGRADING-pre-2.8 docs/rel_notes.txt docs/txt/Bugzilla-Guide.txt
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/%{name}.conf
%dir %{_bugzilladir}
%{_bugzilladir}/css
%{_bugzilladir}/docs
%{_bugzilladir}/template
%{_bugzilladir}/data
%{_bugzilladir}/graphs
%{_bugzilladir}/Bugzilla
%attr(755,root,root) %{_bugzilladir}/*.cgi
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_bugzilladir}/globals.pl
%{_bugzilladir}/[!g]*.pl
%{_bugzilladir}/*.pm
%{_bugzilladir}/*.html
%{_bugzilladir}/*.js
%{_bugzilladir}/*.gif
%{_bugzilladir}/*.jpg
%{_bugzilladir}/*.txt
%dir /var/lib/%{name}
%attr(770,root,http) /var/lib/%{name}/data
%attr(775,root,http) /var/lib/%{name}/graphs
