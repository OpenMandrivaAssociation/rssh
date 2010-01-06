Summary:	Restricted shell for scp or sftp
Name:		rssh
Version:	2.3.2
Release:	%mkrel 9
License:	BSD
Group:		Networking/Remote access
URL:		http://www.pizzashack.org/rssh/
#gw this is tar.gz for signature checking
Source0:	http://prdownloads.sourceforge.net/rssh/%{name}-%{version}.tar.gz
Source1:	http://prdownloads.sourceforge.net/rssh/%{name}-%{version}.tar.gz.sig 
Patch0:     rssh-2.3.2-subversion-support.patch
Requires:	openssh
BuildRequires:	openssh-server
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
rssh is a restricted shell, used as a login shell, that allows users to perform
only scp, sftp, cvs, svnserve (Subversion), rdist, and/or rsync operations.

%prep
%setup -q
%patch0 -p 1

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
rm -rf %{buildroot}
%makeinstall

install -m 755 -D conf_convert %{buildroot}%{_datadir}/%{name}/conf_convert

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

%clean
rm -rf %{buildroot}

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
%defattr(-,root,root)
%doc AUTHORS ChangeLog CHROOT COPYING README SECURITY TODO README.2.2.8-8mdv.upgrade.urpmi
%config(noreplace) %{_sysconfdir}/rssh.conf
%attr(0755,root,root) %{_bindir}/rssh
%attr(4755,root,root) %{_libexecdir}/rssh_chroot_helper
%{_mandir}/man?/*
%{_datadir}/rssh
