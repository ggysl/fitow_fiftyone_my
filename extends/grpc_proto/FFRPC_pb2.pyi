from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class m_bbox(_message.Message):
    __slots__ = ["xmax", "xmin", "ymax", "ymin"]
    XMAX_FIELD_NUMBER: _ClassVar[int]
    XMIN_FIELD_NUMBER: _ClassVar[int]
    YMAX_FIELD_NUMBER: _ClassVar[int]
    YMIN_FIELD_NUMBER: _ClassVar[int]
    xmax: float
    xmin: float
    ymax: float
    ymin: float
    def __init__(self, xmin: _Optional[float] = ..., ymin: _Optional[float] = ..., xmax: _Optional[float] = ..., ymax: _Optional[float] = ...) -> None: ...

class m_ids(_message.Message):
    __slots__ = ["ids"]
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class m_image_info(_message.Message):
    __slots__ = ["height", "img_id", "img_path", "instances", "seg_map_path", "width"]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    IMG_ID_FIELD_NUMBER: _ClassVar[int]
    IMG_PATH_FIELD_NUMBER: _ClassVar[int]
    INSTANCES_FIELD_NUMBER: _ClassVar[int]
    SEG_MAP_PATH_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    height: int
    img_id: int
    img_path: str
    instances: _containers.RepeatedCompositeFieldContainer[m_instance]
    seg_map_path: str
    width: int
    def __init__(self, img_path: _Optional[str] = ..., img_id: _Optional[int] = ..., seg_map_path: _Optional[str] = ..., height: _Optional[int] = ..., width: _Optional[int] = ..., instances: _Optional[_Iterable[_Union[m_instance, _Mapping]]] = ...) -> None: ...

class m_instance(_message.Message):
    __slots__ = ["bbox", "bbox_label", "ignore_flag", "mask"]
    BBOX_FIELD_NUMBER: _ClassVar[int]
    BBOX_LABEL_FIELD_NUMBER: _ClassVar[int]
    IGNORE_FLAG_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    bbox: _containers.RepeatedScalarFieldContainer[float]
    bbox_label: str
    ignore_flag: int
    mask: _containers.RepeatedCompositeFieldContainer[m_mask]
    def __init__(self, ignore_flag: _Optional[int] = ..., bbox: _Optional[_Iterable[float]] = ..., bbox_label: _Optional[str] = ..., mask: _Optional[_Iterable[_Union[m_mask, _Mapping]]] = ...) -> None: ...

class m_label_stream(_message.Message):
    __slots__ = ["ids", "image_info", "len", "msg"]
    IDS_FIELD_NUMBER: _ClassVar[int]
    IMAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    LEN_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    image_info: m_image_info
    len: int
    msg: str
    def __init__(self, msg: _Optional[str] = ..., len: _Optional[int] = ..., ids: _Optional[_Iterable[str]] = ..., image_info: _Optional[_Union[m_image_info, _Mapping]] = ...) -> None: ...

class m_length(_message.Message):
    __slots__ = ["len"]
    LEN_FIELD_NUMBER: _ClassVar[int]
    len: int
    def __init__(self, len: _Optional[int] = ...) -> None: ...

class m_mask(_message.Message):
    __slots__ = ["points"]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, points: _Optional[_Iterable[float]] = ...) -> None: ...

class m_say(_message.Message):
    __slots__ = ["msg"]
    MSG_FIELD_NUMBER: _ClassVar[int]
    msg: str
    def __init__(self, msg: _Optional[str] = ...) -> None: ...
