import os, sys
sys.path.insert(0, os.path.dirname(__file__))

import FFRPC_pb2
import FFRPC_pb2_grpc

import grpc
import asyncio
from concurrent.futures import ThreadPoolExecutor

from fiftyone import DatasetView
import numpy as np
from multiprocessing import Process, Manager

multi_manager = Manager()

class FFRPCServer(FFRPC_pb2_grpc.FFRPCServicer):
    def __init__(self, dataset: DatasetView, *args, **kwargs):
        self.ds = dataset
        print(f"grpc监听进程已启动! 监听端口: {kwargs['port']}")

    def GetIDs(self, request, context):
        return FFRPC_pb2.m_ids(ids=self.ds.count_values("id"))

    def GetDatasetInfos(self, request, context):
        return FFRPC_pb2.m_say(msg=self.ds.__str__())

    def GetLength(self, request, context):
        return FFRPC_pb2.m_length(len=len(self.ds))

    def _labels_iter(self, ds: DatasetView, field: str):
        _samples: DatasetView = ds.select_fields(["filepath", field])
        _samples.compute_metadata(overwrite=False, skip_failures=True, num_workers=8)
        img_id = 0
        for sample in _samples.iter_samples(progress=True):
            img_w = sample.metadata["width"]
            img_h = sample.metadata["height"]
            if sample[field] is not None:
                np_bboxes = np.array([d["bounding_box"] for d in sample[field]["detections"]], dtype=np.float64)
                np_bboxes[:, [0, 2]] *= img_w
                np_bboxes[:, [1, 3]] *= img_h
                bboxes = np_bboxes.tolist()
                labels = [d["label"] for d in sample[field]["detections"]]
            else:
                bboxes = []
                labels = []

            instances = [
                FFRPC_pb2.m_instance(
                    ignore_flag=0,
                    bbox=bbox,
                    bbox_label=label,
                    mask=[]
                ) for bbox, label in zip(bboxes, labels)
            ]
            
            yield FFRPC_pb2.m_label_stream(
                image_info= FFRPC_pb2.m_image_info(
                    img_path=sample["filepath"],
                    img_id=img_id,
                    seg_map_path="",
                    height=img_h,
                    width=img_w,
                    instances=instances)
            )
            img_id += 1

    def GetLabels(self, request_iterator, context):
        ds_view = self.ds
        for request in request_iterator:
            msg = request.msg
            if msg == "get_ids":
                yield FFRPC_pb2.m_label_stream(ids=ds_view.count_values("id"))
            elif msg[:8] == "get_all:":
                m_l = multi_manager.list()
                p = Process(target=p_run_iter, args=(ds_view, msg[8:], m_l))
                p.start()
                p.join()
                for filepath, img_id, img_w, img_h, bboxes, labels in m_l:
                    instances = [
                        FFRPC_pb2.m_instance(
                            ignore_flag=0,
                            bbox=bbox,
                            bbox_label=label,
                            mask=[]
                        ) for bbox, label in zip(bboxes, labels)
                    ]
                    
                    yield FFRPC_pb2.m_label_stream(
                        image_info= FFRPC_pb2.m_image_info(
                            img_path=filepath,
                            img_id=img_id,
                            seg_map_path="",
                            height=img_h,
                            width=img_w,
                            instances=instances)
                    )
                del m_l
                yield FFRPC_pb2.m_label_stream(msg="get_all:EOF")
            elif msg == "get_length":
                yield FFRPC_pb2.m_label_stream(len=len(ds_view))
            elif msg == "get_infos":
                yield FFRPC_pb2.m_label_stream(msg=ds_view.__str__())
            elif msg == "reset":
                ds_view = self.ds
                yield FFRPC_pb2.m_label_stream(msg=ds_view.__str__())
            elif msg[:5] == "expr:":
                ds_view = eval(f"ds_view.{msg[5:]}")
                yield FFRPC_pb2.m_label_stream(msg=ds_view.__str__())
            elif len(msg) > 10:
                # TODO 解析单个图片信息
                yield FFRPC_pb2.m_label_stream(msg="")
            else:
                print("Label流处理收到未知消息!")
                yield FFRPC_pb2.m_label_stream(msg=f"Label流处理收到未知消息! msg: {msg}")

    def HeartBeat(self, request_iterator, context):
        for request in request_iterator:
            if request.msg == "2":
                yield FFRPC_pb2.Say(msg="3")
            else:
                yield FFRPC_pb2.Say(msg="-1")

async def serve_async_FFRPC(port: int, dataset: DatasetView):
    server = grpc.aio.server(ThreadPoolExecutor(128), options=[
        ('grpc.max_send_message_length', 2147483647),
        ('grpc.max_receive_message_length', 2147483647),
        ("grpc.so_reuseport", 1),
        ("grpc.use_local_subchannel_pool", 1)
    ])
    FFRPC_pb2_grpc.add_FFRPCServicer_to_server(FFRPCServer(port=port, dataset=dataset), server)
    server.add_insecure_port(f"[::]:{port}")
    await server.start()
    await server.wait_for_termination()

def run_FFRPC_server(port: int, dataset: DatasetView):
    asyncio.run(serve_async_FFRPC(port, dataset))

def p_run_iter(ds, field, all_results):
    _samples: DatasetView = ds.select_fields(["filepath", field])
    _samples.compute_metadata(overwrite=False, skip_failures=True, num_workers=8)
    img_id = 0
    for sample in _samples.iter_samples(progress=True):
        img_w = sample.metadata["width"]
        img_h = sample.metadata["height"]
        if sample[field] is not None:
            np_bboxes = np.array([d["bounding_box"] for d in sample[field]["detections"]], dtype=np.float64)
            np_bboxes[:, [0, 2]] *= img_w
            np_bboxes[:, [1, 3]] *= img_h
            bboxes = np_bboxes.tolist()
            labels = [d["label"] for d in sample[field]["detections"]]
        else:
            bboxes = []
            labels = []
        all_results.append((sample["filepath"], img_id, img_w, img_h, bboxes, labels))
        img_id += 1
    return all_results