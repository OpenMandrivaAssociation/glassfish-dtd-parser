Name:		glassfish-dtd-parser
Version:	1.5.1
Release:	1
Summary:	SAX-like API for parsing XML DTDs
Group:		Development/Java
License:	BSD
URL:		https://github.com/eclipse-ee4j/jaxb-dtd-parser
Source0:	https://github.com/eclipse-ee4j/jaxb-dtd-parser/archive/refs/tags/%{version}.tar.gz#/glassfish-dtd-parser-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name dtd-parser --link %{name}

Obsoletes:	%{name}-javadoc < %{version}-%{release}

%description
This is the Eclipse DTD parser used by the JAXB implementation.
1.5.1 replaces the 2012 1.2 snapshot. It is a named module,
com.sun.xml.dtdparser, and compiles at release 11. There are no
third-party dependencies. The license is the Eclipse Distribution
License, the 3-clause BSD license. Tests are skipped.

%prep
%autosetup -n jaxb-dtd-parser-%{version}
rm -rf dtd-parser/src/test
find . -name '*.jar' -delete
find . \( -name '*.so' -o -name '*.dll' -o -name '*.dylib' -o -name '*.class' \) -delete
python - <<'PY'
from pathlib import Path

java_files = list(Path("dtd-parser/src/main/java").rglob("*.java"))
if len(java_files) != 16:
    raise SystemExit("java files " + str(len(java_files)))
module_info = Path("dtd-parser/src/main/java/module-info.java").read_text(encoding="utf-8")
if "module com.sun.xml.dtdparser" not in module_info:
    raise SystemExit("module name")
if list(Path(".").rglob("*.jar")) or list(Path(".").rglob("*.class")):
    raise SystemExit("prebuilt binary remains")
for pom in Path(".").rglob("pom.xml"):
    pom.unlink()

Path("pom.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.sun.xml.dtd-parser</groupId>
  <artifactId>dtd-parser</artifactId>
  <version>%{version}</version>
  <packaging>jar</packaging>
  <name>DTD Parser</name>
  <description>SAX-like API for parsing XML DTDs.</description>
  <url>https://github.com/eclipse-ee4j/jaxb-dtd-parser</url>
  <licenses>
    <license>
      <name>BSD-3-Clause</name>
      <url>https://www.eclipse.org/org/documents/edl-v10.php</url>
    </license>
  </licenses>
  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.release>11</maven.compiler.release>
  </properties>
  <build>
    <sourceDirectory>dtd-parser/src/main/java</sourceDirectory>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.12.1</version>
        <configuration>
          <release>11</release>
        </configuration>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jar-plugin</artifactId>
        <version>3.3.0</version>
      </plugin>
    </plugins>
  </build>
</project>
""", encoding="utf-8")
pom = Path("pom.xml").read_text(encoding="utf-8")
poms = sorted(str(path) for path in Path(".").rglob("pom.xml"))
if poms != ["pom.xml"]:
    raise SystemExit("poms " + str(poms))
for needle in (
    "<artifactId>dtd-parser</artifactId>",
    "<version>%{version}</version>",
    "<release>11</release>",
    "<sourceDirectory>dtd-parser/src/main/java</sourceDirectory>",
):
    if needle not in pom:
        raise SystemExit("pom missing " + needle)
for needle in ("junit", "SNAPSHOT", "<source>", "<target>", "<parent>", "oss-parent", "jacoco"):
    if needle in pom:
        raise SystemExit("pom still contains " + needle)
PY

%build -a
java --module-path target/dtd-parser-%{version}.jar --describe-module com.sun.xml.dtdparser > module-describe.txt
grep -q '^com.sun.xml.dtdparser' module-describe.txt || { cat module-describe.txt; exit 1; }
if grep -q ' automatic$' module-describe.txt; then cat module-describe.txt; exit 1; fi

%files -f .mfiles
%doc LICENSE.md README.md NOTICE.md
