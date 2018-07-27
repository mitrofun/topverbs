FROM alpine:3.8
COPY . /topverbs
RUN apk update && apk add --update --no-cache --progress \
    make \
    python3 \
    bash bash-completion \
    && apk add --no-cache --virtual=.build-dependencies \
    python3-dev \
    && pip3 install --upgrade pip setuptools \
    && pip3 install --no-cache-dir -r /topverbs/requirements/qa.txt
WORKDIR /topverbs
CMD ["/bin/bash"]