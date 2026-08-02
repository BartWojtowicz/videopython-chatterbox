try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version  # For Python <3.8

# FORK: upstream reads version("chatterbox-tts"). This distribution is named
# videopython-chatterbox, so that lookup raises PackageNotFoundError at import.
# This is the only line that differs from upstream 0.1.7.
__version__ = version("videopython-chatterbox")


from .tts import ChatterboxTTS
from .vc import ChatterboxVC
from .mtl_tts import ChatterboxMultilingualTTS, SUPPORTED_LANGUAGES