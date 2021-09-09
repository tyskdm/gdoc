FROM python:3.8

RUN apt update && apt upgrade -y

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN set -x && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

ENV PATH /root/.poetry/bin:$PATH
RUN poetry config virtualenvs.create false

RUN curl -sSLO https://github.com/jgm/pandoc/releases/download/2.14.2/pandoc-2.14.2-1-amd64.deb && \
    dpkg -i pandoc-2.14.2-1-amd64.deb && \
    rm pandoc-2.14.2-1-amd64.deb

RUN apt install -y doxygen

# Copy your own .bashrc to home dir of root.
# Comment it out if you don't need it.
COPY .devcontainer/.bashrc /root/
