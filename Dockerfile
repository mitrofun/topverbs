FROM alpine:3.8

COPY . /topverbs

RUN apk update && apk add --update --no-cache --progress \
    make \
    python3 \
    ca-certificates \
    bash bash-completion \
    && update-ca-certificates 2>/dev/null || true \
    && apk add --no-cache --virtual=.build-dependencies \
    python3-dev \
    && pip3 install --upgrade pip setuptools \
    && pip3 install --no-cache-dir -r /topverbs/requirements/qa.txt

WORKDIR /topverbs

RUN python3 -m nltk.downloader -d /topverbs/nltk_data averaged_perceptron_tagger