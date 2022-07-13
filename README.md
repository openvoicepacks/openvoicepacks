![image](assets/site/assets/logos/svg/horizontal-coral.svg)

![GitHub](https://img.shields.io/github/license/benfairless/openvoicepacks?style=flat-square)
![GitHub release](https://img.shields.io/github/v/release/benfairless/openvoicepacks?style=flat-square)

Generate and customise complete voice packs for OpenTX and EdgeTX radios.

Powered by modern Text-to-Speech (TTS) engines like AWS Polly and Piper.

> 🚧 **Work in Progress**: Core audio generation is complete. A CLI tool is in active development - early adopters welcome!

Unhappy with downloading sound packs for your radio only to find they are incomplete?
OpenVoicePacks uses self-hosted and cloud text-to-speech generation to create comprehensive voice packs to suit your needs, giving you a consistent voice pack that covers default sounds as well as any custom lines you would like to add.

## Features
- Generate complete soundpacks from a simple config file.
- Support for multiple TTS providers (More coming soon).
- FUTURE: Output in correct OpenTX/EdgeTX SD card structure.
- FUTURE: Templating for quick localisation and customisation
- FUTURE: Normalised audio for consistent volume across phrases
- FUTURE: Community repository for sharing and downloading packs


## Technical details

All audio files are generated as 16kHz single-channel `.wav` files, ensuring compatibility with all popular EdgeTX / OpenTX radios.

Currently supported speech engines:
- [Amazon Polly](https://aws.amazon.com/polly/)
- [Piper](https://github.com/OHF-Voice/piper1-gpl)

## Requirements

- Python 3.13
- ffmpeg

## Quick Start

### Install
```bash
pip install openvoicepacks
```

## Planned UX

Create a custom voicepack configuration:
``` bash
> openvoicepacks init --provider piper

Voicepack config created from template at 'my-voicepack.yaml'
```

Build your custom voicepack:
``` bash
> openvoicepacks build my-voicepack.yaml

Building voicepack 'my-voicepack' using Piper TTS.
[####################-------------------------------------] [57/236]

Completed building voicepacks.
my-voicepack: ./voicepacks/my-voicepack.zip
```

## Road map

- Add support for additional TTS providers.
- CLI front-end.
- Web-based repository for sharing packs.
- Community-driven themed packs.
