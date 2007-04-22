%define	oname	glob2
%define	name	globulation2
%define	version	0.8.23
%define	release	%mkrel 1
%define	Summary	Globulation2 - a state of the art Real Time Strategy (RTS) game

Summary:	%{Summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Games/Strategy
Source0:	http://www.ysagoon.com/glob2/data/glob2-%{version}.tar.bz2
Source1:	http://moneo.phear.org/~nct/glob2gfx.tar.bz2
Source2:	http://goldeneye.sked.ch/~smagnena/sans.ttf
Source11:	%{name}16.png
Source12:	%{name}32.png
Source13:	%{name}48.png
URL:		http://ysagoon.com/glob2/
BuildRequires:	autoconf2.5 freetype-devel oggvorbis-devel SDL-devel
BuildRequires:	SDL_image-devel SDL_net-devel speex-devel SDL_ttf-devel
BuildRequires:	boost-devel MesaGLU-devel desktop-file-utils
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
rm -f missing
aclocal
autoheader
automake --add-missing
autoconf-2.5x
%configure2_5x	--bindir=%{_gamesbindir} \
		--datadir=%{_gamesdatadir} \
CPPFLAGS="`pkg-config --cflags speex`"
%make

%install
rm -rf %{buildroot}

%makeinstall_std
tar -xjf %{SOURCE1} -C %{buildroot}%{_gamesdatadir}/%{oname}/data
install %{SOURCE2} %{buildroot}%{_gamesdatadir}/%{oname}/data/fonts

for d in applications pixmaps; do
  mv %{buildroot}%{_gamesdatadir}/$d %{buildroot}%{_datadir}
done

install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

mkdir -p %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name}  <<EOF
?package(%name): \ 
command="%{_gamesbindir}/%{oname}" needs="X11" \
icon="%{name}.png" \
section="More Applications/Games/Strategy" \
title="Globulation2"  \
longtitle="%{Summary}" \
xdg="true"
EOF

desktop-file-install	--vendor="" \
			--remove-category="Application" \
			--add-category="X-MandrivaLinux-MoreApplications-Games-Strategy" \
			--dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%attr(755,root,root) %{_gamesbindir}/%{oname}
%dir %{_gamesdatadir}/%{oname}
%{_gamesdatadir}/%{oname}/*
%{_menudir}/%{name}
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
