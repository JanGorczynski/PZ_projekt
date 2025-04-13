FROM golang:1.24

RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

ENV VENV_PATH=/opt/venv
RUN python3 -m venv $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

RUN pip install --no-cache-dir \
    numpy \
    matplotlib \
    seaborn

WORKDIR /app

COPY . .

RUN go install

ENV SIZE=1000 HILLS=7 WRECKS=9 SUBMARINE=4

ENTRYPOINT ["sh", "-c", "oceangate run --size $SIZE --hills $HILLS --wrecks $WRECKS --submarine $SUBMARINE"]