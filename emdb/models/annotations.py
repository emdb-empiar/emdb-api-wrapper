from typing import Optional, TYPE_CHECKING, List

from pydantic import BaseModel, PrivateAttr

if TYPE_CHECKING:
    from emdb.client import EMDBClient


class EMDBAnnotation(BaseModel):
    id: str
    database: str
    sample_id: str
    provenance: str
    title: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    type: Optional[str] = None
    score: Optional[float] = None

    @classmethod
    def from_api(cls, data: dict, database: str, sample_id: str) -> "EMDBAnnotation":
        """
        Create an EMDBAnnotation instance from API data.

        :param database: The source of annotation (e.g., "orcid", "empiar", "pdb").
        :param sample_id: The sample ID associated with the annotation.
        :param data: The data returned by the EMDB API.
        :return: An instance of EMDBAnnotation.
        """
        annotation = cls(
            id=data.get("id"),
            database=database,
            sample_id=sample_id,
            provenance=data.get("method"),
        )
        if "title" in data:
            annotation.title = data["title"]
        if "start" in data:
            annotation.start = data["start"]
        if "end" in data:
            annotation.end = data["end"]
        if "type" in data:
            annotation.type = data["type"]
        if "score" in data:
            annotation.score = data["score"]
        return annotation


class EMDBSupramoleculeSample(BaseModel):
    """
    Model for supramolecule in EMDB annotations.
    This model is used to represent a supramolecule in EMDB annotations.
    """
    id: int
    type: str
    complex_portal: Optional[List[EMDBAnnotation]] = None

    @classmethod
    def from_api(cls, data: dict, mol_id: str) -> "EMDBSupramoleculeSample":
        """
        Create an EMDBSupramolecule instance from API data.

        :param mol_id: Supramolecule ID. The same ID is used in the EMDB sample.
        :param data: The data returned by the EMDB API.
        :return: An instance of EMDBSupramolecule.
        """
        cpx = []

        if "annotations" in data:
            annotations = data["annotations"]
            complex_portal_data = annotations.get("CPX", [])
            for annotation in complex_portal_data:
                cpx.append(EMDBAnnotation.from_api(annotation, database="Complex Portal", sample_id=mol_id))

        supramolecule =  cls(
            id=int(mol_id[1:]),
            type=data.get("type"),
        )

        if cpx:
            supramolecule.complex_portal = cpx if cpx else None

        return supramolecule

    def __str__(self):
        return (f"<EMDBSupramoleculeSample "
                f"id={self.id} "
                f"type={self.type} "
                f"complex_portal_count={len(self.complex_portal) if self.complex_portal else 0}>")


class EMDBMacromoleculeSample(BaseModel):
    """
    Model for macromolecule sample in EMDB annotations.
    This model is used to represent a macromolecule sample in EMDB annotations.
    """
    id: int
    type: str
    uniprot: Optional[List[EMDBAnnotation]] = None
    pfam: Optional[List[EMDBAnnotation]] = None
    interpro: Optional[List[EMDBAnnotation]] = None
    gene_ontology: Optional[List[EMDBAnnotation]] = None
    cath: Optional[List[EMDBAnnotation]] = None
    chebi: Optional[List[EMDBAnnotation]] = None
    chembl: Optional[List[EMDBAnnotation]] = None
    drugbank: Optional[List[EMDBAnnotation]] = None
    pdbekb: Optional[List[EMDBAnnotation]] = None
    alphafolddb: Optional[List[EMDBAnnotation]] = None
    scop2: Optional[List[EMDBAnnotation]] = None

    @classmethod
    def from_api(cls, data: dict, mol_id: str) -> "EMDBMacromoleculeSample":
        """
        Create an EMDBMacromoleculeSample instance from API data.

        :param mol_id: Macromolecule ID. The same ID is used in the EMDB sample.
        :param data: The data returned by the EMDB API.
        :return: An instance of EMDBMacromoleculeSample.
        """
        uniprot = []
        pfam = []
        interpro = []
        gene_ontology_cell = []
        gene_ontology_process = []
        gene_ontology_function = []
        cath = []
        chebi = []
        chembl = []
        drugbank = []
        pdbekb = []
        alphafolddb = []
        scop2 = []

        if "annotations" in data:
            annotations = data["annotations"]
            uniprot_data = annotations.get("UNIPROT", [])
            for annotation in uniprot_data:
                uniprot.append(EMDBAnnotation.from_api(annotation, database="UniProt", sample_id=mol_id))
            pfam_data = annotations.get("PFAM", [])
            for annotation in pfam_data:
                pfam.append(EMDBAnnotation.from_api(annotation, database="PFAM", sample_id=mol_id))
            interpro_data = annotations.get("INTERPRO", [])
            for annotation in interpro_data:
                interpro.append(EMDBAnnotation.from_api(annotation, database="InterPro", sample_id=mol_id))
            gene_ontology_data = annotations.get("GO", {})
            gene_ontology_cell_data = gene_ontology_data.get("C", [])
            gene_ontology_process_data = gene_ontology_data.get("P", [])
            gene_ontology_function_data = gene_ontology_data.get("F", [])
            for annotation in gene_ontology_cell_data:
                gene_ontology_cell.append(EMDBAnnotation.from_api(annotation, database="GO", sample_id=mol_id))
            for annotation in gene_ontology_process_data:
                gene_ontology_process.append(EMDBAnnotation.from_api(annotation, database="GO", sample_id=mol_id))
            for annotation in gene_ontology_function_data:
                gene_ontology_function.append(EMDBAnnotation.from_api(annotation, database="GO", sample_id=mol_id))
            cath_data = annotations.get("CATH", [])
            for annotation in cath_data:
                cath.append(EMDBAnnotation.from_api(annotation, database="CATH", sample_id=mol_id))
            chebi_data = annotations.get("CHEBI", [])
            for annotation in chebi_data:
                chebi.append(EMDBAnnotation.from_api(annotation, database="ChEBI", sample_id=mol_id))
            chembl_data = annotations.get("CHEMBL", [])
            for annotation in chembl_data:
                chembl.append(EMDBAnnotation.from_api(annotation, database="ChEMBL", sample_id=mol_id))
            drugbank_data = annotations.get("DRUGBANK", [])
            for annotation in drugbank_data:
                drugbank.append(EMDBAnnotation.from_api(annotation, database="DrugBank", sample_id=mol_id))
            pdbekb_data = annotations.get("PDBEKB", [])
            for annotation in pdbekb_data:
                pdbekb.append(EMDBAnnotation.from_api(annotation, database="PDBEKBD", sample_id=mol_id))
            alphafolddb_data = annotations.get("ALPHAFOLDDB", [])
            for annotation in alphafolddb_data:
                alphafolddb.append(EMDBAnnotation.from_api(annotation, database="AlphaFoldDB", sample_id=mol_id))
            scop2_data = annotations.get("SCOP2", [])
            for annotation in scop2_data:
                scop2.append(EMDBAnnotation.from_api(annotation, database="SCOP2", sample_id=mol_id))

        macromolecule = cls(
            id=int(mol_id[1:]),
            type=data.get("type", "")
        )
        if uniprot:
            macromolecule.uniprot = uniprot
        if pfam:
            macromolecule.pfam = pfam
        if interpro:
            macromolecule.interpro = interpro
        if gene_ontology_cell:
            macromolecule.gene_ontology = gene_ontology_cell
        if gene_ontology_process:
            macromolecule.gene_ontology.extend(gene_ontology_process)
        if gene_ontology_function:
            macromolecule.gene_ontology.extend(gene_ontology_function)
        if cath:
            macromolecule.cath = cath
        if chebi:
            macromolecule.chebi = chebi
        if chembl:
            macromolecule.chembl = chembl
        if drugbank:
            macromolecule.drugbank = drugbank
        if pdbekb:
            macromolecule.pdbekb = pdbekb
        if alphafolddb:
            macromolecule.alphafolddb = alphafolddb
        if scop2:
            macromolecule.scop2 = scop2

        return macromolecule

    def __str__(self):
        return (f"<EMDBMacromoleculeSample "
                f"id={self.id} "
                f"type={self.type} "
                f"uniprot_count={len(self.uniprot) if self.uniprot else 0} "
                f"pfam_count={len(self.pfam) if self.pfam else 0} "
                f"interpro_count={len(self.interpro) if self.interpro else 0} "
                f"gene_ontology_count={len(self.gene_ontology) if self.gene_ontology else 0} "
                f"cath_count={len(self.cath) if self.cath else 0} "
                f"chebi_count={len(self.chebi) if self.chebi else 0} "
                f"chembl_count={len(self.chembl) if self.chembl else 0} "
                f"drugbank_count={len(self.drugbank) if self.drugbank else 0} "
                f"pdbekb_count={len(self.pdbekb) if self.pdbekb else 0} "
                f"alphafolddb_count={len(self.alphafolddb) if self.alphafolddb else 0} "
                f"scop2_count={len(self.scop2) if self.scop2 else 0}>")


class EMDBAnnotations(BaseModel):
    """
    Model for EMDB annotations.
    This model is used to store annotations related to an EMDB entry.
    """
    emdb_id: str
    macromolecules: List[EMDBMacromoleculeSample] = []
    supramolecules: List[EMDBSupramoleculeSample] = []
    orcid: Optional[List[EMDBAnnotation]] = None
    empiar: Optional[List[EMDBAnnotation]] = None
    pdb: Optional[List[EMDBAnnotation]] = None
    _client: Optional["EMDBClient"] = PrivateAttr(default=None)

    @classmethod
    def from_api(cls, data: dict, client: "EMDBClient") -> "EMDBAnnotations":
        """
        Create an EMDBAnnotations instance from API data.

        :param data: The data returned by the EMDB API.
        :param client: The EMDBClient instance used to make the API request.
        :return: An instance of EMDBAnnotations.
        """
        orcid = []
        empiar = []
        pdb = []
        if "annotations" in data:
            annotations = data["annotations"]

            orcids = annotations.get("ORCID", [])
            for annotation in orcids:
                orcid.append(EMDBAnnotation.from_api(annotation, database="ORCID", sample_id="all"))
            empiars = annotations.get("EMPIAR", [])
            for annotation in empiars:
                empiar.append(EMDBAnnotation.from_api(annotation, database="EMPIAR", sample_id="all"))
            pdbs = annotations.get("PDB", [])
            for annotation in pdbs:
                pdb.append(EMDBAnnotation.from_api(annotation, database="PDB", sample_id="all"))

        obj = cls(
            emdb_id=data.get("emdb_id"),
            macromolecules=[
                EMDBMacromoleculeSample.from_api(mol_data, mol_id) for mol_id, mol_data in data.get("macromolecules", {}).items()
            ],
            supramolecules=[
                EMDBSupramoleculeSample.from_api(supramol_data, supramol_id) for supramol_id, supramol_data in data.get("supramolecules", {}).items()
            ],
            _client=client
        )

        if orcid:
            obj.orcid = orcid
        if empiar:
            obj.empiar = empiar
        if pdb:
            obj.pdb = pdb

        return obj

    def __str__(self):
        return (f"<EMDBAnnotations "
                f"emdb_id={self.emdb_id} "
                f"orcid_count={len(self.orcid) if self.orcid else 0} "
                f"empiar_count={len(self.empiar) if self.empiar else 0} "
                f"pdb_count={len(self.pdb) if self.pdb else 0}"
                f">")


