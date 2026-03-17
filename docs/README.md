# Adobe Audition for Windows Toolkit Documentation

## Quick Start

```python
from adobe_toolkit import AdobeAuditionClient

client = AdobeAuditionClient()
if client.is_installed():
    client.connect()
    print(f"Version: {client.get_version()}")
```

## API Reference

See individual module documentation.
