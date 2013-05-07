# https://bugzilla.redhat.com/show_bug.cgi?id=955781

%define modname datagrepper
%define eggname datagrepper

Name:           datagrepper
Version:        0.1.1
Release:        2%{?dist}
Summary:        A webapp to query fedmsg history

License:        GPLv2+
URL:            https://github.com/fedora-infra/datagrepper
Source0:        https://pypi.python.org/packages/source/d/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
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
Requires:  python-datanommer-models >= 0.4.3
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

mkdir -p %{buildroot}%{_datadir}/%{modname}/apache/
install -m 644 apache/%{modname}.wsgi %{buildroot}%{_datadir}/%{modname}/apache/%{modname}.wsgi
install -m 644 apache/%{modname}.conf %{buildroot}%{_datadir}/%{modname}/apache/%{modname}.conf

mkdir -p %{buildroot}%{_sysconfdir}/%{modname}/
install -m 644 apache/%{modname}.cfg %{buildroot}%{_sysconfdir}/%{modname}/%{modname}.cfg

%files
%doc README.rst COPYING
%config(noreplace) %{_sysconfdir}/%{modname}/
%{_datadir}/%{modname}/
%{python_sitelib}/%{modname}/
%{python_sitelib}/%{eggname}-%{version}-py%{python_version}.egg-info/

%changelog
* Mon May 06 2013 Ian Weller <iweller@redhat.com> - 0.1.1-2
- Replace pyver macro definition with python_version

* Fri May 03 2013 Ian Weller <iweller@redhat.com> - 0.1.1-1
- Update to upstream 0.1.1 (adds license text)
- Fix python2-devel BR
- Mark config file as noreplace
- Remove useradd commands in post
- Install sample httpd configuration file
- Add version to requires on datanommer.models
- Remove python_sitelib macro definition
- Fix file permissions for config files

* Tue Apr 23 2013 Ian Weller <iweller@redhat.com> - 0.1-1
- Bump version number to 0.1 (0.0.1 never happened)
- Remove system executable macros
- Fix install location of apache/datagrepper.cfg

* Mon Apr 22 2013 Ralph Bean <rbean@redhat.com> - 0.0.1-1
- Initial packaging.
