import json
import re
from dataclasses import dataclass

from src.settings import settings


@dataclass
class LogInfo:
    log_type: str
    cat_name: str


class LogClassifier:
    def __init__(self):
        with open(settings.class_index_to_class_path, "r") as f:
            self._index2class = json.load(f)
        with open(settings.log_type_to_class_index_path, "r") as f:
            self._logtype2class_index = json.load(f)
        self._unk = "Unhandled error"

    def _replace_parameters(self, x: str):
        return re.sub(r"[\:\=]\s?[^\,\]\s]+", "", x)

    def _apply_stemming(self, x: str):
        for stem in self._logtype2class_index.keys():
            if x.startswith(stem):
                return stem
        return self._unk

    def _process_raw(self, log_s: str):
        return self._apply_stemming(self._replace_parameters(log_s))

    def predict(self, log_s: str):
        log_type = self._process_raw(log_s)
        cat_id = self._logtype2class_index[log_type]
        cat_name = self._index2class[str(cat_id)]

        return LogInfo(log_type, cat_name)
