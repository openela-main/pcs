Name:                 pcs
Version:              0.10.17
Release:              2%{?dist}
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
# https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing#Good_Licenses
# GPL-2.0-only: pcs
# Apache-2.0: dataclasses, tornado
# Apache-2.0 or BSD-3-Clause: dateutil
# MIT: backports, dacite, ember, ethon, handlebars, jquery, jquery-ui,
#      mustermann, rack, rack-protection, rack-test, sinatra, tilt
# MIT and (BSD-2-Clause or GPL-2.0-or-later): nio4r
# GPL-2.0-only or Ruby: json
# BSD-2-Clause or Ruby: open4, ruby2_keywords
# BSD-3-Clause: puma
# BSD-3-Clause and MIT: ffi
License:              GPL-2.0-only AND Apache-2.0 AND MIT AND BSD-3-Clause AND (Apache-2.0 OR BSD-3-Clause) AND (BSD-2-Clause OR Ruby) AND (BSD-2-Clause OR GPL-2.0-or-later) AND (GPL-2.0-only or Ruby)
URL:                  https://github.com/ClusterLabs/pcs
Group:                System Environment/Base
Summary:              Pacemaker/Corosync Configuration System
#building only for architectures with pacemaker and corosync available
ExclusiveArch:        i686 x86_64 s390x ppc64le aarch64

# When specifying a commit, use its long hash
%global version_or_commit %{version}
# %%global version_or_commit d5642c2ede0d6555603bc385dc35e581d2f0fddd
%global pcs_source_name %{name}-%{version_or_commit}

# ui_commit can be determined by hash, tag or branch
%global ui_commit 0.1.13
%global ui_modules_version 0.1.13
%global ui_src_name pcs-web-ui-%{ui_commit}

%global pcs_snmp_pkg_name  pcs-snmp

%global pyagentx_version   0.4.pcs.2
%global dataclasses_version 0.8
%global dacite_version  1.8.1
%global dateutil_version  2.8.2
%global version_rubygem_backports  3.24.1
%global version_rubygem_ethon  0.16.0
%global version_rubygem_ffi  1.15.5
%global version_rubygem_json  2.6.3
%global version_rubygem_mustermann  2.0.2
%global version_rubygem_nio4r 2.5.9
%global version_rubygem_open4  1.3.4
%global version_rubygem_puma 6.3.0
%global version_rubygem_rack  2.2.7
%global version_rubygem_rack_protection  2.2.4
%global version_rubygem_rack_test  2.1.0
%global version_rubygem_rexml  3.2.5
%global version_rubygem_ruby2_keywords  0.0.5
%global version_rubygem_sinatra  2.2.4
%global version_rubygem_tilt  2.2.0

# javascript bundled libraries for old web-ui
%global ember_version 1.4.0
%global handlebars_version 1.2.1
%global jquery_ui_version 1.12.1
%global jquery_version 3.6.0

# DO NOT UPDATE
# Tornado 6.2 requires Python 3.7+
%global tornado_version    6.1.0

%global pcs_bundled_dir pcs_bundled
%global pcsd_public_dir pcsd/public
%global rubygem_bundle_dir pcsd/vendor/bundle
%global rubygem_cache_dir %{rubygem_bundle_dir}/cache

# mangling shebang in /usr/lib/pcsd/vendor/bundle/ruby/gems/rack-2.0.5/test/cgi/test from /usr/bin/env ruby to #!/usr/bin/ruby
#*** ERROR: ./usr/lib/pcsd/vendor/bundle/ruby/gems/rack-2.0.5/test/cgi/test.ru has shebang which doesn't start with '/' (../../bin/rackup)
#mangling shebang in /usr/lib/pcsd/vendor/bundle/ruby/gems/rack-2.0.5/test/cgi/rackup_stub.rb from /usr/bin/env ruby to #!/usr/bin/ruby
#*** WARNING: ./usr/lib/pcsd/vendor/bundle/ruby/gems/rack-2.0.5/test/cgi/sample_rackup.ru is executable but has empty or no shebang, removing executable bit
#*** WARNING: ./usr/lib/pcsd/vendor/bundle/ruby/gems/rack-2.0.5/test/cgi/lighttpd.conf is executable but has empty or no shebang, removing executable bit
#*** ERROR: ambiguous python shebang in /usr/lib/pcsd/vendor/bundle/ruby/gems/ffi-1.9.25/ext/ffi_c/libffi/generate-darwin-source-and-headers.py: #!/usr/bin/env python. Change it to python3 (or python2) explicitly.
%undefine __brp_mangle_shebangs

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
Source0:              %{url}/archive/%{?v_prefix}%{version_or_commit}/%{pcs_source_name}.tar.gz
Source1:              HAM-logo.png

Source41:             https://github.com/ondrejmular/pyagentx/archive/v%{pyagentx_version}/pyagentx-%{pyagentx_version}.tar.gz
Source42:             https://github.com/tornadoweb/tornado/archive/v%{tornado_version}/tornado-%{tornado_version}.tar.gz
Source43:             https://github.com/ericvsmith/dataclasses/archive/%{dataclasses_version}/dataclasses-%{dataclasses_version}.tar.gz
Source44:             https://github.com/konradhalas/dacite/archive/v%{dacite_version}/dacite-%{dacite_version}.tar.gz
Source45:             https://pypi.python.org/packages/source/p/python-dateutil/python-dateutil-%{dateutil_version}.tar.gz

Source81:             https://rubygems.org/downloads/backports-%{version_rubygem_backports}.gem
Source82:             https://rubygems.org/downloads/ethon-%{version_rubygem_ethon}.gem
Source83:             https://rubygems.org/downloads/ffi-%{version_rubygem_ffi}.gem
Source84:             https://rubygems.org/downloads/json-%{version_rubygem_json}.gem
Source85:             https://rubygems.org/downloads/rexml-%{version_rubygem_rexml}.gem
Source86:             https://rubygems.org/downloads/mustermann-%{version_rubygem_mustermann}.gem
# We needed to re-upload open4 rubygem because of issues with sources in gating.
# Unfortunately, there was no newer version available, therefore we had to
# change its 'version' ourselves.
Source87:             https://rubygems.org/downloads/open4-%{version_rubygem_open4}.gem#/open4-%{version_rubygem_open4}-1.gem
Source88:             https://rubygems.org/downloads/rack-%{version_rubygem_rack}.gem
Source89:             https://rubygems.org/downloads/rack-protection-%{version_rubygem_rack_protection}.gem
Source90:             https://rubygems.org/downloads/rack-test-%{version_rubygem_rack_test}.gem
Source91:             https://rubygems.org/downloads/sinatra-%{version_rubygem_sinatra}.gem
Source92:             https://rubygems.org/downloads/tilt-%{version_rubygem_tilt}.gem
Source93:             https://rubygems.org/downloads/nio4r-%{version_rubygem_nio4r}.gem
Source94:             https://rubygems.org/downloads/puma-%{version_rubygem_puma}.gem
Source95:             https://rubygems.org/downloads/ruby2_keywords-%{version_rubygem_ruby2_keywords}.gem

Source100:            https://github.com/ClusterLabs/pcs-web-ui/archive/%{ui_commit}/%{ui_src_name}.tar.gz
Source101:            https://github.com/ClusterLabs/pcs-web-ui/releases/download/%{ui_modules_version}/pcs-web-ui-node-modules-%{ui_modules_version}.tar.xz

# pcs patches: <= 200
# Patch1: bzNUMBER-01-name.patch
Patch1:               do-not-support-cluster-setup-with-udp-u-transport.patch
Patch2:               bz2218841-01-fix-displaying-duplicate-records-in-property-command.patch
Patch3:               bz2219388-01-use-a-filter-when-extracting-a-config-backup-tarball.patch

# ui patches: >200
# Patch201: bzNUMBER-01-name.patch

# git for patches
BuildRequires:        git-core
# printf from coreutils is used in makefile, head is used in spec
BuildRequires:        coreutils
# python for pcs
BuildRequires:        platform-python
BuildRequires:        python3-devel
BuildRequires:        platform-python-setuptools
BuildRequires:        python3-pycurl
BuildRequires:        python3-pip
BuildRequires:        python3-pyparsing
BuildRequires:        python3-cryptography
BuildRequires:        python3-lxml
# for building bundled python packages
BuildRequires:        python3-wheel
# for bundled python dateutil
BuildRequires:        python3-setuptools_scm
# gcc for compiling custom rubygems
BuildRequires:        gcc
BuildRequires:        gcc-c++
# ruby and gems for pcsd
BuildRequires:        ruby >= 2.2.0
BuildRequires:        ruby-devel
BuildRequires:        rubygems
BuildRequires:        rubygem-bundler
# ruby libraries for tests
BuildRequires:        rubygem-test-unit
# for touching patch files (sanitization function)
BuildRequires:        diffstat
# for post, preun and postun macros
BuildRequires:        systemd
# pam is used for authentication inside daemon (python ctypes)
# needed for tier0 tests during build
BuildRequires:        pam

# pcsd fonts and font management tools for creating symlinks to fonts
BuildRequires:        fontconfig
BuildRequires:        liberation-sans-fonts
BuildRequires:        make
BuildRequires:        overpass-fonts
# Red Hat logo for creating symlink of favicon
BuildRequires:        redhat-logos

# for building web ui
BuildRequires:        npm

# cluster stack packages for pkg-config
BuildRequires:        booth
BuildRequires:        corosync-qdevice-devel
BuildRequires:        corosynclib-devel >= 3.0
BuildRequires:        fence-agents-common
BuildRequires:        pacemaker-libs-devel >= 2.0.0
BuildRequires:        resource-agents
BuildRequires:        sbd

# python and libraries for pcs, setuptools for pcs entrypoint
Requires:             platform-python
Requires:             python3-lxml
Requires:             platform-python-setuptools
Requires:             python3-clufter => 0.70.0
Requires:             python3-pycurl
Requires:             python3-pyparsing
Requires:             python3-cryptography
# ruby and gems for pcsd
Requires:             ruby >= 2.2.0
Requires:             rubygems
# for killall
Requires:             psmisc
# cluster stack and related packages
Requires:             pcmk-cluster-manager >= 2.0.0
Suggests:             pacemaker
Requires:             (corosync >= 2.99 if pacemaker)
# pcs enables corosync encryption by default so we require libknet1-plugins-all
Requires:             (libknet1-plugins-all if corosync)
Requires:             pacemaker-cli >= 2.0.0
# for post, preun and postun macros
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
# pam is used for authentication inside daemon (python ctypes)
# more details: https://bugzilla.redhat.com/show_bug.cgi?id=1717113
Requires:             pam
# pcsd fonts
Requires:             liberation-sans-fonts
Requires:             overpass-fonts
# favicon Red Hat logo
Requires:             redhat-logos
# needs logrotate for /etc/logrotate.d/pcsd
Requires:             logrotate

Provides:             bundled(tornado) = %{tornado_version}
Provides:             bundled(dataclasses) = %{dataclasses_version}
Provides:             bundled(dacite) = %{dacite_version}
Provides:             bundled(dateutil) = %{dateutil_version}
Provides:             bundled(backports) = %{version_rubygem_backports}
Provides:             bundled(ethon) = %{version_rubygem_ethon}
Provides:             bundled(ffi) = %{version_rubygem_ffi}
Provides:             bundled(json) = %{version_rubygem_json}
Provides:             bundled(mustermann) = %{version_rubygem_mustermann}
Provides:             bundled(nio4r) = %{version_rubygem_nio4r}
Provides:             bundled(open4) = %{version_rubygem_open4}
Provides:             bundled(puma) = %{version_rubygem_puma}
Provides:             bundled(rack) = %{version_rubygem_rack}
Provides:             bundled(rack_protection) = %{version_rubygem_rack_protection}
Provides:             bundled(rack_test) = %{version_rubygem_rack_test}
Provides:             bundled(rexml) = %{version_rubygem_rexml}
Provides:             bundled(ruby2_keywords) = %{version_rubygem_ruby2_keywords}
Provides:             bundled(sinatra) = %{version_rubygem_sinatra}
Provides:             bundled(tilt) = %{version_rubygem_tilt}

# javascript bundled libraries for old web-ui
Provides:             bundled(ember) = %{ember_version}
Provides:             bundled(handlebars) = %{handlebars_version}
Provides:             bundled(jquery) = %{jquery_version}
Provides:             bundled(jquery-ui) = %{jquery_ui_version}

%description
pcs is a corosync and pacemaker configuration tool.  It permits users to
easily view, modify and create pacemaker based clusters.

# pcs-snmp package definition
%package -n %{pcs_snmp_pkg_name}
Group:                System Environment/Base
Summary:              Pacemaker cluster SNMP agent
# https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing#Good_Licenses
# GPL-2.0-only: pcs
# BSD-2-Clause: pyagentx
License:              GPL-2.0-only and BSD-2-Clause
URL:                  https://github.com/ClusterLabs/pcs

# tar for unpacking pyagentx source tarball
BuildRequires:        tar

Requires:             pcs = %{version}-%{release}
Requires:             pacemaker
Requires:             net-snmp

Provides:             bundled(pyagentx) = %{pyagentx_version}

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
%autosetup -D -T -b 100 -a 101 -S git -n %{ui_src_name} -N
%autopatch -p1 -m 201
# update_times_patch %%{PATCH201}

# patch pcs sources
%autosetup -S git -n %{pcs_source_name} -N
%autopatch -p1 -M 200
# update_times_patch %%{PATCH1}
update_times_patch %{PATCH1}
update_times_patch %{PATCH2}
update_times_patch %{PATCH3}

# generate .tarball-version if building from an untagged commit, not a released version
# autogen uses git-version-gen which uses .tarball-version for generating version number
%if "%{version}" != "%{version_or_commit}"
  echo "%version+$(echo "%{version_or_commit}" | head -c 8)" > %{_builddir}/%{pcs_source_name}/.tarball-version
%endif

cp -f %SOURCE1 %{pcsd_public_dir}/images

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
# For reason why we are renaming open4 rubygem, see comment of source
# definition above.
cp -f %SOURCE87 %{rubygem_cache_dir}/open4-%{version_rubygem_open4}.gem
cp -f %SOURCE88 %{rubygem_cache_dir}
cp -f %SOURCE89 %{rubygem_cache_dir}
cp -f %SOURCE90 %{rubygem_cache_dir}
cp -f %SOURCE91 %{rubygem_cache_dir}
cp -f %SOURCE92 %{rubygem_cache_dir}
cp -f %SOURCE93 %{rubygem_cache_dir}
cp -f %SOURCE94 %{rubygem_cache_dir}
cp -f %SOURCE95 %{rubygem_cache_dir}


# 2) prepare python bundles
mkdir -p %{pcs_bundled_dir}/src
cp -f %SOURCE41 rpm/
cp -f %SOURCE42 rpm/
cp -f %SOURCE43 rpm/
cp -f %SOURCE44 rpm/
cp -f %SOURCE45 rpm/

%build
%define debug_package %{nil}

./autogen.sh
%{configure} --enable-local-build --enable-use-local-cache-only --enable-individual-bundling --enable-booth-enable-authfile-set --enable-booth-enable-authfile-unset PYTHON=%{__python3} ruby_CFLAGS="%{optflags}" ruby_LIBS="%{build_ldflags}"
make all

# build pcs-web-ui
make -C %{_builddir}/%{ui_src_name} build BUILD_USE_EXISTING_NODE_MODULES=true

%install
rm -rf $RPM_BUILD_ROOT
pwd

%make_install

# something like make install for pcs-web-ui
cp -r %{_builddir}/%{ui_src_name}/build  ${RPM_BUILD_ROOT}%{_libdir}/%{pcsd_public_dir}/ui

# prepare license files
# some rubygems do not have a license file (thin)
mv %{rubygem_bundle_dir}/gems/backports-%{version_rubygem_backports}/LICENSE.txt backports_LICENSE.txt
mv %{rubygem_bundle_dir}/gems/ethon-%{version_rubygem_ethon}/LICENSE ethon_LICENSE
mv %{rubygem_bundle_dir}/gems/ffi-%{version_rubygem_ffi}/COPYING ffi_COPYING
mv %{rubygem_bundle_dir}/gems/ffi-%{version_rubygem_ffi}/LICENSE ffi_LICENSE
mv %{rubygem_bundle_dir}/gems/ffi-%{version_rubygem_ffi}/LICENSE.SPECS ffi_LICENSE.SPECS
mv %{rubygem_bundle_dir}/gems/json-%{version_rubygem_json}/LICENSE json_LICENSE
mv %{rubygem_bundle_dir}/gems/mustermann-%{version_rubygem_mustermann}/LICENSE mustermann_LICENSE
mv %{rubygem_bundle_dir}/gems/nio4r-%{version_rubygem_nio4r}/license.md nio4r_license.md
mv %{rubygem_bundle_dir}/gems/nio4r-%{version_rubygem_nio4r}/ext/libev/LICENSE nio4r_libev_LICENSE
mv %{rubygem_bundle_dir}/gems/open4-%{version_rubygem_open4}/LICENSE open4_LICENSE
mv %{rubygem_bundle_dir}/gems/puma-%{version_rubygem_puma}/LICENSE puma_LICENSE
mv %{rubygem_bundle_dir}/gems/rack-%{version_rubygem_rack}/MIT-LICENSE rack_MIT-LICENSE
mv %{rubygem_bundle_dir}/gems/rack-protection-%{version_rubygem_rack_protection}/License rack-protection_License
mv %{rubygem_bundle_dir}/gems/rack-test-%{version_rubygem_rack_test}/MIT-LICENSE.txt rack-test_MIT-LICENSE.txt
mv %{rubygem_bundle_dir}/gems/ruby2_keywords-%{version_rubygem_ruby2_keywords}/LICENSE ruby2_keywords_LICENSE
mv %{rubygem_bundle_dir}/gems/sinatra-%{version_rubygem_sinatra}/LICENSE sinatra_LICENSE
mv %{rubygem_bundle_dir}/gems/tilt-%{version_rubygem_tilt}/COPYING tilt_COPYING

# symlink favicon into pcsd directories
ln -fs /etc/favicon.png ${RPM_BUILD_ROOT}%{_libdir}/%{pcsd_public_dir}/images/favicon.png


cp %{pcs_bundled_dir}/src/pyagentx-*/LICENSE.txt pyagentx_LICENSE.txt
cp %{pcs_bundled_dir}/src/pyagentx-*/CONTRIBUTORS.txt pyagentx_CONTRIBUTORS.txt
cp %{pcs_bundled_dir}/src/pyagentx-*/README.md pyagentx_README.md

cp %{pcs_bundled_dir}/src/tornado-*/LICENSE tornado_LICENSE
cp %{pcs_bundled_dir}/src/tornado-*/README.rst tornado_README.rst

cp %{pcs_bundled_dir}/src/dataclasses-*/LICENSE.txt dataclasses_LICENSE.txt
cp %{pcs_bundled_dir}/src/dataclasses-*/README.rst dataclasses_README.rst

cp %{pcs_bundled_dir}/src/dacite-*/LICENSE dacite_LICENSE
cp %{pcs_bundled_dir}/src/dacite-*/README.md dacite_README.md

cp %{pcs_bundled_dir}/src/python-dateutil-*/LICENSE dateutil_LICENSE
cp %{pcs_bundled_dir}/src/python-dateutil-*/README.rst dateutil_README.rst

# We are not building debug package for pcs but we need to add MiniDebuginfo
# to the bundled shared libraries from rubygem extensions in order to satisfy
# rpmdiff's binary stripping checker.
# Therefore we call find-debuginfo.sh script manually in order to strip
# binaries and add MiniDebugInfo with .gnu_debugdata section
/usr/lib/rpm/find-debuginfo.sh -j2 -m -i -S debugsourcefiles.list
# find-debuginfo.sh generated some files into /usr/lib/debug  and
# /usr/src/debug/ that we don't want in the package
rm -rf $RPM_BUILD_ROOT%{_libdir}/debug
rm -rf $RPM_BUILD_ROOT/usr/lib/debug
rm -rf $RPM_BUILD_ROOT%{_prefix}/src/debug

# We can remove files required for gem compilation
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{rubygem_bundle_dir}/gems/ffi-%{version_rubygem_ffi}/ext
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{rubygem_bundle_dir}/gems/json-%{version_rubygem_json}/ext
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{rubygem_bundle_dir}/gems/nio4r-%{version_rubygem_nio4r}/ext
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{rubygem_bundle_dir}/gems/puma-%{version_rubygem_puma}/ext

%check
run_all_tests(){
  #run pcs tests

  # disabled tests:
  #
  # pcs_test.tier0.lib.commands.test_resource_agent.DescribeAgentUtf8.test_describe
  #   For an unknown reason this test is failing in mock environment and
  #   passing outside the mock environment.
  #   TODO: Investigate the issue

    %{__python3} pcs_test/suite --tier0 -v --vanilla --all-but \
    pcs_test.tier0.daemon.app.test_app_remote.SyncConfigMutualExclusive.test_get_not_locked \
    pcs_test.tier0.daemon.app.test_app_remote.SyncConfigMutualExclusive.test_post_not_locked \

  test_result_python=$?

  #run pcsd tests and remove them
  GEM_HOME=$RPM_BUILD_ROOT%{_libdir}/%{rubygem_bundle_dir} ruby \
    -I$RPM_BUILD_ROOT%{_libdir}/pcsd \
    -Ipcsd/test \
    pcsd/test/test_all_suite.rb
  test_result_ruby=$?

  if [ $test_result_python -ne 0 ]; then
    return $test_result_python
  fi
  return $test_result_ruby
}

remove_all_tests() {
  # remove javascript testing files
  rm -r -v $RPM_BUILD_ROOT%{_libdir}/%{pcsd_public_dir}/js/dev
}

run_all_tests
remove_all_tests

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
%doc tornado_README.rst
%doc dacite_README.md
%doc dateutil_README.rst
%doc dataclasses_README.rst
%license tornado_LICENSE
%license dacite_LICENSE
%license dateutil_LICENSE
%license dataclasses_LICENSE.txt
%license COPYING
# rugygem licenses
%license backports_LICENSE.txt
%license ethon_LICENSE
%license ffi_COPYING
%license ffi_LICENSE
%license ffi_LICENSE.SPECS
%license json_LICENSE
%license mustermann_LICENSE
%license nio4r_license.md
%license nio4r_libev_LICENSE
%license open4_LICENSE
%license puma_LICENSE
%license rack_MIT-LICENSE
%license rack-protection_License
%license rack-test_MIT-LICENSE.txt
%license ruby2_keywords_LICENSE
%license sinatra_LICENSE
%license tilt_COPYING
%{python3_sitelib}/*
%{_sbindir}/pcs
%{_sbindir}/pcsd
%{_libdir}/pcs/*
%{_libdir}/pcsd/*
%{_unitdir}/pcsd.service
%{_unitdir}/pcsd-ruby.service
%{_datadir}/bash-completion/completions/pcs
%{_sharedstatedir}/pcsd
%config(noreplace) %{_sysconfdir}/pam.d/pcsd
%dir %{_var}/log/pcsd
%config(noreplace) %{_sysconfdir}/logrotate.d/pcsd
%config(noreplace) %{_sysconfdir}/sysconfig/pcsd
%ghost %config(noreplace) %attr(0600,root,root) %{_sharedstatedir}/pcsd/cfgsync_ctl
%ghost %config(noreplace) %attr(0600,root,root) %{_sharedstatedir}/pcsd/known-hosts
%ghost %config(noreplace) %attr(0600,root,root) %{_sharedstatedir}/pcsd/pcsd.cookiesecret
%ghost %config(noreplace) %attr(0600,root,root) %{_sharedstatedir}/pcsd/pcsd.crt
%ghost %config(noreplace) %attr(0600,root,root) %{_sharedstatedir}/pcsd/pcsd.key
%ghost %config(noreplace) %attr(0644,root,root) %{_sharedstatedir}/pcsd/pcs_settings.conf
%ghost %config(noreplace) %attr(0644,root,root) %{_sharedstatedir}/pcsd/pcs_users.conf
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
* Tue Jan 09 2024 OpenELA Technical Steering Committee <tsc@openela.org> - 0.10.17
- Debrand PCS

* Thu Jul 13 2023 Michal Pospisil <mpospisi@redhat.com> - 0.10.17-2
- Make use of filters when extracting tarballs to enhance security if provided by Python (`pcs config restore` command)
- Do not display duplicate records in commands `pcs property [config] --all` and `pcs property describe`
- Resolves: rhbz#2218841 rhbz#2219388

* Mon Jun 19 2023 Michal Pospisil <mpospisi@redhat.com> - 0.10.17-1
- Rebased to the latest upstream sources (see CHANGELOG.md)
- Updated bundled rubygems: tilt, puma
- Resolves: rhbz#2112259 rhbz#2163439 rhbz#2166289

* Thu May 25 2023 Michal Pospisil <mpospisi@redhat.com> - 0.10.16-1
- Rebased to the latest upstream sources (see CHANGELOG.md)
- Updated bundled dependencies: dacite
- Added bundled rubygems: nio4r, puma
- Removed bundled rubygems: daemons, eventmachine, thin
- Updated bundled rubygems: backports, rack, rack-test, tilt
- Resolves: rhbz#1957591 rhbz#2022748 rhbz#2160555 rhbz#2163439 rhbz#2166289 rhbz#2166294 rhbz#2176490 rhbz#2178700 rhbz#2178707 rhbz#2179010 rhbz#2180378 rhbz#2189958

* Thu Feb 9 2023 Michal Pospisil <mpospisi@redhat.com> - 0.10.15-4
- Fixed enabling/disabling sbd when cluster is not running
- Added BuildRequires: pam - needed for tier0 tests during build
- Resolves: rhbz#2166243

* Mon Jan 16 2023 Michal Pospisil <mpospisi@redhat.com> - 0.10.15-3
- Allow time values in stonith-watchdog-time property
- Resource/stonith agent self-validation of instance attributes is now disabled by default, as many agents do not work with it properly
- Updated bundled rubygems: rack, rack-protection, sinatra
- Added license for ruby2_keywords
- Resolves: rhbz#2158804 rhbz#2159455

* Fri Dec 16 2022 Michal Pospisil <mpospisi@redhat.com> - 0.10.15-2
- Added warning when omitting validation of misconfigured resource
- Fixed displaying of bool and integer values in `pcs resource config` command
- Updated bundled rubygems: ethon, json, rack-protection, sinatra
- Resolves: rhbz#2151166 rhbz#2151511

* Wed Nov 23 2022 Michal Pospisil <mpospisi@redhat.com> - 0.10.15-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Updated Python bundled dependency dateutil
- Resolves: rhbz#2112002 rhbz#2112263 rhbz#2112291 rhbz#2132582

* Tue Oct 25 2022 Miroslav Lisik <mlisik@redhat.com> - 0.10.14-6
- Rebased to latest upstream sources (see CHANGELOG.md)
- Updated rubygem bundled packages: mustermann, rack, rack-protection, rack-test, sinatra, tilt
- Resolves: rhbz#1816852 rhbz#1918527 rhbz#2112267 rhbz#2112291

* Wed Aug 17 2022 Miroslav Lisik <mlisik@redhat.com> - 0.10.14-4
- Fixed enable sbd from webui
- Resolves: rhbz#2117650

* Mon Aug 08 2022 Miroslav Lisik <mlisik@redhat.com> - 0.10.14-3
- Fixed `pcs quorum device remove`
- Resolves: rhbz#2115326

* Thu Jul 28 2022 Miroslav Lisik <mlisik@redhat.com> - 0.10.14-2
- Fixed booth ticket mode value case insensitive
- Fixed booth sync check whether /etc/booth exists
- Resolves: rhbz#1786964 rhbz#1791670

* Fri Jun 24 2022 Miroslav Lisik <mlisik@redhat.com> - 0.10.14-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Updated bundled rubygems: rack
- Resolves: rhbz#2059500 rhbz#2096787 rhbz#2097383 rhbz#2097391 rhbz#2097392 rhbz#2097393

* Tue May 24 2022 Miroslav Lisik <mlisik@redhat.com> - 0.10.13-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Updated pcs-web-ui
- Updated bundled rubygems: backports, daemons, ethon ffi, json, ruby2_keywords, thin
- Resolves: rhbz#1730232 rhbz#1786964 rhbz#1791661 rhbz#1791670 rhbz#1874624 rhbz#1909904 rhbz#1950551 rhbz#1954099 rhbz#2019894 rhbz#2023845 rhbz#2059500 rhbz#2064805 rhbz#2068456

* Thu May 05 2022 Miroslav Lisik <mlisik@redhat.com> - 0.10.12-7
- Updated bundled rubygems: sinatra, rack-protection
- Resolves: rhbz#2081332

* Fri Feb 11 2022 Miroslav Lisik <mlisik@redhat.com> - 0.10.12-6
- Fixed processing agents not conforming to OCF schema
- Resolves: rhbz#2050274

* Tue Feb 01 2022 Miroslav Lisik <mlisik@redhat.com> - 0.10.12-5
- Fixed snmp client
- Resolves: rhbz#2047983

* Tue Jan 25 2022 Miroslav Lisik <mlisik@redhat.com> - 0.10.12-4
- Fixed cluster destroy in web ui
- Fixed covscan issue in web ui
- Resolves: rhbz#1970508

* Fri Jan 14 2022 Miroslav Lisik <mlisik@redhat.com> - 0.10.12-3
- Fixed 'pcs resource move --autodelete' command
- Fixed removing of unavailable fence-scsi storage device
- Fixed ocf validation of ocf linbit drdb agent
- Fixed creating empty cib
- Updated pcs-web-ui
- Resolves: rhbz#1990784 rhbz#2022463 rhbz#2032997 rhbz#2036633

* Wed Dec 15 2021 Miroslav Lisik <mlisik@redhat.com> - 0.10.12-2
- Fixed rsc update cmd when unable to get agent metadata
- Fixed enabling corosync-qdevice
- Resolves: rhbz#1384485 rhbz#2028902

* Thu Dec 02 2021 Miroslav Lisik <mlisik@redhat.com> - 0.10.12-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Updated pcs-web-ui
- Resolves: rhbz#1552470 rhbz#1997011 rhbz#2017311 rhbz#2017312 rhbz#2024543 rhbz#2012128

* Mon Nov 22 2021 Miroslav Lisik <mlisik@redhat.com> - 0.10.11-2
- Rebased to latest upstream sources (see CHANGELOG.md)
- Removed 'export PYTHONCOERCECLOCALE=0'
- Resolves: rhbz#1384485 rhbz#1936833 rhbz#1968088 rhbz#1990784 rhbz#2012128

* Mon Nov 01 2021 Miroslav Lisik <mlisik@redhat.com> - 0.10.11-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Updated pcs-web-ui
- Enabled wui patching
- Resolves: rhbz#1533090 rhbz#1970508 rhbz#1997011 rhbz#2003066 rhbz#2003068 rhbz#2012128

* Fri Aug 27 2021 Miroslav Lisik <mlisik@redhat.com> - 0.10.10-2
- Fixed create resources with depth operation attribute
- Resolves: rhbz#1998454

* Thu Aug 19 2021 Ondrej Mular <omular@redhat.com> - 0.10.10-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Updated pcs-web-ui
- Resolves: rhbz#1885293 rhbz#1847102 rhbz#1935594

* Tue Aug 10 2021 Miroslav Lisik <mlisik@redhat.com> - 0.10.9-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Resolves: rhbz#1432097 rhbz#1847102 rhbz#1935594 rhbz#1984901

* Tue Jul 20 2021 Miroslav Lisik <mlisik@redhat.com> - 0.10.8-4
- Rebased to latest upstream sources (see CHANGELOG.md)
- Resolves: rhbz#1759995 rhbz#1872378 rhbz#1935594

* Thu Jul 08 2021 Miroslav Lisik <mlisik@redhat.com> - 0.10.8-3
- Rebased to latest upstream sources (see CHANGELOG.md)
- Gating changes
- Resolves: rhbz#1678273 rhbz#1690419 rhbz#1750240 rhbz#1759995 rhbz#1872378 rhbz#1909901 rhbz#1935594

* Thu Jun 10 2021 Miroslav Lisik <mlisik@redhat.com> - 0.10.8-2
- Rebased to latest upstream sources (see CHANGELOG.md)
- Updated pcs-web-ui
- Resolves: rhbz#1285269 rhbz#1290830 rhbz#1720221 rhbz#1841019 rhbz#1854238 rhbz#1882291 rhbz#1885302 rhbz#1886342 rhbz#1896458 rhbz#1922996 rhbz#1927384 rhbz#1927394 rhbz#1930886 rhbz#1935594

* Mon Feb 01 2021 Miroslav Lisik <mlisik@redhat.com> - 0.10.8-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Updated pcs-web-ui
- Updated python bundled dependencies: dacite, dataclasses
- Resolves: rhbz#1457314 rhbz#1619818 rhbz#1667066 rhbz#1762816 rhbz#1794062 rhbz#1845470 rhbz#1856397 rhbz#1877762 rhbz#1917286

* Thu Dec 17 2020 Miroslav Lisik <mlisik@redhat.com> - 0.10.7-3
- Rebased to latest upstream sources (see CHANGELOG.md)
- Add BuildRequires: make
- Resolves: rhbz#1667061 rhbz#1667066 rhbz#1774143 rhbz#1885658

* Fri Nov 13 2020 Miroslav Lisik <mlisik@redhat.com> - 0.10.7-2
- Rebased to latest upstream sources (see CHANGELOG.md)
- Changed BuildRequires from git to git-core
- Resolves: rhbz#1869399 rhbz#1885658 rhbz#1896379

* Wed Oct 14 2020 Miroslav Lisik <mlisik@redhat.com> - 0.10.7-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Added python bundled dependency dateutil
- Fixed virtual bundle provides for ember, handelbars, jquery and jquery-ui
- Resolves: rhbz#1222691 rhbz#1741056 rhbz#1851335 rhbz#1862966 rhbz#1869399 rhbz#1873691 rhbz#1875301 rhbz#1883445 rhbz#1885658 rhbz#1885841

* Tue Aug 11 2020 Miroslav Lisik <mlisik@redhat.com> - 0.10.6-4
- Fixed invalid CIB error caused by resource and operation defaults with mixed and-or rules
- Updated pcs-web-ui
- Resolves: rhbz#1867516

* Thu Jul 16 2020 Miroslav Lisik <mlisik@redhat.com> - 0.10.6-3
- Added Upgrade CIB if user specifies on-fail=demote
- Fixed rpmdiff issue with binary stripping checker
- Fixed removing non-empty tag by removing tagged resource group or clone
- Resolves: rhbz#1843079 rhbz#1857295

* Thu Jun 25 2020 Miroslav Lisik <mlisik@redhat.com> - 0.10.6-2
- Added resource and operation defaults that apply to specific resource/operation types
- Added Requires/BuildRequires: python3-pyparsing
- Added Requires: logrotate
- Fixed resource and stonith documentation
- Fixed rubygem licenses
- Fixed update_times()
- Updated rubygem rack to version 2.2.3
- Removed BuildRequires execstack (it is not needed)
- Resolves: rhbz#1805082 rhbz#1817547

* Thu Jun 11 2020 Miroslav Lisik <mlisik@redhat.com> - 0.10.6-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Added python bundled dependencies: dacite, dataclasses
- Added new bundled rubygem ruby2_keywords
- Updated rubygem bundled packages: backports, ethon, ffi, json, mustermann, rack, rack_protection, rack_test, sinatra, tilt
- Updated pcs-web-ui
- Updated test run, only tier0 tests are running during build
- Removed BuildRequires needed for tier1 tests which were removed for build (pacemaker-cli, fence_agents-*, fence_virt, booth-site)
- Resolves: rhbz#1387358 rhbz#1684676 rhbz#1722970 rhbz#1778672 rhbz#1782553 rhbz#1790460 rhbz#1805082 rhbz#1810017 rhbz#1817547 rhbz#1830552 rhbz#1832973 rhbz#1833114 rhbz#1833506 rhbz#1838853 rhbz#1839637

* Fri Mar 20 2020 Miroslav Lisik <mlisik@redhat.com> - 0.10.4-6
- Fixed communication between python and ruby daemons
- Resolves: rhbz#1783106

* Thu Feb 13 2020 Miroslav Lisik <mlisik@redhat.com> - 0.10.4-5
- Fixed link to sbd man page from `sbd enable` doc
- Fixed safe-disabling clones, groups, bundles
- Fixed sinatra wrapper performance issue
- Fixed detecting fence history support
- Fixed cookie options
- Updated hint for 'resource create ... master'
- Updated gating tests execution, smoke tests run from upstream sources
- Resolves: rhbz#1750427 rhbz#1781303 rhbz#1783106 rhbz#1793574

* Mon Jan 20 2020 Tomas Jelinek <tojeline@redhat.com> - 0.10.4-4
- Fix testsuite for pacemaker-2.0.3-4
- Resolves: rhbz#1792946

* Mon Dec 02 2019 Ivan Devat <idevat@redhat.com> - 0.10.4-3
- Added basic resource views in new webUI
- Resolves: rhbz#1744060

* Fri Nov 29 2019 Miroslav Lisik <mlisik@redhat.com> - 0.10.4-2
- Added disaster recovery support
- Fixed error message when cluster is not set up
- Removed '-g' option from rubygem's cflags because it does not generate .gnu_debugdata and option '-K' for strip command was removed
- Resolves: rhbz#1676431 rhbz#1743731

* Thu Nov 28 2019 Miroslav Lisik <mlisik@redhat.com> - 0.10.4-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Add '-g' to rubygem's cflags
- Resolves: rhbz#1743704 rhbz#1741586 rhbz#1750427

* Mon Nov 18 2019 Miroslav Lisik <mlisik@redhat.com> - 0.10.3-2
- Rebased to latest upstream sources (see CHANGELOG.md)
- Do not strip .gnu_debugdata section from binaries
- Resolves: rhbz#1631514 rhbz#1631519 rhbz#1734361 rhbz#1743704

* Mon Oct 21 2019 Miroslav Lisik <mlisik@redhat.com> - 0.10.3-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Resolves: rhbz#1442116 rhbz#1631514 rhbz#1631519 rhbz#1673835 rhbz#1698763 rhbz#1728890 rhbz#1734361 rhbz#1743704 rhbz#1743735 rhbz#1744056

* Tue Aug 13 2019 Tomas Jelinek <tojeline@redhat.com> - 0.10.2-4
- Generate 256 bytes long corosync authkey so clusters can start when FIPS is enabled
- Resolves: rhbz#1740218

* Mon Jul 08 2019 Ivan Devat <idevat@redhat.com> - 0.10.2-3
- Options starting with - and -- are no longer ignored for non-root users
- Resolves: rhbz#1725183

* Thu Jun 27 2019 Ivan Devat <idevat@redhat.com> - 0.10.2-2
- Fixed crashes in the `pcs host auth` command
- Command `pcs resource bundle reset` no longer accepts the container type
- Fixed id conflict with current bundle configuration in i`pcs resource bundle reset`
- Resolves: rhbz#1657166 rhbz#1676957

* Thu Jun 13 2019 Ivan Devat <idevat@redhat.com> - 0.10.2-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Added pam as required package
- An alternative webUI rebased to latest upstream sources
- Resolves: rhbz#1673907 rhbz#1679196 rhbz#1714663 rhbz#1717113

* Tue May 21 2019 Ivan Devat <idevat@redhat.com> - 0.10.1-9
- Added git as required package in tests/tests.yml
- Resolves: rhbz#1673907

* Mon May 20 2019 Ivan Devat <idevat@redhat.com> - 0.10.1-8
- Rebased to latest upstream sources (see CHANGELOG.md)
- Added an alternative webUI
- Resolves: rhbz#1673907 rhbz#1679197 rhbz#1667058

* Mon May 06 2019 Ondrej Mular <omular@redhat.com> - 0.10.1-7
- Enable upstream tests in gating
- Update tilt ruby gem
- Resolves: rhbz#1682129

* Thu May 02 2019 Ondrej Mular <omular@redhat.com> - 0.10.1-6
- Rebased to latest upstream sources (see CHANGELOG.md)
- Updated Red Hat logo
- Improved configuration files permissions in rpm
- Removed multi_json rubygem
- Excluded files required for building gems from rpm
- Resolves: rhbz#1625386 rhbz#1653316 rhbz#1655055 rhbz#1657166 rhbz#1659144 rhbz#1660702 rhbz#1664828 rhbz#1665404 rhbz#1667040 rhbz#1667053 rhbz#1667058 rhbz#1667090 rhbz#1668223 rhbz#1673822 rhbz#1673825 rhbz#1674005 rhbz#1676945 rhbz#1676957 rhbz#1682129 rhbz#1687562 rhbz#1687965 rhbz#1698373 rhbz#1700543

* Mon Mar 25 2019 Ondrej Mular <omular@redhat.com> - 0.10.1-5
- Enable gating
- Resolves: rhbz#1682129

* Wed Jan 30 2019 Ivan Devat <idevat@redhat.com> - 0.10.1-4
- Fixed crash when using unsupported options in commands `pcs status` and `pcs config`
- Resolves: rhbz#1668422

* Mon Jan 14 2019 Ivan Devat <idevat@redhat.com> - 0.10.1-3
- Fixed configuration names of link options that pcs puts to corosync.conf during cluster setup
- Fixed webUI issues in cluster setup
- Command `pcs resource show` was returned back and was signed as deprecated
- Added dependency on libknet1-plugins-all
- Resolves: rhbz#1661059 rhbz#1659051 rhbz#1664057

* Thu Dec 13 2018 Ondrej Mular <omular@redhat.com> - 0.10.1-2
- Fix documentation
- Resolves: rhbz#1656953

* Fri Nov 23 2018 Ivan Devát <idevat@redhat.com> - 0.10.1-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Udp/udpu transport is marked as unsupported
- Require pcmk-cluster-manager instead of pacemaker
- Require platform-python-setuptools instead of python3-setuptools
- Resolves: rhbz#1650109 rhbz#1183103 rhbz#1648942 rhbz#1650510 rhbz#1388398 rhbz#1651197 rhbz#1553736

* Fri Oct 26 2018 Ondrej Mular <omular@redhat.com> - 0.10.0.alpha.7-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Resolves: rhbz#1553736 rhbz#1615891 rhbz#1436217 rhbz#1596050 rhbz#1554310 rhbz#1553718 rhbz#1638852 rhbz#1620190 rhbz#1158816 rhbz#1640477

* Wed Oct 17 2018 Ondrej Mular <omular@redhat.com> - 0.10.0.alpha.6-3
- Add dependency on rubygems package
- Resolves: rhbz#1553736

* Thu Oct 04 2018 Ondrej Mular <omular@redhat.com> - 0.10.0.alpha.6-2
- Enable tests
- Cleanup of unnecessary bundle ruby-gem files
- Switch Require: python3 dependency to platform-python
- Added required linker flags
- Resolves: rhbz#1633613 rhbz#1630616

* Wed Sep 19 2018 Ivan Devát <idevat@redhat.com> - 0.10.0.alpha.6-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Resolves: rhbz#1553736

* Thu Sep 13 2018 Ivan Devát <idevat@redhat.com> - 0.10.0.alpha.5-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Resolves: rhbz#1553736 rhbz#1542288 rhbz#1619620

* Thu Sep 13 2018 Ivan Devát <idevat@redhat.com> - 0.10.0.alpha.4-2
- Fixed symlinks correction for rubygem ffi
- Resolves: rhbz#1553736

* Wed Sep 12 2018 Ivan Devát <idevat@redhat.com> - 0.10.0.alpha.4-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Resolves: rhbz#1549535 rhbz#1578955 rhbz#1158816 rhbz#1183103 rhbz#1536121 rhbz#1573344 rhbz#1619620 rhbz#1533866 rhbz#1578898 rhbz#1595829 rhbz#1605185 rhbz#1615420 rhbz#1566430 rhbz#1578891 rhbz#1591308 rhbz#1554953

* Mon Aug 06 2018 Ivan Devát <idevat@redhat.com> - 0.10.0.alpha.3-1
- Rebased to latest upstream sources (see CHANGELOG.md)
- Removed ruby dependencies (the dependencies are bundled instead)
- Resolves: rhbz#1611990

* Thu Aug 02 2018 Ivan Devát <idevat@redhat.com> - 0.10.0.alpha.2-1
- Rebased to latest upstream sources (see CHANGELOG.md)

* Wed Jul 18 2018 Ivan Devát <idevat@redhat.com> - 0.10.0.alpha.1-1
- Rebased to latest upstream sources (see CHANGELOG.md)

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
