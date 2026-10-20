# -*- coding: utf-8 -*-
"""Helpers for Odoo 20 binary fields.

Binary fields return the raw file bytes. The timbrado API still expects
base64 text, and binary fields reject a plain bytes assignment.
"""
import base64

from odoo.tools.binary import BinaryBytes


def binary_content(value):
    """Return the raw bytes stored in a binary field."""
    if not value:
        return b""
    if isinstance(value, str):
        return base64.b64decode(value)
    content = getattr(value, "content", None)
    if content is not None:
        return bytes(content)
    return bytes(value)


def binary_b64(value):
    """Return the base64 text of a binary field, for JSON API payloads."""
    if not value:
        return ""
    to_base64 = getattr(value, "to_base64", None)
    if to_base64:
        return to_base64()
    if isinstance(value, str):
        return value
    return base64.b64encode(bytes(value)).decode()


def binary_text(value, encoding="utf-8"):
    """Return file bytes as text.

    Odoo 20 binary fields expose the raw file. Callers that used to do
    ``attachment.raw.decode('utf-8')`` need the XML text, not a second base64.
    """
    if not value:
        return ""
    if isinstance(value, str):
        return value
    return binary_content(value).decode(encoding)


def qr_image(drawing):
    """Barcode drawing as a value that can be stored on a binary field."""
    image = drawing.asString("jpg")
    if isinstance(image, str):
        image = image.encode("latin-1")
    return BinaryBytes(image)
