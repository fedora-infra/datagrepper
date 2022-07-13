# https://bugzilla.redhat.com/show_bug.cgi?id=955781
%global pypi_name datagrepper
%global pypi_version 1.0.1

Name:           %{pypi_name}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        A webapp to query fedmsg history

License:        GPLv2+
URL:            https://github.com/fedora-infra/datagrepper
Source0:        %{pypi_source}

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  python3-devel
BuildRequires:  python3-fedmsg-core
BuildRequires:  python3-fedmsg-meta-fedora-infrastructure
BuildRequires:  python3-flask-sqlalchemy
BuildRequires:  python3-freezegun
BuildRequires:  python3-mock
BuildRequires:  python3-nose
BuildRequires:  python3-pygal
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx

%description
A webapp to retrieve historical information about messages on the fedmsg
bus.  It is a JSON api for the datanommer message store.

%prep
%autosetup
# makes build_sphinx find it
# cannot move, we need to keep sources there, as they are used on runtime
cp -a %{pypi_name}/docs .

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel
make %{?_smp_mflags} -C %{pypi_name}/docs html

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

mkdir -p %{buildroot}%{_libexecdir}/%{pypi_name}
install -m 644 apache/%{pypi_name}.wsgi %{buildroot}%{_libexecdir}/%{pypi_name}/%{pypi_name}.wsgi

mkdir -p %{buildroot}%{_sysconfdir}/%{pypi_name}/
install -m 644 apache/%{pypi_name}.cfg %{buildroot}%{_sysconfdir}/%{pypi_name}/%{pypi_name}.cfg

%check
%pyproject_check_import
%{pytest} -v

%files -n %{pypi_name} -f %{pyproject_files}
%doc README.md %{pypi_name}/docs/_build/html/ apache/%{pypi_name}.conf
%license COPYING
%config(noreplace) %{_sysconfdir}/%{pypi_name}/
%{_libexecdir}/%{pypi_name}/%{pypi_name}.wsgi

%changelog
* Fri May 13 2022 Lenka Segura <lsegura@redhat.com> - 1.0.0-1
- new version

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.9.7-3
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 22 2020 Ralph Bean <rbean@redhat.com> - 0.9.7-1
- new version

* Wed Aug 12 2020 Ralph Bean <rbean@redhat.com> - 0.9.6-1
- Latest upstream

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.9.5-9
- Rebuilt for Python 3.9

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 02 2019 Kevin Fenzi <kevin@scrye.com> - 0.9.5-7
- Add patch to fix tests.

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.5-6
- Rebuilt for Python 3.8

* Fri Aug 02 2019 Lukas Slebodnik <lslebodn@fedoraproject.org> - 0.9.5-5
- Fix start with delta parameter
- backport of upstream fix https://github.com/fedora-infra/datagrepper/issues/218

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.5-3
- Switch to Python 3 (#1677977)
- Build the docs
- Use automatic dependencies

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 14 2018 Ralph Bean <rbean@redhat.com> - 0.9.5-1
- new version

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 18 2018 Ralph Bean <rbean@redhat.com> - 0.9.4-1
- new version

* Mon Mar 12 2018 Ralph Bean <rbean@redhat.com> - 0.9.3-1
- new version

* Thu Feb 22 2018 Ralph Bean <rbean@redhat.com> - 0.9.1-2
- Conditionals for dependencies.

* Wed Feb 21 2018 Ralph Bean <rbean@redhat.com> - 0.9.1-1
- new version

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 22 2017 Ralph Bean <rbean@redhat.com> - 0.8.0-1
- new version

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 08 2015 Ralph Bean <rbean@redhat.com> - 0.7.1-1
- new version

* Thu Oct 08 2015 Ralph Bean <rbean@redhat.com> - 0.7.0-1
- new version

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 24 2015 Ralph Bean <rbean@redhat.com> - 0.6.0-1
- new version
- Removed lots of no-longer-needed deps.

* Tue Sep 09 2014 Ralph Bean <rbean@redhat.com> - 0.5.1-1
- Hide charts from users.  They are too slow on the full dataset.

* Mon Sep 08 2014 Ralph Bean <rbean@redhat.com> - 0.5.0-1
- Latest upstream.
- New dep on python-pygal.

* Wed Aug 06 2014 Ralph Bean <rbean@redhat.com> - 0.4.2-1
- Latest bugfix release with css and javascript fixes.
- Remove patch.
- Fix rhel6 conditionals?

* Thu Jul 10 2014 Ralph Bean <rbean@redhat.com> - 0.4.1-4
- Bump release.

* Tue Jul 08 2014 Ralph Bean <rbean@redhat.com> - 0.4.1-3
- Fix rhel conditionals for rhel7.
- Patch out flask-sqlalchemy for rhel7.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 02 2014 Ralph Bean <rbean@redhat.com> - 0.4.1-1
- Websockets and autoscrolling.
- Remove pygments patch.

* Wed Mar 19 2014 Ralph Bean <rbean@redhat.com> - 0.4.0-3
- Start running the test suite.

* Tue Mar 04 2014 Ralph Bean <rbean@redhat.com> - 0.4.0-2
- Patch some pygments stuff to support el6.

* Tue Mar 04 2014 Ralph Bean <rbean@redhat.com> - 0.4.0-1
- Fix widget css
- Added an extra-large size for message cards
- Default order is descending now.

* Fri Feb 21 2014 Ralph Bean <rbean@redhat.com> - 0.3.3-1
- New /raw api option to query for an arbitrary string
- New /raw api option to query for negative filters.
- New /widget.js self-expanding javascript widget.

* Sun Feb 09 2014 Ralph Bean <rbean@redhat.com> - 0.3.2-1
- Cosmetic fixes.

* Sun Feb 09 2014 Ralph Bean <rbean@redhat.com> - 0.3.1-1
- Frontend and docs improvements by charulagrl.

* Fri Jan 10 2014 Ralph Bean <rbean@redhat.com> - 0.3.0-1
- Message counter on the frontpage.
- Introduction of the HTML cards work by charulagrl.

* Fri Sep 27 2013 Ian Weller <iweller@redhat.com> - 0.2.1-1
- Update to upstream 0.2.1

* Wed Sep 18 2013 Ian Weller <iweller@redhat.com> - 0.2.0-1
- Update to upstream 0.2.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 06 2013 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.1.4-3
- Backport patch from commit 2f8c98b in upstream repo

* Fri May 17 2013 Ralph Bean <rbean@redhat.com> - 0.1.4-2
- Apply temporary sed statement to fix datagrepper.wsgi.

* Fri May 17 2013 Ralph Bean <rbean@redhat.com> - 0.1.4-1
- Latest upstream.
- Ability to request an order for your results.
- Ability to request metadata to be sent along with your results.
- Ability to request the last N items regardless of time.

* Mon May 13 2013 Ralph Bean <rbean@redhat.com> - 0.1.3-2
- Apply a patch to fix a spelling typo in the main file.

* Mon May 13 2013 Ralph Bean <rbean@redhat.com> - 0.1.3-1
- Fix to configurable base url.
- Support old docutils and code-block directive.
- Support a callback querystring argument to allow JSONP responses.

* Fri May 10 2013 Ralph Bean <rbean@redhat.com> - 0.1.2-1
- Added configurable base_url for docs.
- Fix timedelta.total_seconds for python2.6.

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
