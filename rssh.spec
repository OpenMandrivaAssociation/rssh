Summary:	Restricted shell for scp or sftp
Name:		rssh
Version:	2.3.2
Release:	%mkrel 8
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

%clean
rm -rf %{buildroot}

%files
%defattr(644, root, root, 0755)
%doc AUTHORS ChangeLog CHROOT COPYING README SECURITY TODO
%config(noreplace) %{_sysconfdir}/rssh.conf
%attr(0755,root,root) %{_bindir}/rssh
%attr(4755,root,root) %{_libexecdir}/rssh_chroot_helper
%{_mandir}/man?/*
