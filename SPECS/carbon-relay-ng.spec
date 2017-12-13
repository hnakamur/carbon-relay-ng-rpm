%define carbon_relay_ng_user carbon-relay-ng
%define carbon_relay_ng_group carbon-relay-ng

%define debug_package %{nil}

# NOTE: Follow step in Makefile of carbon-relay-ng to detect additional_commits.
# Run the following command in the carbon-relay-ng git work directory.
# git describe --tags --always
%global additional_commits 11
%global commit             20ce86599a47875ff635b3ab5ecb8b049fcd7d78
%global shortcommit        %(echo %{commit} | cut -c 1-7)

Name:	        carbon-relay-ng
# NOTE: I'm using the same version scheme as carbon-relay-ng in the
# raintank pacakge repository described at
# https://github.com/graphite-ng/carbon-relay-ng#installation
Epoch:          1
Version:	0.9.3_%{additional_commits}_g%{shortcommit}
Release:	1%{?dist}
Summary:	Fast carbon relay+aggregator with admin interfaces for making changes online

License:	BSD
URL:		https://github.com/graphite-ng/carbon-relay-ng


# NOTE: carbon-relay-ng.tar.gz was created with the following commands.
#
# mkdir -p carbon-relay-ng/src/github.com/graphite-ng
# cd carbon-relay-ng
# export GOPATH=$PWD
# cd src/github.com/graphite-ng
# git clone https://github.com/graphite-ng/carbon-relay-ng
# cd carbon-relay-ng
# git checkout 20ce86599a47875ff635b3ab5ecb8b049fcd7d78
# cd $GOPATH/..
# tar cf - carbon-relay-ng | gzip -9 > carbon-relay-ng.tar.gz
Source0:	carbon-relay-ng.tar.gz

BuildRequires:  golang >= 1.9
BuildRequires:  go-bindata
BuildRequires:  git

%description
Fast carbon relay+aggregator with admin interfaces for making changes online

%prep
%setup -n %{name}

%build
export GOPATH=%{_builddir}/%{name}
cd %{_builddir}/%{name}/src/github.com/graphite-ng/%{name}
%{__make}

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{name}
%{__mkdir} -p %{buildroot}%{_localstatedir}/run/%{name}
%{__mkdir} -p %{buildroot}%{_mandir}/man1

srcdir=%{_builddir}/%{name}/src/github.com/graphite-ng/%{name}
%{__install} -pD -m 755 ${srcdir}/%{name} %{buildroot}%{_bindir}/%{name}
%{__install} -pD -m 644 ${srcdir}/examples/carbon-relay-ng.ini %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
%{__install} -pD -m 644 ${srcdir}/examples/carbon-relay-ng-tmpfiles.conf %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf
%{__install} -pD -m 644 ${srcdir}/examples/carbon-relay-ng.service %{buildroot}%{_unitdir}/%{name}.service
%{__install} -pD -m 644 ${srcdir}/man/man1/carbon-relay-ng.1 %{buildroot}%{_mandir}/man1/%{name}.1
gzip %{buildroot}%{_mandir}/man1/%{name}.1

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%attr(0755,%{carbon_relay_ng_user},%{carbon_relay_ng_group}) %dir %{_localstatedir}/run/%{name}
%{_unitdir}/%{name}.service
%{_mandir}/man1/%{name}.1.gz

%pre
# Add the "carbon" user
getent group %{carbon_relay_ng_group} >/dev/null || groupadd -r %{carbon_relay_ng_group}
getent passwd %{carbon_relay_ng_user} >/dev/null || \
    useradd -r -g %{carbon_relay_ng_group} -s /sbin/nologin \
    --no-create-home --home %{_localstatedir}/run/%{name} %{carbon_relay_ng_user}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun

%changelog
* Wed Dec 13 2017 <hnakamur@gmail.com> - 0.9.3_11_g20ce865-1
- 0.9.3_11_g20ce865-1
