# based on https://github.com/gentoo/gentoo-docker-images

FROM gentoo/portage:latest as portage
FROM gentoo/python:latest

COPY --from=portage /var/db/repos/gentoo /var/db/repos/gentoo

ENV ACCEPT_KEYWORDS="~amd64"
RUN emerge -q dev-python/tox

WORKDIR /usr/src/gcm
COPY pyproject.toml README.md tox.ini ./
COPY scripts scripts
COPY src src
COPY tests tests

CMD tox
