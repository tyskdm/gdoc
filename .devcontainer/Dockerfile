FROM python:3.8

RUN apt-get update && apt-get upgrade -y
ENV DEBCONF_NOWARNINGS=yes

RUN /usr/local/bin/python -m pip install --upgrade pip

# poetry
RUN set -x && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

ENV PATH /root/.poetry/bin:$PATH
RUN poetry config virtualenvs.create false

# pandoc
RUN curl -sSLO https://github.com/jgm/pandoc/releases/download/2.14.2/pandoc-2.14.2-1-amd64.deb && \
    dpkg -i pandoc-2.14.2-1-amd64.deb && \
    rm pandoc-2.14.2-1-amd64.deb

# doxygen
RUN apt-get install -y doxygen graphviz

# PlantUML
RUN apt-get install -y default-jre graphviz fonts-migmix
# In addtion,
# 1. download plantuml.jar into here from `https://plantuml.com/download`.
# 2. add execution path to `./plantuml`.
#    For this, run `./postCreateCommand` inside container.
#
# Some other japanese-fonts are:
# fonts-ipafont fonts-takao-mincho fonts-takao-gothic fonts-migmix fonts-noto-cjk

# Copy your own .bashrc to home dir of root.
# Comment it out if you don't need it.
COPY .devcontainer/.bashrc /root/
