# Setup Notes for PyMC3



I think pymc3 needs python 3.6, the linear regression example failed on python 3.5.2 (see https://github.com/pymc-devs/pymc3/issues/2771)

I'm tryting to use pyenv to put python 3.6 on ubuntu 16.04. However, `import theano` fails. I think I need to build cpython with --enable-shared to resolve this, see https://github.com/pyenv/pyenv-installer/issues/56. This worked :). The approach I used was

Install pyenv.

Build cpython 3.6 with shared library:
```bash
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.6.5
pyenv global 3.6.5
```

Install PyMC3, see http://docs.pymc.io/notebooks/getting_started.html#Installation:
```bash
pip install pymc3
```

Another error: https://github.com/pymc-devs/pymc3/issues/3068, fixing by installing latest pymc3 from master using `pip install -U git+https://github.com/pymc-devs/pymc3.git`.