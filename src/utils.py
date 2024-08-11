# Utils.py
# Pdfix utils

import math

from pdfixsdk.Pdfix import PdfMatrix

pi = 3.1415926535897932384626433832795


def pdf_matrix_concat(m: PdfMatrix, m1: PdfMatrix, prepend: bool) -> PdfMatrix:
    ret = PdfMatrix()
    if prepend:
        swap = m
        m = m1
        m1 = swap
    ret.a = m.a * m1.a + m.b * m1.c
    ret.b = m.a * m1.b + m.b * m1.d
    ret.c = m.c * m1.a + m.d * m1.c
    ret.d = m.c * m1.b + m.d * m1.d
    ret.e = m.e * m1.a + m.f * m1.c + m1.e
    ret.f = m.e * m1.b + m.f * m1.d + m1.f
    return ret


def pdf_matrix_rotate(m: PdfMatrix, radian: float, prepend: bool) -> PdfMatrix:
    cos_value = math.cos(radian)
    sin_value = math.sin(radian)
    m1 = PdfMatrix()
    m1.a = cos_value
    m1.b = sin_value
    m1.c = -sin_value
    m1.d = cos_value
    return pdf_matrix_concat(m, m1, prepend)


def pdf_matrix_translate(m: PdfMatrix, x: float, y: float, prepend: bool) -> PdfMatrix:
    ret = m
    if prepend:
        ret.e = m.e + x * m.a + y + m.c
        ret.f = m.f + y * m.d + x * m.b
    ret.e = m.e + x
    ret.f = m.f + y
    return ret


def pdf_matrix_inverse(orig: PdfMatrix) -> PdfMatrix:
    inverse = PdfMatrix()
    i = orig.a * orig.d - orig.b * orig.c
    if abs(i) == 0:
        return inverse
    j = -i
    inverse.a = orig.d / i
    inverse.b = orig.b / j
    inverse.c = orig.c / j
    inverse.d = orig.a / i
    inverse.e = (orig.c * orig.f - orig.d * orig.e) / i
    inverse.f = (orig.a * orig.f - orig.b * orig.e) / j
    return inverse


def pdf_matrix_scale(m: PdfMatrix, sx: float, sy: float, prepend: bool) -> PdfMatrix:
    m.a *= sx
    m.d *= sy
    if prepend:
        m.b *= sx
        m.c *= sy
    m.b *= sy
    m.c *= sx
    m.e *= sx
    m.f *= sy
    return m
