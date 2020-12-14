from recap import URI, CfgNode as CN
import typing
import torch
import logging

from chesscog.core.training.train import train_model
from chesscog.core import device, DEVICE

logger = logging.getLogger(__name__)


def _train_model(model_type: str) -> typing.Tuple[torch.nn.Module, CN]:
    model_file = next((URI("models://") / model_type).glob("*.pt"))
    yaml_file = URI("config://transfer_learning") / \
        model_type / f"{model_file.stem}.yaml"
    cfg = CN.load_yaml_with_base(yaml_file)
    dataset_name = {
        "occupancy_classifier": "occupancy",
        "piece_classifier": "pieces"
    }[model_type]
    cfg.DATASET.PATH = f"data://transfer_learning/{dataset_name}"
    cfg.DATASET.WORKERS = 0
    run_dir = URI("runs://transfer_learning") / model_type
    model = torch.load(model_file, map_location=DEVICE)
    model = device(model)
    is_inception = "inception" in model_file.stem.lower()
    train_model(cfg, run_dir, model, is_inception, model_file.stem)


for model_type in ("occupancy_classifier", "piece_classifier"):
    logger.info(f"Starting training for {model_type}")
    _train_model(model_type)
    logger.info(f"Finished training for {model_type}")
