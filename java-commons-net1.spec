
%bcond_with		tests		# tests are broken. see note above.
%bcond_without	javadoc		# don't build javadoc

%include	/usr/lib/rpm/macros.java
%define		srcname	commons-net1
Summary:	Commons Net - utility functions and components
Summary(pl.UTF-8):	Commons Net - funkcje i komponenty narzędziowe
Name:		java-commons-net1
Version:	1.4.1
Release:	1
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://www.apache.org/dist/commons/net/source/commons-net-%{version}-src.tar.gz
# Source0-md5:	ccbb3f67b55e8a7a676499db4386673c
Patch0:		disable-tests.patch
URL:		http://commons.apache.org/net/
BuildRequires:	ant
%{?with_tests:BuildRequires:	ant-junit}
BuildRequires:	java-oro >= 2.0.8
BuildRequires:	jdk
BuildRequires:	jpackage-utils
%{?with_tests:BuildRequires:	junit}
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	java-oro >= 2.0.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Jakarta Commons Net is a set of utility functions and reusable
components that should be a help in any Java environment.

%description -l pl.UTF-8
Jakarta Commons Net to zestaw funkcji narzędziowych i komponentów
wielokrotnego użycia, które mogą być pomocne w każdym środowisku Javy.

%package javadoc
Summary:	Jakarta Commons Net documentation
Summary(pl.UTF-8):	Dokumentacja do Jakarta Commons Net
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Jakarta Commons Net documentation.

%description javadoc -l pl.UTF-8
Dokumentacja do Jakarta Commons Net.

%package examples
Summary:	Examples for Commons Net
Summary(pl.UTF-8):	Przykłady dla Commons Net
Group:		Documentation
Requires:	jpackage-utils

%description examples
Commons Net examples.

%description examples -l pl.UTF-8
Przykłady Commons Net.

%package sources
Summary:	Commons Net source code
Summary(pl.UTF-8):	Źródła Commons Net
Group:		Documentation
Requires:	jpackage-utils

%description sources
Commons Net source code.

%description sources -l pl.UTF-8
Kod źródłowy Commons Net.

%prep
%setup -q -n commons-net-%{version}

%patch0 -p0

%build

CLASSPATH=$(build-classpath oro)

%ant clean jar javadoc \
	-Dnoget=1 \
	-Dbuild.sysclasspath=first \
	-Dversion=%{version}

%if %{with tests}
CLASSPATH=$CLASSPATH:$(build-classpath junit)
%ant test \
	-Dnoget=1 \
	-Dbuild.sysclasspath=first \
	-Dversion=%{version}
%endif

%{jar} cf target/commons-net-1.4.1.src.jar -C src/java org

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_javadocdir}/%{srcname}-%{version},%{_examplesdir},%{_javasrcdir}}

install target/commons-net-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -sf %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

%if %{with javadoc}
cp -a dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

cp -a src/java/examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
install target/commons-net-%{version}.jar $RPM_BUILD_ROOT%{_javasrcdir}/%{srcname}.src.jar

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%files sources
%defattr(644,root,root,755)
%{_javasrcdir}/%{srcname}.src.jar
