# Copyright 1999-2005 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: /var/cvsroot/gentoo-x86/x11-wm/metacity/metacity-2.8.6-r1.ebuild,v 1.7 2005/01/22 06:47:49 vapier Exp $

inherit gnome2 eutils

DESCRIPTION="Gnome default windowmanager"
HOMEPAGE="http://www.gnome.org/"

LICENSE="GPL-2"
SLOT="0"
KEYWORDS="x86 ppc alpha sparc hppa amd64 ia64 ~mips ~ppc64 arm"
IUSE="xinerama"

# not parallel-safe; see bug #14405
MAKEOPTS="${MAKEOPTS} -j1"

RDEPEND="virtual/x11
	>=x11-libs/pango-1.2
	>=x11-libs/gtk+-2.2.0-r1
	>=gnome-base/gconf-2
	>=x11-libs/startup-notification-0.7"

DEPEND="${RDEPEND}
	sys-devel/gettext
	>=dev-util/pkgconfig-0.12.0
	>=dev-util/intltool-0.29"

# Compositor is too unreliable
G2CONF="${G2CONF} $(use_enable xinerama) --disable-compositor"

DOCS="AUTHORS ChangeLog HACKING INSTALL NEWS README *txt"

src_unpack() {

	unpack ${A}
	# Fix the logout shortcut problems, by moving the keybindings
	# into here, from control-center, fixes bug #52034
	epatch ${FILESDIR}/metacity-2-logout.patch
	epatch ${FILESDIR}/metacity-2.8.6-window-placement.patch

}

pkg_postinst() {

	gnome2_pkg_postinst

	einfo "Metacity & Xorg X11 with composite enabled may cause unwanted border effects"

}
