%define	oname	glob2
%define	name	globulation2
%define	version	0.9.1
%define	release	%mkrel 2
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
Source11:	%{name}16.png
Source12:	%{name}32.png
Source13:	%{name}48.png
URL:		http://www.globulation2.org
BuildRequires:	autoconf oggvorbis-devel SDL-devel fribidi-devel
BuildRequires:	SDL_image-devel SDL_net-devel speex-devel SDL_ttf-devel
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

%build
scons %_smp_mflags BINDIR=%{_gamesbindir} INSTALLDIR=%{_gamesdatadir} CXXFLAGS='%{optflags}'

%install
rm -rf %{buildroot}
mkdir -p %buildroot%_gamesdatadir/%oname %buildroot%_gamesbindir

find -name SConscript | xargs rm
cp -a campaigns data maps scripts %buildroot%_gamesdatadir/%{oname}
install -m755 src/%{oname} %buildroot%_gamesbindir

tar -xjf %{SOURCE1} -C %{buildroot}%{_gamesdatadir}/%{oname}/data
install %{SOURCE2} %{buildroot}%{_gamesdatadir}/%{oname}/data/fonts

install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

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

%postun
%{clean_menus}

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root)
%doc AUTHORS README TODO
%attr(755,root,root) %{_gamesbindir}/%{oname}
%{_gamesdatadir}/%{oname}
%{_datadir}/applications/*
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
