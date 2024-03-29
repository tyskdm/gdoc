FROM python:3.10

RUN apt-get update && apt-get upgrade -y
ENV DEBCONF_NOWARNINGS=yes

RUN /usr/local/bin/python -m pip install --upgrade pip

# pandoc
RUN curl -sSLO https://github.com/jgm/pandoc/releases/download/2.19.2/pandoc-2.19.2-1-amd64.deb && \
    dpkg -i pandoc-2.19.2-1-amd64.deb && \
    rm pandoc-2.19.2-1-amd64.deb

# doxygen
RUN apt-get install -y doxygen graphviz

# PlantUML
RUN apt-get install -y default-jre graphviz fonts-migmix
# In addtion,
# 1. download plantuml.jar to here from `https://plantuml.com/download`.
# 2. add execution path to `./plantuml`.
#    For this, run `./postCreateCommand` inside container.
#
# Some other japanese-fonts are:
# fonts-ipafont fonts-takao-mincho fonts-takao-gothic fonts-migmix fonts-noto-cjk

# Other utils
RUN apt-get install -y gitk less cloc

# Creating a non-root user
# https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#_creating-a-nonroot-user
# 1. ARGs
ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=$USER_UID
# 2. Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    # && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
# ********************************************************
# * Anything else you want to do like clean up goes here *
# ********************************************************
# 3. [Optional] Set the default user. Omit if you want to keep the default as root.
USER $USERNAME

# python and pip
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/${USERNAME}/.local/bin:$PATH"

# poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.in-project true
