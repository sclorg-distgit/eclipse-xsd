%{?scl:%scl_package eclipse-xsd}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 1

# No release tag yet, see ebz#495966
%global git_tag 650f7f219637792760c8fd7d34d1d1aa9058d539

Name:      %{?scl_prefix}eclipse-xsd
Version:   2.12.0
Release:   1.%{baserelease}%{?dist}
Summary:   XML Schema Definition (XSD) Eclipse plug-in
License:   EPL
URL:       http://www.eclipse.org/modeling/mdt/?project=xsd

Source0:   http://git.eclipse.org/c/xsd/org.eclipse.xsd.git/snapshot/org.eclipse.xsd-%{git_tag}.tar.xz

# Build with maven/tycho instead of pdebuild, these patches have been sent upstream, see:
# https://bugs.eclipse.org/bugs/show_bug.cgi?id=438418
Patch0:    0002-Migrate-to-shared-license.patch
Patch1:    0003-438418-Migrate-to-tycho-build.patch

BuildArch:        noarch

BuildRequires:    %{?scl_prefix}tycho
BuildRequires:    %{?scl_prefix}tycho-extras
BuildRequires:    %{?scl_prefix}eclipse-pde >= 1:4.4.0
BuildRequires:    %{?scl_prefix}eclipse-emf-sdk >= 2.11.0
BuildRequires:    %{?scl_prefix}eclipse-license
Requires:         %{?scl_prefix}eclipse-platform >= 1:4.4.0
Requires:         %{?scl_prefix}eclipse-emf-runtime >= 2.11.0

%description
The XML Schema Definition (XSD) plug-in is a library that provides an API for
manipulating the components of an XML Schema as described by the W3C XML
Schema specifications, as well as an API for manipulating the DOM-accessible
representation of XML Schema as a series of XML documents.

%package   sdk
Summary:   Eclipse XSD SDK
Requires:  %{?scl_prefix}eclipse-pde >= 1:4.4.0
Requires:  %{?scl_prefix}eclipse-emf-sdk >= 2.11.0
Requires:  %{name} = %{version}-%{release}

%description sdk
Documentation and developer resources for the Eclipse XML Schema Definition
(XSD) plug-in.

%package   examples
Summary:   Eclipse XSD examples
Requires:  %{name}-sdk = %{version}-%{release}

%description examples
Installable versions of the example projects from the SDKs that demonstrate how
to use the XML Schema Definition (XSD) plug-ins.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n org.eclipse.xsd-%{git_tag}

find -name *.jar -exec rm -rf {} \;
find -name *.class -exec rm -rf {} \;

%patch0 -p1
%patch1 -p1

%mvn_package "::pom::" __noinstall
%mvn_package ":::{sources,sources-feature}:" sdk
%mvn_package ":org.eclipse.xsd.{sdk,doc,cheatsheets}" sdk
%mvn_package ":org.eclipse.xsd.example.installer" sdk
%mvn_package ":org.eclipse.xsd.example" examples
%mvn_package ":" runtime
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_build -j -f
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles-runtime

%files sdk -f .mfiles-sdk

%files examples -f .mfiles-examples	

%changelog
* Thu Jul 28 2016 Mat Booth <mat.booth@redhat.com> - 2.12.0-1.1
- Auto SCL-ise package for rh-eclipse46 collection

* Mon Jun 13 2016 Mat Booth <mat.booth@redhat.com> - 2.12.0-1
- Update to Neon release
- Drop old obsoletes

* Fri Mar 11 2016 Mat Booth <mat.booth@redhat.com> - 2.11.0-3
- Rebuilt to fix qualifiers

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 05 2015 Mat Booth <mat.booth@redhat.com> - 2.11.0-1
- Update to Mars release

* Mon Sep 14 2015 Roland Grunberg <rgrunber@redhat.com> - 2.10.1-5
- Rebuild as an Eclipse p2 Droplet.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Dec 10 2014 Mat Booth <mat.booth@redhat.com> - 2.10.1-3
- Install source features

* Mon Dec 8 2014 Alexander Kurtakov <akurtako@redhat.com> 2.10.1-2
- Build with xmvn.

* Wed Oct 01 2014 Mat Booth <mat.booth@redhat.com> - 2.10.1-1
- Update to Luna SR1 release
- Drop upstreamed patch

* Wed Aug 13 2014 Mat Booth <mat.booth@redhat.com> - 2.10.0-2
- Qualifier should be lexographically greater than upstream's

* Wed Jun 25 2014 Mat Booth <mat.booth@redhat.com> - 2.10.0-1
- Update to latest upstream release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 07 2014 Mat Booth <mat.booth@redhat.com> - 2.9.2-2
- Add examples sub-package.

* Wed Mar 12 2014 Mat Booth <mat.booth@redhat.com> - 2.9.2-1
- Initial release of separate XSD package.