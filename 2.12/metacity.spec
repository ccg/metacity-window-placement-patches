#
# spec file for package metacity (Version 2.12.0)
#
# Copyright (c) 2005 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://www.suse.de/feedback/
#

# norootforbuild
# neededforbuild  gnome-filesystem gnome2-devel-packages intltool perl-XML-Parser startup-notification startup-notification-devel

BuildRequires: aaa_base acl attr bash bind-utils bison bzip2 coreutils cpio cpp cracklib cvs cyrus-sasl db devs diffutils e2fsprogs file filesystem fillup findutils flex gawk gdbm-devel gettext-devel glibc glibc-devel glibc-locale gpm grep groff gzip info insserv klogd less libacl libattr libcom_err libgcc libnscd libselinux libstdc++ libxcrypt libzio m4 make man mktemp module-init-tools ncurses ncurses-devel net-tools netcfg openldap2-client openssl pam pam-modules patch permissions popt procinfo procps psmisc pwdutils rcs readline sed strace sysvinit tar tcpd texinfo timezone unzip util-linux vim zlib zlib-devel alsa alsa-devel atk atk-devel audiofile audiofile-devel autoconf automake binutils cairo cairo-devel esound esound-devel expat fontconfig fontconfig-devel freetype2 freetype2-devel gcc gconf2 gconf2-devel gdbm gettext glib2 glib2-devel glitz glitz-devel gnome-filesystem gnome-keyring gnome-keyring-devel gnome-vfs2 gnome-vfs2-devel gnutls gnutls-devel gtk2 gtk2-devel intltool libart_lgpl libart_lgpl-devel libbonobo libbonobo-devel libbonoboui libbonoboui-devel libgcrypt libgcrypt-devel libglade2 libglade2-devel libgnome libgnome-devel libgnomecanvas libgnomecanvas-devel libgnomeprint libgnomeprint-devel libgnomeprintui libgnomeprintui-devel libgnomeui libgnomeui-devel libgpg-error libgpg-error-devel libjpeg libjpeg-devel libpixman libpixman-devel libpng libpng-devel libtool libwnck libwnck-devel libxml2 libxml2-devel mDNSResponder mDNSResponder-devel openssl-devel orbit2 orbit2-devel pango pango-devel perl perl-XML-Parser pkgconfig popt-devel resmgr rpm startup-notification startup-notification-devel update-desktop-files xorg-x11-devel xorg-x11-libs

Name:         metacity
%define prefix   /opt/gnome
%define sysconfdir /etc%{prefix}
License:      GPL
Group:        System/GUI/GNOME
Autoreqprov:  on
Version:      2.12.0
Release:      4
Summary:      A fast Window Manager for the GNOME 2.x Desktop
Source:       metacity-%{version}.tar.bz2
Source1:      %name.desktop
Patch:        metacity-ping-timeout.patch
Patch2:       metacity-preconf.dif
Patch3:       metacity-6626-raise-on-click.diff
Patch4:       metacity-2.12-placement.patch
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
PreReq:       filesystem gconf2

%description
Metacity is a fast window manager for the GNOME 2.x Desktop. It can be
seen as an alternative to Sawfish. Many users prefer Metacity because
it integrates well with the GNOME 2.x Desktop.



%debug_package
%prep
%setup -n metacity-%{version}
%patch -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
rename no nb po/no.*
sed "s/\(ALL_LINGUAS.*\) no /\1 nb /" configure.in > configure.in.tmp && \
        mv configure.in.tmp configure.in
intltoolize --force
autoreconf -fi
## HACK ALERT BEGIN
# work around 9.2 deficiency
if test -f /usr/X11R6/%_lib/libXfixes.a -a ! -f /usr/X11R6/%_lib/libXfixes.so ; then
    ln -sf /usr/X11R6/%_lib/libXfixes.so.? src/libXfixes.so
    export LDFLAGS="-L."
fi
## HACK ALERT END
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" \
  ./configure \
    --prefix=%prefix \
    --sysconfdir=%sysconfdir \
    --datadir=%prefix/share \
    --mandir=%prefix/share/man \
    --localstatedir=/var/%_lib \
    --libexecdir=%{prefix}/lib/metacity \
    --libdir=%prefix/%_lib \
    --disable-schemas-install \
    --disable-compositor
make 

%install
make install DESTDIR=$RPM_BUILD_ROOT
# install kdm/gdm entry
install -m 0755 -d $RPM_BUILD_ROOT/usr/share/xsessions/
install -m 0644 %SOURCE1 $RPM_BUILD_ROOT/usr/share/xsessions/
%suse_update_desktop_file $RPM_BUILD_ROOT/usr/share/xsessions/%name.desktop
rm $RPM_BUILD_ROOT%{prefix}/%{_lib}/*.*a

%post
%run_ldconfig
export GCONF_CONFIG_SOURCE=`opt/gnome/bin/gconftool-2 --get-default-source` 
opt/gnome/bin/gconftool-2 --makefile-install-rule etc/opt/gnome/gconf/schemas/metacity.schemas >/dev/null

%postun
%run_ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{prefix}/bin/*
%{prefix}/share/locale/*/LC_MESSAGES/*.mo
/etc/%{prefix}/gconf/schemas/metacity.schemas
%{prefix}/%_lib/*.so
%{prefix}/%_lib/*.so.*
%{prefix}/lib/metacity
%{prefix}/share/man/man*/*
/opt/gnome/share/gnome/wm-properties/*.desktop
%{prefix}/share/metacity
%{prefix}/share/themes/*
%{prefix}/include/metacity-1
%{prefix}/%_lib/pkgconfig/*.pc
/usr/share/xsessions

%changelog -n metacity
* Mon Oct 17 2005 - Chad Glendenin <ccg_spam@yahoo.com> 2.12.0-4
- Added window-placement patch.
* Tue Sep 06 2005 - gekker@suse.de
- Update to version 2.12.0 (GNOME 2.12)
* Tue Aug 23 2005 - gekker@suse.de
- Update to version 2.11.3
* Thu Aug 11 2005 - gekker@suse.de
- Update to version 2.11.2
* Tue Aug 02 2005 - gekker@suse.de
- Update to version 2.11.1
* Fri Jul 22 2005 - gekker@suse.de
- Update to version 2.11.0
- Remove *.*a files from package
* Thu Jul 21 2005 - federico@novell.com
- Added metacity-6626-raise-on-click.diff; this adds a boolean GConf
  key called /apps/metacity/general/raise_on_click that controls whether
  windows get raised to the front when a button is pressed on them.  Fixes
  bug #6626.
* Wed Jun 22 2005 - gekker@suse.de
- Update to version 2.10.1
* Thu Mar 17 2005 - sbrabec@suse.cz
- Disabled metacity's compositing manager (#61691).
* Thu Mar 10 2005 - gekker@suse.de
- Update to version 2.10.0 (GNOME 2.10).
* Fri Mar 04 2005 - gekker@suse.de
- Update to version 2.9.34
* Fri Feb 11 2005 - gekker@suse.de
- Update to version 2.9.13
* Thu Feb 10 2005 - adrian@suse.de
- install session desktop file
* Sun Feb 06 2005 - gekker@suse.de
- Update to version 2.9.8
* Wed Jan 19 2005 - clahey@suse.de
- Updated to version 2.9.3.
* Tue Jan 04 2005 - gekker@suse.de
- Update to version 2.9.2
* Wed Dec 22 2004 - gekker@suse.de
- Update to version 2.9.0
- Remove titlebar-font-setup.patch, included in update.
* Tue Nov 23 2004 - ro@suse.de
- fix build on 9.2 (missing so links for libXfixes)
* Tue Nov 02 2004 - mmj@suse.de
- Locale rename: no -> nb
* Tue Oct 12 2004 - sbrabec@suse.cz
- Fixed libexecdir for bi-arch (#47050).
* Thu Apr 29 2004 - hhetter@suse.de
- updated 2.8.0 [GNOME2.6]
* Fri Mar 12 2004 - hhetter@suse.de
- default theme to Industrial
* Wed Mar 10 2004 - sbrabec@suse.cz
- Fixed gconf schemas installation (#33114).
* Mon Mar 01 2004 - sbrabec@suse.cz
- Allow setting of titlebar font in gnome-font-properties (workaround
  for bug #31388, http://bugzilla.gnome.org/show_bug.cgi?id=104177).
- Disable schemas installation during %%install.
* Wed Feb 25 2004 - hhetter@suse.de
- apply metacity-ping-timeout.patch, increase the time
  metacity detects crashed programs
* Thu Feb 12 2004 - hhetter@suse.de
- gconf schema (de-)installation in %%post and %%postun
* Mon Feb 09 2004 - hhetter@suse.de
- updated to version 2.6.3 [GNOME2.4.2]
* Sat Jan 10 2004 - adrian@suse.de
- add %%run_ldconfig
* Thu Oct 09 2003 - sbrabec@suse.cz
- Updated to version 2.6.2 (GNOME 2.4).
* Mon Jul 14 2003 - sbrabec@suse.cz
- GNOME prefix change to /opt/gnome.
* Tue Jun 24 2003 - sbrabec@suse.cz
- Updated to version 2.4.55.
- Updated neededforbuild.
- Prefix clash fix (wm-properties).
- Fixed directory owhership.
* Thu Mar 13 2003 - sbrabec@suse.cz
- Fixed desktop hang for certain transient loops (k3b-setup, bug 24069).
- Allow startup-notification.
* Thu Feb 06 2003 - hhetter@suse.de
- updated to version 2.4.34 [GNOME 2.2.0]
* Fri Jan 31 2003 - sf@suse.de
- fixed library path for lib64
* Tue Jan 14 2003 - hhetter@suse.de
- updated to verion 2.4.13
* Mon Jan 06 2003 - sbrabec@suse.cz
- Updated to version 2.4.8.
- Updated %%files.
* Wed Oct 23 2002 - hhetter@suse.de
- fix kde datadir
- fix wrong docdir
- updated to version 2.4.2
- FHS fix
* Fri Sep 27 2002 - ro@suse.de
- Added alsa alsa-devel to neededforbuild (esound)
* Tue Aug 20 2002 - hhetter@suse.de
- added PreReq: filesystem
* Mon Aug 12 2002 - hhetter@suse.de
- updated to version 2.4.0
- fix filelist for new theme conventions
* Sat Jul 27 2002 - adrian@suse.de
- fix neededforbuild
* Fri Jun 14 2002 - hhetter@suse.de
- provide schemas
* Mon Jun 10 2002 - hhetter@suse.de
- initial SuSE Package
