Name: pcs
Version: 0.11.10
Release: 1%{?dist}.1
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
# https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing#Good_Licenses
# GPL-2.0-only: pcs
# MIT: backports, childprocess, dacite, ethon, mustermann, rack,
#      rack-protection, rack-session, rack-test, rackup, sinatra, tilt
# MIT and (BSD-2-Clause or GPL-2.0-or-later): nio4r
# BSD-2-Clause or Ruby: base64, ruby2_keywords
# BSD-3-Clause: puma
# BSD-3-Clause and MIT: ffi
License: GPL-2.0-only AND MIT AND BSD-3-Clause AND (BSD-2-Clause OR Ruby) AND (BSD-2-Clause OR GPL-2.0-or-later)
URL: https://github.com/ClusterLabs/pcs
Group: System Environment/Base
Summary: Pacemaker/Corosync Configuration System
#building only for architectures with pacemaker and corosync available
ExclusiveArch: i686 x86_64 s390x ppc64le aarch64

# To build an official pcs release, comment out branch_or_commit
# Use long commit hash or branch name to build an unreleased version
# %%global branch_or_commit dbb53b89e16735d4edf85248d02024bb6de53a55

%global version_or_commit %{version}
%if 0%{?branch_or_commit:1}
  %global version_or_commit %{branch_or_commit}
  %global tarball_version %{version}+%(echo %{branch_or_commit} | head -c 8)
%endif
%global pcs_source_name %{name}-%{version_or_commit}

# To build an official pcs-web-ui release, comment out ui_branch_or_commit
# Last tagged version, also used as fallback version for untagged tarballs
%global ui_version 0.1.23
# Use long commit hash or branch name to build an unreleased version
# %%global ui_branch_or_commit 54730df523389a3c87abad7e47c44e30b33a2647
%global ui_modules_version 0.1.23

%global ui_version_or_commit %{ui_version}
%if 0%{?ui_branch_or_commit:1}
  %global ui_version_or_commit %{ui_branch_or_commit}
  %global ui_tarball_version %{ui_version}-%(echo %{ui_branch_or_commit} | head -c 8)
%endif
%global ui_src_name pcs-web-ui-%{ui_version_or_commit}


%global pcs_snmp_pkg_name  pcs-snmp

%global pyagentx_version   0.4.pcs.2
%global dacite_version  1.9.2
%global version_rubygem_backports  3.25.1
%global version_rubygem_base64 0.2.0
%global version_rubygem_childprocess  5.1.0
%global version_rubygem_ethon  0.16.0
%global version_rubygem_ffi  1.17.2
%global version_rubygem_logger 1.7.0
%global version_rubygem_mustermann  3.0.3
%global version_rubygem_nio4r 2.7.4
%global version_rubygem_puma 6.6.0
%global version_rubygem_rack 3.2.3
%global version_rubygem_rack_protection  4.1.1
%global version_rubygem_rack_session 2.1.1
%global version_rubygem_rack_test  2.2.0
%global version_rubygem_rackup 2.2.1
%global version_rubygem_ruby2_keywords  0.0.5
%global version_rubygem_sinatra  4.1.1
%global version_rubygem_tilt  2.6.0

%global min_compatible_pacemaker_version 2.1.0
%global first_incompatible_pacemaker_version 3.0.0

%global pcs_bundled_dir pcs_bundled
%global pcsd_public_dir pcsd/public
%global rubygem_bundle_dir pcsd/vendor/bundle
%global rubygem_cache_dir %{rubygem_bundle_dir}/cache

# https://fedoraproject.org/wiki/Changes/Avoid_usr_bin_python_in_RPM_Build#Python_bytecompilation
# Enforce python3 because bytecompilation of tornado produced warnings:
# DEPRECATION WARNING: python2 invoked with /usr/bin/python.
#    Use /usr/bin/python3 or /usr/bin/python2
#    /usr/bin/python will be removed or switched to Python 3 in the future.
%global __python %{__python3}

# prepend v for folder in GitHub link when using tagged tarball
%if "%{version}" == "%{version_or_commit}"
  %global v_prefix v
%endif

# part after the last slash is recognized as filename in look-aside cache
Source0: %{url}/archive/%{?v_prefix}%{version_or_commit}/%{pcs_source_name}.tar.gz

Source41: https://github.com/ondrejmular/pyagentx/archive/v%{pyagentx_version}/pyagentx-%{pyagentx_version}.tar.gz
Source44: https://github.com/konradhalas/dacite/archive/v%{dacite_version}/dacite-%{dacite_version}.tar.gz

Source81: https://rubygems.org/downloads/backports-%{version_rubygem_backports}.gem
Source82: https://rubygems.org/downloads/ethon-%{version_rubygem_ethon}.gem
Source83: https://rubygems.org/downloads/ffi-%{version_rubygem_ffi}.gem
Source84: https://rubygems.org/downloads/nio4r-%{version_rubygem_nio4r}.gem
Source85: https://rubygems.org/downloads/puma-%{version_rubygem_puma}.gem
Source86: https://rubygems.org/downloads/mustermann-%{version_rubygem_mustermann}.gem
Source87: https://rubygems.org/downloads/childprocess-%{version_rubygem_childprocess}.gem
Source88: https://rubygems.org/downloads/rack-%{version_rubygem_rack}.gem
Source89: https://rubygems.org/downloads/rack-protection-%{version_rubygem_rack_protection}.gem
Source90: https://rubygems.org/downloads/rack-test-%{version_rubygem_rack_test}.gem
Source91: https://rubygems.org/downloads/sinatra-%{version_rubygem_sinatra}.gem
Source92: https://rubygems.org/downloads/tilt-%{version_rubygem_tilt}.gem
Source93: https://rubygems.org/downloads/ruby2_keywords-%{version_rubygem_ruby2_keywords}.gem
Source94: https://rubygems.org/downloads/base64-%{version_rubygem_base64}.gem
Source95: https://rubygems.org/downloads/rack-session-%{version_rubygem_rack_session}.gem
Source96: https://rubygems.org/downloads/rackup-%{version_rubygem_rackup}.gem
Source97: https://rubygems.org/downloads/logger-%{version_rubygem_logger}.gem

Source100: https://github.com/ClusterLabs/pcs-web-ui/archive/%{ui_version_or_commit}/%{ui_src_name}.tar.gz
Source101: https://github.com/ClusterLabs/pcs-web-ui/releases/download/%{ui_version_or_commit}/pcs-web-ui-node-modules-%{ui_modules_version}.tar.xz

# pcs patches: <= 200
# Patch1: bzNUMBER-01-name.patch
Patch1: do-not-support-cluster-setup-with-udp-u-transport.patch

# ui patches: >200
# Patch201: bzNUMBER-01-name.patch


# git for patches
BuildRequires: git-core
# printf from coreutils is used in makefile, head is used in spec
BuildRequires: coreutils
# find is used in Makefile and also somewhere else
BuildRequires: findutils
# python for pcs
BuildRequires: python3-cryptography
BuildRequires: python3-dateutil >= 2.7.0
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pycurl
BuildRequires: python3-pip
BuildRequires: python3-pyparsing
BuildRequires: python3-lxml
# for building bundled python packages
BuildRequires: python3-wheel
# for bundled python dateutil
BuildRequires: python3-setuptools_scm
BuildRequires: python3-tornado
# gcc for compiling custom rubygems
BuildRequires: gcc
BuildRequires: gcc-c++
# for rubygem ffi
BuildRequires: libffi-devel
# ruby and gems for pcsd
BuildRequires: ruby >= 2.5
BuildRequires: ruby-devel
BuildRequires: rubygems
BuildRequires: rubygem-bundler
BuildRequires: rubygem-json
BuildRequires: rubygem-rexml
# ruby libraries for tests
BuildRequires: rubygem-test-unit
# for touching patch files (sanitization function)
BuildRequires: diffstat
# for post, preun and postun macros
BuildRequires: systemd
# pam is used for authentication inside daemon (python ctypes)
# needed for tier0 tests during build
BuildRequires: pam
BuildRequires: make
# Red Hat logo for creating symlink of favicon
BuildRequires: redhat-logos
# for building web ui
BuildRequires: npm
# cluster stack packages for pkg-config
BuildRequires: booth
BuildRequires: corosynclib-devel >= 3.0
# Buildroot only package, provides pkgconfig of corosync-qdevice for autotools
BuildRequires: corosync-qdevice-devel
BuildRequires: fence-agents-common
BuildRequires: pacemaker-libs-devel >= %{min_compatible_pacemaker_version}, pacemaker-libs-devel < %{first_incompatible_pacemaker_version}
BuildRequires: resource-agents
BuildRequires: sbd
# for working with qdevice certificates (certutil) - used in configure.ac
BuildRequires: nss-tools
# for generating MiniDebugInfo with find-debuginfo
BuildRequires: debugedit
# pcs now provides a pc file
BuildRequires: pkgconfig

# python and libraries for pcs, setuptools for pcs entrypoint
Requires: python3 >= 3.9
Requires: python3-cryptography
Requires: python3-dateutil >= 2.7.0
Requires: python3-lxml
Requires: python3-setuptools
Requires: python3-pycurl
Requires: python3-pyparsing
Requires: python3-tornado
# ruby and gems for pcsd
Requires: ruby >= 2.5
Requires: rubygems
Requires: rubygem-json
Requires: rubygem-rexml
# for killall
Requires: psmisc
# cluster stack and related packages
Requires: pcmk-cluster-manager >= %{min_compatible_pacemaker_version}, pcmk-cluster-manager < %{first_incompatible_pacemaker_version}
Suggests: pacemaker >= %{min_compatible_pacemaker_version}, pacemaker < %{first_incompatible_pacemaker_version}
Requires: (corosync >= 3.0 if pacemaker)
# pcs enables corosync encryption by default so we require libknet1-plugins-all
Requires: (libknet1-plugins-all if corosync)
Requires: pacemaker-cli >= %{min_compatible_pacemaker_version}, pacemaker-cli < %{first_incompatible_pacemaker_version}
# for post, preun and postun macros
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
# pam is used for authentication inside daemon (python ctypes)
# more details: https://bugzilla.redhat.com/show_bug.cgi?id=1717113
Requires: pam
# favicon Red Hat logo
Requires: redhat-logos
# needs logrotate for /etc/logrotate.d/pcsd
Requires: logrotate
# for working with qdevice certificates (certutil)
Requires: nss-tools


Provides: bundled(python3-dacite) = %{dacite_version}

Provides: bundled(rubygem-backports) = %{version_rubygem_backports}
Provides: bundled(rubygem-base64) = %{version_rubygem_base64}
Provides: bundled(rubygem-childprocess) = %{version_rubygem_childprocess}
Provides: bundled(rubygem-ethon) = %{version_rubygem_ethon}
Provides: bundled(rubygem-ffi) = %{version_rubygem_ffi}
Provides: bundled(rubygem-logger) = %{version_rubygem_logger}
Provides: bundled(rubygem-mustermann) = %{version_rubygem_mustermann}
Provides: bundled(rubygem-nio4r) = %{version_rubygem_nio4r}
Provides: bundled(rubygem-puma) = %{version_rubygem_puma}
Provides: bundled(rubygem-rack) = %{version_rubygem_rack}
Provides: bundled(rubygem-rack-protection) = %{version_rubygem_rack_protection}
Provides: bundled(rubygem-rack-session) = %{version_rubygem_rack_session}
Provides: bundled(rubygem-rack-test) = %{version_rubygem_rack_test}
Provides: bundled(rubygem-rackup) = %{version_rubygem_rackup}
Provides: bundled(rubygem-ruby2_keywords) = %{version_rubygem_ruby2_keywords}
Provides: bundled(rubygem-sinatra) = %{version_rubygem_sinatra}
Provides: bundled(rubygem-tilt) = %{version_rubygem_tilt}

Provides: bundled(pcs-web-ui) = %{!?ui_tarball_version:%{ui_version}}%{?ui_tarball_version}


%description
pcs is a corosync and pacemaker configuration tool.  It permits users to
easily view, modify and create pacemaker based clusters.

# pcs-snmp package definition
%package -n %{pcs_snmp_pkg_name}
Group: System Environment/Base
Summary: Pacemaker cluster SNMP agent
# https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing#Good_Licenses
# GPL-2.0-only: pcs
# BSD-2-Clause: pyagentx
License: GPL-2.0-only AND BSD-2-Clause
URL: https://github.com/ClusterLabs/pcs

# tar for unpacking pyagentx source tarball
BuildRequires: tar

Requires: pcs = %{version}-%{release}
Requires: pacemaker
Requires: net-snmp

Provides: bundled(python3-pyagentx) = %{pyagentx_version}

%description -n %{pcs_snmp_pkg_name}
SNMP agent that provides information about pacemaker cluster to the master agent (snmpd)

%prep
# -- following is inspired by python-simplejon.el5 --
# Update timestamps on the files touched by a patch, to avoid non-equal
# .pyc/.pyo files across the multilib peers within a build

update_times(){
  # update_times <reference_file> <file_to_touch> ...
  # set the access and modification times of each file_to_touch to the times
  # of reference_file

  # put all args to file_list
  file_list=("$@")
  # first argument is reference_file: so take it and remove from file_list
  reference_file=${file_list[0]}
  unset file_list[0]

  for fname in ${file_list[@]}; do
    # some files could be deleted by a patch therefore we test file for
    # existance before touch to avoid exit with error: No such file or
    # directory
    # diffstat cannot create list of files without deleted files
    test -e $fname && touch -r $reference_file $fname
  done
}

update_times_patch(){
  # update_times_patch <patch_file_name>
  # set the access and modification times of each file in patch to the times
  # of patch_file_name

  patch_file_name=$1

  # diffstat
  # -l lists only the filenames. No histogram is generated.
  # -p override the logic that strips common pathnames,
  #    simulating the patch "-p" option. (Strip the smallest prefix containing
  #    num leading slashes from each file name found in the patch file)
  update_times ${patch_file_name} `diffstat -p1 -l ${patch_file_name}`
}

# documentation for setup/autosetup/autopatch:
#   * http://ftp.rpm.org/max-rpm/s1-rpm-inside-macros.html
#   * https://rpm-software-management.github.io/rpm/manual/autosetup.html
# patch web-ui sources
# -n <name> — Set Name of Build Directory
# -T — Do Not Perform Default Archive Unpacking
# -b <n> — Unpack The nth Sources Before Changing Directory
# -a <n> — Unpack The nth Sources After Changing Directory
# -N — disables automatic patch application, use autopatch to apply patches
#
# 1. unpack sources (-b 0)
# 2. then cd into sources tree (the setup macro itself)
# 3. then unpack node_modules into sources tree (-a 1).
%autosetup -T -b 100 -a 101 -N -n %{ui_src_name}
%autopatch -p1 -m 201
# update_times_patch %%{PATCH201}

# patch pcs sources
%autosetup -S git -n %{pcs_source_name} -N
%autopatch -p1 -M 200
# update_times_patch %%{PATCH1}
update_times_patch %{PATCH1}


# generate .tarball-version if building from an untagged commit, not a released version
# autogen uses git-version-gen which uses .tarball-version for generating version number
%if 0%{?tarball_version:1}
  echo %{tarball_version} > %{_builddir}/%{pcs_source_name}/.tarball-version
%endif


%if 0%{?ui_tarball_version:1}
  echo %{ui_tarball_version} > %{_builddir}/%{ui_src_name}/.tarball-version
%endif

# prepare dirs/files necessary for building all bundles
# -----------------------------------------------------
# 1) rubygems sources

mkdir -p %{rubygem_cache_dir}
cp -f %SOURCE81 %{rubygem_cache_dir}
cp -f %SOURCE82 %{rubygem_cache_dir}
cp -f %SOURCE83 %{rubygem_cache_dir}
cp -f %SOURCE84 %{rubygem_cache_dir}
cp -f %SOURCE85 %{rubygem_cache_dir}
cp -f %SOURCE86 %{rubygem_cache_dir}
cp -f %SOURCE87 %{rubygem_cache_dir}
cp -f %SOURCE88 %{rubygem_cache_dir}
cp -f %SOURCE89 %{rubygem_cache_dir}
cp -f %SOURCE90 %{rubygem_cache_dir}
cp -f %SOURCE91 %{rubygem_cache_dir}
cp -f %SOURCE92 %{rubygem_cache_dir}
cp -f %SOURCE93 %{rubygem_cache_dir}
cp -f %SOURCE94 %{rubygem_cache_dir}
cp -f %SOURCE95 %{rubygem_cache_dir}
cp -f %SOURCE96 %{rubygem_cache_dir}
cp -f %SOURCE97 %{rubygem_cache_dir}


# 2) prepare python bundles
mkdir -p %{pcs_bundled_dir}/src
cp -f %SOURCE41 rpm/
cp -f %SOURCE44 rpm/

%build
%define debug_package %{nil}

# We left off by setting up pcs, so we are in its directory now
./autogen.sh
%{configure} --enable-local-build --enable-use-local-cache-only \
  --enable-individual-bundling --with-pcsd-default-cipherlist='PROFILE=SYSTEM' \
  --enable-booth-enable-authfile-unset --enable-booth-enable-authfile-set \
  PYTHON=%{__python3} ruby_CFLAGS="%{optflags}" ruby_LIBS="%{build_ldflags}"
make all

# Web UI build
# Switch to web ui folder first
cd ../%{ui_src_name}
./autogen.sh
%{configure} \
  --disable-cockpit \
  --with-pcsd-webui-dir="%{_libdir}/%{pcsd_public_dir}/ui"
make all

%install
rm -rf %{buildroot}
pwd

# Install cockpit pcs-web-ui
cd ../%{ui_src_name}
%make_install

# symlink favicon into pcsd directories
mkdir -p %{buildroot}%{_libdir}/%{pcsd_public_dir}/ui/static/media
ln -fs /etc/favicon.png %{buildroot}%{_libdir}/%{pcsd_public_dir}/ui/static/media/favicon.png

# prepare pcs-web-ui files (not needed for pcs as pcs installs them in Makefile)
mkdir -p %{buildroot}/%{_defaultlicensedir}/%{name}
mv COPYING %{buildroot}/%{_defaultlicensedir}/%{name}/COPYING_WUI.md

mkdir -p %{buildroot}/%{_docdir}/%{name}
mv CHANGELOG.md %{buildroot}/%{_docdir}/%{name}/CHANGELOG_WUI.md
mv README.md %{buildroot}/%{_docdir}/%{name}/README_WUI.md


# Install pcs
cd ../%{pcs_source_name}
%make_install

# RHEL-7716 - fix rubygem permissions - remove write access for owner's group
# and other users
chmod --recursive g-w,o-w %{buildroot}%{_libdir}/%{rubygem_bundle_dir}

# prepare license files
mv %{rubygem_bundle_dir}/gems/backports-%{version_rubygem_backports}/LICENSE.txt backports_LICENSE.txt
mv %{rubygem_bundle_dir}/gems/base64-%{version_rubygem_base64}/LICENSE.txt base64_LICENSE.txt
mv %{rubygem_bundle_dir}/gems/childprocess-%{version_rubygem_childprocess}/LICENSE childprocess_LICENSE
mv %{rubygem_bundle_dir}/gems/ethon-%{version_rubygem_ethon}/LICENSE ethon_LICENSE
mv %{rubygem_bundle_dir}/gems/ffi-%{version_rubygem_ffi}/COPYING ffi_COPYING
mv %{rubygem_bundle_dir}/gems/ffi-%{version_rubygem_ffi}/LICENSE ffi_LICENSE
mv %{rubygem_bundle_dir}/gems/ffi-%{version_rubygem_ffi}/LICENSE.SPECS ffi_LICENSE.SPECS
mv %{rubygem_bundle_dir}/gems/logger-%{version_rubygem_logger}/BSDL logger_BSDL
mv %{rubygem_bundle_dir}/gems/logger-%{version_rubygem_logger}/COPYING logger_COPYING
mv %{rubygem_bundle_dir}/gems/mustermann-%{version_rubygem_mustermann}/LICENSE mustermann_LICENSE
mv %{rubygem_bundle_dir}/gems/nio4r-%{version_rubygem_nio4r}/license.md nio4r_license.md
mv %{rubygem_bundle_dir}/gems/nio4r-%{version_rubygem_nio4r}/ext/libev/LICENSE nio4r_libev_LICENSE
mv %{rubygem_bundle_dir}/gems/puma-%{version_rubygem_puma}/LICENSE puma_LICENSE
mv %{rubygem_bundle_dir}/gems/rack-%{version_rubygem_rack}/MIT-LICENSE rack_MIT-LICENSE
mv %{rubygem_bundle_dir}/gems/rack-protection-%{version_rubygem_rack_protection}/License rack-protection_License
mv %{rubygem_bundle_dir}/gems/rack-session-%{version_rubygem_rack_session}/license.md rack-session_license.md
mv %{rubygem_bundle_dir}/gems/rack-test-%{version_rubygem_rack_test}/MIT-LICENSE.txt rack-test_MIT-LICENSE.txt
mv %{rubygem_bundle_dir}/gems/rackup-%{version_rubygem_rackup}/license.md rackup_license.md
mv %{rubygem_bundle_dir}/gems/ruby2_keywords-%{version_rubygem_ruby2_keywords}/LICENSE ruby2_keywords_LICENSE
mv %{rubygem_bundle_dir}/gems/sinatra-%{version_rubygem_sinatra}/LICENSE sinatra_LICENSE
mv %{rubygem_bundle_dir}/gems/tilt-%{version_rubygem_tilt}/COPYING tilt_COPYING

cp %{pcs_bundled_dir}/src/pyagentx-*/LICENSE.txt pyagentx_LICENSE.txt
cp %{pcs_bundled_dir}/src/pyagentx-*/CONTRIBUTORS.txt pyagentx_CONTRIBUTORS.txt
cp %{pcs_bundled_dir}/src/pyagentx-*/README.md pyagentx_README.md

cp %{pcs_bundled_dir}/src/dacite-*/LICENSE dacite_LICENSE
cp %{pcs_bundled_dir}/src/dacite-*/README.md dacite_README.md

# We are not building debug package for pcs but we need to add MiniDebuginfo
# to the bundled shared libraries from rubygem extensions in order to satisfy
# rpmdiff's binary stripping checker.
# Therefore we call find-debuginfo from debugedit manually in order to strip
# binaries and add MiniDebugInfo with .gnu_debugdata section
find-debuginfo -j2 -m -i -S debugsourcefiles.list
# find-debuginfo generated some files into /usr/lib/debug  and
# /usr/src/debug/ that we don't want in the package
rm -rf %{buildroot}%{_libdir}/debug
rm -rf %{buildroot}/usr/lib/debug
rm -rf %{buildroot}%{_prefix}/src/debug

# We can remove files required for gem compilation
rm -rf %{buildroot}%{_libdir}/%{rubygem_bundle_dir}/gems/ffi-%{version_rubygem_ffi}/ext
rm -rf %{buildroot}%{_libdir}/%{rubygem_bundle_dir}/gems/nio4r-%{version_rubygem_nio4r}/ext
rm -rf %{buildroot}%{_libdir}/%{rubygem_bundle_dir}/gems/puma-%{version_rubygem_puma}/ext

# Sinatra contains example applications which are unnecessary (discovered by brp_mangle_shebangs)
rm -rf %{buildroot}%{_libdir}/%{rubygem_bundle_dir}/gems/sinatra-%{version_rubygem_sinatra}/examples
rm -rf %{buildroot}%{_libdir}/%{rubygem_bundle_dir}/gems/sinatra-%{version_rubygem_sinatra}/examples

# Puma contains an unnecessary rc init script (discovered by brp_mangle_shebangs)
rm -rf %{buildroot}%{_libdir}/%{rubygem_bundle_dir}/gems/puma-%{version_rubygem_puma}/docs/jungle/rc.d
rm -rf %{buildroot}%{_libdir}/%{rubygem_bundle_dir}/gems/puma-%{version_rubygem_puma}/docs/jungle/rc.d

# Remove unused rubygem executables with wrong shebangs (discovered by brp_mangle_shebangs)
rm -fv %{buildroot}/%{_libdir}/pcsd/vendor/bundle/gems/puma-*/bin/puma
rm -fv %{buildroot}/%{_libdir}/pcsd/vendor/bundle/gems/puma-*/bin/pumactl
rm -fv %{buildroot}/%{_libdir}/pcsd/vendor/bundle/gems/rackup-*/bin/rackup
rm -fv %{buildroot}/%{_libdir}/pcsd/vendor/bundle/gems/tilt-*/bin/tilt

%check
# In the building environment LC_CTYPE is set to C which causes tests to fail
# due to python prints a warning about it to stderr. The following environment
# variable disables the warning.
# On the live system either UTF8 locale is set or the warning is emmited
# which breaks pcs. That is the correct behavior since with wrong locales it
# would be probably broken anyway.
# The main concern here is to make the tests pass.
# See https://fedoraproject.org/wiki/Changes/python3_c.utf-8_locale for details.
export PYTHONCOERCECLOCALE=0

run_all_tests(){
  #run pcs tests

  # disabled tests:
  #
  # pcs_test.tier0.daemon.app.test_app_remote.SyncConfigMutualExclusive
  # 	disabled due to race conditions on slower machines

    %{__python3} pcs_test/suite --tier0 -v --vanilla --all-but \
    pcs_test.tier0.daemon.app.test_app_remote.SyncConfigMutualExclusive.test_get_not_locked \
    pcs_test.tier0.daemon.app.test_app_remote.SyncConfigMutualExclusive.test_post_not_locked \

  test_result_python=$?

  #run pcsd tests and remove them
  GEM_HOME=%{buildroot}%{_libdir}/%{rubygem_bundle_dir} ruby \
    -I%{buildroot}%{_libdir}/pcsd \
    -Ipcsd/test \
    pcsd/test/test_all_suite.rb
  test_result_ruby=$?

  if [ $test_result_python -ne 0 ]; then
    return $test_result_python
  fi
  return $test_result_ruby
}

run_all_tests

%posttrans
# Make sure the new version of the daemon is running.
# Also, make sure to start pcsd-ruby if it hasn't been started or even
# installed before. This is done by restarting pcsd.service.
%{_bindir}/systemctl daemon-reload
%{_bindir}/systemctl try-restart pcsd.service


%post
%systemd_post pcsd.service
%systemd_post pcsd-ruby.service

%post -n %{pcs_snmp_pkg_name}
%systemd_post pcs_snmp_agent.service

%preun
%systemd_preun pcsd.service
%systemd_preun pcsd-ruby.service

%preun -n %{pcs_snmp_pkg_name}
%systemd_preun pcs_snmp_agent.service

%postun
%systemd_postun_with_restart pcsd.service
%systemd_postun_with_restart pcsd-ruby.service

%postun -n %{pcs_snmp_pkg_name}
%systemd_postun_with_restart pcs_snmp_agent.service

%files
%doc CHANGELOG.md
%doc README.md
%doc %{_docdir}/%{name}/CHANGELOG_WUI.md
%doc %{_docdir}/%{name}/README_WUI.md
%doc dacite_README.md
%license dacite_LICENSE
%license COPYING
%license %{_defaultlicensedir}/%{name}/COPYING_WUI.md
# rubygem licenses
%license backports_LICENSE.txt
%license base64_LICENSE.txt
%license childprocess_LICENSE
%license ethon_LICENSE
%license ffi_COPYING
%license ffi_LICENSE
%license ffi_LICENSE.SPECS
%license logger_BSDL
%license logger_COPYING
%license mustermann_LICENSE
%license nio4r_license.md
%license nio4r_libev_LICENSE
%license puma_LICENSE
%license rack_MIT-LICENSE
%license rack-protection_License
%license rack-session_license.md
%license rack-test_MIT-LICENSE.txt
%license rackup_license.md
%license ruby2_keywords_LICENSE
%license sinatra_LICENSE
%license tilt_COPYING
%{python3_sitelib}/*
%{_sbindir}/pcs
%{_sbindir}/pcsd
%{_libdir}/pcs/*
%{_libdir}/pcsd/*
%{_libdir}/pkgconfig/pcs.pc
%{_unitdir}/pcsd.service
%{_unitdir}/pcsd-ruby.service
%{_datadir}/bash-completion/completions/pcs
%ghost %attr(0700,root,root) %{_sharedstatedir}/pcsd
%ghost %attr(0700,root,root) %{_var}/log/pcsd
%config(noreplace) %{_sysconfdir}/pam.d/pcsd
%config(noreplace) %{_sysconfdir}/logrotate.d/pcsd
%config(noreplace) %{_sysconfdir}/sysconfig/pcsd
%ghost %config(noreplace) %attr(0600,root,root) %{_sharedstatedir}/pcsd/cfgsync_ctl
%ghost %config(noreplace) %attr(0600,root,root) %{_sharedstatedir}/pcsd/known-hosts
%ghost %config(noreplace) %attr(0600,root,root) %{_sharedstatedir}/pcsd/pcsd.cookiesecret
%ghost %config(noreplace) %attr(0600,root,root) %{_sharedstatedir}/pcsd/pcsd.crt
%ghost %config(noreplace) %attr(0600,root,root) %{_sharedstatedir}/pcsd/pcsd.key
%ghost %config(noreplace) %attr(0644,root,root) %{_sharedstatedir}/pcsd/pcs_settings.conf
%ghost %config(noreplace) %attr(0600,root,root) %{_sharedstatedir}/pcsd/pcs_users.conf
%{_mandir}/man8/pcs.*
%{_mandir}/man8/pcsd.*
%exclude %{_libdir}/pcs/pcs_snmp_agent
%exclude %{_libdir}/pcs/%{pcs_bundled_dir}/packages/pyagentx*


%files -n %{pcs_snmp_pkg_name}
%{_libdir}/pcs/pcs_snmp_agent
%{_libdir}/pcs/%{pcs_bundled_dir}/packages/pyagentx*
%{_unitdir}/pcs_snmp_agent.service
%{_datadir}/snmp/mibs/PCMK-PCS*-MIB.txt
%{_mandir}/man8/pcs_snmp_agent.*
%config(noreplace) %{_sysconfdir}/sysconfig/pcs_snmp_agent
%doc CHANGELOG.md
%doc pyagentx_CONTRIBUTORS.txt
%doc pyagentx_README.md
%license COPYING
%license pyagentx_LICENSE.txt


%changelog
* Thu Oct 23 2025 Michal Pospíšil <mpospisi@redhat.com> - 0.11.10-1%{?dist}.1
- Fixed CVE-2025-59830, CVE-2025-61770, CVE-2025-61771, CVE-2025-61772, CVE-2025-61919 by updating bundled rubygem rack
  Resolves: RHEL-120945, RHEL-121035, RHEL-123630, RHEL-123642, RHEL-124938

* Wed Jul 9 2025 Michal Pospisil <mpospisi@redhat.com> - 0.11.10-1
- Rebased pcs to the latest sources (see CHANGELOG.md)
  Resolves: RHEL-77194, RHEL-92044
- Updated pcs-web-ui to 0.1.23 (see CHANGELOG_WUI.md)
  Resolves: RHEL-76309, RHEL-99805
- There is now a changelog for the pcsd web UI
  Resolves: RHEL-86233
- Fixed directory permissions for RHEL Image Mode
  Resolves: RHEL-97220
- Updated bundled rubygem rack

* Wed May 14 2025 Michal Pospisil <mpospisi@redhat.com> - 0.11.9-3
- Rebased pcs to the latest sources (see CHANGELOG.md)
  Resolves: RHEL-35420, RHEL-76055, RHEL-76059, RHEL-76060, RHEL-76153, RHEL-76154, RHEL-76170, RHEL-76177, RHEL-82894
- Rebased pcs-web-ui to the latest sources
  Resolves: RHEL-76310, RHEL-76311, RHEL-76312, RHEL-79317, RHEL-85196, RHEL-85197, RHEL-85745
- The upstream version of pcs-web-ui can now be queried through RPM - see bundled(pcs-web-ui)
  Resolves: RHEL-86229
- Updated bundled rubygems: backports, childprocess, ffi, puma, rack, rack-protection, rack-session, rack-test, sinatra, tilt
  Resolves: RHEL-90151
- Bundled rubygem logger

* Fri Feb 14 2025 Michal Pospisil <mpospisi@redhat.com> - 0.11.9-2
- Fixed restarting bundles
  Resolves: RHEL-79055
- Fixed deletion of misconfigured bundles
  Resolves: RHEL-79160
- Fixed filtering of resource clones in web console
  Resolves: RHEL-78653
- Updated bundled rubygem rack
  Resolves: RHEL-79500

* Mon Jan 13 2025 Michal Pospisil <mpospisi@redhat.com> - 0.11.9-1
- Rebased pcs to the latest sources (see CHANGELOG.md)
  Resolves: RHEL-44420
- Updated pcs-web-ui to 0.1.22

* Mon Dec 16 2024 Michal Pospisil <mpospisi@redhat.com> - 0.11.8-2
- Rebased pcs to the latest sources (see CHANGELOG.md)
  Resolves: RHEL-46303, RHEL-69040
- Rebased pcs-web-ui to the latest sources
  Resolves: RHEL-69272, RHEL-69278, RHEL-69279, RHEL-69280, RHEL-69281, RHEL-69282

* Tue Nov 19 2024 Michal Pospisil <mpospisi@redhat.com> - 0.11.8-2
- Rebased to the latest sources (see CHANGELOG.md)
  Resolves: RHEL-16232, RHEL-46284, RHEL-46286, RHEL-46293, RHEL-55441, RHEL-61738, RHEL-61901
- Updated pcs-web-ui to 0.1.21
- Updated bundled rubygems: ffi, mustermann, puma, rack, rackup, tilt
- Removed bundled rubygem webrick
- New runtime dependency python3-tornado which has been bundled in previous versions

* Tue Jul 9 2024 Michal Pospisil <mpospisi@redhat.com> - 0.11.8-1
- Updated pcs-web-ui to 0.1.20
- Rebased to the latest sources (see CHANGELOG.md)
  Resolves: RHEL-34781

* Tue Jun 18 2024 Michal Pospisil <mpospisi@redhat.com> - 0.11.7-4
- Rebased to the latest sources (see CHANGELOG.md)
  Resolves: RHEL-7701, RHEL-7737, RHEL-17962, RHEL-34781
- Fixed grammatical error in pcs-web-ui
  Resolves: RHEL-7726

* Tue May 21 2024 Michal Pospisil <mpospisi@redhat.com> - 0.11.7-3
- Rebased to the latest sources (see CHANGELOG.md)
  Resolves: RHEL-2977, RHEL-16231, RHEL-21051, RHEL-25854, RHEL-27492, RHEL-28749, RHEL-34781, RHEL-36514
- Updated pcs-web-ui to 0.1.19
  Resolves: RHEL-7726, RHEL-21895, RHEL-21896, RHEL-21897
- Updated bundled rubygems: backports, childprocess, nio4r, puma, rack, rack-protection, sinatra
- Bundled new rubygems: base64, rack-session, rackup, webrick

* Tue Mar 19 2024 Michal Pospisil <mpospisi@redhat.com> - 0.11.7-2
- Fixed CVE-2024-25126, CVE-2024-26141, CVE-2024-26146 in bundled dependency rack
  Resolves: RHEL-26446, RHEL-26448, RHEL-26450

* Fri Jan 05 2024 Michal Pospisil <mpospisi@redhat.com> - 0.11.7-1
- Rebased to the latest sources (see CHANGELOG.md)
  Resolves: RHEL-7740

* Mon Nov 13 2023 Michal Pospisil <mpospisi@redhat.com> - 0.11.6-6
- Rebased to the latest upstream sources (see CHANGELOG.md)
  Resolves: RHEL-7582, RHEL-7583, RHEL-7669, RHEL-7672, RHEL-7697, RHEL-7698, RHEL-7700, RHEL-7703, RHEL-7719, RHEL-7725, RHEL-7730, RHEL-7738, RHEL-7739, RHEL-7740, RHEL-7744, RHEL-7746
- TLS cipher setting in pcsd now follows system-wide crypto policies by default
  Resolves: RHEL-7724
- Tightened permissions of bundled rubygems to be 755 or stricter
  Resolves: RHEL-7716

* Thu Nov 2 2023 Michal Pospisil <mpospisi@redhat.com> - 0.11.6-5
- No changes, fixing an error in a new quality control process
- Resolves: RHEL-15217

* Fri Oct 27 2023 Michal Pospisil <mpospisi@redhat.com> - 0.11.6-4
- No changes, testing a new quality control process
- Resolves: RHEL-15217

* Fri Jul 14 2023 Michal Pospisil <mpospisi@redhat.com> - 0.11.6-3
- Refreshing any page in pcs-web-ui no longer causes it to display a blank page
- Resolves: rhbz#2222788

* Mon Jul 10 2023 Michal Pospisil <mpospisi@redhat.com> - 0.11.6-2
- Added BuildRequires: debugedit - for generating MiniDebugInfo - triggered by removing find-debuginfo.sh from rpm
- Make use of filters when extracting tarballs to enhance security if provided by Python (pcs config restore command)
- Exporting constraints with rules in form of pcs commands now escapes # and fixes spaces in dates to make the commands valid
- Constraints containing options unsupported by pcs are not exported and a warning is printed instead
- Using spaces in dates in location constraint rules is deprecated
- Resolves: rhbz#2163953 rhbz#2216434 rhbz#2217850 rhbz#2219407

* Tue Jun 20 2023 Michal Pospisil <mpospisi@redhat.com> - 0.11.6-1
- Rebased to the latest upstream sources (see CHANGELOG.md)
- Updated bundled rubygems: puma, tilt
- Resolves: rhbz#1465829 rhbz#2163440 rhbz#2168155

* Wed May 31 2023 Michal Pospisil <mpospisi@redhat.com> - 0.11.5-2
- Fixed a regression causing crash in `pcs resource move` command (broken since pcs-0.11.5)
- Resolves: rhbz#2210855

* Mon May 22 2023 Michal Pospisil <mpospisi@redhat.com> - 0.11.5-1
- Rebased to the latest upstream sources (see CHANGELOG.md)
- Updated pcs-web-ui
- Updated bundled dependencies: tornado, dacite
- Added bundled rubygems: nio4r, puma
- Removed bundled rubygems: daemons, eventmachine, thin, webrick
- Updated bundled rubygems: backports, rack, rack-protection, rack-test, sinatra, tilt
- Added dependency nss-tools - for working with qdevice certificates
- Resolves: rhbz#1423473 rhbz#1860626 rhbz#2160664 rhbz#2163440 rhbz#2163914 rhbz#2163953 rhbz#2168155 rhbz#2168617 rhbz#2174735 rhbz#2174829 rhbz#2175881 rhbz#2177996 rhbz#2178701 rhbz#2178714 rhbz#2179902 rhbz#2180379 rhbz#2182810

* Tue Mar 28 2023 Michal Pospisil <mpospisi@redhat.com> - 0.11.4-7
- Fix displaying differences between configuration checkpoints in “pcs config checkpoint diff” command
- Fix “pcs stonith update-scsi-devices” command which was broken since Pacemaker-2.1.5-rc1
- Fixed loading of cluster status in the web interface when fencing levels are configured
- Fixed a vulnerability in pcs-web-ui-node-modules
- Updated bundled rubygem rack
- Resolves: rhbz#2179901 rhbz#2180697 rhbz#2180704 rhbz#2180708 rhbz#2180978 rhbz#2183180

* Mon Feb 13 2023 Michal Pospisil <mpospisi@redhat.com> - 0.11.4-6
- Fixed broken filtering in create resource/fence device wizards in the web interface
- Added BuildRequires: pam - needed for tier0 tests during build
- Resolves: rhbz#2167471

* Thu Feb 02 2023 Michal Pospisil <mpospisi@redhat.com> - 0.11.4-5
- Fixed enabling/disabling sbd when cluster is not running
- Resolves: rhbz#2166249

* Fri Jan 13 2023 Michal Pospisil <mpospisi@redhat.com> - 0.11.4-4
- Rebuilt with fixed patches
- Resolves: rhbz#2158790 rhbz#2159454

* Thu Jan 12 2023 Michal Pospisil <mpospisi@redhat.com> - 0.11.4-3
- Allow time values in stonith-watchdog-time property
- Resource/stonith agent self-validation of instance attributes is now disabled by default, as many agents do not work with it properly.
- Updated bundled rubygems: rack, rack-protection, sinatra
- Added license for ruby2_keywords
- Resolves: rhbz#2158790 rhbz#2159454

* Wed Dec 14 2022 Michal Pospisil <mpospisi@redhat.com> - 0.11.4-2
- Fixed stopping of pcsd service using systemctl stop pcsd command
- Fixed smoke test execution during gating
- Added warning when omitting validation of misconfigured resource
- Fixed displaying of bool and integer values in `pcs resource config` command
- Updated bundled rubygems: ethon, rack-protection, sinatra
- Resolves: rhbz#2148124 rhbz#2151164 rhbz#2151524

* Tue Nov 22 2022 Michal Pospisil <mpospisi@redhat.com> - 0.11.4-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Updated pcs-web-ui
- Resolves: rhbz#1620043 rhbz#2019464 rhbz#2099653 rhbz#2109633 rhbz#2112293 rhbz#2116295 rhbz#2117600 rhbz#2117601

* Mon Oct 24 2022 Miroslav Lisik <mlisik@redhat.com> - 0.11.3-5
- Rebased to latest upstream sources (see CHANGELOG.md)
- Updated pcs-web-ui
- Added bundled rubygem: childprocess
- Removed bundled rubygem: open4
- Updated bundled rubygems: mustermann, rack, rack-protection, rack-test, sinatra, tilt
- Resolves: rhbz#1493416 rhbz#1796827 rhbz#2059147 rhbz#2092950 rhbz#2112079 rhbz#2112270 rhbz#2112293 rhbz#2117599 rhbz#2117601

* Mon Sep 05 2022 Miroslav Lisik <mlisik@redhat.com> - 0.11.3-4
- Fixed ruby socket permissions
- Resolves: rhbz#2116841

* Thu Jul 28 2022 Miroslav Lisik <mlisik@redhat.com> - 0.11.3-3
- Fixed booth ticket mode value case insensitive
- Fixed booth sync check whether /etc/booth exists
- Resolves: rhbz#2026725 rhbz#2058243

* Tue Jul 12 2022 Miroslav Lisik <mlisik@redhat.com> - 0.11.3-2
- Fixed 'pcs resource restart' traceback
- Resolves: rhbz#2102663

* Fri Jun 24 2022 Miroslav Lisik <mlisik@redhat.com> - 0.11.3-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Updated pcs-web-ui
- Updated bundled rubygems: rack
- Resolves: rhbz#2059122 rhbz#2059177 rhbz#2059501 rhbz#2095695 rhbz#2096886 rhbz#2097730 rhbz#2097731 rhbz#2097732 rhbz#2097733 rhbz#2097778

* Thu May 19 2022 Miroslav Lisik <mlisik@redhat.com> - 0.11.2-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Updated pcs-web-ui
- Updated bundled rubygems: backports, daemons, ethon ffi, ruby2_keywords, thin
- Stopped bundling rubygem-rexml (use distribution package instead)
- Resolves: rhbz#1301204 rhbz#2024522 rhbz#2026725 rhbz#2029844 rhbz#2039884 rhbz#2053177 rhbz#2054671 rhbz#2058243 rhbz#2058246 rhbz#2058247 rhbz#2058251 rhbz#2058252 rhbz#2059142 rhbz#2059145 rhbz#2059148 rhbz#2059149 rhbz#2059501 rhbz#2064818 rhbz#2068457 rhbz#2076585

* Wed May 04 2022 Miroslav Lisik <mlisik@redhat.com> - 0.11.1-11
- Updated bundled rubygems: sinatra, rack-protection
- Resolves: rhbz#2081334

* Tue Feb 01 2022 Miroslav Lisik <mlisik@redhat.com> - 0.11.1-10
- Fixed snmp client
- Fixed translating resource roles in colocation constraint
- Resolves: rhbz#2048640

* Tue Jan 25 2022 Miroslav Lisik <mlisik@redhat.com> - 0.11.1-9
- Fixed cluster destroy in web ui
- Fixed covscan issue in web ui
- Resolves: rhbz#2044409

* Fri Jan 14 2022 Miroslav Lisik <mlisik@redhat.com> - 0.11.1-8
- Fixed 'pcs resource move' command
- Fixed removing of unavailable fence-scsi storage device
- Fixed ocf validation of ocf linbit drdb agent
- Fixed creating empty cib
- Updated pcs-web-ui
- Resolves: rhbz#1990787 rhbz#2033248 rhbz#2039883 rhbz#2040420

* Wed Dec 15 2021 Miroslav Lisik <mlisik@redhat.com> - 0.11.1-7
- Fixed enabling corosync-qdevice
- Fixed resource update command when unable to get agent metadata
- Fixed revert of disallowing to clone a group with a stonith
- Resolves: rhbz#1811072 rhbz#2019836 rhbz#2032473

* Thu Dec 02 2021 Miroslav Lisik <mlisik@redhat.com> - 0.11.1-6
- Rebased to latest upstream sources (see CHANGELOG.md)
- Updated pcs web ui
- Resolves: rhbz#1990787 rhbz#1997019 rhbz#2012129 rhbz#2024542 rhbz#2027678 rhbz#2027679

* Thu Nov 18 2021 Miroslav Lisik <mlisik@redhat.com> - 0.11.1-5
- Rebased to latest upstream sources (see CHANGELOG.md)
- Resolves: rhbz#1990787 rhbz#2018969 rhbz#2019836 rhbz#2023752 rhbz#2012129

* Tue Nov 02 2021 Miroslav Lisik <mlisik@redhat.com> - 0.11.1-4
- Rebased to latest upstream sources (see CHANGELOG.md)
- Updated pcs web ui
- Enabled wui patching
- Resolves: rhbz#1811072 rhbz#1945305 rhbz#1997019 rhbz#2012129

* Thu Aug 26 2021 Miroslav Lisik <mlisik@redhat.com> - 0.11.1-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Resolves: rhbz#1283805 rhbz#1910644 rhbz#1910645  rhbz#1956703 rhbz#1956706 rhbz#1985981 rhbz#1991957 rhbz#1996062 rhbz#1996067

* Tue Aug 24 2021 Miroslav Lisik <mlisik@redhat.com> - 0.11.0.alpha.1-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Updated pcs web ui
- Resolves: rhbz#1283805 rhbz#1910644 rhbz#1910645 rhbz#1985981 rhbz#1991957 rhbz#1996067

* Thu Aug 19 2021 DJ Delorie <dj@redhat.com> - 0.10.9-2
- Rebuilt for libffi 3.4.2 SONAME transition.
  Related: rhbz#1891914

* Tue Aug 10 2021 Miroslav Lisik <mlisik@redhat.com> - 0.10.9-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Resolves: rhbz#1991957

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 0.10.8-11
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Tue Jul 20 2021 Miroslav Lisik <mlisik@redhat.com> - 0.10.8-10
- Rebased to latest upstream sources (see CHANGELOG.md)
- Fixed web-ui build
- Fixed tests for pacemaker 2.1
- Resolves: rhbz#1975440 rhbz#1922302

* Tue Jun 22 2021 Mohan Boddu <mboddu@redhat.com> - 0.10.8-9
- Rebuilt for RHEL 9 BETA for openssl 3.0
  Related: rhbz#1971065

* Wed Jun 16 2021 Miroslav Lisik <mlisik@redhat.com> - 0.10.8-8
- Rebuild with fixed gaiting tests
- Stopped bundling rubygem-json (use distribution package instead)
- Fixed patches
- Resolves: rhbz#1881064

* Tue Jun 15 2021 Miroslav Lisik <mlisik@redhat.com> - 0.10.8-7
- Fixed License tag
- Rebuild with fixed dependency for gating tier0 tests
- Resolves: rhbz#1881064

* Thu Jun 10 2021 Miroslav Lisik <mlisik@redhat.com> - 0.10.8-6
- Rebased to latest upstream sources (see CHANGELOG.md)
- Removed clufter related commands
- Resolves: rhbz#1881064

* Wed Apr 28 2021 Miroslav Lisik <mlisik@redhat.com> - 0.10.8-5
- Updated pcs web ui node modules
- Fixed build issue on low memory build hosts
- Resolves: rhbz#1951272

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 0.10.8-4
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Thu Mar 04 2021 Miroslav Lisik <mlisik@redhat.com> - 0.10.8-3
- Replace pyOpenSSL with python-cryptography
- Resolves: rhbz#1927404

* Fri Feb 19 2021 Miroslav Lisik <mlisik@redhat.com> - 0.10.8-2
- Bundle rubygem depedencies and python3-tornado
- Resolves: rhbz#1929710

* Thu Feb 04 2021 Miroslav Lisik <mlisik@redhat.com> - 0.10.8-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Updated pcs-web-ui
- Updated bundled python dependency: dacite
- Changed BuildRequires from git to git-core
- Added conditional (Build)Requires: rubygem(rexml)
- Added conditional Requires: rubygem(webrick)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan  7 2021 Vít Ondruch <vondruch@redhat.com> - 0.10.7-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.0

* Thu Nov 26 2020 Ondrej Mular <omular@redhat.com> - 0.10.7-2
- Python 3.10 related fix

* Wed Sep 30 2020 Miroslav Lisik <mlisik@redhat.com> - 0.10.7-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Added dependency on python packages pyparsing and dateutil
- Fixed virtual bundle provides for ember, handelbars, jquery and jquery-ui
- Removed dependency on python3-clufter

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Miroslav Lisik <mlisik@redhat.com> - 0.10.6-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Updated pcs-web-ui
- Stopped bundling tornado (use distribution package instead)
- Stopped bundling rubygem-tilt (use distribution package instead)
- Removed rubygem bundling
- Removed unneeded BuildRequires: execstack, gcc, gcc-c++
- Excluded some tests for tornado daemon

* Tue Jul 21 2020 Tom Stellard <tstellar@redhat.com> - 0.10.5-8
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Wed Jul 15 2020 Ondrej Mular <omular@redhat.com> - 0.10.5-7
- Use fixed upstream version of dacite with Python 3.9 support
- Split upstream tests in gating into tiers

* Fri Jul 03 2020 Ondrej Mular <omular@redhat.com> - 0.10.5-6
- Use patched version of dacite compatible with Python 3.9
- Resolves: rhbz#1838327

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.10.5-5
- Rebuilt for Python 3.9

* Thu May 07 2020 Ondrej Mular <omular@redhat.com> - 0.10.5-4
- Rebased to latest upstream sources (see CHANGELOG.md)
- Run only tier0 tests in check section

* Fri Apr 03 2020 Ondrej Mular <omular@redhat.com> - 0.10.5-3
- Enable gating

* Fri Mar 27 2020 Ondrej Mular <omular@redhat.com> - 0.10.5-2
- Remove usage of deprecated module xml.etree.cElementTree
- Resolves: rhbz#1817695

* Wed Mar 18 2020 Miroslav Lisik <mlisik@redhat.com> - 0.10.5-1
- Rebased to latest upstream sources (see CHANGELOG.md)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 28 2019 Miroslav Lisik <mlisik@redhat.com> - 0.10.4-1
- Rebased to latest upstream sources (see CHANGELOG.md)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.3-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 23 2019 Ondrej Mular <omular@redhat.com> - 0.10.3-1
- Rebased to latest upstream sources (see CHANGELOG.md)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.2-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 14 2019 Ondrej Mular <omular@redhat.com> - 0.10.2-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Added pam as required package
- An alternative webUI rebased to latest upstream sources
- Improved configuration files permissions in rpm

* Tue Mar 19 2019 Tomas Jelinek <tojeline@redhat.com> - 0.10.1-4
- Removed unused dependency rubygem-multi_json
- Removed files needed only for building rubygems from the package

* Mon Feb 04 2019 Ivan Devát <idevat@redhat.com> - 0.10.1-3
- Corrected gem install flags

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 09 2019 Ivan Devát <idevat@redhat.com> - 0.10.1-1
- Rebased to latest upstream sources (see CHANGELOG.md)

* Tue Oct 09 2018 Ondrej Mular <omular@redhat.com> - 0.10.0.alpha.6-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Resolves: rhbz#1618911

* Fri Aug 31 2018 Ivan Devát <idevat@redhat.com> - 0.10.0.alpha.2-3
- Started bundling rubygem-tilt (rubygem-tilt is orphaned in fedora due to rubygem-prawn dependency)
- Enabled passing tests

* Sat Aug 25 2018 Ivan Devát <idevat@redhat.com> - 0.10.0.alpha.2-2
- Fixed error with missing rubygem location during pcsd start
- Resolves: rhbz#1618911

* Thu Aug 02 2018 Ivan Devát <idevat@redhat.com> - 0.10.0.alpha.2-1
- Rebased to latest upstream sources (see CHANGELOG.md)

* Wed Jul 25 2018 Ivan Devát <idevat@redhat.com> - 0.9.164-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.164-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.164-2
- Rebuilt for Python 3.7

* Mon Apr 09 2018 Ondrej Mular <omular@redhat.com> - 0.9.164-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Fixed: CVE-2018-1086, CVE-2018-1079

* Mon Feb 26 2018 Ivan Devát <idevat@redhat.com> - 0.9.163-2
- Fixed crash when adding a node to a cluster

* Tue Feb 20 2018 Ivan Devát <idevat@redhat.com> - 0.9.163-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Adapted for Rack 2 and Sinatra 2

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.160-5
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.160-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 0.9.160-3
- Rebuilt for switch to libxcrypt

* Fri Jan 05 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.160-2
- F-28: rebuild for ruby25
- Workaround for gem install option

* Wed Oct 18 2017 Ondrej Mular <omular@redhat.com> - 0.9.160-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- All pcs tests are temporarily disabled because of issues in pacemaker.

* Thu Sep 14 2017 Ondrej Mular <omular@redhat.com> - 0.9.159-4
- Bundle rubygem-rack-protection which is being updated to 2.0.0 in Fedora.
- Removed setuptools patch.
- Disabled debuginfo subpackage.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.159-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.159-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Ondrej Mular <omular@redhat.com> - 0.9.159-1
- Rebased to latest upstream sources (see CHANGELOG.md)

* Tue May 23 2017 Tomas Jelinek <tojeline@redhat.com> - 0.9.156-3
- Fixed python locales issue preventing build-time tests to pass
- Bundle rubygem-tilt which is being retired from Fedora

* Thu Mar 23 2017 Tomas Jelinek <tojeline@redhat.com> - 0.9.156-2
- Fixed Cross-site scripting (XSS) vulnerability in web UI CVE-2017-2661
- Re-added support for clufter as it is now available for Python 3

* Wed Feb 22 2017 Tomas Jelinek <tojeline@redhat.com> - 0.9.156-1
- Rebased to latest upstream sources (see CHANGELOG.md)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.155-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Vít Ondruch <vondruch@redhat.com> - 0.9.155-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.4

* Wed Jan 04 2017 Adam Williamson <awilliam@redhat.com> - 0.9.155-1
- Latest release 0.9.155
- Fix tests with Python 3.6 and lxml 3.7
- Package the license as license, not doc
- Use -f param for rm when wiping test directories as they are nested now

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com>
- Rebuild for Python 3.6

* Tue Oct 18 2016 Tomas Jelinek <tojeline@redhat.com> - 0.9.154-2
- Fixed upgrading from pcs-0.9.150

* Thu Sep 22 2016 Tomas Jelinek <tojeline@redhat.com> - 0.9.154-1
- Re-synced to upstream sources
- Spec file cleanup and fixes

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.150-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Apr 11 2016 Tomas Jelinek <tojeline@redhat.com> - 0.9.150-1
- Re-synced to upstream sources
- Make pcs depend on python3
- Spec file cleanup

* Tue Feb 23 2016 Tomas Jelinek <tojeline@redhat.com> - 0.9.149-2
- Fixed rubygems issues which prevented pcsd from starting
- Added missing python-lxml dependency

* Thu Feb 18 2016 Tomas Jelinek <tojeline@redhat.com> - 0.9.149-1
- Re-synced to upstream sources
- Security fix for CVE-2016-0720, CVE-2016-0721
- Fixed rubygems issues which prevented pcsd from starting
- Rubygems built with RELRO
- Spec file cleanup
- Fixed multilib .pyc/.pyo issue

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.144-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Vít Ondruch <vondruch@redhat.com> - 0.9.144-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Fri Sep 18 2015 Tomas Jelinek <tojeline@redhat.com> - 0.9.144-1
- Re-synced to upstream sources

* Tue Jun 23 2015 Tomas Jelinek <tojeline@redhat.com> - 0.9.141-2
- Added requirement for psmisc for killall

* Tue Jun 23 2015 Tomas Jelinek <tojeline@redhat.com> - 0.9.141-1
- Re-synced to upstream sources

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.140-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Tomas Jelinek <tojeline@redhat.com> - 0.9.140-1
- Re-synced to upstream sources

* Fri May 22 2015 Tomas Jelinek <tojeline@redhat.com> - 0.9.139-4
- Fix for CVE-2015-1848, CVE-2015-3983 (sessions not signed)

* Thu Mar 26 2015 Tomas Jelinek <tojeline@redhat.com> - 0.9.139-3
- Add BuildRequires: systemd (rhbz#1206253)

* Fri Feb 27 2015 Tomas Jelinek <tojeline@redhat.com> - 0.9.139-2
- Reflect clufter inclusion (rhbz#1180723)

* Thu Feb 19 2015 Tomas Jelinek <tojeline@redhat.com> - 0.9.139-1
- Re-synced to upstream sources

* Sat Jan 17 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.115-5
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.115-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.115-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 06 2014 Tomas Jelinek <tojeline@redhat.com> - 0.9.115-2
- Rebuild to fix ruby dependencies

* Mon Apr 21 2014 Chris Feist <cfeist@redhat.com> - 0.9.115-1
- Re-synced to upstream sources

* Fri Dec 13 2013 Chris Feist <cfeist@redhat.com> - 0.9.102-1
- Re-synced to upstream sources

* Wed Jun 19 2013 Chris Feist <cfeist@redhat.com> - 0.9.48-1
- Rebuild with upstream sources

* Thu Jun 13 2013 Chris Feist <cfeist@redhat.com> - 0.9.44-5
- Added fixes for building rpam with ruby-2.0.0

* Mon Jun 03 2013 Chris Feist <cfeist@redhat.com> - 0.9.44-4
- Rebuild with upstream sources

* Tue May 07 2013 Chris Feist <cfeist@redhat.com> - 0.9.41-2
- Resynced to upstream sources

* Fri Apr 19 2013 Chris Feist <cfeist@redhat.com> - 0.9.39-1
- Fixed gem building
- Re-synced to upstream sources

* Mon Mar 25 2013 Chris Feist <cfeist@rehdat.com> - 0.9.36-4
- Don't try to build gems at all

* Mon Mar 25 2013 Chris Feist <cfeist@rehdat.com> - 0.9.36-3
- Removed all gems from build, will need to find pam package in the future

* Mon Mar 25 2013 Chris Feist <cfeist@redhat.com> - 0.9.36-2
- Removed duplicate libraries already present in fedora

* Mon Mar 18 2013 Chris Feist <cfeist@redhat.com> - 0.9.36-1
- Resynced to latest upstream

* Mon Mar 11 2013 Chris Feist <cfeist@redhat.com> - 0.9.33-1
- Resynched to latest upstream
- pcsd has been moved to /usr/lib to fix /usr/local packaging issues

* Thu Feb 21 2013 Chris Feist <cfeist@redhat.com> - 0.9.32-1
- Resynced to latest version of pcs/pcsd

* Mon Nov 05 2012 Chris Feist <cfeist@redhat.com> - 0.9.27-3
- Build on all archs

* Thu Oct 25 2012 Chris Feist <cfeist@redhat.com> - 0.9.27-2
- Resync to latest version of pcs
- Added pcsd daemon

* Mon Oct 08 2012 Chris Feist <cfeist@redhat.cmo> - 0.9.26-1
- Resync to latest version of pcs

* Thu Sep 20 2012 Chris Feist <cfeist@redhat.cmo> - 0.9.24-1
- Resync to latest version of pcs

* Thu Sep 20 2012 Chris Feist <cfeist@redhat.cmo> - 0.9.23-1
- Resync to latest version of pcs

* Wed Sep 12 2012 Chris Feist <cfeist@redhat.cmo> - 0.9.22-1
- Resync to latest version of pcs

* Thu Sep 06 2012 Chris Feist <cfeist@redhat.cmo> - 0.9.19-1
- Resync to latest version of pcs

* Tue Aug 07 2012 Chris Feist <cfeist@redhat.com> - 0.9.12-1
- Resync to latest version of pcs

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 24 2012 Chris Feist <cfeist@redhat.com> - 0.9.4-1
- Resync to latest version of pcs
- Move cluster creation options to cluster sub command.

* Mon May 07 2012 Chris Feist <cfeist@redhat.com> - 0.9.3.1-1
- Resync to latest version of pcs which includes fixes to work with F17.

* Mon Mar 19 2012 Chris Feist <cfeist@redhat.com> - 0.9.2.4-1
- Resynced to latest version of pcs

* Mon Jan 23 2012 Chris Feist <cfeist@redhat.com> - 0.9.1-1
- Updated BuildRequires and %%doc section for fedora

* Fri Jan 20 2012 Chris Feist <cfeist@redhat.com> - 0.9.0-2
- Updated spec file for fedora specific changes

* Mon Jan 16 2012 Chris Feist <cfeist@redhat.com> - 0.9.0-1
- Initial Build
