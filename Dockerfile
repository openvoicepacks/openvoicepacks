FROM python:3.13-slim

# Update packages and install ffmpeg for audio processing
RUN apt-get update \
  && apt-get upgrade \
  && apt-get install -y ffmpeg --no-install-recommends \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install OpenVoicePacks and create user
COPY dist/openvoicepacks* /tmp/
RUN pip install /tmp/openvoicepacks*.whl --root-user-action ignore --compile --no-cache-dir \
  && rm /tmp/openvoicepacks* \
  && useradd -m openvoicepacks -d /opt/openvoicepacks

USER openvoicepacks
WORKDIR /opt/openvoicepacks
ENTRYPOINT [ "/usr/local/bin/python", "-m", "openvoicepacks" ]
