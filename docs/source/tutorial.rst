Tutorial
========

This tutorial walks you through the main functionality of the EMDB Python Client, including retrieving entries, accessing metadata, downloading files, working with validation and annotation data, and performing searches.

.. contents::
   :local:
   :depth: 2

Accessing an Entry
------------------

To retrieve an EMDB entry by ID:

.. code-block:: python

    from emdb.client import EMDB

    client = EMDB()
    entry = client.get_entry("EMD-8117")

You can now access various attributes:

.. code-block:: python

    print(entry.id)       # 'EMD-8117'
    print(entry.method)   # 'Single particle analysis'
    print(entry.resolution)  # e.g., 2.8


General Metadata
----------------
You can access general metadata about the entry from the admin attribute:

.. code-block:: python

    general = entry.admin

    # Accessing authors
    authors = [author['valueOf_'] for author in general['authors_list']['author']]
    # ['Gao Y', 'Cao E']

    # Accessing title
    general['title']
    # 'Structure of TRPV1 in complex with DkTx and RTX, determined in lipid nanodisc'

    # Accessing dates
    ## Deposition date
    general['key_dates']['deposition']  # Deposited on '2016-05-16T00:00:00'
    general['key_dates']['map_release']  # Released on '2016-05-25T00:00:00'
    general['key_dates']['update']  # Last updated on '2024-11-13T00:00:00'


    # Accessing grant information
    for grant in general['grant_support']['grant_reference']:
        print(grant['code'], grant['funding_body'], grant['country'])
    # R01NS047723 National Institutes of Health/National Institute of Neurological Disorders and Stroke (NIH/NINDS) United States
    # R37NS065071 National Institutes of Health/National Institute of Neurological Disorders and Stroke (NIH/NINDS) United States
    # S10OD020054 National Institutes of Health/Office of the Director United States
    # R01GM098672 National Institutes of Health/National Institute of General Medical Sciences (NIH/NIGMS) United States

Publication Information
-----------------------
You can access publication information via the `citations` attribute:

.. code-block:: python

    citations = entry.citations
    main_citation = citations['primary_citation']['citation_type']

    authors = [a['valueOf_'] for a in sorted(main_citation['author'], key=lambda x: x['order'])]
    # ['Gao Y', 'Cao E', 'Julius D', 'Cheng Y']

    title = main_citation['title']
    # 'TRPV1 structures in nanodiscs reveal mechanisms of ligand and lipid action'

    journal = main_citation['journal']
    # 'Nature'


Related entries
---------------

You can access related entries via the `related_emdb_ids` attribute:

.. code-block:: python

    related = entry.related_emdb_ids
    for rel in related:
        print(rel['emdb_id'], rel['relationship'])


.. code-block:: text

    # EMD-8118 {'other': 'other EM volume'}
    # EMD-8119 {'other': 'other EM volume'}
    # EMD-8120 {'other': 'other EM volume'}
    # EMD-5776 {'other': 'other EM volume'}

Fitted Models
-------------
Similarly, you can access fitted models via the `related_pdb_ids` attribute:

.. code-block:: python

    fitted_models = entry.related_pdb_ids
    for model in fitted_models:
        print(model['pdb_id'], model['relationship'])


.. code-block:: text

    5irx {'in_frame': 'FULLOVERLAP'}

Sample Information
------------------

You can access sample information via the `sample` attribute. Sample information is divided by macromolecules (e.g., proteins, nucleic acids, and ligands) and supramolecules (e.g., complexes, tissues and cellular structures):

.. code-block:: python

    sample = entry.sample
    macromolecules = sample['macromolecule_list']['macromolecule']
    supramolecules = sample['supramolecule_list']['supramolecule']

    for macromolecule in macromolecules:
        print(macromolecule['macromolecule_id'], macromolecule['name']['valueOf_'], macromolecule['instance_type'])

    for supramolecule in supramolecules:
        print(supramolecule['supramolecule_id'], supramolecule['name']['valueOf_'], supramolecule['instance_type'], supramolecule['macromolecule_list']['macromolecule'])



.. code-block:: text

    # Macromolecules
    1 Transient receptor potential cation channel subfamily V member 1 protein_or_peptide
    2 Tau-theraphotoxin-Hs1a protein_or_peptide
    3 (4R,7S)-4-hydroxy-N,N,N-trimethyl-4,9-dioxo-7-[(pentanoyloxy)methyl]-3,5,8-trioxa-4lambda~5~-phosphatetradecan-1-aminium ligand
    4 (2S)-3-{[(S)-(2-aminoethoxy)(hydroxy)phosphoryl]oxy}-2-(hexanoyloxy)propyl hexanoate ligand
    5 resiniferatoxin ligand
    6 (2S)-2-(acetyloxy)-3-{[(R)-(2-aminoethoxy)(hydroxy)phosphoryl]oxy}propyl pentanoate ligand

    # Supramolecules
    1 TRPV1 ion channel in complex with DkTx and RTX complex_supramolecule [{'instance_type': 'macromolecule', 'macromolecule_id': 1}, {'instance_type': 'macromolecule', 'macromolecule_id': 2}]
    2 Transient receptor potential cation channel subfamily V member 1 complex_supramolecule [{'instance_type': 'macromolecule', 'macromolecule_id': 1}]
    3 Tau-theraphotoxin-Hs1a complex_supramolecule [{'instance_type': 'macromolecule', 'macromolecule_id': 2}]


Experiment Information
----------------------
You can access experiment information via the `structure_determination_list` attribute:

.. code-block:: python

    experiments = entry.structure_determination_list['structure_determination']
    for exp in experiments:
        # Specimen preparation
        specimen_prepararion_list = exp['specimen_preparation_list']['specimen_preparation']

        # Microscopy
        microscopy_list = exp['microscopy_list']['microscopy']

        # Reconstruction
        reconstruction_list = exp['image_processing']


Files
-----

You can access the list of available files via the `deposited_files` attribute:

.. code-block:: python

    files = entry.deposited_files

.. code-block:: text

    [<PrimaryMapFile filename=emd_8117.map.gz, size_kbytes=28312.0, format=CCP4>,
    <FigureFile filename=400_8117.gif>,
    <HalfMapFile filename=emd_8117_half_map_1.map.gz, size_kbytes=28312.0, format=CCP4>,
    <HalfMapFile filename=emd_8117_half_map_2.map.gz, size_kbytes=28312.0, format=CCP4>,
    <ModelCifFile pdb_id=5irx filename=5irx_updated.cif>]

Files can also be accessed individually by their type:

.. code-block:: python

    primary_map = entry.primary_map
    metadata_files = entry.metadata_files
    half_maps = entry.half_maps
    additional_maps = entry.additional_maps
    masks = entry.masks
    figure = entry.figure
    pdb_models = entry.pdb_models

You can a single download files using the `download` method, or download all files using the `download_all_files` method:

.. code-block:: python

    # Download a single file
    entry.primary_map.download("/path/to/save/emd_8117.map.gz")

    # Download all files
    entry.download_all_files("/path/to/save/")

Working with Validation Data
----------------------------

You can access validation information via the `get_validation()` method:

.. code-block:: python

    validation = entry.get_validation()

    validation.recommended_contour_level
    validation.general.model_map_ratio
    validation.general.model_volume
    validation.general.surface_ratio


.. code-block:: text

    {'recl': 3.5, 'sigma': 3.5}
    {'overlap_to_model': 0.392, 'overlap_to_map': 0.699, 'model_to_map': 1.784}
    {'volume': 209811.7492326317, 'radius': 1.5}
    {'before_masking': 1.118, 'lowpassed': 0.764, 'lowpassed_toraw': 0.684, 'after_masking': 1.106}

You can also access the model validation scores for the entry:

.. code-block:: python

    scores = validation.scores
    atom_inclusion = scores.atom_inclusion
    qscores = scores.qscore
    smoc = scores.smoc
    ccc = scores.ccc

    # These scores return a list per model
    print(qscores)
    # [<EMDBModelScore metric=qscore, pdb_id=5irx, average_color=#7A8484, average_score=0.521>]

    # You can iterate over the residues
    model_qscore = qscores[0]
    for residue in model_qscore.residues:
        print(residue)

.. code-block:: text

    {'chain': 'A', 'position': 335, 'amino_acid': 'THR', 'color': '#7A7D7D', 'score': 0.493}
    {'chain': 'A', 'position': 336, 'amino_acid': 'PRO', 'color': '#7A8C8C', 'score': 0.552}
    {'chain': 'A', 'position': 337, 'amino_acid': 'LEU', 'color': '#7A8383', 'score': 0.517}
    {'chain': 'A', 'position': 338, 'amino_acid': 'ALA', 'color': '#7A7878', 'score': 0.473}
    {'chain': 'A', 'position': 339, 'amino_acid': 'LEU', 'color': '#7A7F7F', 'score': 0.499}
    {'chain': 'A', 'position': 340, 'amino_acid': 'ALA', 'color': '#7A7A7A', 'score': 0.48}
    {'chain': 'A', 'position': 341, 'amino_acid': 'ALA', 'color': '#7A8686', 'score': 0.528}
    {'chain': 'A', 'position': 342, 'amino_acid': 'SER', 'color': '#7A9393', 'score': 0.58}
    {'chain': 'A', 'position': 343, 'amino_acid': 'SER', 'color': '#7A8B8B', 'score': 0.548}
    {'chain': 'A', 'position': 344, 'amino_acid': 'GLY', 'color': '#7A7474', 'score': 0.457}
    {'chain': 'A', 'position': 345, 'amino_acid': 'LYS', 'color': '#7A9F9F', 'score': 0.627}
    ...

The validation graphs can be accessed via the `plots` attribute. You can either fetch the data or plot it directly:

.. code-block:: python

    # Fetch the data
    validation_plots = validation.plots
    # <EMDBValidationPlots density_distribution=True, rawmap_density_distribution=True, rotationally_averaged_power_spectrum=True, rawmap_rotationally_averaged_power_spectrum=True, masked_local_res_histogram=True, unmasked_local_res_histogram=True, fsc=True>

    # Plot the data
    validation_plots.fsc.plot()

Working with Annotations
------------------------

The EMDB cross-references annotations are empowered by `EMICSS <https://www.ebi.ac.uk/emdb/emicss>`_. Annotations are organized as entry-level annotations (e.g., publication, corresponding PDB and EMPIAR entries, etc.) and sample-level (e.g., UniProt identifiers, AlphaFold DB models, etc.) annotations.

Entry level annotations:

* ORCID
* EMPIAR
* PDB

Supramolecule annotation:

* Complex Portal

Macromolecule annotations:

* UniProt
* Pfam
* InterPro
* Gene Ontology (GO)
* CATH
* ChEBI
* ChEMBL
* SCOP2
* DrugBank
* PDBe-Kb
* AlphaFold DB

You can access the annotations via the `get_annotations()` method of the entry:

.. code-block:: python

    annotations = entry.get_annotations()

    annotations.orcid
    # [<ORCIDAnnotation id=0000-0003-1248-1828 sample_id=all provenance=EuropePMC title=Gao Y>, <ORCIDAnnotation id=0000-0001-9535-0369 sample_id=all provenance=EuropePMC title=Cheng Y>]
    annotations.empiar
    # [<EMPIARAnnotation id=EMPIAR-10059 sample_id=all provenance=EMPIAR>]
    annotations.pdb
    # [<PDBAnnotation id=5irx sample_id=all provenance=AUTHOR>]

    annotations.macromolecules[0].uniprot
    # [<UniProtAnnotation id=O35433 sample_id=m1 provenance=EMDB>]

    print(annotations.macromolecules)

.. code-block:: text

    [EMDBMacromoleculeSample(id=1, type='protein', uniprot=[<UniProtAnnotation id=O35433 sample_id=m1 provenance=EMDB>], pfam=[<PfamAnnotation id=PF00023 sample_id=m1 provenance=PDBe title=Ank start=95 end=177>, <PfamAnnotation id=PF00520 sample_id=m1 provenance=PDBe title=Ion_trans start=324 end=566>], interpro=[<InterProAnnotation id=IPR024862 sample_id=m1 provenance=PDBe title=TRPV start=13 end=634>, <InterProAnnotation id=IPR002110 sample_id=m1 provenance=PDBe title=Ankyrin_rpt start=17 end=257>, <InterProAnnotation id=IPR024862 sample_id=m1 provenance=PDBe title=TRPV start=13 end=629>, <InterProAnnotation id=IPR036770 sample_id=m1 provenance=PDBe title=Ankyrin_rpt-contain_sf start=6 end=310>, <InterProAnnotation id=IPR002110 sample_id=m1 provenance=PDBe title=Ankyrin_rpt start=42 end=257>, <InterProAnnotation id=IPR005821 sample_id=m1 provenance=PDBe title=Ion_trans_dom start=330 end=565>, <InterProAnnotation id=IPR008347 sample_id=m1 provenance=PDBe title=TrpV1-4 start=36 end=635>], gene_ontology=[<GeneOntologyAnnotation id=GO:0016020 sample_id=m1 provenance=PDBe title=membrane type=CELLULAR COMPONENT>], gene_ontology_cell=[<GeneOntologyAnnotation id=GO:0016020 sample_id=m1 provenance=PDBe title=membrane type=CELLULAR COMPONENT>], gene_ontology_process=[], gene_ontology_function=[], cath=[], chebi=[], chembl=[], drugbank=[], pdbekb=[<PDBeKbAnnotation id=O35433 sample_id=m1 provenance=UniProtKB>], alphafolddb=[<AlphaFoldDBAnnotation id=O35433 sample_id=m1 provenance=AlphaFold DB>], scop2=[]),
    EMDBMacromoleculeSample(id=2, type='protein', uniprot=[<UniProtAnnotation id=P0CH43 sample_id=m2 provenance=EMDB>], pfam=[], interpro=[], gene_ontology=[<GeneOntologyAnnotation id=GO:0005576 sample_id=m2 provenance=PDBe title=extracellular region type=CELLULAR COMPONENT>, <GeneOntologyAnnotation id=GO:0090729 sample_id=m2 provenance=PDBe title=toxin activity type=MOLECULAR FUNCTION>, <GeneOntologyAnnotation id=GO:0008289 sample_id=m2 provenance=PDBe title=lipid binding type=MOLECULAR FUNCTION>, <GeneOntologyAnnotation id=GO:0099106 sample_id=m2 provenance=PDBe title=ion channel regulator activity type=MOLECULAR FUNCTION>], gene_ontology_cell=[<GeneOntologyAnnotation id=GO:0005576 sample_id=m2 provenance=PDBe title=extracellular region type=CELLULAR COMPONENT>], gene_ontology_process=[], gene_ontology_function=[<GeneOntologyAnnotation id=GO:0090729 sample_id=m2 provenance=PDBe title=toxin activity type=MOLECULAR FUNCTION>, <GeneOntologyAnnotation id=GO:0008289 sample_id=m2 provenance=PDBe title=lipid binding type=MOLECULAR FUNCTION>, <GeneOntologyAnnotation id=GO:0099106 sample_id=m2 provenance=PDBe title=ion channel regulator activity type=MOLECULAR FUNCTION>], cath=[], chebi=[], chembl=[], drugbank=[], pdbekb=[<PDBeKbAnnotation id=P0CH43 sample_id=m2 provenance=UniProtKB>], alphafolddb=[<AlphaFoldDBAnnotation id=P0CH43 sample_id=m2 provenance=AlphaFold DB>], scop2=[]),
    EMDBMacromoleculeSample(id=5, type='ligand', uniprot=[], pfam=[], interpro=[], gene_ontology=[], gene_ontology_cell=[], gene_ontology_process=[], gene_ontology_function=[], cath=[], chebi=[<ChEBIAnnotation id=8809 sample_id=m5 provenance=PDBe-CCD title=resiniferatoxin>], chembl=[<ChEMBLAnnotation id=CHEMBL17976 sample_id=m5 provenance=PDBe-CCD title=resiniferatoxin>], drugbank=[<DrugBankAnnotation id=DB06515 sample_id=m5 provenance=PDBe-CCD title=resiniferatoxin>], pdbekb=[], alphafolddb=[], scop2=[])]

Searching for Entries (Lazy Mode)
---------------------------------

You can search and retrieve entry objects. This is done in a lazy manner, meaning that the search results are not fetched until you iterate over them or access their attributes.
The EMDB search uses Lucene syntax, allowing you to use various keywords and filters. There is a tutorial on the EMDB website that explains how to use the search syntax: https://www.ebi.ac.uk/emdb/documentation/search.
Also refer to the documentation for the list of available search fields: https://www.ebi.ac.uk/emdb/documentation/search/fields.

The example below shows how to retrieve all the entries released in 16/07/2025:

.. code-block:: python

    results = client.search('release_date:"2025-7-16T00:00:00Z"')
    # EMDBSearchResults(entries=[<LazyEMDBEntry EMD-52440>, <LazyEMDBEntry EMD-53168>, <LazyEMDBEntry EMD-62921>, <LazyEMDBEntry EMD-52995>, ...])

    for entry in results:
        print(entry.id, entry.method, entry.resolution)

.. code-block:: text

    EMD-52440 singleParticle 2.8
    EMD-53168 singleParticle 3.2
    EMD-62921 singleParticle 2.39
    EMD-52995 singleParticle 3.3
    EMD-53164 singleParticle 4.4
    EMD-52768 singleParticle 3.0
    EMD-61466 singleParticle 3.6
    EMD-45377 singleParticle 2.55
    EMD-52992 singleParticle 4.2
    EMD-60711 singleParticle 8.63
    ...

Searching and Returning a DataFrame
-----------------------------------

You can also get search results as a Pandas DataFrame:

.. code-block:: python

    df = client.csv_search('release_date:"2025-7-16T00:00:00Z"')
    print(df.head())

.. code-block:: text

        emdb_id structure_determination_method  resolution
    0  EMD-52440                 singleParticle        2.80
    1  EMD-53168                 singleParticle        3.20
    2  EMD-62921                 singleParticle        2.39
    3  EMD-52995                 singleParticle        3.30
    4  EMD-53164                 singleParticle        4.40
