# Installation

There are two installation options available to you:

- [Python](#python-installation)

- [Docker](#docker-installation)


## Python installation

### External dependencies

OpenVoicePacks relies on the powerful media conversion tool [FFmpeg](https://www.ffmpeg.org/) in order to do some audio processing. As this cannot be installed through Python, you will need to install it manually.

=== ":fontawesome-brands-windows: Windows"
    Currently unsupported.

=== ":simple-apple: MacOS"
    ```bash
    brew install ffmpeg
    ```

=== ":simple-debian: Debian / :simple-ubuntu: Ubuntu"
    ```bash
    apt install ffmpeg
    ```

=== ":simple-fedora: Fedora / :simple-redhat: RHEL"
    ```bash
    dnf install ffmpeg-free
    ```

=== ":simple-archlinux: ArchLinux"
    ```bash
    pacman -S ffmpeg
    ```



## Docker installation

Firstly make sure you have [Docker](https://www.docker.com/get-started/) or another container runtime installed.

```bash
$ docker run -it --rm -v $(pwd):/opt/openvoicepacks openvoicepacks/openvoicepacks:latest
```
