from typing import Any, Dict, List, Mapping, Set

import torch

from vtorch.postprocessing.default import PredictionPostprocessor


def post_process_predictions_by_language(
    raw_predictions: torch.Tensor, languages: List[str], language_post_processors: Dict[str, PredictionPostprocessor]
) -> torch.Tensor:
    predictions = torch.zeros_like(raw_predictions)
    for post_processor_language, post_processor in language_post_processors.items():
        serial_indices = [
            serial_index for serial_index, language in enumerate(languages) if language == post_processor_language
        ]
        if len(serial_indices) == 0:
            continue
        predictions[serial_indices] = post_processor.postprocess(raw_predictions[serial_indices])
    return predictions


def is_mention_supported(mention: Mapping[str, Any], supported_languages: Set[str], missing_language: str) -> bool:
    return mention.get("language", mention.get("lang", missing_language)) in supported_languages
