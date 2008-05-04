%define	oname	glob2

Summary:	Globulation2 - a state of the art Real Time Strategy (RTS) game
Name:		globulation2
Version:	0.9.3
Release:	%mkrel 1
License:	GPLv3
Group:		Games/Strategy
URL:		http://www.globulation2.org
Source0:	http://dl.sv.nongnu.org/releases/%{oname}/%{version}/%{oname}-%{version}.tar.bz2
Source1:	http://moneo.phear.org/~nct/glob2gfx.tar.bz2
Source2:	http://goldeneye.sked.ch/~smagnena/sans.ttf
# fwang: patch0 from fedora
Patch0:		glob2-texts.pl.patch
BuildRequires:	oggvorbis-devel
BuildRequires:	SDL-devel
BuildRequires:	fribidi-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_net-devel
BuildRequires:	speex-devel
BuildRequires:	SDL_ttf-devel
BuildRequires:	boost-devel MesaGLU-devel
BuildRequires:	scons
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

chmod -x {src/*.h,src/*.cpp,libgag/include/*.h,gnupg/*,libgag/src/*.cpp,scripts/*,data/*.txt,campaigns/*,AUTHORS,COPYING,README}

%build
# data should be installed into datadir rather than gamesdatadir,
# otherwise it cannot find them :(
scons %{_smp_mflags} BINDIR="%{_gamesbindir}" INSTALLDIR="%{_datadir}" CXXFLAGS="%{optflags}"

%install
#---- FEDORA
mkdir -p %{buildroot}%{_datadir}/%{oname}/{data/fonts,data/gfx/cursor,data/gui,data/icons,data/zik,maps,scripts,campaigns}
cp -r {data,campaigns,scripts,maps} %{buildroot}%{_datadir}/%{oname}/

# AUTHORS needs to be there for credits
cp AUTHORS %{buildroot}%{_datadir}/%{oname}/

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

tar -xjf %{SOURCE1} -C %{buildroot}%{_datadir}/%{oname}/data
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

%post
%{update_menus}
%update_icon_cache hicolor

%postun
%{clean_menus}
%clean_icon_cache hicolor

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_gamesbindir}/%{oname}
%{_datadir}/%{oname}
%{_datadir}/applications/*
%{_iconsdir}/hicolor/*/apps/%{name}.png
