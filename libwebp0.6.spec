%global _hardened_build 1
%global real_name libwebp

Name:          %{real_name}0.6
Version:       0.6.0
Release:       2%{?dist}
URL:           http://webmproject.org/
Summary:       Library and tools for the WebP graphics format
# Additional IPR is licensed as well. See PATENTS file for details
License:       BSD
Source0:       http://downloads.webmproject.org/releases/webp/%{real_name}-%{version}.tar.gz

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: freeglut-devel
BuildRequires: giflib-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: libtool

Obsoletes:     %{name}-java < %{version}-%{release}
Provides:      %{name}-java == %{version}-%{release}

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


%install
%make_install
find "%{buildroot}/%{_libdir}" -name "*.la" -delete

%{?ldconfig_scriptlets}

%files
%license COPYING
%doc README PATENTS NEWS AUTHORS
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


%changelog
* Fri Mar 11 2022 Simone Caronni <negativo17@gmail.com> - 0.6.0-2
- Drop java bindings, update SPEC file.

* Mon Aug 14 2017 Simone Caronni <negativo17@gmail.com> - 0.6.0-1
- Update to 0.6.0.
- Rename to libwebp0.6 for RHEL 7 compatibility.

* Sat Oct 29 2016 Sandro Mani <manisandro@gmail.com> - 0.5.1-2
- Backport e2affacc35f1df6cc3b1a9fa0ceff5ce2d0cce83 (CVE-2016-9085, rhbz#1389338)
