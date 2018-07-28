FROM alpine:3.8

COPY . /lib/topverbs

RUN apk update && apk add --update --no-cache --progress \
    make \
    python3 \
    git \
    ca-certificates \
    bash bash-completion \
    && update-ca-certificates 2>/dev/null || true \
    && apk add --no-cache --virtual=.build-dependencies \
    python3-dev \
    && pip3 install --upgrade pip setuptools \
    && pip3 install --no-cache-dir -r /lib/topverbs/requirements/qa.txt

WORKDIR /lib/topverbs

RUN python3 -m nltk.downloader averaged_perceptron_tagger