from typing import TYPE_CHECKING, Optional, Dict, List

from pydantic import BaseModel

if TYPE_CHECKING:
    from emdb.client import EMDBClient


class EMDBEntry(BaseModel):
    id: str
    method: Optional[str]
    resolution: Optional[float]
    admin: Dict
    citations: Dict
    related_emdb_ids: List[Dict]
    related_pdb_ids: List[Dict]
    sample: Dict
    structure_determination_list: List[Dict]
    primary_map: Dict
    additional_files: Dict

    _client: "EMDBClient" = None  # private attribute

    @classmethod
    def from_api(cls, data: dict, client: "EMDBClient") -> "EMDBEntry":
        """
        Create an EMDBEntry instance from API data.

        :param data: Dictionary containing EMDB entry data.
        :param client: An instance of EMDBClient to interact with the API.
        :return: An instance of EMDBEntry.
        """
        try:
            method = data['structure_determination_list']['structure_determination'][0]['method']
        except KeyError:
            method = None
        try:
            resolution = data['structure_determination_list']['structure_determination'][0]['image_processing'][0]['final_reconstruction']['resolution']['valueOf_']
        except KeyError:
            resolution = None
        try:
            citations = data['crossreferences']['citation_list']
        except KeyError:
            citations = {}
        try:
            related_emdb_ids = data['crossreferences']['emdb_list']['emdb_reference']
        except KeyError:
            related_emdb_ids = []
        try:
            related_pdb_ids = data['crossreferences']['pdb_list']['pdb_reference']
        except KeyError:
            related_pdb_ids = []

        return cls(
            id=data["emdb_id"],
            method=method,
            resolution=resolution,
            admin=data.get("admin", {}),
            citations=citations,
            related_emdb_ids=related_emdb_ids,
            related_pdb_ids=related_pdb_ids,
            sample=data.get("sample", {}),
            structure_determination_list=data.get("structure_determination_list", {}).get("structure_determination", []),
            primary_map=data.get("map", {}),
            additional_files=data.get("interpretation", {}),
            _client=client
        )

    def __str__(self):
        return f"<EMDBEntry id={self.id}, method={self.method}, resolution={self.resolution}>"
