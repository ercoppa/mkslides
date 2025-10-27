import logging
from pathlib import Path

from omegaconf import DictConfig

from mkslides.markupgenerator import MarkupGenerator

logger = logging.getLogger(__name__)


def build(
    config: DictConfig,
    input_path: Path,
    output_path: Path,
    strict: bool,
    assets_dir: Path | None = None,
) -> None:
    markup_generator = MarkupGenerator(config, output_path, strict, assets_dir)
    markup_generator.create_or_clear_output_directory()
    markup_generator.process_markdown(input_path)
