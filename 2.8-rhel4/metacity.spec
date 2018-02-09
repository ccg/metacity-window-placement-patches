%define gettext_package metacity

Summary: Metacity window manager
Name: metacity
Version: 2.8.6
Release: 2.9
URL: http://ftp.gnome.org/pub/gnome/sources/metacity/
Source0: %{name}-%{version}.tar.bz2
License: GPL
Group: User Interface/Desktops
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: gtk2-devel >= 2.2.0
BuildRequires: pango-devel >= 1.2.0
BuildRequires: fontconfig-devel
BuildRequires: GConf2-devel >= 2.2.0
BuildRequires: desktop-file-utils >= 0.3
BuildRequires: libglade2-devel >= 2.0.0
BuildRequires: intltool >= 0.22
BuildRequires: startup-notification-devel >= 0.7
BuildRequires: libtool automake14 autoconf
Requires: startup-notification >= 0.7

Requires: redhat-artwork >= 0.62

Patch0: metacity-2.3.987-default-theme.patch
Patch1: metacity-2.4.13.90-ctrlaltdel.patch
Patch2: metacity-2.8.5-right-alt.patch
Patch3: metacity-2.4.55-unshade-artifact.patch
Patch4: metacity-2.8.6-raise-on-click.patch
Patch5: metacity-2.8.6-strict-pointer-mode.patch
Patch6: metacity-2.4.55-other-unshade-artifact.patch
Patch7: metacity-2.8.6-wireframe-resize-popup.patch
Patch8: metacity-2.8.6-fix-up-keyboard-resize-and-move.patch
Patch9: metacity-2.8.6.rhel4-window-placement.patch

%description

Metacity is a simple window manager that integrates nicely with 
GNOME 2.

%prep
%setup -q

%patch0 -p1 -b .default-theme
%patch1 -p1 -b .ctrlaltdel
%patch2 -p0 -b .right-alt
%patch3 -p0 -b .unshade-artifact
%patch4 -p1 -b .raise-on-click
%patch5 -p1 -b .strict-pointer-mode
%patch6 -p1 -b .other-unshade-artifact
%patch7 -p1 -b .wireframe-resize-popup
%patch8 -p1 -b .fix-up-keyboard-resize-and-move
%patch9 -p1 -b .window-placement

%build

export LIBS="-L/usr/X11R6/%{_lib} -lXext -lX11"
%configure

make

SHOULD_HAVE_DEFINED="HAVE_SM HAVE_XINERAMA HAVE_XFREE_XINERAMA HAVE_SHAPE HAVE_RANDR HAVE_STARTUP_NOTIFICATION"

for I in $SHOULD_HAVE_DEFINED; do
  if ! grep -q "define $I" config.h; then
    echo "$I was not defined in config.h"
    grep "$I" config.h
    exit 1
  else
    echo "$I was defined as it should have been"
    grep "$I" config.h
  fi
done

%install
rm -rf $RPM_BUILD_ROOT

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%makeinstall
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

/bin/rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{gettext_package}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="metacity.schemas"
for S in $SCHEMAS; do
  gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S > /dev/null
done

%postun -p /sbin/ldconfig

%files -f %{gettext_package}.lang
%defattr(-,root,root)
%doc README AUTHORS COPYING NEWS HACKING doc/theme-format.txt doc/metacity-theme.dtd
%{_bindir}/*
%{_libexecdir}/*
%{_datadir}/gnome/wm-properties/metacity.desktop
%{_sysconfdir}/gconf/schemas/*.schemas
%{_datadir}/metacity
%{_datadir}/themes
%{_datadir}/pixmaps
%{_includedir}/*
%{_libdir}/lib*.so*
%{_libdir}/lib*.a
%{_libdir}/pkgconfig/*

%changelog
* Fri Aug 25 2006 Chad Glendenin <ccg_spam@yahoo.com> 2.8.6-2.9
- Added window-placement patch (http://glendenin.com/chad/metacity/)

* Wed Aug 17 2005 Ray Strode <rstrode@redhat.com> - 2.8.6-2.8
- fix crash on startup (bug 166175)

* Thu Aug  4 2005 Ray Strode <rstrode@redhat.com> - 2.8.6-2.7
- Make keyboard move behavior more sane in shaded mode.
- Disable keyboard resize in shaded mode.

* Fri Jul 29 2005 Ray Strode <rstrode@redhat.com> - 2.8.6-2.6
- Add updated patch from gnome bug 310888.

* Fri Jul 22 2005 Ray Strode <rstrode@redhat.com> - 2.8.6-2.5
- Fix up some problems with the initial resize popup patch
  (bug 164000)

* Wed Jul 20 2005 Ray Strode <rstrode@redhat.com> - 2.8.6-2.4
- Fix edge snapping in wireframe mode (bug 130088)
- Fix mouse resizing and moving (bug 156894)
- Impove resize popup patch

* Wed May 26 2005 Ray Strode <rstrode@redhat.com> - 2.8.6-2.3
- Draw resize popup in wireframe mode (bug #156293).

* Thu Mar 31 2005 Ray Strode <rstrode@redhat.com> - 2.8.6-2.2
- In reduced resources mode, clean up the entire wireframe on unshade,
  not just the part inside of the window frame (bug #153022).

* Tue Oct 26 2004 Havoc Pennington <hp@redhat.com> - 2.8.6-2.1
- forward-port the RHEL3 patches that aren't upstream yet
  or aren't suitable for upstream

* Sat Oct 16 2004 Havoc Pennington <hp@redhat.com> 2.8.6-2
- remove all the rerunning of autotools, intltool, etc. cruft; seemed to be breaking build

* Fri Oct 15 2004 Havoc Pennington <hp@redhat.com> 2.8.6-1
- upgrade to 2.8.6, fixes a lot of focus bugs primarily.

* Fri Oct 15 2004 Soren Sandmann <sandmann@redhat.com> - 2.8.5-3
- Kludge around right alt problem (#132379)

* Mon Oct 11 2004 Alexander Larsson <alexl@redhat.com> - 2.8.5-2
- Require startup-notification 0.7 (without this we'll crash)

* Thu Sep 23 2004 Alexander Larsson <alexl@redhat.com> - 2.8.5-1
- update to 2.8.5

* Tue Aug 31 2004 Alex Larsson <alexl@redhat.com> 2.8.4-1
- update to 2.8.4

* Tue Aug 24 2004 Warren Togami <wtogami@redhat.com> 2.8.3-1
- update to 2.8.3

* Thu Aug  5 2004 Mark McLoughlin <markmc@redhat.com> 2.8.2-1
- Update to 2.8.2
- Remove systemfont patch - upstream now

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May  6 2004 Havoc Pennington <hp@redhat.com> 2.8.1-2
- fix mangled Summary

* Thu May  6 2004 Havoc Pennington <hp@redhat.com> 2.8.1-1
- 2.8.1

* Thu Apr  1 2004 Alex Larsson <alexl@redhat.com> 2.8.0-1
- update to 2.8.0

* Wed Mar 10 2004 Mark McLoughlin <markmc@redhat.com> 2.7.1-1
- Update to 2.7.1

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Alexander Larsson <alexl@redhat.com> 2.7.0-1
- update to 2.7.0
- removed reduced resouces patch (its now upstream)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Oct 27 2003 Havoc Pennington <hp@redhat.com> 2.6.3-1
- 2.6.3

* Wed Oct  1 2003 Havoc Pennington <hp@redhat.com> 2.6.2-1
- 2.6.2

* Thu Sep  4 2003 Havoc Pennington <hp@redhat.com> 2.5.3-3
- put reduced resources patch back in

* Fri Aug 22 2003 Elliot Lee <sopwith@redhat.com> 2.5.3-2
- Work around libXrandr need for extra $LIBS

* Fri Aug 15 2003 Alexander Larsson <alexl@redhat.com> 2.5.3-1
- update for gnome 2.3

* Mon Jul 28 2003 Havoc Pennington <hp@redhat.com> 2.4.55-7
- rebuild

* Mon Jul 28 2003 Havoc Pennington <hp@redhat.com> 2.4.55-6
- backport the "reduced_resources" patch with wireframe

* Mon Jul 07 2003 Christopher Blizzard <blizzard@redhat.com> 2.4.55-4
- add patch to fix mouse down problems in mozilla

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 29 2003 Havoc Pennington <hp@redhat.com> 2.4.55-2
- rebuild

* Thu May 29 2003 Havoc Pennington <hp@redhat.com> 2.4.55-1
- 2.4.55

* Wed May 14 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add proper ldconfig calls for shared libs

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 21 2003 Havoc Pennington <hp@redhat.com> 2.4.34-2
- fix a crash in multihead situations, #84412

* Wed Feb  5 2003 Havoc Pennington <hp@redhat.com> 2.4.34-1
- 2.4.34
- try disabling smp_mflags and see if it fixes build

* Wed Jan 22 2003 Havoc Pennington <hp@redhat.com>
- 2.4.21.90 with a bunch o' fixes

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan 16 2003 Havoc Pennington <hp@redhat.com>
- bind Ctrl+Alt+Del to logout, #72973

* Wed Jan 15 2003 Havoc Pennington <hp@redhat.com>
- 2.4.13.90 cvs snap with event queue lag fix

* Fri Jan 10 2003 Havoc Pennington <hp@redhat.com>
- 2.4.13

* Thu Dec 12 2002 Havoc Pennington <hp@redhat.com>
- 2.4.8

* Mon Dec  2 2002 Havoc Pennington <hp@redhat.com>
- 2.4.5.90
- add little script after configure that checks what config.h
  contains, to be sure we detected all the right features.

* Tue Oct 29 2002 Havoc Pennington <hp@redhat.com>
- 2.4.3
- remove patches that have gone upstream

* Tue Aug 27 2002 Havoc Pennington <hp@redhat.com>
- fix shaded window decorations in Bluecurve theme

* Sat Aug 24 2002 Havoc Pennington <hp@redhat.com>
- fix the mplayer-disappears-on-de-fullscreen bug

* Sat Aug 24 2002 Havoc Pennington <hp@redhat.com>
- add some fixes from CVS for #71163 #72379 #72478 #72513

* Thu Aug 22 2002 Havoc Pennington <hp@redhat.com>
- patch .schemas.in instead of .schemas so we get right default theme/fonts

* Tue Aug 20 2002 Havoc Pennington <hp@redhat.com>
- grow size of top resize, and display proper cursor on enter notify
- require latest intltool to try and fix metacity.schemas by
  regenerating it in non-UTF-8 locale

* Thu Aug 15 2002 Havoc Pennington <hp@redhat.com>
- default to Sans Bold font, fixes #70920 and matches graphic design spec

* Thu Aug 15 2002 Havoc Pennington <hp@redhat.com>
- 2.4.0.91 with raise/lower keybindings for msf, fixes to fullscreen
- more apps that probably intend to be, fix for changing number of
  workspaces, fix for moving windows in multihead

* Tue Aug 13 2002 Havoc Pennington <hp@redhat.com>
- update build requires

* Mon Aug 12 2002 Havoc Pennington <hp@redhat.com>
- upgrade to cvs snap 2.4.0.90 with pile of bugfixes from 
  this weekend
- change default theme to bluecurve and require new redhat-artwork

* Tue Aug  6 2002 Havoc Pennington <hp@redhat.com>
- 2.4.0
- themes are moved, require appropriate redhat-artwork

* Thu Aug  1 2002 Havoc Pennington <hp@redhat.com>
- munge the desktop file to be in toplevel menus and 
  not show in KDE

* Tue Jul 23 2002 Havoc Pennington <hp@redhat.com>
- don't use system font by default as metacity's 
  font is now in the system font dialog

* Tue Jul 23 2002 Havoc Pennington <hp@redhat.com>
- 2.3.987.92 cvs snap

* Fri Jul 12 2002 Havoc Pennington <hp@redhat.com>
- 2.3.987.91 cvs snap

* Mon Jun 24 2002 Havoc Pennington <hp@redhat.com>
- 2.3.987.90 cvs snap

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- rebuild for new libraries

* Mon Jun 10 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Mon Jun 10 2002 Havoc Pennington <hp@redhat.com>
- 2.3.987
- default to redhat theme

* Fri Jun 07 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Tue Jun  4 2002 Havoc Pennington <hp@redhat.com>
- 2.3.610.90 cvs snap

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 20 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Fri May 17 2002 Havoc Pennington <hp@redhat.com>
- 2.3.377

* Thu May  2 2002 Havoc Pennington <hp@redhat.com>
- 2.3.233

* Thu Apr 25 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment
- add gconf schemas boilerplate

* Mon Apr 15 2002 Havoc Pennington <hp@pobox.com>
- 2.3.89

* Tue Oct 30 2001 Havoc Pennington <hp@redhat.com>
- 2.3.34

* Fri Oct 13 2001 Havoc Pennington <hp@redhat.com>
- 2.3.21 

* Mon Sep 17 2001 Havoc Pennington <hp@redhat.com>
- 2.3.8
- 2.3.13

* Wed Sep  5 2001 Havoc Pennington <hp@redhat.com>
- Initial build.


