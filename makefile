# default python executable, used until virtualenv has been setup
SYSPY := $(if ${SYSPY},${SYSPY},python)
# virtualenv python executable, used after virtualenv has been setup
ENVPY := env/bin/python
PKG := pytgen

TXIFC := pytgen-vtx
RXIFC := pytgen-vrx

setup:
	${SYSPY} -m pip install --upgrade pip
	${SYSPY} -m pip install --upgrade virtualenv
	${SYSPY} -m virtualenv env

init:
	${ENVPY} -m pip install -r requirements.txt

lint:
	${ENVPY} -m black --line-length 79 ${PKG} tests setup.py
	${ENVPY} -m pytype ${PKG} setup.py
	${ENVPY} -m flake8 ${PKG} tests setup.py

test:
	${ENVPY} -m pytest -sv

dist: clean
	${ENVPY} setup.py sdist bdist_wheel
	ls -lht dist

install: dist
	${ENVPY} -m pip install --upgrade --force-reinstall dist/*.whl

release:
	${ENVPY} -m pip install --upgrade twine
	${ENVPY} -m twine upload -u ${TWINE_USERNAME} -p ${TWINE_PASSWORD} dist/*

clean:
	rm -rf dist build *.egg-info .pytype
	find . -type d -name ".pytest_cache" | xargs rm -rf
	find . -type d -name "__pycache__" | xargs rm -rf
	find . -type f -name "*.pyc" | xargs rm -rf

ifc:
	ip link show ${TXIFC} 2> /dev/null || ( \
		ip link add dev ${TXIFC} type veth peer name ${RXIFC} \
		&& ip link set dev ${TXIFC} up \
		&& ip link set dev ${RXIFC} up \
		&& ip link show ${TXIFC} \
		&& ip link show ${RXIFC} \
	)

rmifc:
	ip link delete ${TXIFC}

version:
	@grep "version =" setup.py | cut -d\" -f 2

.PHONY: setup init install lint test dist release clean version ifc rmifc
