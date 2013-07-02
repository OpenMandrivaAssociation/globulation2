%define scmrev 4236
%define	oname	glob2

Summary:	A state of the art Real Time Strategy (RTS) game
Name:		globulation2
Version:	0.9.4.5
%if 0%scmrev
Release:	0.%scmrev.1
Source0:	%oname-%scmrev.tar.xz
%else
Release:	2
Source0:	http://dl.sv.nongnu.org/releases/%{oname}/%{version}/%{oname}-%{version}.tar.gz
%endif
License:	GPLv3
Group:		Games/Strategy
URL:		http://www.globulation2.org
Source2:	http://goldeneye.sked.ch/~smagnena/sans.ttf
Patch0:		glob2-0.9.4.1-gcc44.patch
Patch1:		glob2-0.9.4.5-linkage.patch

BuildRequires:	scons
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(fribidi)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(portaudio-2.0)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(SDL_image)
BuildRequires:	pkgconfig(SDL_net)
BuildRequires:	pkgconfig(SDL_ttf)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(vorbis)

%description
Glob2 is a state of the art Real Time Strategy (RTS) game. It is free
software released under the terms of the GNU General Public License.

Globulation in a whole is an on-going project to create an innovative
high quality gameplay by minimizing micro-managment and assigning
automatically the tasks to the units. The player just has to order
the number of units he wants for a selected task and the units will
do their best to satisfy your requirements.

Glob2 can be played by a single player, through your Local Area
Network (LAN), or through Internet thanks to Ysagoon Online Game (YOG),
a meta-server. It also features a scripting language for versatile
gameplay and an integrated map editor.

%prep
%if 0%scmrev
%setup -q -n %oname
%else
%setup -q -n %{oname}-%{version}
%endif
%patch0 -p0 -b .gcc~
%patch1 -p1 -b .compile~

chmod -x {src/*.h,src/*.cpp,libgag/include/*.h,gnupg/*,libgag/src/*.cpp,scripts/*,data/*.txt,campaigns/*,COPYING,README}

%build
# data should be installed into datadir rather than gamesdatadir,
# otherwise it cannot find them :(
scons %{_smp_mflags} BINDIR="%{_gamesbindir}" INSTALLDIR="%{_datadir}" CXXFLAGS="%{optflags}" --portaudio=true

%install
#---- FEDORA
mkdir -p %{buildroot}%{_datadir}/%{oname}/{data/fonts,data/gfx/cursor,data/gui,data/icons,data/zik,maps,scripts,campaigns}
cp -r {data,campaigns,scripts,maps} %{buildroot}%{_datadir}/%{oname}/

# AUTHORS needs to be there for credits
#cp AUTHORS %{buildroot}%{_datadir}/%{oname}/

mkdir -p %{buildroot}%{_gamesbindir}
install -m755 src/glob2 %{buildroot}%{_gamesbindir}/

find %{buildroot} -name SConscript -exec rm -f {} \;

#(tpg) not needed
rm -fr %{buildroot}%{_datadir}/%{oname}/data/%{oname}.desktop

for f in 128x128 16x16 24x24 32x32 48x48 64x64; do
mkdir -p %{buildroot}%{_iconsdir}/hicolor/$f/apps
mv %{buildroot}%{_datadir}/%{oname}/data/icons/glob2-icon-$f.png %{buildroot}%{_iconsdir}/hicolor/$f/apps/%{name}.png
done
rm -rf %{buildroot}%{_datadir}/%{oname}/data/icons
#---- FEDORA

install %{SOURCE2} %{buildroot}%{_datadir}/%{oname}/data/fonts

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Globulation2
Comment=Globulation2 - a state of the art Real Time Strategy (RTS) game
Exec=%{_gamesbindir}/%{oname}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=Game;StrategyGame;
EOF

%files
%doc README
%{_gamesbindir}/%{oname}
%{_datadir}/%{oname}
%{_datadir}/applications/*
%{_iconsdir}/hicolor/*/apps/%{name}.png



%changelog
* Sun Jun 10 2012 Matthew Dawkins <mattydaw@mandriva.org> 0.9.4.4-5
+ Revision: 804354
- rebuild for boost libs
- cleaned up spec

* Mon Mar 14 2011 Funda Wang <fwang@mandriva.org> 0.9.4.4-4
+ Revision: 644480
- rebuild for new boost

* Mon Aug 23 2010 Funda Wang <fwang@mandriva.org> 0.9.4.4-3mdv2011.0
+ Revision: 572191
- rebuild for new boost

* Thu Aug 05 2010 Funda Wang <fwang@mandriva.org> 0.9.4.4-2mdv2011.0
+ Revision: 566098
- rebuild for new boost

  + Florent Monnier <blue_prawn@mandriva.org>
    - updated to version 0.9.4.4

* Mon Feb 08 2010 Anssi Hannula <anssi@mandriva.org> 0.9.4.1-3mdv2010.1
+ Revision: 501882
- rebuild for new boost

* Wed Feb 03 2010 Funda Wang <fwang@mandriva.org> 0.9.4.1-2mdv2010.1
+ Revision: 500057
- rebuild for new boost

* Mon Aug 24 2009 Funda Wang <fwang@mandriva.org> 0.9.4.1-1mdv2010.0
+ Revision: 420633
- new verison 0.9.4.1

* Wed Mar 11 2009 Emmanuel Andry <eandry@mandriva.org> 0.9.4-1mdv2009.1
+ Revision: 353583
- update files list
- New version 0.9.4
- drop patch 0 (merged upstream)

* Sat Dec 20 2008 Funda Wang <fwang@mandriva.org> 0.9.3-4mdv2009.1
+ Revision: 316574
- rebuild for new boost

* Mon Aug 18 2008 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.9.3-3mdv2009.0
+ Revision: 273469
- rebuild against new boost

* Sat Aug 02 2008 Couriousous <couriousous@mandriva.org> 0.9.3-2mdv2009.0
+ Revision: 260747
- Remove source1, use game gfx
- Fix build

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Sun May 04 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.9.3-1mdv2009.0
+ Revision: 201106
- drop patch0
- new version

* Fri Feb 29 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.9.2-1mdv2008.1
+ Revision: 176944
- new version
- new license policy
- put icons into fd.o compiliant directory
- fix permission of files
- spec file clean

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 04 2007 Funda Wang <fwang@mandriva.org> 0.9.1-3mdv2008.1
+ Revision: 105669
- rebuild for new boost

* Sat Sep 22 2007 Funda Wang <fwang@mandriva.org> 0.9.1-2mdv2008.0
+ Revision: 92190
- fix building
- Back to %%_gamesdatadir
- use own icons
- disable boost_thread-mt
- INSTALL to %%_gamesdatadir/%%oname
- Merge fedora SPEC

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - rebuild

* Sun Sep 02 2007 Funda Wang <fwang@mandriva.org> 0.9.1-1mdv2008.0
+ Revision: 78406
- fix building with scons
- New version 0.9.1

* Sun Apr 22 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 0.8.23-1mdv2008.0
+ Revision: 16805
- new version 0.8.23


* Mon Dec 04 2006 Olivier Blin <oblin@mandriva.com> 0.8.21-6mdv2007.0
+ Revision: 90546
- fix pixmaps location
- Import globulation2

* Wed Sep 27 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.8.21-5mdv2007.0
- bag one final buildrequires!

* Wed Sep 27 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.8.21-4mdv2007.0
- more buildrequires*#¤"#%%"&¤&%%

* Tue Sep 26 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.8.21-3mdv2007.0
- fix buildrequires

* Tue Sep 26 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.8.21-2mdv2007.0
- fix xdg menu

* Fri Aug 18 2006 Lenny Cartier <lenny@mandriva.com> 0.8.21-1mdv2007.0
- 0.8.21
- xdg

* Wed May 18 2005 Lenny Cartier <lenny@mandrakesoft.com> 0.8.15-1mdk
- 0.8.15

* Wed Feb 16 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.8.12-1mdk
- 0.8.12

* Wed Jan 19 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.8.11-1mdk
- 0.8.11

* Tue Jan 04 2005 Lenny Cartier <lenny@mandrakesoft.com> 0.8.10-1mdk
- 0.8.10

* Tue Oct 12 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.8.9-1mdk
- 0.8.9

* Wed Jun 30 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.8.6-1mdk
- 0.8.6
- cleanups
- move stuff to %%{_gamesbindir} and %%{_gamesdatadir}
- fix menu section
- fix icon
- fix buildrequires

* Wed Jun 30 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.8.5-3mdk
- rebuild for new g++

* Sat May 15 2004 Antoine Ginies <aginies@n2.mandrakesoft.com> 0.8.5-2mdk
- merge diff between version

* Mon May 03 2004 Bruno VASTA <bruno.vasta@infodia.fr>                                     |
- initial mdk rpm release, based on an old Che's fedora package

* Sat Mar 20 2004 Che
- initial rpm release

