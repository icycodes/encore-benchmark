FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash ripgrep ssh && \
    pip3 install --break-system-packages pytest-json-ctrf requests && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -L https://encore.dev/install.sh | bash && \
    ln -s /root/.encore/bin/encore /usr/local/bin/encore && \
    ln -s /root/.encore/bin/git-remote-encore /usr/local/bin/git-remote-encore && \
    ln -s /root/.encore/bin/tsbundler-encore /usr/local/bin/tsbundler-encore && \
    ln -s /root/.encore/bin/tsparser-encore /usr/local/bin/tsparser-encore

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="generate-harbor-tasks"
LABEL Description="Task environment for Encore.ts, including Encore CLI and Python test dependencies."

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]

# Container contents:
#   - always required apt packages: curl wget ca-certificates git python3 python3-pip python3-pytest bash ripgrep ssh
#   - always required pip3 packages: pytest-json-ctrf requests
#   - Encore CLI installed via curl script
