MAKEFLAGS=-r
CC ?= gcc
PANDOC ?= pandoc
DESTDIR ?= /
VCHAN_PKG = $(if $(BACKEND_VMM),vchan-$(BACKEND_VMM),vchan)
HAVE_PAM_APPL = $(or $(and $(wildcard /usr/include/security/pam_appl.h),1),)
.SUFFIXES:
os := $(shell lsb_release -is)
CFLAGS += -I. -I../libqrexec -g -O2 -Wall -Wextra -Werror \
    $(shell pkg-config --cflags $(VCHAN_PKG)) -fstack-protector \
    -fstack-protector-strong -fPIC -std=gnu11 -D_POSIX_C_SOURCE=200809L \
	-D_GNU_SOURCE $(if $(HAVE_PAM_APPL),-DHAVE_PAM,-UHAVE_PAM) \
	-Wstrict-prototypes -Wold-style-definition -Wmissing-declarations -Werror=vla
LDFLAGS += -pie -Wl,-z,relro,-z,now -L../libqrexec
LDLIBS += -lqrexec-utils $(shell pkg-config --libs $(VCHAN_PKG)) $(if $(HAVE_PAM_APPL),-lpam,)

.PHONY: all clean install

remove_generated := \
	rm -f -- *.o *~ qrexec-agent qrexec-client-vm *.o.dep *.gcda *.gcno

all: qrexec-agent qrexec-client-vm qrexec-fork-server qrexec-client-vm.1.gz
.PHONY: all clean install .PHONY
qrexec-agent: qrexec-agent.o qrexec-agent-data.o
qrexec-fork-server: qrexec-fork-server.o qrexec-agent-data.o
qrexec-client-vm: qrexec-client-vm.o qrexec-agent-data.o
clean:
ifeq ($(BUILDDIR),)
	$(remove_generated)
else
	cd -P -- $(BUILDDIR) && $(remove_generated)
endif


install: all
	install -d $(DESTDIR)/etc/qubes-rpc $(DESTDIR)/usr/lib/qubes \
		$(DESTDIR)/usr/bin $(DESTDIR)/usr/share/man/man1
	install qrexec-agent $(DESTDIR)/usr/lib/qubes
	install qrexec-client-vm $(DESTDIR)/usr/bin
	install -d $(DESTDIR)/usr/share/man/man1
	install qrexec-client-vm.1.gz $(DESTDIR)/usr/share/man/man1
	ln -sf ../../bin/qrexec-client-vm $(DESTDIR)/usr/lib/qubes/qrexec-client-vm
	ln -sf ../../bin/qrexec-client-vm $(DESTDIR)/usr/lib/qubes/qrexec_client_vm
	install qrexec-fork-server $(DESTDIR)/usr/bin
ifeq ($(os), Debian)
	install -D -m 0644 qrexec.pam.debian $(DESTDIR)/etc/pam.d/qrexec
else ifeq ($(os), Ubuntu)
	install -D -m 0644 qrexec.pam.debian $(DESTDIR)/etc/pam.d/qrexec
else ifeq ($(os), Arch)
	install -D -m 0644 qrexec.pam.archlinux $(DESTDIR)/etc/pam.d/qrexec
else ifeq ($(os), Gentoo)
	install -D -m 0644 qrexec.pam.gentoo $(DESTDIR)/etc/pam.d/qrexec
else
	install -D -m 0644 qrexec.pam $(DESTDIR)/etc/pam.d/qrexec
endif

%.1: %.rst
	$(PANDOC) -s -t man $< > $@

%.1.gz: %.1
	gzip -f $<

%: %.o
	$(CC) $(LDFLAGS) -pie -g -o $@ $^ $(LDLIBS)

%.o: %.c
	$(CC) $< -c -o $@ $(CFLAGS) -MD -MP -MF $@.dep

-include *.o.dep
