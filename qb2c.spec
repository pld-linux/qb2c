Summary:	Qbasic to C conversion
Summary(pl):	Konwerter z Qbasic na C
Name:		qb2c
Version:	3.40
Release:	1
Group:		Development/Languages
Group(pl):	Programowanie/Jêzyki
Source0:	ftp://darkstar.irb.hr/pub/qb2c/%{name}.tgz
Copyright:	freely distributable
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package attempts to conver Microsoft QBASIC programs into
compilable C code. A 'brun' script is also provided to directly
execute a qbasic program.

%description -l pl
Ten pakiet próbuje dokonaæ konwersji programów pisanych w Microsoft 
QBASIC w kod kompatybilny z C. 

%prep
%setup -q -n %{name} -c

%build
gcc %{rpmcflags} -o bcpp bcpp.c
gcc %{rpmcflags} -o qb2c qb2c.c -lm
gcc %{rpmcflags} -o calib calib.c -lm
gcc %{rpmcflags} -c -w x11int.c rotated.c gifencode.c gifdecode.c pickpalette.c
ar -cr libqbX11.a x11int.o rotated.o gifencode.o gifdecode.o pickpalette.o

cat <<EOF >bcc
#!/bin/sh
qb2c -b -C $1 $2 $3 $4 $5 $6
if test $? = 0
 then
 gcc -o $1 $1.c -L`pwd` -lqbX11 -L/usr/X11/lib -lX11 -lm
fi
EOF

cat <<EOF >brun
#!/bin/sh
TEMPNAM=`mktemp /tmp/qb.XXXXXX`
rm -f $TEMPNAM
qb2c -b -C $1 $2 $3 $4 $5
if test $? = 0
 then
 gcc -o $TEMPNAM $1.c -L`pwd` -lqbX11 -L/usr/X11/lib -lX11 -lm
 if test $? = 0
  then
  $TEMPNAM $2 $3 $4 $5
 fi
fi
EOF

cat <<EOF >run
#!/bin/sh
TEMPNAM=`mktemp /tmp/qb.XXXXXX`
rm -f $TEMPNAM
gcc -o $TEMPNAM $1.c -L`pwd` -lqbX11 -L/usr/X11/lib -lX11 -lm
if test $? = 0
 then
 $TEMPNAM $2 $3 $4 $5
fi
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},/usr/X11R6/lib}
install bcpp qb2c calib brun bcc run $RPM_BUILD_ROOT%{_bindir}
install libqbX11.a $RPM_BUILD_ROOT/usr/X11R6/lib
gzip -9nf IAFA-PACKAGE README manual.txt

%files
%defattr(644,root,root,755)
%doc *gz
%attr(755,root,root) %{_bindir}/*
/usr/X11R6/lib/libqbX11.a

%clean
rm -rf $RPM_BUILD_ROOT
