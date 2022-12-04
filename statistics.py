from fiftyone import DatasetView, Dataset
from fiftyone.utils.eval.coco import COCODetectionResults
from fiftyone.core.session.session import Session

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
