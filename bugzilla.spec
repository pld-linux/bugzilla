%include	/usr/lib/rpm/macros.perl
Summary:	Bug tracking system
Summary(pl):	System �ledzenia b��d�w
Name:		bugzilla
Version:	2.16.2
Release:	0.2
License:	GPL
Group:		Web/Aplications
Source0:	http://ftp.mozilla.org/pub/webtools/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Patch0:		%{name}-httpd_user.patch
URL:		http://www.bugzilla.org/
Requires:	mysql
Requires:	perl-DBD-mysql
REquires:	webserver
BuildRequires:	perl
#PreReq:		-
#Requires(pre,post):	-
#Requires(preun):	-
#Requires(postun):	-
#Provides:	-
#Obsoletes:	-
#Conflicts:	-
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'perl(localconfig)' 'perl(data::params)' 'perl(data::versioncache)'

%define		_bugzilladir	/usr/share/bugzilla

%description
blah

%description -l pl
blah

%prep
%setup -q
%patch0 -p1

%build
perl -pi -e 's@#\!/usr/bonsaitools/bin/perl@#\!/usr/bin/perl@' *cgi *pl Bug.pm processmail syncshadowdb

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/httpd,%{_bugzilladir}/{css,docs/{html,images},template},/var/lib/%{name}/{data,graphs}}

install *.{cgi,gif,html,jpg,js,pl,pm,txt} processmail syncshadowdb $RPM_BUILD_ROOT%{_bugzilladir}
install css/*.css $RPM_BUILD_ROOT%{_bugzilladir}/css
install docs/html/*.html $RPM_BUILD_ROOT%{_bugzilladir}/docs/html
install docs/images/*.{gif,jpg} $RPM_BUILD_ROOT%{_bugzilladir}/docs/images

cp -r template/en $RPM_BUILD_ROOT%{_bugzilladir}/template
find -name CVS -type d | xargs rm -rf

ln -s /var/lib/%{name}/data $RPM_BUILD_ROOT%{_bugzilladir}
ln -s /var/lib/%{name}/graphs $RPM_BUILD_ROOT%{_bugzilladir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
	if [ -f /etc/httpd/httpd.conf ] && \
	    ! grep -q "^Include.*/bugzilla.conf" /etc/httpd/httpd.conf; then
		echo "Include /etc/httpd/bugzilla.conf" >> /etc/httpd/httpd.conf
	fi
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%postun
if [ "$1" = "0" ]; then
	umask 027
	grep -E -v "^Include.*bugzilla.conf" /etc/httpd/httpd.conf > \
		/etc/httpd/httpd.conf.tmp
	mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
	        /etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README UPGRADING UPGRADING-pre-2.8 docs/rel_notes.txt docs/txt/Bugzilla-Guide.txt
%config(noreplace) %verify(not size mtime md5) /etc/httpd/%{name}.conf
%dir %{_bugzilladir}
%{_bugzilladir}/css
%{_bugzilladir}/docs
%{_bugzilladir}/template
%{_bugzilladir}/data
%{_bugzilladir}/graphs
%attr(755,root,root) %{_bugzilladir}/*.cgi
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_bugzilladir}/globals.pl
%{_bugzilladir}/[!g]*.pl
%{_bugzilladir}/*.pm
%{_bugzilladir}/*.html
%{_bugzilladir}/*.js
%{_bugzilladir}/*.gif
%{_bugzilladir}/*.jpg
%{_bugzilladir}/*.txt
%{_bugzilladir}/processmail
%{_bugzilladir}/syncshadowdb
%dir /var/lib/%{name}
%attr(770,root,http) /var/lib/%{name}/data
%attr(775,root,http) /var/lib/%{name}/graphs
