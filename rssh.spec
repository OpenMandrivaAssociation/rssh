Summary:	Restricted shell for scp or sftp
Name:		rssh
Version:	2.3.2
Release:	%mkrel 6
License:	BSD
Group:		Networking/Remote access
URL:		http://www.pizzashack.org/rssh/
#gw this is tar.gz for signature checking
Source0:	http://prdownloads.sourceforge.net/rssh/%{name}-%{version}.tar.gz
Source1:	http://prdownloads.sourceforge.net/rssh/%{name}-%{version}.tar.gz.sig 
Requires:	openssh
BuildRequires:	openssh-clients
BuildRequires:	openssh-server
BuildRequires:	cvs
BuildRequires:	rdist
BuildRequires:	rsync
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
rssh is a restricted shell for use with ssh, which allows the system
administrator to restrict a user's access to a system via scp or sftp, or both.

%prep

%setup -q

%build
%configure2_5x \
    --with-sftp-server=%{_libdir}/ssh/sftp-server
%make 

%install
rm -rf %{buildroot}

%makeinstall

install -m 755 -D conf_convert.sh %{buildroot}%{_datadir}/%{name}/conf_convert.sh

%clean
rm -rf %{buildroot}

%files
%defattr(644, root, root, 0755)
%doc AUTHORS ChangeLog CHROOT COPYING README SECURITY TODO
%config(noreplace) %{_sysconfdir}/rssh.conf
%attr(0755,root,root) %{_bindir}/rssh
%attr(4755,root,root) %{_libexecdir}/rssh_chroot_helper
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/conf_convert.sh
%{_mandir}/man?/*
