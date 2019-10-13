Name     : dolittle-edge-agent
Version  : 2.1.0
Release  : 1
URL      : https://github.com/dolittle-edge/Agent/archive/2.1.0.tar.gz
Summary  : No detailed summary available
Group    : Development/Tools
License  : MIT
Source0  : https://github.com/dolittle-edge/Agent/archive/2.1.0.tar.gz
BuildRequires : buildreq-golang

%description
# Dolittle Edge Agent
This project represents the Dolittle Edge Agent. Its job is to run at the host level and
provide information / telemetry back to the cloud environment and also provide functionality
for the cloud to call upon to perform actions on the edge.

%prep
%setup -q -n Agent-2.1.0

%build
pushd Source/
go build -mod=vendor
popd
ls -lR

%install
rm -rf %{buildroot}

# Install binary
install -d %{buildroot}/usr/bin
install -p -m 755 Source/agent %{buildroot}/usr/bin/dolittle-edge-agent

# Install service
install -m 0644 -D Source/dolittle-edge-agent.service %{buildroot}/usr/lib/systemd/system/dolittle-edge-agent.service
mkdir -p %{buildroot}/usr/lib/systemd/system/multi-user.target.wants
pushd %{buildroot}/usr/lib/systemd/system/multi-user.target.wants
ln -sf ../dolittle-edge-agent.service dolittle-edge-agent.service
popd


%post
%systemd_post dolittle-edge-agent.service
%preun
%systemd_preun dolittle-edge-agent.service
%postun
%systemd_postun_with_restart dolittle-edge-agent.service


%files
%defattr(-,root,root,-)

/usr/bin/dolittle-edge-agent

/usr/lib/systemd/system/dolittle-edge-agent.service
/usr/lib/systemd/system/multi-user.target.wants/dolittle-edge-agent.service
