Project goals
=============

## Order of development

- Core library: abstracting TTS and normalizing inputs and outputs.
- CLI tool: practical utility for power users who want to generate packs quickly.
- Packaging: make it easy for non-technical people to install and use.
- Templating/localisation: lowers the barrier for non-technical users and makes it global.
- Repository/community hub: turns it from a tool into an ecosystem.

## Improvements

Config flexibility: If you allow configs to be inheritable, people could write just parts of a pack instead of regenerating everything and the rest could be merged from a known good pack.

Audio consistency: Different TTS services can vary in volume and tone. A normalisation step (RMS or LUFS leveling) would make packs feel more polished.

Caching: If someone regenerates the same phrase with the same voice, caching the WAV avoids unnecessary API calls and costs.

### More immediate
- CLI tool for building voicepacks.
- Remove ffmpeg requirement and use native Python method for wave conversion.
- Web repository of existing sound packs.
- Generate default 'system' data from EdgeTX repository automatically.
- Cache provider responses, speeding up generation where sound data already exists locally.
- Multiprocessing.
- Support for more TTS services.
- Multilingual support.
- Create a dictionary of terms for consistent terminology.

## Strategies

Upstream collaboration: If we can get OpenTX/EdgeTX maintainers to link to OpenVoicePacks in their docs or forums, that’s basically a stamp of approval and would drive adoption.

## UX ideas

```bash
# Create new voice pack
> openvoicepacks create
> openvoicepacks create --name "My Voice Pack"
> openvoicepacks create --provider piper
> openvoicepacks create --provider piper --voice alan
> openvoicepacks create --from-template en_GB
# List available voices
> openvoicepacks list voices
> openvoicepacks list voices --provider piper
> openvoicepacks list voices --provider piper --language en_GB
> openvoicepacks list voices --provider polly
# Merge voice pack files
> openvoicepacks merge original.yaml modified.yaml -o merged.yaml
# Generate voice pack from file
> openvoicepacks build pack.yaml
> openvoicepacks build pack.yaml -o output_directory
> openvoicepacks build pack.yaml --dry-run
> openvoicepacks build pack.yaml --no-zip
> openvoicepacks build pack.yaml --no-checksum
```

## Links

### CI
https://pypi.org/project/diff-cover/
https://docs.astral.sh/ruff/integrations/
https://github.com/apps/renovate
https://github.com/commitizen-tools/commitizen

### Radios
https://github.com/EdgeTX/edgetx-sdcard-sounds

### Providers
https://github.com/coqui-ai/TTS
https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech?view=azure-python

### Caching
https://docs.peewee-orm.com/en/latest/

# CLI
https://click.palletsprojects.com/en/stable/
https://github.com/mkdocs/mkdocs-click

### Documentation
https://mermaid.js.org/syntax/classDiagram.html
https://github.com/manuzhang/mkdocs-htmlproofer-plugin
https://github.com/pawamoy/mkdocs-spellcheck
https://github.com/aklajnert/mkdocs-simple-hooks
https://github.com/six-two/mkdocs-placeholder-plugin
https://lukasgeiter.github.io/mkdocs-awesome-nav/
https://squidfunk.github.io/mkdocs-material/setup/setting-up-versioning/
https://google.github.io/styleguide/pyguide.html

### Audio
https://medium.com/python-other/three-ways-to-convert-the-sample-rate-of-an-wav-audio-file-to-16k-python-code-389e941cab8c

### Plugins
https://stackoverflow.com/questions/563022/whats-python-good-practice-for-importing-and-offering-optional-features


## Technical improvements

**Error Handling**

- Use more specific exception messages and types where possible.
- Consider custom exceptions for provider-specific errors.

**Logging**

- Ensure logging is consistent and meaningful across all modules.
- Use appropriate log levels (debug, info, warning, error).

**Code Structure**

- Consider splitting large classes or modules if they grow too complex.
- Use helper functions for repeated logic.
- Consider moving providers and prover-specific VoiceModels to a plugin system.
- Review docstrings, 'arguments' should be 'args' etc.

**Dependency Management**

- Document all external dependencies in pyproject.toml and README.md.
- Add checks for required binaries (e.g., ffmpeg) at runtime.
- Make piper an optional dependency as it is significantly larger.
- Remove the need for FFmpeg would also result in significant size reduction.

**Internationalisation**

- Consider swapping from British English to US English for spelling in logic.
- Use i18n for internationalisation of strings.

**Consistency**

- Use consistent terminology and naming conventions throughout (e.g., always "synthesise", always "Voice object").

**Audio processing**

- Move away from PyDub and consider using ffmpeg directly, or see if we can do WAVE bitrate conversion ourselves.

**Testing**

- Test base classes with full coverage, to enable provider-specific code to be moved to plugins.
