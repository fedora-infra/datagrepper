%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get _python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

%define modname datagrepper
%define eggname datagrepper

Name:           datagrepper
Version:        0.1
Release:        1%{?dist}
Summary:        A webapp to query fedmsg history

License:        GPLv2+
URL:            https://github.com/fedora-infra/datagrepper
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools

%if %{?rhel}%{!?rhel:0} >= 6
BuildRequires:  python-sqlalchemy0.7
%else
BuildRequires:  python-sqlalchemy
%endif

BuildRequires:  python-flask
BuildRequires:  python-flask-sqlalchemy
BuildRequires:  python-flask-wtf
BuildRequires:  python-kitchen
BuildRequires:  python-datanommer-models
BuildRequires:  python-docutils
BuildRequires:  fedmsg

## Not needed for testing only when working with postgresql
#BuildRequires:  python-psycopg2

%if %{?rhel}%{!?rhel:0} >= 6
Requires:  python-sqlalchemy0.7
%else
Requires:  python-sqlalchemy
%endif

Requires:  python-flask
Requires:  python-flask-sqlalchemy
Requires:  python-flask-wtf
Requires:  python-kitchen
Requires:  python-datanommer-models
Requires:  python-docutils
Requires:  fedmsg

# Needed!
Requires:  python-psycopg2

%description
A webapp to retrieve historical information about messages on the fedmsg
bus.  It is a JSON api for the datanommer message store.

%prep
%setup -q

%if %{?rhel}%{!?rhel:0} >= 6
# Make sure that epel/rhel picks up the correct version of webob
awk 'NR==1{print "import __main__; __main__.__requires__ = __requires__ = [\"sqlalchemy>=0.7\"]; import pkg_resources"}1' setup.py > setup.py.tmp
mv setup.py.tmp setup.py
%endif

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build \
    --install-data=%{_datadir} --root %{buildroot}

mkdir -p %{buildroot}%{_datadir}/%{modname}/apache
install apache/%{modname}.wsgi %{buildroot}%{_datadir}/%{modname}/apache/%{modname}.wsgi

mkdir -p %{buildroot}%{_sysconfdir}/%{modname}/
install apache/%{modname}.cfg %{buildroot}%{_sysconfdir}/%{modname}/%{modname}.cfg

%pre
%{_sbindir}/groupadd -r %{modname} &>/dev/null || :
%{_sbindir}/useradd  -r -s /sbin/nologin -d %{_datadir}/%{modname} -M \
              -c 'DataGrepper' -g %{modname} %{modname} &>/dev/null || :

%files
%doc README.rst
%config %{_sysconfdir}/%{modname}/
%{_datadir}/%{modname}/
%{python_sitelib}/%{modname}/
%{python_sitelib}/%{eggname}-%{version}-py%{pyver}.egg-info/

%changelog
* Tue Apr 23 2013 Ian Weller <iweller@redhat.com> - 0.1-1
- Bump version number to 0.1 (0.0.1 never happened)
- Remove system executable macros
- Fix install location of apache/datagrepper.cfg

* Mon Apr 22 2013 Ralph Bean <rbean@redhat.com> - 0.0.1-1
- Initial packaging.
