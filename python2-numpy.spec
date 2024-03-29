#uncomment next line for a release candidate or a beta
#%%global relc rc1

%global modname numpy

%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
%global blaslib flexiblas
%global blasvar %{nil}
%else
%global blaslib openblas
%global blasvar p
%endif

Name:           python2-numpy
Version:        1.16.6
Release:        8%{?dist}
Epoch:          1
Summary:        A fast multidimensional array facility for Python 2

# Everything is BSD except for class SafeEval in numpy/lib/utils.py which is Python
License:        BSD and Python
URL:            http://www.numpy.org/
Source0:        https://github.com/%{modname}/%{modname}/releases/download/v%{version}/%{modname}-%{version}.tar.gz

BuildRequires:  python2.7 python2-setuptools gcc-gfortran gcc
BuildRequires:  Cython
BuildRequires: %{blaslib}-devel
%{?python_provide:%python_provide python2-%{modname}}
Provides:       libnpymath-static = %{epoch}:%{version}-%{release}
Provides:       libnpymath-static%{?_isa} = %{epoch}:%{version}-%{release}

%description
NumPy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays.  NumPy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type.

There are also basic facilities for discrete fourier transform,
basic linear algebra and random number generation. Also included in
this package is a version of f2py that works properly with NumPy.


%package -n python2-numpy-f2py
Summary:        f2py for numpy
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
%{?python_provide:%python_provide python2-numpy-f2py}


%description -n python2-numpy-f2py
This package includes a version of f2py that works properly with NumPy.


%prep
%autosetup -n %{modname}-%{version}%{?relc} -p1

# Force re-cythonization (ifed for PKG-INFO presence in setup.py)
rm PKG-INFO

# openblas is provided by flexiblas by default; otherwise,
# Use openblas pthreads as recommended by upstream (see comment in site.cfg.example)
cat >> site.cfg <<EOF
[openblas]
libraries = %{blaslib}%{blasvar}
library_dirs = %{_libdir}
EOF

%build
%set_build_flags

env OPENBLAS=%{_libdir} \
    BLAS=%{_libdir} \
    LAPACK=%{_libdir} CFLAGS="%{optflags}" \
    %{__python2} setup.py build

%install

#%%{__python2} setup.py install -O1 --skip-build --root %%{buildroot}
# skip-build currently broken, this works around it for now
env OPENBLAS=%{_libdir} \
    FFTW=%{_libdir} BLAS=%{_libdir} \
    LAPACK=%{_libdir} CFLAGS="%{optflags}" \
    %{__python2} setup.py install --root %{buildroot}
pushd %{buildroot}%{_bindir} &> /dev/null
rm -f %{buildroot}%{_bindir}/f2py
popd &> /dev/null

%files -n python2-numpy
%license LICENSE.txt
%doc THANKS.txt site.cfg.example
%dir %{python2_sitearch}/%{modname}
%{python2_sitearch}/%{modname}/*.py*
%{python2_sitearch}/%{modname}/core
%{python2_sitearch}/%{modname}/distutils
%{python2_sitearch}/%{modname}/doc
%{python2_sitearch}/%{modname}/fft
%{python2_sitearch}/%{modname}/lib
%{python2_sitearch}/%{modname}/linalg
%{python2_sitearch}/%{modname}/ma
%{python2_sitearch}/%{modname}/random
%{python2_sitearch}/%{modname}/testing
%{python2_sitearch}/%{modname}/tests
%{python2_sitearch}/%{modname}/compat
%{python2_sitearch}/%{modname}/matrixlib
%{python2_sitearch}/%{modname}/polynomial
%{python2_sitearch}/%{modname}-*.egg-info
%exclude %{python2_sitearch}/%{modname}/LICENSE.txt

%files -n python2-numpy-f2py
%{_bindir}/f2py2
%{_bindir}/f2py%{python2_version}
%{python2_sitearch}/%{modname}/f2py



%changelog

* Sat Apr 30 2022 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.6-8
- Updated to 1.16.6

* Fri Aug 21 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1:1.16.4-10
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.16.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Gwyn Ciesla <gwync@protonmail.com> - 1:1.16.4-8
- Move old numpy provides to python3-numpy.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.16.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 07 2019 Gwyn Ciesla <gwync@protonmail.com> - 1:1.16.4-6
- Drop tests and their BRs.

* Sat Aug 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1:1.16.4-5
- Reintroduce libnpymath.a

* Tue Jul 30 2019 Gwyn Ciesla <gwync@protonmail.com> - 1:1.16.4-4
- Split out from main numpy SRPM.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.16.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 20 2019 Kalev Lember <klember@redhat.com> - 1:1.16.4-2
- Avoid hardcoding /usr prefix

* Tue May 28 2019 Gwyn Ciesla <gwync@protonmail.com> - 1:1.16.4-1
- 1.16.4

* Thu May 16 2019 Orion Poplawski <orion@nwra.com> - 1:1.16.3-2
- Build only with openblasp (bugz#1709161)

* Mon Apr 22 2019 Gwyn Ciesla <gwync@protonmail.com> - 1:1.16.3-1
- 1.16.3.

* Tue Feb 26 2019 Gwyn Ciesla <gwync@protonmail.com> - 1:1.16.2-1
- 1.16.2.

* Fri Feb 01 2019 Gwyn Ciesla <limburgher@gmail.com> - 1:1.16.1-1
- 1.16.1.

* Tue Jan 22 2019 Gwyn Ciesla <limburgher@gmail.com> - 1:1.16.0-1
- 1.16.0.

* Wed Aug 29 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1:1.15.1-2
- Switch to pytest for running tests during check
- Stop ignoring failures when running tests
- Set PATH in check so that f2py tests work
- Update docs to match release
- Remove outdated workaround from rhbz#849713

* Wed Aug 22 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1:1.15.1-1
- Update to latest version

* Sat Aug 11 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1:1.15.0-2
- Fix broken build on s390x
- Remove bytecode produced by pytest
- Re-enable tests on s390x

* Tue Jul 24 2018 Gwyn Ciesla <limburgher@gmail.com> - 1:1.15.0-1
- 1.15.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.14.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1:1.14.5-2
- Rebuilt for Python 3.7

* Wed Jun 13 2018 Gwyn Ciesla <limburgher@gmail.com> - 1:1.14.5-1
- 1.14.5

* Tue May 01 2018 Gwyn Ciesla <limburgher@gmail.com> - 1:1.14.3-1
- 1.14.3

* Mon Mar 12 2018 Gwyn Ciesla <limburgher@gmail.com> - 1:1.14.2-1
- 1.14.2

* Wed Feb 21 2018 Gwyn Ciesla <limburgher@gmail.com> - 1:1.14.1-1
- 1.14.1

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.14.0-0.rc1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 13 2017 Gwyn Ciesla <limburgher@gmail.com> - 1:1.14.0-0.rc1
- 1.14.0 rc1

* Mon Dec 11 2017 Iryna Shcherbina <ishcherb@redhat.com> - 1:1.13.3-5
- Fix ambiguous Python 2 dependency declarations
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Nov 16 2017 Gwyn Ciesla <limburgher@gmail.com> - 1:1.13.3-4
- Split out doc subpackage.

* Mon Nov 06 2017 Merlin Mathesius <mmathesi@redhat.com> - 1:1.13.3-3
- Cleanup spec file conditionals

* Tue Oct 31 2017 Christian Dersch <lupinix@mailbox.org> - 1:1.13.3-2
- set proper environment variables for openblas

* Wed Oct 04 2017 Gwyn Ciesla <limburgher@gmail.com> - 1:1.13.3-1
- 1.13.3

* Thu Sep 28 2017 Gwyn Ciesla <limburgher@gmail.com> - 1:1.13.2-1
- 1.13.2

* Tue Aug 08 2017 Gwyn Ciesla <limburgher@gmail.com> - 1:1.13.1-4
- Use openblas where available, BZ 1472318.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Gwyn Ciesla <limburgher@gmail.com> - 1:1.13.1-1
- 1.13.1 final

* Fri Jun 09 2017 Gwyn Ciesla <limburgher@gmail.com> - 1:1.13.0-1
- 1.13.0 final

* Fri May 19 2017 Gwyn Ciesla <limburgher@gmail.com> - 1:1.13.0-0.rc2
- 1.13.0 rc2

* Thu May 11 2017 Gwyn Ciesla <limburgher@gmail.com> - 1:1.13.0-0.rc1
- 1.13.0 rc1

* Wed Mar 29 2017 Gwyn Ciesla <limburgher@gmail.com> - 1:1.12.1-1
- 1.12.1

* Tue Jan 31 2017 Simone Caronni <negativo17@gmail.com> - 1:1.12.0-1
- Update to 1.12.0, build with gcc 7.0.

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 1:1.11.2-2
- Rebuild for Python 3.6

* Mon Oct 3 2016 Orion Poplawski <orion@cora.nwra.com> - 1:1.11.2-1
- Update to 1.11.2 final

* Thu Sep 15 2016 Jon Ciesla <limburgher@gmail.com> - 1:1.11.2-0.rc1
- Update to 1.11.2rc1, BZ 1340440.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.11.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jun 28 2016 Orion Poplawski <orion@cora.nwra.com> - 1:1.11.1-1
- Update to 1.11.1 final

* Tue Jun 07 2016 Jon Ciesla <limburgher@gmail.com> - 1:1.11.1-0.rc1
- Update to 1.11.1rc1, BZ 1340440.

* Mon Mar 28 2016 Orion Poplawski <orion@cora.nwra.com> - 1:1.11.0-4
- Update to 1.11.0 final

* Wed Mar 23 2016 Orion Poplawski <orion@cora.nwra.com> - 1:1.11.0-3.rc2
- Update to 1.11.0rc2

* Sun Mar  6 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1:1.11.0-2.b3
- Bump Release. 1b2 is higher than 0b3

* Wed Feb 10 2016 Jon Ciesla <limburgher@gmail.com> - 1:1.11.0-0.b3
- Update to 1.11.0b2, BZ 1306249.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.11.0-1b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 31 2016 Jon Ciesla <limburgher@gmail.com> - 1:1.11.0-0.b2
- Update to 1.11.0b2, BZ 1303387.

* Tue Jan 26 2016 Jon Ciesla <limburgher@gmail.com> - 1:1.11.0-020161016.cc2b04git
- Update to git snapshot (due to build issue) after 1.11.0b1, BZ 1301943.

* Thu Jan 07 2016 Jon Ciesla <limburgher@gmail.com> - 1:1.10.4-1
- Update to 1.10.4, BZ 1296509.

* Tue Dec 15 2015 Jon Ciesla <limburgher@gmail.com> - 1:1.10.2-1
- Update to 1.10.2, BZ 1291674.

* Tue Dec 08 2015 Jon Ciesla <limburgher@gmail.com> - 1:1.10.2-0.2.rc2
- Update to 1.10.2rc1, BZ 1289550.

* Fri Nov 13 2015 Orion Poplawski <orion@cora.nwra.com> - 1:1.10.2-0.1.rc1
- Update to 1.10.2rc1
- Drop opt-flags patch applied upstream

* Fri Nov 13 2015 Kalev Lember <klember@redhat.com> - 1:1.10.1-6
- Add provides to satisfy numpy%%{_isa} requires in other packages

* Thu Nov 12 2015 Orion Poplawski <orion@nwra.com> - 1:1.10.1-5
- Re-add provides f2py

* Thu Nov 12 2015 Kalev Lember <klember@redhat.com> - 1:1.10.1-4
- Fix obsoletes / provides for numpy -> python2-numpy rename

* Wed Oct 14 2015 Thomas Spura <tomspur@fedoraproject.org> - 1:1.10.1-3
- Remove fortran flags or arm would build with -march=x86-64

* Wed Oct 14 2015 Thomas Spura <tomspur@fedoraproject.org> - 1:1.10.1-2
- Provide python2-* packages
- Run tests with verbose=2

* Tue Oct 13 2015 Jon Ciesla <limburgher@gmail.com> - 1:1.10.1-1
- Update to 1.10.1, BZ 1271022.

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.com> - 1:1.10.0-2
- Rebuilt for Python3.5 rebuild

* Tue Oct 06 2015 Jon Ciesla <limburgher@gmail.com> - 1:1.10.0-1
- Update to 1.10.0 final.

* Wed Sep 02 2015 Jon Ciesla <limburgher@gmail.com> - 1:1.10.0-0.b1
- Update to 1.10.0b1, BZ 1252641.

* Thu Aug 13 2015 Orion Poplawski <orion@nwra.com> - 1:1.9.2-3
- Add python2-numpy provides (bug #1249423)
- Spec cleanup

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 1 2015 Orion Poplawski <orion@nwra.com> - 1:1.9.2-1
- Update to 1.9.2

* Tue Jan 6 2015 Orion Poplawski <orion@nwra.com> - 1:1.9.1-2
- Add upstream patch to fix xerbla linkage (bug #1172834)

* Tue Nov 04 2014 Jon Ciesla <limburgher@gmail.com> - 1:1.9.1-1
- Update to 1.9.1, BZ 1160273.

* Sun Sep 7 2014 Orion Poplawski <orion@nwra.com> - 1:1.9.0-1
- Update to 1.9.0

* Wed Aug 27 2014 Orion Poplawski <orion@nwra.com> - 1:1.9.0-0.1.rc1
- Update to 1.9.0rc1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Aug 10 2014 Orion Poplawski <orion@nwra.com> - 1:1.8.2-1
- Update to 1.8.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 9 2014 Orion Poplawski <orion@nwra.com> - 1:1.8.1-3
- Rebuild for Python 3.4

* Wed May 07 2014 Jaromir Capik <jcapik@redhat.com> - 1:1.8.1-2
- Fixing FTBFS on ppc64le (#1078354)

* Tue Mar 25 2014 Orion Poplawski <orion@nwra.com> - 1:1.8.1-1
- Update to 1.8.1

* Tue Mar 4 2014 Orion Poplawski <orion@nwra.com> - 1:1.8.0-5
- Fix __pycache__ ownership (bug #1072467)

* Mon Feb 10 2014 Thomas Spura <tomspur@fedoraproject.org> - 1:1.8.0-4
- Fix CVE-2014-1858, CVE-2014-1859: #1062009, #1062359

* Mon Nov 25 2013 Orion Poplawski <orion@nwra.com> - 1:1.8.0-3
- Ship doc module (bug #1034357)

* Wed Nov 6 2013 Orion Poplawski <orion@nwra.com> - 1:1.8.0-2
- Move f2py documentation to f2py package (bug #1027394)

* Wed Oct 30 2013 Orion Poplawski <orion@nwra.com> - 1:1.8.0-1
- Update to 1.8.0 final

* Mon Oct 14 2013 Orion Poplawski <orion@nwra.com> - 1:1.8.0-0.7.rc2
- Update to 1.8.0rc2
- Create clean site.cfg
- Use serial atlas

* Mon Sep 23 2013 Orion Poplawski <orion@nwra.com> - 1:1.8.0-0.6.b2
- Add [atlas] to site.cfg for new atlas library names

* Sun Sep 22 2013 Orion Poplawski <orion@nwra.com> - 1:1.8.0-0.5.b2
- Update site.cfg for new atlas library names

* Sat Sep 21 2013 David Tardon <dtardon@redhat.com> - 1:1.8.0-0.4.b2
- rebuild for atlas 3.10

* Tue Sep 10 2013 Jon Ciesla <limburgher@gmail.com> - 1:1.8.0-0.3.b2
- Fix libdir path in site.cfg, BZ 1006242.

* Sun Sep 8 2013 Orion Poplawski <orion@nwra.com> - 1:1.8.0-0.2.b2
- Update to 1.8.0b2

* Wed Sep 4 2013 Orion Poplawski <orion@nwra.com> - 1:1.8.0-0.1.b1
- Update to 1.8.0b1
- Drop f2py patch applied upstream

* Tue Aug 27 2013 Jon Ciesla <limburgher@gmail.com> - 1:1.7.1-5
- URL Fix, BZ 1001337

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Tomas Tomecek <ttomecek@redhat.com> - 1:1.7.1-3
- Fix rpmlint warnings
- Update License
- Apply patch: change shebang of f2py to use binary directly

* Sun Jun 2 2013 Orion Poplawski <orion@nwra.com> - 1:1.7.1-2
- Specfile cleanup (bug #969854)

* Wed Apr 10 2013 Orion Poplawski <orion@nwra.com> - 1:1.7.1-1
- Update to 1.7.1

* Sat Feb 9 2013 Orion Poplawski <orion@nwra.com> - 1:1.7.0-1
- Update to 1.7.0 final

* Sun Dec 30 2012 Orion Poplawski <orion@nwra.com> - 1:1.7.0-0.5.rc1
- Update to 1.7.0rc1

* Thu Sep 20 2012 Orion Poplawski <orion@nwra.com> - 1:1.7.0-0.4.b2
- Update to 1.7.0b2
- Drop patches applied upstream

* Wed Aug 22 2012 Orion Poplawski <orion@nwra.com> - 1:1.7.0-0.3.b1
- Add patch from github pull 371 to fix python 3.3 pickle issue
- Remove cython .c source regeneration - fails now

* Wed Aug 22 2012 Orion Poplawski <orion@nwra.com> - 1:1.7.0-0.2.b1
- add workaround for rhbz#849713 (fixes FTBFS)

* Tue Aug 21 2012 Orion Poplawski <orion@cora.nwra.com> - 1:1.7.0-0.1.b1
- Update to 1.7.0b1
- Rebase python 3.3 patchs to current git master
- Drop patches applied upstream

* Sun Aug  5 2012 David Malcolm <dmalcolm@redhat.com> - 1:1.6.2-5
- rework patches for 3.3 to more directly reflect upstream's commits
- re-enable test suite on python 3
- forcibly regenerate Cython .c source to avoid import issues on Python 3.3

* Sun Aug  5 2012 Thomas Spura <tomspur@fedoraproject.org> - 1:1.6.2-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3
- needs unicode patch

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 1:1.6.2-3
- remove rhel logic from with_python3 conditional

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 20 2012 Orion Poplawski <orion@cora.nwra.com> - 1:1.6.2-1
- Update to 1.6.2 final

* Sat May 12 2012 Orion Poplawski <orion@cora.nwra.com> - 1:1.6.2rc1-0.1
- Update to 1.6.2rc1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 7 2011 Orion Poplawski <orion@cora.nwra.com> - 1:1.6.1-1
- Update to 1.6.1

* Fri Jun 17 2011 Jon Ciesla <limb@jcomserv.net> - 1:1.6.0-2
- Bump and rebuild for BZ 712251.

* Mon May 16 2011 Orion Poplawski <orion@cora.nwra.com> - 1:1.6.0-1
- Update to 1.6.0 final

* Mon Apr 4 2011 Orion Poplawski <orion@cora.nwra.com> - 1:1.6.0-0.2.b2
- Update to 1.6.0b2
- Drop import patch fixed upstream

* Thu Mar 31 2011 Orion Poplawski <orion@cora.nwra.com> - 1:1.6.0-0.1.b1
- Update to 1.6.0b1
- Build python3  module with python3
- Add patch from upstream to fix build time import error

* Wed Mar 30 2011 Orion Poplawski <orion@cora.nwra.com> - 1:1.5.1-1
- Update to 1.5.1 final

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5.1-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Dan Horák <dan[at]danny.cz> - 1:1.5.1-0.3
- fix the AttributeError during tests
- fix build on s390(x)

* Wed Dec 29 2010 David Malcolm <dmalcolm@redhat.com> - 1:1.5.1-0.2
- rebuild for newer python3

* Wed Oct 27 2010 Thomas Spura <tomspur@fedoraproject.org> - 1:1.5.1-0.1
- update to 1.5.1rc1
- add python3 subpackage
- some spec-cleanups

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1:1.4.1-6
- actually add the patch this time

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1:1.4.1-5
- fix segfault within %%check on 2.7 (patch 2)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1:1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 18 2010 Dan Horák <dan[at]danny.cz> 1.4.1-3
- ignore the "Ticket #1299 second test" failure on s390(x)

* Thu Jun 24 2010 Jef Spaleta <jspaleta@fedoraprject.org> 1.4.1-2
- source commit fix

* Thu Jun 24 2010 Jef Spaleta <jspaleta@fedoraprject.org> 1.4.1-1
- New upstream release. Include backported doublefree patch

* Mon Apr 26 2010 Jon Ciesla <limb@jcomserv.net> 1.3.0-8
- Moved distutils back to the main package, BZ 572820.

* Thu Apr 08 2010 Jon Ciesla <limb@jcomserv.net> 1.3.0-7
- Reverted to 1.3.0 after upstream pulled 1.4.0, BZ 579065.

* Tue Mar 02 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-5
- Linking /usr/include/numpy to .h files, BZ 185079.

* Tue Feb 16 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-4
- Re-enabling atlas BR, dropping lapack Requires.

* Wed Feb 10 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-3
- Since the previous didn't work, Requiring lapack.

* Tue Feb 09 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-2
- Temporarily dropping atlas BR to work around 562577.

* Fri Jan 22 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-1
- 1.4.0.
- Dropped ARM patch, ARM support added upstream.

* Tue Nov 17 2009 Jitesh Shah <jiteshs@marvell.com> - 1.3.0-6.fa1
- Add ARM support

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-5
- Fixed atlas BR, BZ 505376.

* Fri Apr 17 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-4
- EVR bump for pygame chainbuild.

* Fri Apr 17 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-3
- Moved linalg, fft back to main package.

* Tue Apr 14 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-2
- Split out f2py into subpackage, thanks Peter Robinson pbrobinson@gmail.com.

* Tue Apr 07 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-1
- Update to latest upstream.
- Fixed Source0 URL.

* Thu Apr 02 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-0.rc1
- Update to latest upstream.

* Thu Mar 05 2009 Jon Ciesla <limb@jcomserv.net> 1.2.1-3
- Require python-devel, BZ 488464.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 19 2008 Jon Ciesla <limb@jcomserv.net> 1.2.1-1
- Update to 1.2.1.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.2.0-2
- Rebuild for Python 2.6

* Tue Oct 07 2008 Jon Ciesla <limb@jcomserv.net> 1.2.0-1
- New upstream release, added python-nose BR. BZ 465999.
- Using atlas blas, not blas-devel. BZ 461472.

* Wed Aug 06 2008 Jon Ciesla <limb@jcomserv.net> 1.1.1-1
- New upstream release

* Thu May 29 2008 Jarod Wilson <jwilson@redhat.com> 1.1.0-1
- New upstream release

* Tue May 06 2008 Jarod Wilson <jwilson@redhat.com> 1.0.4-1
- New upstream release

* Mon Feb 11 2008 Jarod Wilson <jwilson@redhat.com> 1.0.3.1-2
- Add python egg to %%files on f9+

* Wed Aug 22 2007 Jarod Wilson <jwilson@redhat.com> 1.0.3.1-1
- New upstream release

* Wed Jun 06 2007 Jarod Wilson <jwilson@redhat.com> 1.0.3-1
- New upstream release

* Mon May 14 2007 Jarod Wilson <jwilson@redhat.com> 1.0.2-2
- Drop BR: atlas-devel, since it just provides binary-compat
  blas and lapack libs. Atlas can still be optionally used
  at runtime. (Note: this is all per the atlas maintainer).

* Mon May 14 2007 Jarod Wilson <jwilson@redhat.com> 1.0.2-1
- New upstream release

* Tue Apr 17 2007 Jarod Wilson <jwilson@redhat.com> 1.0.1-4
- Update gfortran patch to recognize latest gfortran f95 support
- Resolves rhbz#236444

* Fri Feb 23 2007 Jarod Wilson <jwilson@redhat.com> 1.0.1-3
- Fix up cpuinfo bug (#229753). Upstream bug/change:
  http://projects.scipy.org/scipy/scipy/ticket/349

* Thu Jan 04 2007 Jarod Wilson <jwilson@redhat.com> 1.0.1-2
- Per discussion w/Jose Matos, Obsolete/Provide f2py, as the
  stand-alone one is no longer supported/maintained upstream

* Wed Dec 13 2006 Jarod Wilson <jwilson@redhat.com> 1.0.1-1
- New upstream release

* Tue Dec 12 2006 Jarod Wilson <jwilson@redhat.com> 1.0-2
- Rebuild for python 2.5

* Wed Oct 25 2006 Jarod Wilson <jwilson@redhat.com> 1.0-1
- New upstream release

* Wed Sep 06 2006 Jarod Wilson <jwilson@redhat.com> 0.9.8-1
- New upstream release

* Wed Apr 26 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.6-1
- Upstream update

* Thu Feb 16 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.5-1
- Upstream update

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.4-2
- Rebuild for Fedora Extras 5

* Thu Feb  2 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.4-1
- Initial RPM release
- Added gfortran patch from Neal Becker
