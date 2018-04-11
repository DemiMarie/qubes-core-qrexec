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

Name:		qubes-qrexec-vm
Version:	%{version}
Release:	1%{dist}
Summary:	The Qubes qrexec files (qube side)

Group:		Qubes
Vendor:		Invisible Things Lab
License:	GPL
URL:		http://www.qubes-os.org

BuildRequires:	pam-devel

Requires:       python3
Requires:       qubes-qrexec-base

%define _builddir %(pwd)

%description
The Qubes qrexec files for installation on a qube.

%prep
# we operate on the current directory, so no need to unpack anything
# symlink is to generate useful debuginfo packages
rm -f %{name}-%{version}
ln -sf . %{name}-%{version}
%setup -T -D

%build

make all-vm
#make -C doc PYTHON=%{__python3} SPHINXBUILD=sphinx-build-%{python3_version} man

%install
make install-vm \
    DESTDIR=$RPM_BUILD_ROOT \
    UNITDIR=%{_unitdir} \
    PYTHON_SITEPATH=%{python3_sitelib} \
    SYSCONFDIR=%{_sysconfdir}

#make -C doc DESTDIR=$RPM_BUILD_ROOT \
#    PYTHON=%{__python3} SPHINXBUILD=sphinx-build-%{python3_version} \
#    install

%clean
rm -rf $RPM_BUILD_ROOT
rm -f %{name}-%{version}

%files
%defattr(-,root,root,-)

%{_bindir}/qrexec-client-vm
%{_bindir}/qrexec-fork-server

/usr/lib/qubes/qrexec-agent
/usr/lib/qubes/qrexec-client-vm
/usr/lib/qubes/qrexec_client_vm

/etc/pam.d/qrexec
