#
# This is the SPEC file for creating binary RPMs for the Dom0.
#
#
# The Qubes OS Project, http://www.qubes-os.org
#
# Copyright (C) 2010  Joanna Rutkowska <joanna@invisiblethingslab.com>
# Copyright (C) 2010  Rafal Wojtczuk  <rafal@invisiblethingslab.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, see <https://www.gnu.org/licenses/>.
#
#

%{!?version: %define version %(cat version)}

# debug_package hack should be removed when BuildArch:noarch is enabled below
%define debug_package %{nil}

Name:		qubes-qrexec-base
Version:	%{version}
Release:	1%{dist}
Summary:	The Qubes qrexec files (common files)

Group:		Qubes
Vendor:		Invisible Things Lab
License:	GPL
URL:		http://www.qubes-os.org

# Because we have "#!/usr/bin/env python" shebangs, RPM puts
# "Requires: $(which python)" dependency, which, depending on $PATH order, may
# point to /usr/bin/python or /bin/python (because Fedora has this stupid
# /bin -> usr/bin symlink). python*.rpm provides only /usr/bin/python.
AutoReq:	no

BuildRequires:  python3-devel
# for building documentation
BuildRequires:	python3-sphinx
BuildRequires:	python3-dbus
BuildRequires:	qubes-libvchan-devel

Requires:       python3

%define _builddir %(pwd)

%description
The Qubes qrexec files for installation on both dom0 and qube.

%prep
# we operate on the current directory, so no need to unpack anything
# symlink is to generate useful debuginfo packages
rm -f %{name}-%{version}
ln -sf . %{name}-%{version}
%setup -T -D

%build

make all-base
#make -C doc PYTHON=%{__python3} SPHINXBUILD=sphinx-build-%{python3_version} man

%install
make install-base \
    INCLUDEDIR=%{_includedir} \
    LIBDIR=%{_libdir} \
    SYSCONFDIR=%{_sysconfdir} \
    UNITDIR=%{_unitdir} \
    PYTHON_SITEPATH=%{python3_sitelib} \
    DESTDIR=$RPM_BUILD_ROOT

#make -C doc DESTDIR=$RPM_BUILD_ROOT \
#    PYTHON=%{__python3} SPHINXBUILD=sphinx-build-%{python3_version} \
#    install

%clean
rm -rf $RPM_BUILD_ROOT
rm -f %{name}-%{version}

%files
%defattr(-,root,root,-)

%{_bindir}/qrexec-policy
%{_bindir}/qrexec-policy-agent
%{_bindir}/qrexec-policy-graph

%{_includedir}/qrexec.h
%{_includedir}/libqrexec-utils.h
%{_includedir}/libqubes-rpc-filecopy.h

%{_libdir}/libqrexec-utils.so*
%{_libdir}/libqubes-rpc-filecopy.so*

/usr/lib/qubes/qubes-rpc-multiplexer

%dir %{python3_sitelib}/qrexec-*.egg-info
%{python3_sitelib}/qrexec-*.egg-info/*

%dir %{python3_sitelib}/qrexec
%dir %{python3_sitelib}/qrexec/__pycache__
%{python3_sitelib}/qrexec/__pycache__/*
%{python3_sitelib}/qrexec/__init__.py
%{python3_sitelib}/qrexec/cli.py
%{python3_sitelib}/qrexec/agent.py
%{python3_sitelib}/qrexec/gtkhelpers.py
%{python3_sitelib}/qrexec/policycreateconfirmation.py
%{python3_sitelib}/qrexec/rpcconfirmation.py
%{python3_sitelib}/qrexec/utils.py
%{python3_sitelib}/qrexec/graph.py

%dir %{python3_sitelib}/qrexec/tests
%dir %{python3_sitelib}/qrexec/tests/__pycache__
%{python3_sitelib}/qrexec/tests/__pycache__/*
%{python3_sitelib}/qrexec/tests/__init__.py
%{python3_sitelib}/qrexec/tests/cli.py
%{python3_sitelib}/qrexec/tests/gtkhelpers.py
%{python3_sitelib}/qrexec/tests/rpcconfirmation.py

%dir %{python3_sitelib}/qrexec/glade
%{python3_sitelib}/qrexec/glade/PolicyCreateConfirmationWindow.glade
%{python3_sitelib}/qrexec/glade/RPCConfirmationWindow.glade
