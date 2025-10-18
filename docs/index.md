---
title: Why OpenVoicePacks?
hide:
  - navigation
  - toc
---

!!! warning
    OpenVoicePacks is in early Alpha development at the moment. Documentation is a work-in-progress
    and you may find some information is incomplete or incorrect.

![image](assets/logos/svg/horizontal-coral.svg)

<div class="grid" markdown>
<center markdown>

[API Reference](api/openvoicepacks){ .md-button .md-button--primary }

</center>
</div>

---

# Why OpenVoicePacks?

FPV pilots deserve more than outdated or incomplete soundpacks. OpenVoicePacks makes it easy to generate, customize, and share your own - powered by modern Text-to-Speech engines.

<div class="grid cards" markdown>

  - ### 🎨 Customisable
    ---
    Choose your phrases, voices, and languages. Build packs that match your flying style.

  - ### 🌍 Localised
    ---
    Generate packs in multiple languages with simple templates.

  - ### ⚡ Easy to Use
    ---
    From config file to SD card in just a few commands.

  <!-- - ### 🤝 Community Driven
    ---
    Share and download packs from a growing repository of voices and styles. -->

</div>

---

```bash
$ pip install openvoicepacks

$ openvoicepacks create my-pack --from-template en_GB
Voicepack 'my-pack.yaml' created.

$ openvoicepacks build my-pack.yaml
---> 100%
Voicepack 'my-pack' built successfully!
You can now copy the contents of 'my-pack.zip' onto your SDCARD.
```
