PY_BLEND=/tmp/blender-2.77-linux-glibc211-x86_64/2.77/python/
cp -a /usr/lib/python3.4/distutils ${PY_BLEND}/lib/python3.5/ # idem

wget https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py
PYTHON=${PY_BLEND}/bin/python3.5m # changer selon la version de blender...
${PYTHON} /tmp/get-pip.py --user --isolated

${PYTHON} -m pip install shapely pillow --isolated --user
