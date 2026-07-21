"""Registry of tables owned by bettorindex_data_pipelines.

Import snapshot/grade models here as they are added so ``create_owned_tables``
materializes only repo-owned tables — never upstream read mirrors.
"""

from typing import Any

OWNED_MODELS: tuple[type[Any], ...] = ()
