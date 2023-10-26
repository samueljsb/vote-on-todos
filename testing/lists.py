from __future__ import annotations

from collections.abc import Collection

import attrs


@attrs.frozen
class ListRepo:
    list_ids: Collection[str] = ()

    def is_list(self, list_id: str) -> bool:
        return list_id in self.list_ids
