Summary:	Qbasic to C conversion
Summary(pl):	Konwerter z Qbasic na C
Name:		qb2c
Version:	3.41
Release:	3
License:	freely distributable
Group:		Development/Languages
Source0:	http://matrix.irb.hr/~mario/ftp/pub/qb2c/%{name}.tgz
# Source0-md5:	1d877ac5e1f4a406e6cbb5db8cf10640
BuildRequires:	XFree86-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package attempts to conver Microsoft QBASIC programs into
compilable C code. A 'brun' script is also provided to directly
execute a qbasic program.

%description -l pl
Ten pakiet próbuje dokonaæ konwersji programów pisanych w Microsoft
QBASIC w kod kompatybilny z C. Do³±czony jest te¿ skrypt brun do
bezpo¶redniego uruchamiania programów w qbasicu.

%package static
Summary:	Static qbX11 library
Summary(pl):	Statyczna biblioteka qbX11
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description static
Static qbX11 library.

%description static -l pl
Statyczna biblioteka qbX11.

%prep
%setup -q -c

%build
%{__cc} %{rpmcflags} -o bcpp bcpp.c
%{__cc} %{rpmcflags} -o qb2c qb2c.c -lm
%{__cc} %{rpmcflags} -o calib calib.c -lm
%{__cc} %{rpmcflags} -c -w x11int.c rotated.c gifencode.c gifdecode.c pickpalette.c
ar -cr libqbX11.a x11int.o rotated.o gifencode.o gifdecode.o pickpalette.o
rm -f *.o
%{__cc} %{rpmcflags} -fPIC -c -w x11int.c rotated.c gifencode.c gifdecode.c pickpalette.c
%{__cc} %{rpmldflags} -shared -Wl,-soname,libqbX11.so.3 -o libqbX11.so.%{version} *.o \
	-L/usr/X11R6/%{_lib} -lX11 -lm

cat <<EOF >bcc
#!/bin/sh
qb2c -b -C \$1 \$2 \$3 \$4 \$5 \$6
if test \$? = 0 ; then
	gcc -o \$1 \$1.c -L`pwd` -lqbX11 -L/usr/X11R6/%{_lib} -lX11 -lm
fi
EOF

cat <<EOF >brun
#!/bin/sh
TEMPNAM=`mktemp /tmp/qb.XXXXXX`
rm -f \$TEMPNAM
qb2c -b -C \$1 \$2 \$3 \$4 \$5
if test \$? = 0 ; then
	gcc -o \$TEMPNAM \$1.c -L`pwd` -lqbX11 -L/usr/X11R6/%{_lib} -lX11 -lm
	if test \$? = 0 ; then
		\$TEMPNAM \$2 \$3 \$4 \$5
	fi
fi
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}}

install bcpp qb2c calib brun bcc $RPM_BUILD_ROOT%{_bindir}
install libqbX11.* $RPM_BUILD_ROOT%{_libdir}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ANNOUNCEMENT IAFA-PACKAGE README manual.txt
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libqbX11.so.*.*

%files static
%defattr(644,root,root,755)
%{_libdir}/libqbX11.a
