import logging
from abc import abstractmethod
from typing import Any, Iterator

from pydantic import ValidationError

from model import ViewedFilm

logger = logging.getLogger(__name__)


class Transformer:
    @abstractmethod
    def transform(self, data: Iterator[Any]) -> list[Any]:
        pass


class KafkaTransformer(Transformer):
    def transform(self, data: Iterator[bytes]) -> list[ViewedFilm]:
        result = []
        for record in data:
            try:
                result.append(ViewedFilm.parse_raw(record))
            except ValidationError:
                logger.error("Error on creating model ViewedFilm from message %s", record)

        return result
