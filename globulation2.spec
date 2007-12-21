%define	oname	glob2
%define	name	globulation2
%define	version	0.9.1
%define	release	%mkrel 3
%define	Summary	Globulation2 - a state of the art Real Time Strategy (RTS) game

Summary:	%{Summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Games/Strategy
Source0:	http://dl.sv.nongnu.org/releases/%{oname}/%{version}/%{oname}-%{version}.tar.gz
Source1:	http://moneo.phear.org/~nct/glob2gfx.tar.bz2
Source2:	http://goldeneye.sked.ch/~smagnena/sans.ttf
# fwang: patch0,1 from fedora
Patch0:		glob2-texts.pl.patch
Patch1:		glob2-desktopfileinstall.patch
URL:		http://www.globulation2.org
BuildRequires:	autoconf oggvorbis-devel SDL-devel fribidi-devel
BuildRequires:	SDL_image-devel SDL_net-devel speex-devel SDL_ttf-devel
BuildRequires:	boost-devel MesaGLU-devel
BuildRequires:	scons
Provides:	%{oname} = %version-%release
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%setup -q -n %{oname}-%{version}
%patch0 -p0
%patch1 -p0

chmod -x {src/*.h,src/*.cpp,libgag/include/*.h,gnupg/*,libgag/src/*.cpp,scripts/*,data/*.txt,campaigns/*,AUTHORS,COPYING,README,TODO}

%build
# data should be installed into datadir rather than gamesdatadir,
# otherwise it cannot find them :(
scons %_smp_mflags BINDIR=%{_gamesbindir} INSTALLDIR=%{_datadir} CXXFLAGS='%{optflags}'

%install
#---- FEDORA
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{oname}/{data/fonts,data/gfx/cursor,data/gui,data/icons,data/zik,maps,scripts,campaigns}
cp -r {data,campaigns,scripts,maps} $RPM_BUILD_ROOT%{_datadir}/%{oname}/
# AUTHORS needs to be there for credits
cp AUTHORS $RPM_BUILD_ROOT%{_datadir}/%{oname}/

mkdir -p $RPM_BUILD_ROOT%{_gamesbindir}
install -m755 src/glob2 $RPM_BUILD_ROOT%{_gamesbindir}/

find $RPM_BUILD_ROOT -name SConscript -exec rm -f {} \;

for f in 128x128 16x16 24x24 32x32 48x48 64x64; do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$f/apps
mv $RPM_BUILD_ROOT%{_datadir}/%{oname}/data/icons/glob2-icon-$f.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$f/apps/%{name}.png
done
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{oname}/data/icons
#---- FEDORA

tar -xjf %{SOURCE1} -C %{buildroot}%{_datadir}/%{oname}/data
install %{SOURCE2} %{buildroot}%{_datadir}/%{oname}/data/fonts

install -m644 data/icons/glob2-icon-16x16.png -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 data/icons/glob2-icon-32x32.png -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 data/icons/glob2-icon-48x48.png -D %{buildroot}%{_liconsdir}/%{name}.png

mkdir -p %buildroot%_datadir/applications
cat > %buildroot%_datadir/applications/mandriva-%name.desktop << EOF
[Desktop Entry]
Name=Globulation2
Comment=Globulation2 - a state of the art Real Time Strategy (RTS) game
Exec=%_gamesbindir/%oname
Icon=%name
Terminal=false
Type=Application
StartupNotify=false
Categories=Game;StrategyGame;
EOF

%post
%{update_menus}
%update_icon_cache hicolor

%postun
%{clean_menus}
%clean_icon_cache hicolor

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS README TODO
%{_gamesbindir}/%{oname}
%{_datadir}/%{oname}
%{_datadir}/applications/*
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/*/apps/%{name}.png
