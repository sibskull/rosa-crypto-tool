Name:           rosa-crypto-tool
Version:        0.0.8
Release:        alt1
Summary:        Program for working with electronic digital signatures

Group:          Text tools
License:        BSD
URL:            https://abf.io/uxteam/rosa-crypto-tool-devel.git
Source0:        %name-%version.tar

BuildArch:      noarch
BuildRequires(pre): rpm-build-python
BuildRequires:  python-devel
BuildRequires:  python-module-distribute

%description
Program for working with electronic digital signatures.

%prep
%setup -q

%build
%python_build

%install
%python_install
%find_lang %name

%files -f %name.lang
%doc %_defaultdocdir/%name/help.pdf
%python_sitelibdir/*
%_iconsdir/hicolor/48x48/apps/%name.svg

%changelog
* Sun Aug 14 2016 Andrey Cherepanov <cas@altlinux.org> 0.0.8-alt1
- Initial build in Sisyphus

