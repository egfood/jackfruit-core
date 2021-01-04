FROM postgres:11.7-alpine

LABEL maintainer="Yauheni Abakshonak <yauheni_abakshonak@epam.com>"

# add docker user and group first to make sure their IDs get assigned consistently, regardless of whatever dependencies get added
RUN addgroup -S docker && adduser -S -G docker docker

# Copy configure script
COPY configure.sh /docker-entrypoint-initdb.d/configure.sh

RUN chmod 755 /docker-entrypoint-initdb.d/configure.sh