FROM quay.io/pypa/manylinux_2_28_x86_64
COPY lxml-7.0.0a0-cp314-cp314-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl /tmp/lxml-7.0.0a0-cp314-cp314-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl
COPY lxml-7.0.0a0-cp314-cp314t-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl /tmp/lxml-7.0.0a0-cp314-cp314t-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl
RUN python3.14t -m pip install /tmp/lxml-7.0.0a0-cp314-cp314t-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl
RUN python3.14 -m pip install /tmp/lxml-7.0.0a0-cp314-cp314-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl
RUN python3.13 -m pip install lxml

