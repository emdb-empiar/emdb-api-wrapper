from typing import Optional, TYPE_CHECKING, Dict, List

from pydantic import BaseModel, PrivateAttr

if TYPE_CHECKING:
    from emdb.client import EMDBClient


class EMDBValidationGeneral(BaseModel):
    """
    Represents general validation information for an EMDB entry.
    """
    volume_estimate: Optional[dict]
    model_map_ratio: Optional[dict]
    model_volume: Optional[dict]
    surface_ratio: Optional[dict]
    rawmap_contour_level: Optional[float] = None

    @classmethod
    def from_api(cls, data: Dict = None) -> "EMDBValidationGeneral":
        try:
            rawmap_contour_level = data['rawmap_contour_level']['cl']
        except KeyError:
            rawmap_contour_level = None

        return cls(
            volume_estimate=data.get("volume_estimate", None),
            model_map_ratio=data.get("model_map_ratio", None),
            model_volume=data.get("model_volume", None),
            surface_ratio=data.get("surface_ratio", None),
            rawmap_contour_level=rawmap_contour_level
        )

    def __str__(self):
        return (f"<EMDBValidationGeneral "
                f"volume_estimate={self.volume_estimate}, "
                f"model_map_ratio={self.model_map_ratio}, "
                f"model_volume={self.model_volume}, "
                f"surface_ratio={self.surface_ratio}, "
                f"rawmap_contour_level={self.rawmap_contour_level}>")


class EMDBModelScore(BaseModel):
    """
    Represents the model score for an EMDB validation entry.
    """
    metric: str
    pdb_id: str
    average_color: str
    average_score: float
    residues: List[Dict]
    chains: Dict
    bar: Dict

    @classmethod
    def from_api(cls, metric, data: Dict) -> "EMDBModelScore":
        score_data = data.get("data", {})

        if metric == "ccc":
            average_color_key = "averagecc_color"
            average_score_key = "averagecc"
            chains_key = "chainccscore"
            bar_key = "ccc_bar"
            residue_key = "residue"
            score_key = "ccscore"
            color_key = "color"
        elif metric == "smoc":
            average_color_key = "averagesmoc_color"
            average_score_key = "averagesmoc"
            chains_key = "chainsmoc"
            bar_key = "smoc_bar"
            residue_key = "residue"
            score_key = "smoc_scores"
            color_key = "color"
        elif metric == "qscore":
            average_color_key = "averageqscore_color"
            average_score_key = "averageqscore"
            chains_key = "chainqscore"
            bar_key = "qscore_bar"
            residue_key = "residue"
            score_key = "qscore"
            color_key = "color"
        else:
            average_color_key = "average_color"
            average_score_key = "average_score"
            chains_key = "chainccscore"
            bar_key = "bar"
            residue_key = "residue"
            score_key = "score"
            color_key = "color"

        residues = score_data.get(residue_key, [])
        scores = score_data.get(score_key, [])
        colors = score_data.get(color_key, {})
        combined_residues = []
        for r, c, s in zip(residues, colors, scores):
            chain_pos, aa = r.split()  # "A:335", "THR"
            chain, pos = chain_pos.split(":")  # "A", "335"
            combined_residues.append({
                'chain': chain,
                'position': int(pos),
                'amino_acid': aa,
                'color': c,
                'score': s
            })

        return cls(
            metric=metric,
            pdb_id=data.get("name", "").split(".")[0],
            average_color=score_data.get(average_color_key, None),
            average_score=score_data.get(average_score_key, None),
            residues=combined_residues,
            chains=score_data.get(chains_key, None),
            bar=score_data.get(bar_key, None),
        )

    @classmethod
    def from_atom_inclusion(cls, atom_inclusion_by_level: Dict, residue_inclusion: Dict) -> "EMDBModelScore":
        """
        Create an EMDBModelScore instance from atom inclusion data.

        :param atom_inclusion_by_level: Dictionary containing atom inclusion data by level.
        :param residue_inclusion: Dictionary containing residue inclusion data.
        :return: An instance of EMDBModelScore.
        """

        cl_key = next(k for k, v in residue_inclusion.items() if isinstance(v, dict))
        score_data = residue_inclusion[cl_key]

        residues = score_data.get("residue", [])
        scores = score_data.get("inclusion", [])
        colors = score_data.get("color", {})
        combined_residues = []
        for r, c, s in zip(residues, colors, scores):
            chain_pos, aa = r.split()  # "A:335", "THR"
            chain, pos = chain_pos.split(":")  # "A", "335"
            combined_residues.append({
                'chain': chain,
                'position': int(pos),
                'amino_acid': aa,
                'color': c,
                'score': s
            })

        return cls(
            metric="atom_inclusion",
            pdb_id=atom_inclusion_by_level.get("name", "").split(".")[0],
            average_color=atom_inclusion_by_level.get("average_ai_color", None),
            average_score=atom_inclusion_by_level.get("average_ai_model", None),
            residues=combined_residues,
            chains=atom_inclusion_by_level.get("chainaiscore", None),
            bar=atom_inclusion_by_level.get("ai_bar", None)
        )

    def __str__(self):
        return (f"<EMDBModelScore metric={self.metric}, pdb_id={self.pdb_id}, "
                f"average_color={self.average_color}, average_score={self.average_score}>")


class EMDBValidationScores(BaseModel):
    """
    Represents the scores for an EMDB validation entry.
    """
    ccc: Optional[List[EMDBModelScore]]
    atom_inclusion: Optional[List[EMDBModelScore]]
    smoc: Optional[List[EMDBModelScore]]
    qscore: Optional[List[EMDBModelScore]]

    @classmethod
    def from_api(cls, data: Dict) -> "EMDBValidationScores":
        all_ccc_data = data.get("ccc", {})
        all_smoc_data = data.get("smoc", {})
        all_qscore_data = data.get("qscore", {})
        all_residue_inclusion = data.get("residue_inclusion", {})
        all_atom_inclusion_by_level = data.get("atom_inclusion_by_level", {})
        atom_inclusion = []
        for model_index in all_residue_inclusion.keys():
            if model_index in all_atom_inclusion_by_level:
                atom_inclusion.append(
                    EMDBModelScore.from_atom_inclusion(all_atom_inclusion_by_level[model_index], all_residue_inclusion[model_index])
                )

        return cls(
            ccc=[EMDBModelScore.from_api("ccc", ccc_data) for ccc_data in all_ccc_data.values() if ccc_data and isinstance(ccc_data, dict)],
            atom_inclusion=atom_inclusion,
            smoc=[EMDBModelScore.from_api("smoc", smoc_data) for smoc_data in all_smoc_data.values() if smoc_data and isinstance(smoc_data, dict)],
            qscore=[EMDBModelScore.from_api("qscore", qscore_data) for qscore_data in all_qscore_data.values() if qscore_data and isinstance(qscore_data, dict)],
        )

    def __str__(self):
        return (f"<EMDBValidationScores ccc={self.ccc}, atom_inclusion={self.atom_inclusion}, "
                f"smoc={self.smoc}, qscore={self.qscore}>")


class EMDBValidation(BaseModel):
    """
    Represents the validation information for an EMDB entry.
    """
    id: str
    resolution: Optional[float]
    recommended_contour_level: Optional[Dict[str, float]]
    general: EMDBValidationGeneral
    scores: EMDBValidationScores
    # fsc: dict
    # plots: dict
    _client: Optional["EMDBClient"] = PrivateAttr(default=None)

    @classmethod
    def from_api(cls, emdb_id: str, data: dict, client: "EMDBClient") -> "EMDBValidation":
        """
        Create an EMDBValidation instance from API data.

        :param emdb_id: The EMDB ID of the entry to retrieve validation data for.
        :param data: Dictionary containing EMDB validation data.
        :param client: An instance of EMDBClient to interact with the API.
        :return: An instance of EMDBValidation.
        """
        data = data[emdb_id[4:]]
        try:
            resolution = data['resolution']['value']
        except KeyError:
            resolution = None
        try:
            recc_contour_level = data['recommended_contour_level']
        except KeyError:
            recc_contour_level = None

        obj = cls(
            id=emdb_id,
            resolution=resolution,
            recommended_contour_level=recc_contour_level,
            general=EMDBValidationGeneral.from_api(data),
            scores=EMDBValidationScores.from_api(data)
        )
        obj._client = client
        return obj

    def __str__(self):
        return f"<EMDBValidation id={self.id}, resolution={self.resolution}, recommended_contour_level={self.recommended_contour_level}>"







