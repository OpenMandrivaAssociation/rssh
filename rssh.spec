Summary:	Restricted shell for scp or sftp
Name:		rssh
Version:	2.3.4
Release:	1
License:	BSD
Group:		Networking/Remote access
URL:		http://www.pizzashack.org/rssh/
#gw this is tar.gz for signature checking
Source0:	http://prdownloads.sourceforge.net/rssh/%{name}-%{version}.tar.gz
Source1:	http://prdownloads.sourceforge.net/rssh/%{name}-%{version}.tar.gz.sig 
Requires:	openssh
BuildRequires:	openssh-server

%description
rssh is a restricted shell, used as a login shell, that allows users to perform
only scp, sftp, cvs, svnserve (Subversion), rdist, and/or rsync operations.

%prep
%setup -q

%build
%configure2_5x \
    --with-sftp-server=%{_libdir}/ssh/sftp-server \
    --with-rsync=/usr/bin/rsync \
    --with-scp=/usr/bin/scp \
    --with-rdist=/usr/bin/rdist \
    --with-cvs=/usr/bin/cvs \
    --with-svnserve=/usr/bin/svnserve
%make 

%install
%makeinstall

install -m 755 -D conf_convert.sh %{buildroot}%{_datadir}/%{name}/conf_convert.sh

cp rssh.conf.default %{buildroot}/%{_sysconfdir}/rssh.conf
rm -f %{buildroot}/%{_sysconfdir}/rssh.conf.default
cat > README.2.2.8-8mdv.upgrade.urpmi <<EOF
Subversion support

The 2.3.2-8mdv release of the rssh package adds support for Subversion by
adding an additional configuration parameter that, if set, allows an rssh user
to run svnserve -t.

This support requires changing the /etc/rssh.conf file format to add an
additional binary digit to the permissions field.  The package will attempt to
make that change automatically during the upgrade, disabling svnserve for all
users by default, but you may want to double-check the resulting /etc/rssh.conf
file to be sure it's correct.
EOF

%post
# 2.3.2-8mdv added Subversion support, which requires adding another binary
# digit to the user configuration lines in rssh.conf.  When upgrading, run
# the conf_convert script to do so.
if [ $1 = 2 ]; then
    echo 'Adjusting /etc/rssh.conf for file format change'
    %{_datadir}/rssh/conf_convert %{_sysconfdir}/rssh.conf \
        > %{_sysconfdir}/rssh.conf.tmp
    if cmp %{_sysconfdir}/rssh.conf.tmp %{_sysconfdir}/rssh.conf >/dev/null ; then
        rm -f %{_sysconfdir}/rssh.conf.tmp
    else
        mv -f %{_sysconfdir}/rssh.conf.tmp %{_sysconfdir}/rssh.conf
    fi
fi

%files
%doc AUTHORS ChangeLog CHROOT COPYING README SECURITY TODO README.2.2.8-8mdv.upgrade.urpmi
%config(noreplace) %{_sysconfdir}/rssh.conf
%attr(0755,root,root) %{_bindir}/rssh
%attr(4755,root,root) %{_libexecdir}/rssh_chroot_helper
%{_mandir}/man?/*
%{_datadir}/rssh
