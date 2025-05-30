#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-attrs.spec)

Summary:	attrs - classes without boilerplate
Summary(pl.UTF-8):	attrs - klasy bez ramowego kodu
Name:		python-attrs
# keep 21.x here for python2 support
Version:	21.4.0
Release:	5
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/attrs/
Source0:	https://files.pythonhosted.org/packages/source/a/attrs/attrs-%{version}.tar.gz
# Source0-md5:	5a9b5e9ceebc380a13fb93235b11bbda
Patch0:		attrs-intersphinx.patch
URL:		https://pypi.org/project/attrs/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-coverage
BuildRequires:	python-hypothesis
BuildRequires:	python-pympler
BuildRequires:	python-pytest >= 4.3.0
BuildRequires:	python-six
BuildRequires:	python-zope.interface
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-coverage
BuildRequires:	python3-hypothesis
BuildRequires:	python3-pympler
BuildRequires:	python3-pytest >= 4.3.0
BuildRequires:	python3-six
BuildRequires:	python3-zope.interface
%endif
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg-3
BuildRequires:	python3-furo
BuildRequires:	python3-sphinx-notfound-page
BuildRequires:	python3-zope.interface
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
attrs is the Python package that will bring back the joy of writing
classes by relieving you from the drudgery of implementing object
protocols (aka dunder methods).

%description -l pl.UTF-8
attrs to pakiet Pythona, mający przywrócić radość pisania klas
uwalniając od mordęgi implementowania protokołów obiektów (metod z
podwójnym podkreśleniem).

%package -n python3-attrs
Summary:	attrs - classes without boilerplate
Summary(pl.UTF-8):	attrs - klasy bez ramowego kodu
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-attrs
attrs is the Python package that will bring back the joy of writing
classes by relieving you from the drudgery of implementing object
protocols (aka dunder methods).

%description -n python3-attrs -l pl.UTF-8
attrs to pakiet Pythona, mający przywrócić radość pisania klas
uwalniając od mordęgi implementowania protokołów obiektów (metod z
podwójnym podkreśleniem).

%package apidocs
Summary:	API documentation for Python attrs module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona attrs
Group:		Documentation

%description apidocs
API documentation for Pythona attrs module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona attrs.

%prep
%setup -q -n attrs-%{version}
%patch -P0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG.rst LICENSE README.rst
%{py_sitescriptdir}/attr
%{py_sitescriptdir}/attrs
%{py_sitescriptdir}/attrs-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-attrs
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG.rst LICENSE README.rst
%{py3_sitescriptdir}/attr
%{py3_sitescriptdir}/attrs
%{py3_sitescriptdir}/attrs-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
