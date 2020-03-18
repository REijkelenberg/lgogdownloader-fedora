%global use_git 1

%if 0%{?use_git}
  %define _default_patch_fuzz 2
%endif

%global gh_commit    ea0ec2a9bdac3ac2e7446dbfb2189a6a141e512a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     Sude-
%global gh_project   lgogdownloader

%bcond_with qt5

%define libcurl_opt 0
%if 0%{?rhel} && 0%{?rhel} <= 7
  %define libcurl_opt 1
%endif

%define libcurl_version 7.32.0

%if 0%{?libcurl_opt}
  %define libcurl_root /opt/rh/rh-dotnet22/root
  # https://fedoraproject.org/wiki/PackagingDrafts/FilteringAutomaticDependencies
  # https://fedoraproject.org/wiki/EPEL:Packaging_Autoprovides_and_Requires_Filtering
  %filter_from_requires /^libcurl\.so\.4.*$/d
  %filter_setup
%endif

%{!?_licensedir:%global license %doc}

Name:           lgogdownloader
Version:        3.6
%if ! 0%{?use_git}
Release:        1%{?dist}
%else
Release:        2.git%{gh_short}%{?dist}
%endif
Group:          Applications/Internet
License:        WTFPL
URL:            https://sites.google.com/site/gogdownloader/
Summary:        A downloader for GOG.com files

%if ! 0%{?use_git}
#Source0:        https://sites.google.com/site/%{name}/%{name}-%{version}.tar.gz
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/v3.6.tar.gz#/%{name}-%{version}.tar.gz
%else
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz#/%{name}-%{gh_commit}.tar.gz
%endif

# patches from Debian
# https://packages.debian.org/sid/lgogdownloader
Patch0:         lgogdownloader-3.4-reproducible.patch
Patch1:         lgogdownloader-3.4-manpage-whatis.patch
Patch11:        lgogdownloader-3.4-ea0ec2a-manpage-whatis.patch

BuildRequires:  pkgconfig
BuildRequires:  gcc gcc-c++
BuildRequires:  make
BuildRequires:  cmake3 >= 3.0.0
BuildRequires:  help2man
BuildRequires:  gzip
BuildRequires:  grep
BuildRequires:  binutils
%if ! 0%{?libcurl_opt}
BuildRequires:  pkgconfig(libcurl) >= %{libcurl_version}
%else
# sorry for this, but maintaining custom libcurl package takes too much time
BuildRequires:  rh-dotnet22-libcurl-devel >= %{libcurl_version}
%endif
BuildRequires:  pkgconfig(oauth)
BuildRequires:  rhash-devel
BuildRequires:  jsoncpp-devel
BuildRequires:  pkgconfig(htmlcxx)
BuildRequires:  pkgconfig(tinyxml2)
BuildRequires:  boost boost-devel boost-regex boost-date-time boost-filesystem boost-program-options boost-iostreams
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(zlib)
%if %{with qt5}
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5WebEngine)
%endif

%if 0%{?libcurl_opt}
Requires:       rh-dotnet22-libcurl >= %{libcurl_version}
%endif


%description
LGOGDownloader is unofficial downloader to GOG.com for Linux users.
It uses the same API as the official GOGDownloader.


%prep
%if ! 0%{?use_git}
%setup -q
%else
%setup -q -n "%{name}-%{gh_commit}"
%endif
%patch0 -p1
%if ! 0%{?use_git}
%patch1 -p1
%else
%patch11 -p1
%endif


%build
%if 0%{?libcurl_opt}
export LIBCURL_LIBRARY_PATH="%{libcurl_root}%{_libdir}"
export LIBCURL_INCLUDE_PATH="%{libcurl_root}%{_includedir}"

if [[ -n "${LD_LIBRARY_PATH}" ]]; then
  LD_LIBRARY_PATH="${LIBCURL_LIBRARY_PATH}:${LD_LIBRARY_PATH}"
else
  LD_LIBRARY_PATH="${LIBCURL_LIBRARY_PATH}"
fi

export LD_LIBRARY_PATH

if [[ -n "${C_INCLUDE_PATH}" ]]; then
  C_INCLUDE_PATH="${LIBCURL_INCLUDE_PATH}:${C_INCLUDE_PATH}"
else
  C_INCLUDE_PATH="${LIBCURL_INCLUDE_PATH}"
fi

export C_INCLUDE_PATH

if [[ -n "${CPLUS_INCLUDE_PATH}" ]]; then
  CPLUS_INCLUDE_PATH="${LIBCURL_INCLUDE_PATH}:${CPLUS_INCLUDE_PATH}"
else
  CPLUS_INCLUDE_PATH="${LIBCURL_INCLUDE_PATH}"
fi

export CPLUS_INCLUDE_PATH
%endif

%cmake3 \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
%if 0%{?libcurl_opt}
  -DCURL_INCLUDE_DIR="${LIBCURL_INCLUDE_PATH}" \
  -DCURL_LIBRARIES="${LIBCURL_LIBRARY_PATH}" \
  -DCURL_LIBRARY="${LIBCURL_LIBRARY_PATH}/libcurl.so" \
  -DCMAKE_INSTALL_RPATH="${LIBCURL_LIBRARY_PATH}" \
%endif
%if %{with qt5}
  -DUSE_QT_GUI=ON \
%endif
  .

%make_build


%install
%make_install


%files
%doc *.md
%license COPYING
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Wed Mar 18 2020 Ruub <> - 3.6-1
- Forked from oroginal COPR repository
- Update to the latest version

* Sun Mar 03 2019 Tomasz Tomasik <scx.mail@gmail.com> - 3.4-2.gitea0ec2a
- Update to the latest version

* Sun Mar 03 2019 Tomasz Tomasik <scx.mail@gmail.com> - 3.4-1
- Initial package

