import fiftyone as fo
import fiftyone.utils.data as foud

class FitowBaseImporter(foud.GenericSampleDatasetImporter):
    def __init__(self, *args, **kwargs):
        pass
    
    def _parse_one(self):
        raise NotImplementedError("需要写一个解析生成器(核心代码)")

    def __iter__(self):
        self._rel_iter = self._parse_one()
        return self
    
    def __next__(self):
        # img_path, img_name主要用来去重，之所以还加一个filename，因为其可能是编码的，与basename并不一定一样
        img_path, img_name, img_info_dict = next(self._rel_iter)
        return fo.Sample(filepath=img_path, filename=img_name, **img_info_dict)

    def has_dataset_info(self):
        return False

    def get_dataset_info(self):
        return None

    def has_sample_field_schema(self):
        return True

    def get_sample_field_schema(self):
        field_schema = {
            "filename": "fiftyone.core.fields.StringField",
        }
        raise NotImplementedError("自己填新增字段")
        return field_schema