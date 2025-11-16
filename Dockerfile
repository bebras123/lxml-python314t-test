FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    gcc build-essential libxml2-dev libxslt-dev zlib1g-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:${PATH}"

RUN uv python install 3.12
RUN uv python install 3.13
RUN uv python install 3.14
RUN uv python install 3.14t

# Create venvs
RUN uv venv /root/envs/py312 --python 3.12
RUN uv venv /root/envs/py313 --python 3.13
RUN uv venv /root/envs/py314 --python 3.14
RUN uv venv /root/envs/py314t --python 3.14t

RUN /root/envs/py312/bin/python -m ensurepip --upgrade
RUN /root/envs/py313/bin/python -m ensurepip --upgrade
RUN /root/envs/py314/bin/python -m ensurepip --upgrade
RUN /root/envs/py314t/bin/python -m ensurepip --upgrade

RUN uv run --python /root/envs/py312/bin/python -m pip install "lxml" "Cython>=3.2.0" "setuptools"
RUN uv run --python /root/envs/py313/bin/python -m pip install "lxml" "Cython>=3.2.0" "setuptools"
RUN uv run --python /root/envs/py314/bin/python -m pip install "lxml" "Cython>=3.2.0" "setuptools"
RUN uv run --python /root/envs/py314t/bin/python -m pip install "Cython>=3.2.0" "setuptools"


# Add aliases
RUN echo 'alias py312="source /root/envs/py312/bin/activate"'  >> /etc/bash.bashrc && \
    echo 'alias py313="source /root/envs/py313/bin/activate"'  >> /etc/bash.bashrc && \
    echo 'alias py314="source /root/envs/py314/bin/activate"'  >> /etc/bash.bashrc && \
    echo 'alias py314t="source /root/envs/py314t/bin/activate"' >> /etc/bash.bashrc


