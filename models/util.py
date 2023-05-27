from enum import Enum as PyEnum
from PIL import Image as PILImage

##Post Related Work
class PrivacyType(PyEnum):
    PUBLIC = "Public"
    PLATFORM = "Platform"
    FOLLOWERS = "Followers"
    PRIVATE = "Private"