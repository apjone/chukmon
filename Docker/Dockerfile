ARG ARCH=
ARG BUILD_DATE
ARG TAG
FROM ${ARCH}debian:bullseye-slim 

WORKDIR /

# Set locale to UTF-8, otherwise upstream libraries have bytes/string conversion issues
ENV LC_ALL=en.UTF-8 \
   LANG=en.UTF-8 \
   LANGUAGE=en.UTF-8

# Set up Debian prereqs
RUN export DEBIAN_FRONTEND=noninteractive; \
    apt-get update && \
    apt-get install -y \
        -o APT::Install-Suggests=false \
        -o APT::Install-Recommends=false \
        python3 \
        python3-venv \
        python3-virtualenv \
        git && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/apjone/chukmon.git

WORKDIR /chukmon

RUN mkdir /data


RUN python3 -m venv chukmon-env && \
    . chukmon-env/bin/activate && \
    pip install --no-cache-dir --upgrade pip wheel setuptools && \
    pip install --no-cache-dir --upgrade -r requirments.txt && \
    cp env.default .env

RUN sed -i 's#DB_FILE =  "data/chukmon.sqlite"#DB_FILE =  "/data/chukmon.sqlite"#g' .env
RUN sed -i 's#APP_HOST = "127.0.0.1"#APP_HOST = "0.0.0.0"#g' .env



ENTRYPOINT [ "/chukmon/chukmon-env/bin/python3" ]
CMD ["chukmon.py"]

EXPOSE 8181