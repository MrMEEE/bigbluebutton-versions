%if 0%{?fedora}
%bcond_with xmvn_generator
%bcond_without ivy
%else
%bcond_without xmvn_generator
%bcond_with ivy
%endif

%global python_prefix python3
%global python_interpreter %{?__python3}%{!?__python3:dummy}

%global default_jdk %{_prefix}/lib/jvm/java-21-openjdk
%global default_jre %{_prefix}/lib/jvm/jre-21-openjdk

%global maven_home %{_usr}/share/xmvn

Name:           javapackages-tools
Version:        6.2.0
Release:        9%{?dist}
Summary:        Macros and scripts for Java packaging support
License:        BSD-3-Clause
URL:            https://github.com/fedora-java/javapackages
BuildArch:      noarch

Source0:        https://github.com/fedora-java/javapackages/archive/%{version}.tar.gz
Source3:        javapackages-config.json

Source8:        toolchains-openjdk8.xml
Source11:       toolchains-openjdk11.xml
Source17:       toolchains-openjdk17.xml
Source21:       toolchains-openjdk21.xml

Patch0:         0001-coverage-use-usercustomize.patch

BuildRequires:  coreutils
BuildRequires:  which
BuildRequires:  make
BuildRequires:  asciidoc
BuildRequires:  xmlto
BuildRequires:  %{python_prefix}-devel
BuildRequires:  %{python_prefix}-lxml
BuildRequires:  %{python_prefix}-setuptools
BuildRequires:  %{python_prefix}-pytest

Requires:       javapackages-filesystem = %{version}-%{release}
Requires:       coreutils
Requires:       findutils
Requires:       which
# default JRE
Requires:       java-21-openjdk-headless

Provides:       jpackage-utils = %{version}-%{release}

%description
This package provides macros and scripts to support Java packaging.

%package -n javapackages-filesystem
Summary:        Java packages filesystem layout
Provides:       eclipse-filesystem = %{version}-%{release}

%description -n javapackages-filesystem
This package provides some basic directories into which Java packages
install their content.

%package -n maven-local
Summary:        Macros and scripts for Maven packaging support
Requires:       %{name} = %{version}-%{release}
Requires:       javapackages-local = %{version}-%{release}
Requires:       xmvn-minimal
Requires:       mvn(org.fedoraproject.xmvn:xmvn-mojo)
# Common Maven plugins required by almost every build. It wouldn't make
# sense to explicitly require them in every package built with Maven.
Requires:       mvn(org.apache.maven.plugins:maven-compiler-plugin)
Requires:       mvn(org.apache.maven.plugins:maven-jar-plugin)
Requires:       mvn(org.apache.maven.plugins:maven-resources-plugin)
Requires:       mvn(org.apache.maven.plugins:maven-surefire-plugin)

%description -n maven-local
This package provides macros and scripts to support packaging Maven artifacts.

%if %{with ivy}
%package -n ivy-local
Summary:        Local mode for Apache Ivy
Requires:       %{name} = %{version}-%{release}
Requires:       javapackages-local = %{version}-%{release}
Requires:       apache-ivy >= 2.3.0-8
Requires:       xmvn-connector-ivy

%description -n ivy-local
This package implements local mode for Apache Ivy, which allows
artifact resolution using XMvn resolver.
%endif

%package -n %{python_prefix}-javapackages
Summary:        Module for handling various files for Java packaging
Requires:       %{python_prefix}-lxml

%description -n %{python_prefix}-javapackages
Module for handling, querying and manipulating of various files for Java
packaging in Linux distributions

%package -n javapackages-local
Summary:        Non-essential macros and scripts for Java packaging support
Requires:       javapackages-common = %{version}-%{release}
# Java build systems don't have hard requirement on java-devel, so it should be there
Requires:       java-21-openjdk-devel
Requires:       xmvn-tools
%if %{with xmvn_generator}
Requires:       xmvn-generator
%endif

%description -n javapackages-local
This package provides non-essential macros and scripts to support Java packaging.

%package -n javapackages-generators
Summary:        RPM dependency generators for Java packaging support
Requires:       %{name} = %{version}-%{release}
Requires:       %{python_prefix}-javapackages = %{version}-%{release}
Requires:       %{python_interpreter}

%description -n javapackages-generators
RPM dependency generators to support Java packaging.

%package -n javapackages-common
Summary:        Non-essential macros and scripts for Java packaging support
Requires:       javapackages-generators = %{version}-%{release}

%description -n javapackages-common
This package provides non-essential, but commonly used macros and
scripts to support Java packaging.

%package -n javapackages-compat
Summary:        Previously deprecated macros and scripts for Java packaging support
Requires:       javapackages-local = %{version}-%{release}

%description -n javapackages-compat
This package provides previously deprecated macros and scripts to
support Java packaging as well as some additions to them.

%package -n maven-local-openjdk8
Summary:        OpenJDK 8 toolchain for XMvn
RemovePathPostfixes: -openjdk8
Requires:       maven-local
Requires:       java-1.8.0-openjdk-devel

%description -n maven-local-openjdk8
OpenJDK 8 toolchain for XMvn

%package -n maven-local-openjdk11
Summary:        OpenJDK 11 toolchain for XMvn
RemovePathPostfixes: -openjdk11
Requires:       maven-local
Requires:       java-11-openjdk-devel

%description -n maven-local-openjdk11
OpenJDK 11 toolchain for XMvn

%package -n maven-local-openjdk17
Summary:        OpenJDK 17 toolchain for XMvn
RemovePathPostfixes: -openjdk17
Requires:       maven-local
Requires:       java-17-openjdk-devel

%description -n maven-local-openjdk17
OpenJDK 17 toolchain for XMvn

%package -n maven-local-openjdk21
Summary:        OpenJDK 21 toolchain for XMvn
RemovePathPostfixes: -openjdk21
Requires:       maven-local
Requires:       java-21-openjdk-devel

%description -n maven-local-openjdk21
OpenJDK 21 toolchain for XMvn

%prep
%setup -q -n javapackages-%{version}
%patch 0 -p1

%build
%configure --pyinterpreter=%{python_interpreter} \
    --default_jdk=%{default_jdk} --default_jre=%{default_jre} \
    --rpmmacrodir=%{rpmmacrodir}
./build

%install
./install

sed -e 's/.[17]$/&*/' -i files-*

rm -rf %{buildroot}%{_bindir}/gradle-local
rm -rf %{buildroot}%{_datadir}/gradle-local
rm -rf %{buildroot}%{_mandir}/man7/gradle_build.7
%if %{without ivy}
rm -rf %{buildroot}%{_sysconfdir}/ivy
rm -rf %{buildroot}%{_sysconfdir}/ant.d
%endif

mkdir -p %{buildroot}%{maven_home}/conf/
cp -p %{SOURCE8} %{buildroot}%{maven_home}/conf/toolchains.xml-openjdk8
cp -p %{SOURCE11} %{buildroot}%{maven_home}/conf/toolchains.xml-openjdk11
cp -p %{SOURCE17} %{buildroot}%{maven_home}/conf/toolchains.xml-openjdk17
cp -p %{SOURCE21} %{buildroot}%{maven_home}/conf/toolchains.xml-openjdk21

install -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/java/javapackages-config.json

%if 0%{?flatpak}
# make both /app (runtime deps) and /usr (build-only deps) builds discoverable
sed -e '/^JAVA_LIBDIR=/s|$|:/usr/share/java|' \
    -e '/^JNI_LIBDIR=/s|$|:/usr/lib/java|' \
    -i %{buildroot}%{_sysconfdir}/java/java.conf
# /usr path is hard-coded in xmvn
ln -s %{_datadir}/java-utils %{buildroot}%{_usr}/share/java-utils
%endif

%check
./check

%files -f files-tools
%if 0%{?flatpak}
%{_usr}/share/java-utils
%endif

%files -n javapackages-filesystem -f files-filesystem

%files -n javapackages-generators -f files-generators

%files -n javapackages-common -f files-common

%files -n javapackages-compat -f files-compat

%files -n javapackages-local

%files -n maven-local

%if %{with ivy}
%files -n ivy-local -f files-ivy
%endif

%files -n maven-local-openjdk8
%dir %{maven_home}/conf
%{maven_home}/conf/toolchains.xml-openjdk8

%files -n maven-local-openjdk11
%dir %{maven_home}/conf
%{maven_home}/conf/toolchains.xml-openjdk11

%files -n maven-local-openjdk17
%dir %{maven_home}/conf
%{maven_home}/conf/toolchains.xml-openjdk17

%files -n maven-local-openjdk21
%dir %{maven_home}/conf
%{maven_home}/conf/toolchains.xml-openjdk21

%files -n %{python_prefix}-javapackages -f files-python
%license LICENSE

%changelog
* Fri Feb 16 2024 Marian Koncek <mkoncek@redhat.com> - 6.2.0-9
- Switch to OpenJDK 21 as default JDK/JRE

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 20 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 6.2.0-6
- Fix flatpak builds of Java packages

* Thu Oct 19 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.2.0-5
- Backport upstream patch to fix Flatpak builds

* Wed Sep 20 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.2.0-4
- Add support for OpenJDK 21

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.2.0-3
- Convert License tag to SPDX format

* Wed Aug 30 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.2.0-2
- Enable XMvn dependency generator in ELN

* Wed Aug 30 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.2.0-1
- Update to upstream version 6.2.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 6.1.0-9
- Rebuilt for Python 3.12

* Wed Mar 08 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.1.0-8
- Make javapackages-extra depend on jurand

* Wed Jan 25 2023 Marian Koncek <mkoncek@redhat.com> - 6.1.0-7
- Add generated Requires on multiple versions of java-headless

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Aug 19 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.1.0-5
- Fix generated auto-requires on java-headless

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.1.0-3
- Drop ExclusiveArch

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 6.1.0-2
- Rebuilt for Drop i686 JDKs

* Thu Jun 23 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.1.0-1
- Update to upstream version 6.1.0

* Tue Jun 14 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.0.0-10
- Introduce javapackages-extra and javapackages-common subpackages
- Drop metadata for com.sun:tools and sun.jdk:jconsole
- Re-enable tests
- Re-add manpages
- Drop bootstrap mode

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 6.0.0-9
- Rebuilt for Python 3.11

* Thu May 05 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.0.0-8
- Install toolchains.xml in correct location in bootstrap mode

* Thu Jan 27 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.0.0-7
- Switch to OpenJDK 17 as default JDK/JRE

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 14 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.0.0-5
- Bootstrap build for Maven 3.8.4

* Sun Nov 21 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.0.0-4
- Uptate ivy-local classpath

* Wed Nov 17 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 6.0.0-3
- Re-add ivy-local subpackage

* Tue Nov 02 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.0.0-2
- Implement OpenJDK 11 and 17 toolchains

* Mon Jul 26 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.0.0-1
- Update to upstream version 6.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0~alpha-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 14 2021 Sérgio Basto <sergio@serjux.com> - 6.0.0~alpha-8
- Drop apache-ivy is orphan now

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 6.0.0~alpha-7
- Rebuilt for Python 3.10

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.0.0~alpha-6
- Bootstrap build
- Non-bootstrap build

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.0.0~alpha-5
- Implement bootstrap mode

* Thu May 13 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.0.0~alpha-4
- Disable skippedPlugins for now

* Thu May 13 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.0.0~alpha-3
- Fix typos in Requires

* Thu May 13 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.0.0~alpha-2
- Disable javapackages-bootstrap for now

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 30 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.3.0-14
- Add javapackages-generators provides

* Wed Jul 29 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.0.0~alpha-1
- Update to upstream version 6.0.0~alpha

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 17 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.3.1-9
- Add separate subpackage with RPM generators

* Thu Jul 16 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.3.1-8
- Don't use networking during tests

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 5.3.0-12
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jun 10 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.3.0-11
- Use XMvn Javadoc MOJO for generating API docs

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 5.3.0-10
- Rebuilt for Python 3.9

* Tue Apr 28 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.3.0-10
- Switch to OpenJDK 11 as default JDK

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.3.1-7
- Add OpenJDK 8 toolchain configuration

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.3.1-6
- Mass rebuild for javapackages-tools 201902

* Fri Oct 25 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.3.1-5
- Switch to OpenJDK 11 as default JDK

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 5.3.0-8
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 5.3.0-7
- Rebuilt for Python 3.8

* Sun Aug 11 2019 Fabio Valentini <decathorpe@gmail.com> - 5.3.0-6
- Disable gradle support by default.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 28 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.3.1-4
- Enable namespaced dependency generation

* Fri Jun 28 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.3.1-3
- Don't ignore duplicate metadata in namespaced modules

* Fri Jun 28 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.3.1-2
- Introduce javapackages-config-maven-3.6

* Fri Jun 14 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.3.1-1
- Update to upstream version 5.3.1

* Mon Jun 10 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.3.0-7
- Define maven-3.6 install repository

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.3.0-6
- Mass rebuild for javapackages-tools 201901

* Thu Apr 25 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.3.0-5
- Move python modules under java-utils directory

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 20 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.3.0-3
- Make it possible to build SRPM without python-devel installed

* Thu Oct  4 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.3.0-2
- Make javapackages-local require Python interpreter executable path

* Mon Aug 06 2018 Michael Simacek <msimacek@redhat.com> - 5.3.0-1
- Update to upstream version 5.3.0

* Thu Aug  2 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.2.0-6
- Switch auto-requires generator to javapackages-filesystem

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 5.2.0-4
- Rebuilt for Python 3.7

* Mon Jun 25 2018 Michael Simacek <msimacek@redhat.com> - 5.2.0-3
- Disable bytecode compilation outside of site-packages

* Wed Jun 20 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.2.0-2
- Fix running tests on Python 3.7

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 5.2.0-2
- Rebuilt for Python 3.7

* Tue Jun  5 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.2.0-1
- Update to upstream version 5.2.0

* Tue May 15 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.1.0-1
- Update to upstream version 5.1.0
- Introduce javapackages-filesystem package

* Wed May 02 2018 Michael Simacek <msimacek@redhat.com> - 5.0.0-13
- Backport abrt-java-connector changes

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5.0.0-12
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Merlin Mathesius <mmathesi@redhat.com> - 5.0.0-10
- Cleanup spec file conditionals

* Sat Sep 23 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0-9
- Conditionally allow building without asciidoc

* Thu Sep  7 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0-8
- Allow manpages to be either compressed or not

* Thu Aug 17 2017 Michael Simacek <msimacek@redhat.com> - 5.0.0-7
- Fix traceback on corrupt zipfile
- Resolves: rhbz#1481005

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 10 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0-5
- Conditionalize use of XMvn Javadoc MOJO

* Mon Jul 03 2017 Michael Simacek <msimacek@redhat.com> - 5.0.0-4
- Fix default JRE path

* Mon Jul 03 2017 Michael Simacek <msimacek@redhat.com> - 5.0.0-3
- Don't use xmvn javadoc for now

* Wed Jun 21 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0-2
- Re-add dist-tag

* Wed Jun 21 2017 Michael Simacek <msimacek@redhat.com> - 5.0.0-2
- Remove xmvn version requirement

* Wed Jun 21 2017 Michael Simacek <msimacek@redhat.com> - 5.0.0-1
- Update to upstream version 5.0.0

* Tue Mar 14 2017 Michael Simacek <msimacek@redhat.com> - 4.7.0-16
- Force locale in test to fix failures

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb  1 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.7.0-14
- Fix build without gradle

* Tue Jan 31 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.7.0-13
- Allow to conditionally build without gradle

* Tue Dec 20 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.7.0-12
- Non-bootstrap build

* Tue Dec 20 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.7.0-11
- Port to Python 3.6

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 4.7.0-10
- Rebuild for Python 3.6

* Fri Nov 18 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.7.0-9
- Add Requires on which
- Resolves: rhbz#1396395

* Mon Oct  3 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.7.0-8
- Fix generation of versioned OSGi requires

* Tue Sep 06 2016 Michael Simacek <msimacek@redhat.com> - 4.7.0-7
- Remove docs, which were split into java-packaging-howto

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.0-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 29 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.7.0-5
- Remove requires on maven-enforcer-plugin

* Tue Jun 28 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.7.0-4
- Require xmvn-minimal instead of full xmvn

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.7.0-3
- Drop requires on most of parent POMs

* Thu Mar 31 2016 Michal Srb <msrb@redhat.com> - 4.7.0-2
- Add R: findutils (Resolves: rhbz#1321401, thanks Tatsuyuki Ishi)

* Fri Mar 04 2016 Michal Srb <msrb@redhat.com> - 4.7.0-1
- Update to 4.7.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan  4 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.6.0-12
- Move mvn_build and builddep to javapackages-local
- Resolves: rhbz#1290399

* Wed Nov 11 2015 Kalev Lember <klember@redhat.com> - 4.6.0-11
- Disable bootstrap

* Wed Nov 11 2015 Kalev Lember <klember@redhat.com> - 4.6.0-10
- Add bootstrap macro (#1280209)
- Enable bootstrap for Python 3.5 rebuilds

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 28 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.6.0-8
- Backport %%gradle_build macro from 4.7.0-SNAPSHOT

* Mon Oct 19 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.6.0-7
- Don't generate requires on java-headless
- Resolves: rhbz#1272145

* Tue Jul 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.6.0-6
- Use %%license macro

* Fri Jul 10 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.6.0-5
- Add requires on java-devel to javapackages-local

* Tue Jun 30 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.6.0-4
- Remove jpackage-utils obsoletes

* Mon Jun 22 2015 Michal Srb <msrb@redhat.com> - 4.6.0-3
- Rebuild to fix provides

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Michal Srb <msrb@redhat.com> - 4.6.0-1
- Update to upstream version 4.6.0

* Thu Apr 23 2015 Michal Srb <msrb@redhat.com> - 4.5.0-3
- Fix "UnboundLocalError: local variable 'pom_requires' referenced before assignment"

* Tue Apr 21 2015 Michael Simacek <msimacek@redhat.com> - 4.5.0-2
- Remove fedora-review-plugin-java subpackage

* Thu Apr 09 2015 Michal Srb <msrb@redhat.com> - 4.5.0-1
- Update to upstream version 4.5.0

* Wed Apr  1 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.4.0-4
- Remove requires on plexus-tools-pom

* Tue Mar 24 2015 Michael Simacek <msimacek@redhat.com> - 4.4.0-3
- Handle non-utf-8 poms in pom_editor

* Mon Feb 16 2015 Michael Simacek <msimacek@redhat.com> - 4.4.0-2
- Write temporary XML file as UTF-8 in pom_editor

* Mon Feb 16 2015 Michal Srb <msrb@redhat.com> - 4.4.0-1
- Update to upstream version 4.4.0

* Fri Feb 13 2015 Michal Srb <msrb@redhat.com> - 4.3.2-6
- Fix TypeError in maven_depmap (see: rhbz#1191657)

* Thu Feb 12 2015 Michael Simacek <msimacek@redhat.com> - 4.3.2-5
- Workaround for XMvn version bump (rhbz#1191657)

* Fri Jan 23 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.2-4
- Add gradle-local subpackage
- Allow conditional builds with tests skipped

* Mon Jan 19 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.2-3
- Port to lua 5.3.0

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.2-2
- Replace all dashes with dots in versioned provides and requires

* Mon Jan 05 2015 Michal Srb <msrb@redhat.com> - 4.3.2-1
- Update to upstream version 4.3.2
- Fix TypeError in mvn_artifact

* Tue Dec 23 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.1-1
- Update to upstream version 4.3.1

* Sun Dec 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.0-1
- Update to upstream version 4.3.0

* Fri Nov 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-11
- Remove dependency on libxslt

* Fri Nov 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-10
- Scan lib64/ in OSGi dep generators
- Related: rhbz#1166156

* Wed Nov 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-9
- Revert adding namespace support in %%mvn_artifact

* Mon Nov 24 2014 Michal Srb <msrb@redhat.com> - 4.2.0-8
- Add namespace support in %%mvn_artifact

* Fri Nov 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-7
- Fix OSGi provides/requires generation in Java libdir
- Resolves: rhbz#1166156

* Wed Nov 12 2014 Michal Srb <msrb@redhat.com> - 4.2.0-6
- Fix cache problem (Resolves: rhbz#1155185)

* Thu Oct 30 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-5
- Use wrapper script to inject ABRT agent JVM argument
- Fix path to ABRT agent DSO
- Resolves: rhbz#1153652

* Tue Oct 21 2014 Michael Simacek <msimacek@redhat.com> - 4.2.0-4
- Fix pom_editor missing space between xmlns declarations

* Wed Sep 24 2014 Michal Srb <msrb@redhat.com> - 4.2.0-3
- Do not generate OSGi R on eclipse-platform

* Thu Sep 18 2014 Michal Srb <msrb@redhat.com> - 4.2.0-2
- Fix mvn_artifact: generate R, if it's not explicitly disabled

* Thu Jul 24 2014 Michal Srb <msrb@redhat.com> - 4.2.0-1
- Update to upstream version 4.2.0

* Thu Jul 10 2014 Michal Srb <msrb@redhat.com> - 4.1.0-2
- Backport upstream patch for maven.req

* Mon Jun 23 2014 Michal Srb <msrb@redhat.com> - 4.1.0-1
- Update to upstream version 4.1.0

* Thu Jun 12 2014 Michal Srb <msrb@redhat.com> - 4.0.0-8
- Install man page for pom_change_dep

* Tue Jun 10 2014 Michal Srb <msrb@redhat.com> - 4.0.0-7
- Backport fix for maven.prov

* Tue Jun 10 2014 Michal Srb <msrb@redhat.com> - 4.0.0-6
- Update docs

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Michal Srb <msrb@redhat.com> - 4.0.0-4
- Backport patch which adds support for "disableEffectivePom" property

* Thu May 29 2014 Michal Srb <msrb@redhat.com> - 4.0.0-3
- Add BR: javapackages-tools

* Thu May 29 2014 Michal Srb <msrb@redhat.com> - 4.0.0-2
- Backport patches for maven.req
- Remove com.sun:tools and sun.jdk:jconsole provides

* Thu May 29 2014 Michal Srb <msrb@redhat.com> - 4.0.0-1
- Update to 4.0.0

* Wed May 28 2014 Michal Srb <msrb@redhat.com> - 3.5.0-9
- Apply the patch from my previous commit

* Wed May 28 2014 Michal Srb <msrb@redhat.com> - 3.5.0-8
- Generate requires on POM artifacts with "pom" extension

* Wed Apr 30 2014 Michal Srb <msrb@redhat.com> - 3.5.0-7
- Improve support for SCLs

* Wed Apr 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.5.0-6
- Add explicit maven-local requires on java-1.8.0-openjdk-devel

* Thu Mar 27 2014 Michael Simacek <msimacek@redhat.com> - 3.5.0-6
- Install documentation

* Mon Feb 24 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.5.0-5
- Backport java-headless patches

* Mon Feb 10 2014 Michal Srb <msrb@redhat.com> - 3.5.0-4
- Add support for installing Maven artifacts with .hpi extension

* Fri Jan 17 2014 Michael Simacek <msimacek@redhat.com> - 3.5.0-3
- Use upstream method of running tests (nosetests)

* Thu Jan 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.5.0-2
- Add version requirements on xmvn and ivy

* Thu Jan 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.5.0-1
- Update to upstream version 3.5.0
- Add ivy-local subpackage

* Tue Jan  7 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.2-3
- Update patch for ZIP files

* Tue Jan  7 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.2-2
- Allow ZIP files in %%{_javadir}

* Thu Dec 05 2013 Michal Srb <msrb@redhat.com> - 3.4.2-1
- Update to upstream bugfix release 3.4.2

* Wed Dec  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.1-3
- Add Requires on objectweb-pom

* Tue Nov 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4.1-2
- Do not create parent dirs for pom.properties
- Resolves: rhbz#1031769

* Tue Nov 05 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4.1-1
- Update to upstream bugfix release 3.4.1

* Mon Oct 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.0-3
- Fix XMvn configuration for native JNI repos
- Resolves: rhbz#1021608

* Mon Oct 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.0-2
- Require exact version of python-javapackages

* Mon Oct 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.0-1
- Update to upstream version 3.4.0

* Wed Oct  2 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.1-1
- Update to upstream version 3.3.1
- Remove workaround for sisu-guice no_aop

* Tue Oct 01 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.3.0-1
- Update to upstream version 3.3.0

* Wed Sep 25 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2.4-2
- Fix installation of artifacts with classifier

* Tue Sep 24 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2.4-1
- Update to upstream version 3.2.4

* Tue Sep 24 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2.3-1
- Update to upstream version 3.2.3

* Fri Sep 20 2013 Michal Srb <msrb@redhat.com> - 3.2.2-1
- Update to upstream version 3.2.2

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-1
- Update to upstream version 3.2.1

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.0-1
- Update to upstream version 3.2.0

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-1
- Update to upstream version 3.1.2

* Thu Sep 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.1.1-1
- Update to upstream version 3.1.1

* Thu Sep 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.1.0-1
- Update to upstream version 3.1.0

* Mon Sep 16 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-2
- Add depmap for sun.jdk:jconsole

* Fri Sep 13 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-1
- Update to upstream version 3.0.4

* Wed Sep 11 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-1
- Update to upstream version 3.0.3

* Tue Sep 10 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.2-3
- Fix a typo in temporary depmap

* Tue Sep 10 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.2-2
- Make sure we do not provide google guice mapping

* Tue Sep 10 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> 3.0.2-1
- Update to upstream version 3.0.2
- Add separate python-javapackages subpackage
- Add separate fedora-review-plugin-java subpackage
- Enable part of unit tests

* Tue Sep  3 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> 3.0.0-0.2
- Fix javadoc directory override

* Tue Sep  3 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> 3.0.0-0.1
- Update to upstream pre-release version 3.0.0

* Fri Jul 26 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.1-1
- Update to upstream version 2.0.1
- Fix creation of artifact aliases, resolves: rhbz#988462

* Thu Jul 25 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.0-2
- Require maven-resources-plugin by maven-local

* Thu Jul 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.0-1
- Update to upstream version 2.0.0
- Merge functionality of jpackage-utils
- Provide and obsolete jpackage-utils
- %%add_maven_depmap macro now injects pom.properties to every JAR
- %%add_to_maven_depmap and %%update_maven_depmap macros were removed
- maven2jpp-mapdeps.xsl template has been removed
- Macros related to installation of icons and desktop files were removed
- 14 new manual pages were added
- Documentation specific to JPackage was removed
- Add BuildRequires: asciidoc, xmlto

* Mon Jul  1 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.15.0-2
- Add R: jvnet-parent

* Wed Jun  5 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.15.0-1
- Update to upstream version 0.15.0
- Added depmap for tools.jar
- Added support for versioned autorequires
- New plugin metadata from Maven Central

* Tue Jun  4 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.14.1-2
- Add several maven plugins to maven-local requires

* Wed May 29 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.14.1-1
- Update to upstream version 0.14.1 with disabled debugging

* Tue Apr 09 2013 Michal Srb <msrb@redhat.com> - 0.14.0-1
- Update to upstream version 0.14.0

* Mon Apr  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.7-2
- Add R: maven-surefire-provider-junit4 to maven-local

* Fri Mar 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.7-1
- Update to upstream version 0.13.7

* Wed Mar 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.6-4
- Add geronimo-parent-poms to common POMs

* Wed Mar 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.6-3
- Add weld-parent to common POMs

* Wed Mar 20 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.13.6-2
- Fix conditional macro to evaluate properly when fedora is not defined

* Mon Mar 18 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.6-1
- Update to upstream version 0.13.6

* Wed Mar 13 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.5-1
- Update to upstream version 0.13.5

* Wed Mar 13 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.4-1
- Update to upstream version 0.13.4

* Tue Mar 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.3-1
- Update to upstream version 0.13.3

* Thu Mar  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.2-1
- Update to upstream version 0.13.2

* Thu Mar  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.1-1
- Update to upstream version 0.13.1

* Wed Mar  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.0-1
- Update to upstream version 0.13.0

* Wed Mar  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.0-0.1.git2f13366
- Upate to upstream pre-release snapshot 2f13366

* Mon Mar  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.6-1
- Update to upstream version 0.12.6
- Resolves: rhbz#917618 (remove jetty orbit provides)
- Resolves: rhbz#917647 (system.bundle into autogenerated deps)

* Fri Mar  1 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.12.5-1
- Update to upstream version 0.12.5
- Resolves problems with compat package provides and automatic requires

* Wed Feb 27 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.4-2
- Don't mark RPM macro files as configuration

* Mon Feb 25 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.4-1
- Update to upstream version 0.12.4
- Resolves: rhbz#913630 (versioned requires between subpackages)

* Fri Feb 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.3-1
- Update to upstream version 0.12.3
- Resolves: rhbz#913694 (No plugin found for prefix 'X')

* Wed Feb 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.2-1
- Update to upstream version 0.12.2
- Resolves: rhbz#913120 (MAVEN_OPTS are not passed to Maven)

* Mon Feb 18 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.1-1
- Update to upstream version 0.12.1
- Resolves: rhbz#912333 (M2_HOME is not exported)

* Fri Feb 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.0-1
- Update to upstream version 0.12.0
- Implement new pom macros: xpath_replace and xpath_set
- Remove Support-local-depmaps.patch (accepted upstream)

* Fri Feb 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.2-6
- Support local depmaps

* Thu Feb 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.2-5
- Add some maven-local Requires for convenience

* Thu Feb  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.2-4
- Add missing R: httpcomponents-project

* Thu Feb  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.2-3
- Add missing R: jboss-patent

* Wed Feb  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.2-2
- Don't install mvn-local and mvn-rpmbuild on F18

* Wed Jan 30 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.2-1
- Update to upstream version 0.11.2

* Wed Jan 30 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.1-1
- Update to upstream version 0.11.1

* Wed Jan 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.0-1
- Update to upstream version 0.11.0
- Add mvn-local and mvn-rpmbuild scripts

* Mon Jan 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.10.1-1
- Update to upstream version 0.10.1

* Mon Jan  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.10.0-1
- Update to upstream version 0.10.0
- Implement %%xmvn_alias, %%xmvn_file and %%xmvn_package macros
- Fix regex in osgi.attr
- Add support for pre- and post-goals in mvn-build script

* Mon Dec 10 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.9.1-1
- Update to upstream version 0.9.1
- Resolves: rhbz#885636

* Thu Dec  6 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.9.0-1
- Update to latest upstream version
- Enable maven requires generator for xmvn packages
- Enable requires generator for javadoc packages

* Wed Dec  5 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.3-1
- Update to upstream version 0.8.3
- Fix maven provides generator for new XML valid fragments

* Fri Nov 30 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8.2-1
- Update to upstream version 0.8.2

* Fri Nov 30 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8.1-1
- Update to upstream version 0.8.1

* Wed Nov 28 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8.0-1
- Update to upstream version 0.8.0
- Add xmvn macros

* Tue Nov 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.5-3
- Add BR: jpackage-utils

* Tue Nov 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.5-2
- Add maven-local subpackage

* Thu Nov 08 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.5-1
- Fix versioned pom installation by quoting _jpath

* Wed Oct 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.4-1
- Shorten maven filelist filenames

* Wed Oct 31 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.3-1
- Update to upstream version 0.7.3

* Wed Oct 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.2-1
- Make sure add_maven_depmap fails when python tracebacks

* Wed Oct 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.1-1
- Fix problem with exception in default add_maven_depmap invocation

* Tue Oct 30 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.0-1
- Update to latest upstream
- Full support for compat depmap generation
- Generate maven-files-%%{name} with a list of files to package
- Add support for maven repo generation (alpha version)

* Mon Jul 30 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.6.0-1
- Update to upstream version 0.6.0
- Make maven provides versioned
- Add additional pom_ macros to simplify additional pom editing

* Wed Jul 25 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.5.0-1
- Update to upstream version 0.5.0 - add support for add_maven_depmap -v

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  9 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4.1-1
- Update to upstream version 0.4.1
- Fixes #837203

* Wed Jun 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4.0-1
- Update to upstream version 0.4.0

* Tue Mar  6 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.1-1
- Create maven provides from fragments instead of poms

* Thu Feb 16 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.0-3
- Fix maven_depmap installation

* Wed Feb 15 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.0-2
- Add conflicts with older jpackage-utils

* Wed Feb 15 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.0-1
- Initial version split from jpackage-utils
