%_javapackages_macros
Name:          glassfish-dtd-parser
Version:       1.2
Release:       0.8.20120120svn.0%{?dist}
Summary:       Library for parsing XML DTDs
License:       CDDL 1.1 and GPLv2 with exceptions
Url:           http://java.net/projects/dtd-parser
# svn export https://svn.java.net/svn/dtd-parser~svn/trunk/dtd-parser glassfish-dtd-parser-1.2-SNAPSHOT
# find glassfish-dtd-parser-1.2-SNAPSHOT/ -name '*.jar' -delete
# tar czf glassfish-dtd-parser-1.2-SNAPSHOT-src-svn.tar.gz glassfish-dtd-parser-1.2-SNAPSHOT
Source0:       %{name}-%{version}-SNAPSHOT-src-svn.tar.gz
BuildRequires: java-devel
BuildRequires: bsf
BuildRequires: maven-local
BuildRequires: maven-enforcer-plugin
BuildRequires: sonatype-oss-parent

BuildArch:     noarch

%description
Library for parsing XML DTDs.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{version}-SNAPSHOT

%build

%mvn_file :dtd-parser %{name}
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt
