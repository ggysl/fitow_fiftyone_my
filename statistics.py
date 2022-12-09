import numpy as np
from fiftyone import ViewField as F
from fiftyone import DatasetView, Dataset, Detections
from fiftyone.utils.eval.coco import COCODetectionResults
from fiftyone.core.session.session import Session
from .extends.yolov5_s_api import Metrics as YoloV5Metircs

def _format_sep(sentence):
    n_total = 100
    n = round((n_total - len(sentence.encode("gbk")))/2)
    return '-'*n + sentence + '-'*n

def _user_choose(question):
    r = input(question + "(y/n):")
    if r.lower() == "y":
        return True
    else:
        return False

def statistics_api(S_fun):
    def wrapper(self, *args, **kwargs):
        print(_format_sep("Statistics-->" + S_fun.__name__ + "开始运行"))
        result = S_fun(self, *args, **kwargs)
        return result
    return wrapper

class Statistics():
    def __init__(self) -> None:
        pass

    @statistics_api
    def coco_eval(self, dataset: DatasetView, eval_key: str, session: Session, gt_field="ground_truth", pred_field="predictions", classes=None):
        """
        fiftyone目前支持的总的coco指标, 及使用示例.
        其中的各个部分可以拆开
        """
        if not isinstance(dataset, (DatasetView, Dataset)):
            raise ValueError("需选择正确的dataset或view!")

        try:
            eval_results: COCODetectionResults = dataset.load_evaluation_results(eval_key=eval_key)
        except ValueError as e:
            if "evaluation key" not in str(e):
                raise e
            else:
                if not _user_choose(f"没有该{eval_key}, 是否开始创建?"):
                    return
                else:
                    eval_results: COCODetectionResults = dataset.evaluate_detections(
                        pred_field=pred_field,
                        gt_field=gt_field,
                        eval_key=eval_key,
                        classes=classes,
                        method="coco",
                        iou=0.5,
                        compute_mAP=True
                    )

        # 打印AP值
        eval_results.print_report(classes=classes)

        # 打印mAP
        print("mAP: {}".format(eval_results.mAP(classes=classes)))

        # 绘制pr曲线
        pr = eval_results.plot_pr_curves(classes=classes)
        pr.show()

        # 绘制混淆矩阵并交互
        cm = eval_results.plot_confusion_matrix(classes=classes)
        cm.show()
        session.plots.attach(cm)

    def _fo_to_numpy(self, targets: Detections, classes, mode=5, dtype=np.float32):
        """
        fiftyone Detections转成numpy数据接口.
        mode: 5表示标签, 6表示预测
        """
        if mode not in (5, 6):
            raise ValueError(f"mode只能是5, 6; 但是收到值{mode}")

        if targets == None:
            return np.zeros([0, mode], dtype=dtype)
        else:
            if mode == 6:
                np_value =np.array(
                    [[*d["bounding_box"], d["confidence"], classes[d["label"]]] for d in targets["detections"]],
                    dtype=dtype)
                np_value[:, 2:4] = np_value[:, 0:2] + np_value[:, 2:4]
            elif mode == 5:
                np_value =np.array(
                    [[classes[d["label"]], *d["bounding_box"]] for d in targets["detections"]],
                    dtype=dtype)
                np_value[:, 3:5] = np_value[:, 1:3] + np_value[:, 3:5]
            return np_value

    @statistics_api
    def yolov5_eval(self, dataset: DatasetView, eval_dir: str, gt_field="ground_truth", pred_field="predictions", classes: dict=None):
        _samples = dataset.select_fields([gt_field, pred_field])
        classes = {name:i for (i, name) in enumerate(_samples.distinct(F(f"{gt_field}.detections.label")))} \
            if classes == None else classes

        yolov5_metrics = YoloV5Metircs(save_dir=eval_dir, class_names={v:k for (k, v) in classes.items()}, n_classes=len(classes))
        for sample in _samples.iter_samples(progress=True):
            predn = self._fo_to_numpy(sample[pred_field], classes=classes, mode=6)
            labeln = self._fo_to_numpy(sample[gt_field], classes=classes, mode=5)
            yolov5_metrics.process_batch(predn, labeln)
        yolov5_metrics.output()

    @statistics_api
    def delete_eval_key(self, dataset: DatasetView, eval_key):
        """
        删除eval_key.
        fiftyone官方api有, 放在这里更直观一点
        """
        if not isinstance(dataset, (DatasetView, Dataset)):
            raise ValueError("需选择正确的dataset或view!")
        else:
            dataset.delete_evaluation(eval_key=eval_key)