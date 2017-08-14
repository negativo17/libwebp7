%global _hardened_build 1
%global real_name libwebp

Name:          %{real_name}0.6
Version:       0.6.0
Release:       1%{?dist}
URL:           http://webmproject.org/
Summary:       Library and tools for the WebP graphics format
# Additional IPR is licensed as well. See PATENTS file for details
License:       BSD
Source0:       http://downloads.webmproject.org/releases/webp/%{real_name}-%{version}.tar.gz
Source1:       libwebp_jni_example.java

BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: giflib-devel
BuildRequires: libtiff-devel
BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: swig
BuildRequires: autoconf automake libtool
BuildRequires: freeglut-devel

%description
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.


%package tools
Summary:       The WebP command line tools

%description tools
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.


%package devel
Summary:       Development files for libwebp, a library for the WebP format
Requires:      %{name}%{?_isa} = %{version}-%{release}
Conflicts:     %{real_name}-devel%{?_isa}

%description devel
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.


%package java
Summary:       Java bindings for libwebp, a library for the WebP format
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      java-headless
Requires:      jpackage-utils

%description java
Java bindings for libwebp.


%prep
%autosetup -n %{real_name}-%{version}


%build
autoreconf -vif
%ifarch aarch64
export CFLAGS="%{optflags} -frename-registers"
%endif
# Neon disabled due to resulting CFLAGS conflict resulting in
# inlining failed in call to always_inline '[...]': target specific option mismatch
%configure --disable-static --enable-libwebpmux \
           --enable-libwebpdemux --enable-libwebpdecoder \
           --disable-neon
%make_build V=1

# swig generated Java bindings
cp %{SOURCE1} .
cd swig
rm -rf libwebp.jar libwebp_java_wrap.c
mkdir -p java/com/google/webp
swig -ignoremissing -I../src -java \
    -package com.google.webp  \
    -outdir java/com/google/webp \
    -o libwebp_java_wrap.c libwebp.swig

gcc %{optflags} -shared \
    -I/usr/lib/jvm/java/include \
    -I/usr/lib/jvm/java/include/linux \
    -I../src \
    -L../src/.libs -lwebp libwebp_java_wrap.c \
    -o libwebp_jni.so

cd java
javac com/google/webp/libwebp.java
jar cvf ../libwebp.jar com/google/webp/*.class


%install
%make_install
find "%{buildroot}/%{_libdir}" -type f -name "*.la" -delete

# swig generated Java bindings
mkdir -p %{buildroot}/%{_libdir}/%{real_name}-java
cp swig/*.jar swig/*.so %{buildroot}/%{_libdir}/%{real_name}-java/


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc README PATENTS NEWS AUTHORS
%license COPYING
%{_libdir}/libwebp.so.7*
%{_libdir}/libwebpdecoder.so.3*
%{_libdir}/libwebpdemux.so.2*
%{_libdir}/libwebpmux.so.3*

%files tools
%{_bindir}/cwebp
%{_bindir}/dwebp
%{_bindir}/gif2webp
%{_bindir}/img2webp
%{_bindir}/webpmux
%{_bindir}/vwebp
%{_mandir}/man*/*

%files devel
%{_libdir}/libwebp*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*

%files java
%doc libwebp_jni_example.java
%{_libdir}/%{real_name}-java/


%changelog
* Mon Aug 14 2017 Simone Caronni <negativo17@gmail.com> - 0.6.0-1
- Update to 0.6.0.
- Rename to libwebp0.6 for RHEL 7 compatibility.

* Sat Oct 29 2016 Sandro Mani <manisandro@gmail.com> - 0.5.1-2
- Backport e2affacc35f1df6cc3b1a9fa0ceff5ce2d0cce83 (CVE-2016-9085, rhbz#1389338)
