from typing import List, TYPE_CHECKING

from pydantic import BaseModel

from emdb.models.lazy_entry import LazyEMDBEntry

if TYPE_CHECKING:
    from emdb.client import EMDBClient


class EMDBSearchResults(BaseModel):
    entries: List[LazyEMDBEntry]
    _client: "EMDBClient"

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_api(cls, data: str, client: "EMDBClient") -> "EMDBSearchResults":
        lines = data.strip().split("\n")
        if len(lines) < 2:
            return cls(_entries=[], _client=client)
        # Skip the header line and parse the rest
        emdb_ids = lines[1:]

        return cls(
            entries=[LazyEMDBEntry(emdb_id, client) for emdb_id in emdb_ids],
            _client=client,
        )

    def __iter__(self):
        return iter(self.entries)

    def __getitem__(self, index):
        return self.entries[index]

    def __len__(self):
        return len(self.entries)
