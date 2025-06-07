from enum import Enum


class Directories(str, Enum):
    VIDEOS = 'videos'
    PHOTOS = 'photos'
    DOCUMENTS = 'documents'


class PhotoMediaTypes(str, Enum):
    JPEG = "image/jpeg"
    PNG = "image/png"
    GIF = "image/gif"
    BMP = "image/bmp"
    WEBP = "image/webp"
    TIFF = "image/tiff"
    SVG = "image/svg+xml"
    ICO = "image/vnd.microsoft.icon"
    HEIC = "image/heic"
    AVIF = "image/avif"


class VideoMediaTypes(str, Enum):
    MP4 = "video/mp4"
    WEBM = "video/webm"
    OGG = "video/ogg"
    AVI = "video/x-msvideo"
    MOV = "video/quicktime"
    WMV = "video/x-ms-wmv"
    FLV = "video/x-flv"
    MKV = "video/x-matroska"
    M4V = "video/x-m4v"
    THREE_GP = "video/3gpp"
    THREE_G2 = "video/3gpp2"
    TS = "video/mp2t"
    MPEG = "video/mpeg"
    F4V = "video/x-f4v"
    DIVX = "video/divx"
