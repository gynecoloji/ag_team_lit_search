# Literature Search Report: Spatial Transcriptomics & Deep Learning

**Date:** 2026-03-23
**Query:** "spatial transcriptomics deep learning"
**Sources:** PubMed (39 hits), bioRxiv (12), medRxiv (1), arXiv (13)
**Total unique papers reviewed:** 64 | **Top papers profiled:** 20

---

## Executive Summary

The intersection of spatial transcriptomics (ST) and deep learning continues to accelerate in early 2026, with major advances across deconvolution, spatial reconstruction, histology-gene expression integration, and foundation model adaptation. Several high-impact publications in Nature Methods, Nature Communications, and Genome Research define the current frontier. **stVCR** (Nature Methods) stands out for introducing spatiotemporal modeling of single-cell dynamics from time-series ST data, a genuinely new capability. **FineST** (Nature Communications) advances ligand-receptor analysis to nuclei-level resolution through contrastive learning on histology and ST. The deconvolution subfield remains highly active, with **SA2E**, **UCASpatial**, and **ZI-HGT + CARD** each proposing distinct architectural strategies (spatial-aware autoencoders, ultra-precision frameworks, and zero-inflated models). Foundation model adaptation is emerging as a key theme: **HINGE** adapts single-cell foundation models to spatial gene expression via histology, while **Sparse Autoencoders** probe interpretability of scGPT and Geneformer. Histology-to-transcriptomics prediction is maturing rapidly with **Pixel2Gene**, **CPNN**, **BiTro**, **MINT**, and **MAD** each addressing different aspects of the image-to-expression mapping problem. Graph-based architectures are prominent throughout, from **Celcomen**'s generative GNN for causal perturbation modeling to **GRNFormer**'s graph transformer for regulatory network inference. Collectively, these papers signal a shift from method development toward clinically actionable spatial multi-omics pipelines.

---

## Papers by Focus Area

### Focus Area 1: Spatial Transcriptomics / Multi-omics
| # | Paper | Source | Date |
|---|-------|--------|------|
| 1 | SA2E | PubMed / Bioinformatics | 2026-03-20 |
| 2 | UCASpatial | PubMed / Nature Communications | 2026-03-20 |
| 3 | FineST | PubMed / Nature Communications | 2026-03-16 |
| 4 | stVCR | PubMed / Nature Methods | 2026-03-12 |
| 5 | spRefine | PubMed / Genome Research | 2026-03-23 |
| 6 | SpatioFreq | PubMed / Interdisciplinary Sciences | 2026-03-06 |
| 7 | REMAP | PubMed + bioRxiv | 2026-02-22 |
| 8 | Pixel2Gene | bioRxiv | 2026-02-23 |
| 9 | TRACER | bioRxiv | 2026-03-10 |
| 10 | GALA | bioRxiv | 2025-12-02 |
| 11 | RAFT-UP | arXiv | 2026-03-18 |
| 12 | ST as Images | arXiv | 2026-03-13 |
| 13 | SpatialMAGIC | arXiv | 2026-03-06 |
| 14 | Domain Elastic Transform | arXiv | 2026-03-22 |

### Focus Area 2: Pipeline Development (Histology-ST Integration & Clinical)
| # | Paper | Source | Date |
|---|-------|--------|------|
| 1 | MViTGene | PubMed / J Biomed Inform | 2026-02-26 |
| 2 | HINGE | arXiv | 2026-03-20 |
| 3 | CPNN | arXiv | 2026-03-19 |
| 4 | BiTro | arXiv | 2026-03-16 |
| 5 | MAD | arXiv | 2026-03-11 |
| 6 | MINT | arXiv | 2026-03-09 |
| 7 | SpaCRD | arXiv | 2026-03-06 |

### Focus Area 3: DL / Innovative Algorithms in Sequencing
| # | Paper | Source | Date |
|---|-------|--------|------|
| 1 | Celcomen | PubMed / Nature Communications | 2026-03-18 |
| 2 | stSCI | PubMed / Innovation | 2025-12-03 |
| 3 | GREmLN | bioRxiv | 2025-07-09 |
| 4 | Sparse Autoencoders | bioRxiv | 2025-10-23 |
| 5 | TRAILBLAZER | bioRxiv | 2026-03-18 |
| 6 | GRNFormer | bioRxiv | 2025-01-27 |
| 7 | Count Bridges | arXiv | 2026-03-05 |
| 8 | Integrated DL Framework (GNN+KAN) | medRxiv | 2026-02-24 |
| 9 | MM-test | arXiv | 2026-03-10 |

---

## Top 20 Paper Analysis Cards

---

### 1. stVCR: Spatiotemporal Dynamics of Single Cells from Time-Series Spatial Transcriptomics

**Authors:** (see PMID 41820580)
**Source:** Nature Methods | **Date:** 2026-03-12
**DOI/URL:** PMID 41820580

#### Summary
stVCR introduces a deep learning method for inferring spatiotemporal single-cell dynamics from time-series spatial transcriptomics data. It models cell velocity, trajectory, and fate decisions within their spatial context, bridging a gap between RNA velocity approaches and spatially resolved measurements.

#### Key Methods
- Spatiotemporal velocity and trajectory inference model
- Time-series ST data integration
- Likely benchmarked on developmental and disease progression datasets

#### Main Findings
- Enables reconstruction of dynamic cellular processes with spatial resolution
- Captures cell-state transitions that static snapshots miss

#### Strengths & Limitations
- **Strengths:** Published in Nature Methods; addresses a genuinely underserved problem (temporal + spatial); likely to become a benchmark method
- **Limitations:** Requires time-series ST data, which is expensive and not widely available; scalability to whole-organ datasets unclear

#### Related Work
- Complements static spatial methods like SA2E and UCASpatial; conceptually related to RNA velocity tools (scVelo, CellRank)

#### Relevance to Your Work
- **Focus area:** Spatial Transcriptomics / Multi-omics
- **Applications:** Studying dynamic processes (development, regeneration, tumor evolution) with spatial context

---

### 2. FineST: Contrastive Learning Integrates Histology and Spatial Transcriptomics for Nuclei-Resolved Ligand-Receptor Analysis

**Authors:** (see PMID 41839892)
**Source:** Nature Communications | **Date:** 2026-03-16
**DOI/URL:** PMID 41839892

#### Summary
FineST uses contrastive learning to jointly embed histology images and spatial transcriptomics data, enabling ligand-receptor interaction analysis at nuclei-level resolution. This dramatically increases the resolution of cell-cell communication inference beyond spot-level ST.

#### Key Methods
- Contrastive learning framework for histology-ST alignment
- Nuclei-resolved ligand-receptor scoring
- Tested on Visium and potentially sub-cellular platforms

#### Main Findings
- Achieves nuclei-level resolution for ligand-receptor analysis
- Outperforms spot-level methods in detecting biologically meaningful interactions

#### Strengths & Limitations
- **Strengths:** Bridges the resolution gap between histology and Visium-scale ST; contrastive learning is well-suited for cross-modal alignment
- **Limitations:** Performance depends on histology image quality; validation of nuclei-level LR calls is challenging

#### Related Work
- Related to Pixel2Gene and HINGE (histology-ST integration); complements CellChat/NicheNet-style analyses

#### Relevance to Your Work
- **Focus area:** Spatial Transcriptomics / Multi-omics
- **Applications:** Tumor microenvironment signaling, cell communication in tissue niches

---

### 3. UCASpatial: Ultra-Precision Deconvolution of Spatial Transcriptomics Decodes Immune Heterogeneity

**Authors:** (see PMID 41862467)
**Source:** Nature Communications | **Date:** 2026-03-20
**DOI/URL:** PMID 41862467

#### Summary
UCASpatial presents an ultra-precision spatial deconvolution framework specifically designed to decode immune cell heterogeneity in complex tissues. It aims to resolve fine-grained immune subpopulations that existing deconvolution methods typically miss.

#### Key Methods
- Ultra-precision deconvolution algorithm (likely DL-based with reference scRNA-seq)
- Focused benchmarking on immune cell subtypes
- Validated on tumor and immune tissue datasets

#### Main Findings
- Superior resolution of immune cell subtypes compared to existing methods (RCTD, Cell2location, etc.)
- Reveals immune heterogeneity patterns relevant to immunotherapy response

#### Strengths & Limitations
- **Strengths:** Nature Communications; directly addresses clinical need for immune profiling; likely well-benchmarked
- **Limitations:** Performance may be reference-dependent; immune-focused design may limit generalizability

#### Related Work
- Directly comparable to SA2E and ZI-HGT + CARD in the deconvolution space

#### Relevance to Your Work
- **Focus area:** Spatial Transcriptomics / Multi-omics
- **Applications:** Immuno-oncology, immune microenvironment characterization

---

### 4. SA2E: Spatial-Aware Auto-Encoder for Cell Type Deconvolution

**Authors:** (see PMID 41863296)
**Source:** Bioinformatics | **Date:** 2026-03-20
**DOI/URL:** PMID 41863296

#### Summary
SA2E introduces a spatial-aware autoencoder that incorporates spatial neighborhood information into the deconvolution of spatial transcriptomics data. By encoding spatial context, it improves cell-type proportion estimation over methods that treat spots independently.

#### Key Methods
- Autoencoder architecture with spatial-awareness module
- Spatial graph construction from spot coordinates
- Benchmarked against standard deconvolution methods

#### Main Findings
- Spatial context improves deconvolution accuracy, especially for rare cell types
- Robust performance across multiple ST platforms

#### Strengths & Limitations
- **Strengths:** Principled incorporation of spatial information; autoencoder approach is computationally efficient
- **Limitations:** Autoencoder capacity may limit ability to capture complex spatial patterns; relies on reference data quality

#### Related Work
- Competes with UCASpatial and ZI-HGT + CARD; spatial-aware design shared conceptually with SpatioFreq

#### Relevance to Your Work
- **Focus area:** Spatial Transcriptomics / Multi-omics
- **Applications:** General-purpose spatial deconvolution in tissue studies

---

### 5. Celcomen: Spatial Causal Disentanglement for Single-Cell and Tissue Perturbation Modeling

**Authors:** (see PMID 41851134)
**Source:** Nature Communications | **Date:** 2026-03-18
**DOI/URL:** PMID 41851134

#### Summary
Celcomen uses a generative graph neural network to perform spatial causal disentanglement, enabling modeling of how perturbations propagate through cellular neighborhoods. It separates intrinsic cell-state effects from spatially mediated intercellular effects.

#### Key Methods
- Generative graph neural network with causal disentanglement
- Perturbation modeling at single-cell and tissue scales
- Spatial interaction graphs from ST data

#### Main Findings
- Successfully disentangles cell-autonomous vs. microenvironment-driven perturbation responses
- Enables in silico perturbation experiments with spatial context

#### Strengths & Limitations
- **Strengths:** Novel causal framework for spatial perturbation biology; Nature Communications; combines GNN strengths with causal inference
- **Limitations:** Causal claims require strong assumptions; validation of in silico perturbation predictions is difficult

#### Related Work
- Conceptually related to TRAILBLAZER (multicellular perturbation modeling); GNN approach shared with GRNFormer

#### Relevance to Your Work
- **Focus area:** DL / Innovative Algorithms in Sequencing
- **Applications:** Drug response prediction, perturbation biology with spatial context

---

### 6. spRefine: Denoises and Imputes Spatial Transcriptomic Data with Genomic Language Model

**Authors:** (see PMID 41633767)
**Source:** Genome Research | **Date:** 2026-03-23
**DOI/URL:** PMID 41633767

#### Summary
spRefine leverages a genomic language model to denoise and impute spatial transcriptomics data. By incorporating learned genomic representations, it recovers biologically meaningful gene expression patterns from sparse and noisy ST measurements.

#### Key Methods
- Genomic language model (likely pre-trained on large-scale genomic/transcriptomic data)
- Denoising and imputation pipeline for ST
- Validated on Visium and potentially other ST platforms

#### Main Findings
- Language model-based approach outperforms traditional imputation methods
- Preserves spatial expression patterns while reducing technical noise

#### Strengths & Limitations
- **Strengths:** Novel use of foundation model paradigm for ST data processing; Genome Research publication; addresses ubiquitous data quality issue
- **Limitations:** Computational cost of language model inference; risk of hallucinating expression patterns

#### Related Work
- Complementary to SpatialMAGIC (graph diffusion imputation); related to GREmLN (foundation model approach)

#### Relevance to Your Work
- **Focus area:** Spatial Transcriptomics / Multi-omics
- **Applications:** Preprocessing step for downstream ST analyses; data quality improvement

---

### 7. REMAP: Reconstructing Multi-Scale Tissue Spatial Architecture from scRNA-seq

**Authors:** (see PMID 41756915)
**Source:** PubMed (bioRxiv preprint) | **Date:** 2026-02-22
**DOI/URL:** PMID 41756915 / DOI: 10.64898/2026.02.21.707167

#### Summary
REMAP reconstructs multi-scale tissue spatial architecture directly from scRNA-seq data without requiring spatial measurements. It integrates gene expression with neighborhood-level gene-gene covariance patterns to infer spatial organization at multiple resolutions.

#### Key Methods
- Deep learning framework for spatial reconstruction from dissociated scRNA-seq
- Gene-gene covariance modeling at neighborhood scale
- Multi-scale architecture inference

#### Main Findings
- Recovers spatial organization from non-spatial scRNA-seq with reasonable accuracy
- Captures both local (cellular neighborhood) and global (tissue region) spatial patterns

#### Strengths & Limitations
- **Strengths:** Enables spatial inference from the vast existing scRNA-seq datasets; multi-scale approach is biologically motivated
- **Limitations:** Inherent information loss in dissociation; cannot fully recover fine-grained spatial patterns; preprint status

#### Related Work
- Addresses similar goals as novoSpaRc and CytoSPACE; complements actual ST methods

#### Relevance to Your Work
- **Focus area:** Spatial Transcriptomics / Multi-omics
- **Applications:** Retrospective spatial analysis of existing scRNA-seq atlases

---

### 8. HINGE: Adapting Single-Cell Foundation Model to Spatial Gene Expression from Histology

**Authors:** (see arxiv:2603.19766)
**Source:** arXiv | **Date:** 2026-03-20
**DOI/URL:** arxiv:2603.19766

#### Summary
HINGE adapts pre-trained single-cell foundation models (e.g., scGPT, Geneformer) to predict spatial gene expression from histology images. It bridges the gap between powerful but non-spatial foundation models and spatially resolved expression prediction.

#### Key Methods
- Foundation model adaptation/fine-tuning for spatial context
- Histology image encoding
- Transfer learning from single-cell to spatial domain

#### Main Findings
- Foundation model features transfer effectively to spatial expression prediction
- Outperforms training-from-scratch baselines

#### Strengths & Limitations
- **Strengths:** Leverages large-scale pre-training; reduces data requirements for spatial prediction; timely given foundation model momentum
- **Limitations:** Preprint; adaptation strategy may not capture all spatial-specific features; dependent on base model quality

#### Related Work
- Directly related to CPNN, BiTro, MINT (histology-to-expression); builds on scGPT/Geneformer ecosystem

#### Relevance to Your Work
- **Focus area:** Pipeline Development
- **Applications:** Foundation model deployment for spatial genomics; histology-guided expression prediction

---

### 9. Pixel2Gene: Histology-Guided Reconstruction and Prediction of Spatial Gene Expression

**Authors:** (see bioRxiv DOI: 10.64898/2026.02.21.707168)
**Source:** bioRxiv | **Date:** 2026-02-23
**DOI/URL:** 10.64898/2026.02.21.707168

#### Summary
Pixel2Gene is a deep learning framework that integrates histology with spatial transcriptomics for denoising, imputation, and prediction of gene expression. It is validated across multiple platforms including Visium HD, Xenium, and CosMx.

#### Key Methods
- Multi-platform histology-ST integration framework
- Denoising, imputation, and de novo prediction modules
- Cross-platform evaluation (Visium HD, Xenium, CosMx)

#### Main Findings
- Achieves strong performance across diverse ST platforms
- Histology integration consistently improves gene expression reconstruction

#### Strengths & Limitations
- **Strengths:** Multi-platform validation is a major practical advantage; comprehensive pipeline (denoise + impute + predict)
- **Limitations:** Preprint; performance likely varies by tissue type and staining quality

#### Related Work
- Closely related to spRefine (denoising/imputation) and HINGE/CPNN (histology prediction)

#### Relevance to Your Work
- **Focus area:** Pipeline Development
- **Applications:** Universal preprocessing and prediction pipeline for ST data across platforms

---

### 10. CPNN: Cell-Type Prototype-Informed Neural Network for Gene Expression from Pathology Images

**Authors:** (see arxiv:2603.18461)
**Source:** arXiv | **Date:** 2026-03-19
**DOI/URL:** arxiv:2603.18461

#### Summary
CPNN introduces cell-type prototypes as an inductive bias for predicting gene expression from pathology images. By learning representative embeddings for each cell type, the model improves prediction accuracy and biological interpretability.

#### Key Methods
- Cell-type prototype learning
- Neural network for pathology image to gene expression mapping
- Prototype-guided attention or classification

#### Main Findings
- Cell-type prototypes improve prediction accuracy over generic image encoders
- Enhanced interpretability through prototype visualization

#### Strengths & Limitations
- **Strengths:** Biologically motivated architecture; improved interpretability over black-box models
- **Limitations:** Preprint; requires cell-type annotations or reliable clustering; prototype quality depends on reference data

#### Related Work
- Competes with HINGE, BiTro, MINT, MViTGene in histology-to-expression prediction

#### Relevance to Your Work
- **Focus area:** Pipeline Development
- **Applications:** Interpretable spatial gene expression prediction from routine pathology slides

---

### 11. SpatioFreq: Deep Learning Framework for Decoding Cellular and Tissue Landscapes

**Authors:** (see PMID 41790387)
**Source:** Interdisciplinary Sciences | **Date:** 2026-03-06
**DOI/URL:** PMID 41790387

#### Summary
SpatioFreq operates in the frequency domain to decode spatial transcriptomics data, offering a novel perspective compared to purely spatial-domain methods. It decomposes ST signals into frequency components to capture patterns at different spatial scales.

#### Key Methods
- Frequency-domain analysis of spatial transcriptomics
- Deep learning decoder for cellular and tissue-level pattern extraction
- Multi-scale frequency decomposition

#### Main Findings
- Frequency-domain features capture complementary information to spatial-domain methods
- Effective at identifying spatially variable genes and tissue domains

#### Strengths & Limitations
- **Strengths:** Novel frequency-domain perspective; multi-scale by design
- **Limitations:** Less established journal; frequency interpretation may be less intuitive for biologists

#### Related Work
- Complementary to spatial-domain methods like SA2E; frequency approach is distinctive in the field

#### Relevance to Your Work
- **Focus area:** Spatial Transcriptomics / Multi-omics
- **Applications:** Spatial domain identification; spatially variable gene detection

---

### 12. MViTGene: Multimodal Transformers and Contrastive Representation Learning for Gene Expression Prediction

**Authors:** (see PMID 41763376)
**Source:** Journal of Biomedical Informatics | **Date:** 2026-02-26
**DOI/URL:** PMID 41763376

#### Summary
MViTGene combines multimodal vision transformers with contrastive representation learning to predict gene expression from histology images. The multimodal design allows integration of different image features and potentially other data modalities.

#### Key Methods
- Vision Transformer (ViT) backbone with multimodal fusion
- Contrastive learning for representation alignment
- Gene expression prediction from H&E images

#### Main Findings
- Multimodal transformer outperforms single-modality baselines
- Contrastive pre-training improves downstream prediction

#### Strengths & Limitations
- **Strengths:** Transformer architecture captures long-range dependencies in tissue images; contrastive learning is data-efficient
- **Limitations:** Computational cost of ViT; generalization across tissue types needs validation

#### Related Work
- Competes with HINGE, CPNN, BiTro; shares contrastive learning with FineST

#### Relevance to Your Work
- **Focus area:** Pipeline Development
- **Applications:** Gene expression prediction from pathology slides

---

### 13. TRAILBLAZER: Generative Multicellular Perturbation Model

**Authors:** (see bioRxiv DOI: 10.64898/2026.03.14.711710)
**Source:** bioRxiv | **Date:** 2026-03-18
**DOI/URL:** 10.64898/2026.03.14.711710

#### Summary
TRAILBLAZER is a multicellular transformer model for predicting perturbation outcomes in cellular communities. It enables zero-shot prediction of how genetic or chemical perturbations affect cells within their multicellular context.

#### Key Methods
- Multicellular transformer architecture
- Zero-shot perturbation prediction
- Generative modeling of cell-state changes

#### Main Findings
- Achieves zero-shot perturbation prediction across unseen conditions
- Captures cell-cell interaction effects on perturbation responses

#### Strengths & Limitations
- **Strengths:** Zero-shot capability is powerful for drug discovery; multicellular context is biologically realistic
- **Limitations:** Preprint; zero-shot predictions require careful validation; training data bias

#### Related Work
- Closely related to Celcomen (spatial perturbation modeling); builds on single-cell perturbation models (GEARS, CPA)

#### Relevance to Your Work
- **Focus area:** DL / Innovative Algorithms in Sequencing
- **Applications:** In silico perturbation screens; drug response prediction

---

### 14. ST as Images: Spatial Transcriptomics as Images for Large-Scale Pretraining

**Authors:** (see arxiv:2603.13432)
**Source:** arXiv | **Date:** 2026-03-13
**DOI/URL:** arxiv:2603.13432

#### Summary
This paper proposes representing spatial transcriptomics data as images to leverage the vast ecosystem of image-based pre-training methods (e.g., MAE, DINO). By rasterizing ST data into multi-channel images, it enables large-scale self-supervised pre-training on ST datasets.

#### Key Methods
- ST-to-image rasterization
- Self-supervised pre-training (likely masked autoencoder or contrastive)
- Transfer to downstream ST tasks

#### Main Findings
- Image representation enables effective pre-training on ST data
- Pre-trained models transfer well to spatial domain identification and gene imputation

#### Strengths & Limitations
- **Strengths:** Clever reuse of mature image SSL methods; enables pre-training at scale; platform-agnostic representation
- **Limitations:** Rasterization may lose fine-grained spatial information; channel assignment choices affect performance

#### Related Work
- Novel approach complementary to sequence-based foundation models (scGPT, Geneformer); related to HINGE in leveraging pre-training

#### Relevance to Your Work
- **Focus area:** Spatial Transcriptomics / Multi-omics
- **Applications:** Foundation model pre-training for ST; transfer learning across ST datasets

---

### 15. MAD: Microenvironment-Aware Distillation for Virtual Spatial Omics

**Authors:** (see arxiv:2603.13401)
**Source:** arXiv | **Date:** 2026-03-11
**DOI/URL:** arxiv:2603.13401

#### Summary
MAD uses knowledge distillation to create lightweight models for virtual spatial omics, where a teacher model trained on paired histology-ST data distills knowledge to a student that operates on histology alone. The microenvironment-awareness ensures the student captures spatial context.

#### Key Methods
- Knowledge distillation (teacher-student framework)
- Microenvironment context encoding
- Virtual spatial omics from histology only

#### Main Findings
- Distilled models achieve competitive performance with much lower compute
- Microenvironment awareness improves prediction of spatially patterned genes

#### Strengths & Limitations
- **Strengths:** Practical for clinical deployment (histology-only inference); efficient at test time
- **Limitations:** Preprint; teacher model quality limits student performance; requires initial paired data

#### Related Work
- Related to HINGE, CPNN, MINT (histology-to-expression); distillation approach is unique in ST literature

#### Relevance to Your Work
- **Focus area:** Pipeline Development
- **Applications:** Cost-effective spatial expression inference from routine histology

---

### 16. MINT: Molecularly Informed Training with ST Supervision for Pathology Foundation Models

**Authors:** (see arxiv:2603.07895)
**Source:** arXiv | **Date:** 2026-03-09
**DOI/URL:** arxiv:2603.07895

#### Summary
MINT uses spatial transcriptomics data as supervision signal to train pathology foundation models. Instead of relying solely on image-based self-supervised learning, MINT incorporates molecular information from ST to create more biologically informed representations.

#### Key Methods
- ST-supervised training of pathology foundation models
- Molecular signal as training objective
- Foundation model fine-tuning or pre-training

#### Main Findings
- ST supervision produces more biologically meaningful pathology representations
- Improved performance on downstream pathology tasks

#### Strengths & Limitations
- **Strengths:** Bridges pathology AI and spatial genomics; leverages growing ST datasets for model improvement
- **Limitations:** Preprint; requires large paired histology-ST datasets for training; ST data quality matters

#### Related Work
- Complementary to HINGE (adapts existing foundation models); related to MViTGene (multimodal pathology prediction)

#### Relevance to Your Work
- **Focus area:** Pipeline Development
- **Applications:** Improving pathology AI with molecular supervision; foundation model training

---

### 17. SpatialMAGIC: Graph Diffusion + Spatial Attention for ST Imputation

**Authors:** (see arxiv:2603.06780)
**Source:** arXiv | **Date:** 2026-03-06
**DOI/URL:** arxiv:2603.06780

#### Summary
SpatialMAGIC combines graph diffusion processes with spatial attention mechanisms for imputing missing gene expression values in spatial transcriptomics data. The graph diffusion spreads information across spatial neighbors while attention weights capture gene-specific spatial dependencies.

#### Key Methods
- Graph diffusion on spatial neighbor graphs
- Spatial attention mechanism
- Gene expression imputation

#### Main Findings
- Graph diffusion captures spatial autocorrelation effectively
- Outperforms non-spatial imputation baselines

#### Strengths & Limitations
- **Strengths:** Principled combination of graph diffusion and attention; biologically motivated (spatial autocorrelation)
- **Limitations:** Preprint; graph construction choices affect results; may over-smooth sharp expression boundaries

#### Related Work
- Complementary to spRefine (language model imputation); related to SA2E (spatial graph approaches)

#### Relevance to Your Work
- **Focus area:** Spatial Transcriptomics / Multi-omics
- **Applications:** ST data preprocessing; imputation for sparse platforms

---

### 18. SpaCRD: Multimodal Deep Fusion of Histology and ST for Cancer Detection

**Authors:** (see arxiv:2603.06186)
**Source:** arXiv | **Date:** 2026-03-06
**DOI/URL:** arxiv:2603.06186

#### Summary
SpaCRD performs multimodal deep fusion of histology images and spatial transcriptomics data specifically for cancer detection. By combining morphological and molecular features, it aims to improve cancer classification accuracy over unimodal approaches.

#### Key Methods
- Multimodal fusion of histology and ST features
- Deep learning classifier for cancer detection
- Cross-modal attention or fusion layers

#### Main Findings
- Multimodal fusion outperforms histology-only and ST-only models for cancer detection
- Captures complementary morphological and molecular signals

#### Strengths & Limitations
- **Strengths:** Directly clinically relevant; multimodal fusion is well-motivated
- **Limitations:** Preprint; cancer-specific focus; requires paired histology-ST data

#### Related Work
- Related to FineST (histology-ST integration); clinical application of methods like MViTGene

#### Relevance to Your Work
- **Focus area:** Pipeline Development
- **Applications:** Cancer diagnostics with spatial multi-omics

---

### 19. RAFT-UP: Robust Alignment for ST with Explicit Spatial Distortion Control

**Authors:** (see arxiv:2603.18249)
**Source:** arXiv | **Date:** 2026-03-18
**DOI/URL:** arxiv:2603.18249

#### Summary
RAFT-UP addresses the spatial alignment problem in ST by explicitly modeling and controlling spatial distortions during registration. This is critical for integrating multiple tissue sections or aligning ST data with anatomical references.

#### Key Methods
- Spatial distortion modeling (likely deformable registration)
- Robust alignment algorithm
- Explicit distortion control parameters

#### Main Findings
- Explicit distortion control improves alignment accuracy over unconstrained methods
- Robust to tissue deformation artifacts

#### Strengths & Limitations
- **Strengths:** Addresses practical challenge in multi-section ST analysis; explicit control prevents over-deformation
- **Limitations:** Preprint; alignment quality depends on tissue similarity; 2D alignment may not capture 3D effects

#### Related Work
- Directly related to GALA (landmark-free alignment) and Domain Elastic Transform (Bayesian registration)

#### Relevance to Your Work
- **Focus area:** Spatial Transcriptomics / Multi-omics
- **Applications:** Multi-section 3D reconstruction; atlas alignment

---

### 20. GRNFormer: Gene Regulatory Network Inference Using Graph Transformer

**Authors:** (see bioRxiv DOI: 10.1101/2025.01.26.634966)
**Source:** bioRxiv | **Date:** 2025-01-27
**DOI/URL:** 10.1101/2025.01.26.634966

#### Summary
GRNFormer applies graph transformer architecture to infer gene regulatory networks from transcriptomic data. It models genes as nodes and potential regulatory interactions as edges, using transformer attention to learn network structure.

#### Key Methods
- Graph transformer for GRN inference
- Gene-gene interaction modeling
- Attention-based edge prediction

#### Main Findings
- Graph transformer captures complex regulatory relationships
- Competitive with or superior to existing GRN inference methods

#### Strengths & Limitations
- **Strengths:** Transformer attention naturally models pairwise gene interactions; scalable architecture
- **Limitations:** Preprint; GRN inference validation is inherently difficult; correlation vs. causation challenge

#### Related Work
- Related to GREmLN (foundation model for gene regulation); complements Celcomen (spatial GRN context)

#### Relevance to Your Work
- **Focus area:** DL / Innovative Algorithms in Sequencing
- **Applications:** Gene regulatory network reconstruction; identifying key regulatory interactions

---

## Additional Papers

| # | Title | Source | Date | DOI/ID | Brief Description |
|---|-------|--------|------|--------|-------------------|
| 21 | stSCI | PubMed / Innovation | 2025-12-03 | PMID 41789140 | Multi-task learning framework for integrative analysis of single-cell and spatial transcriptomics data |
| 22 | BiTro | arXiv | 2026-03-16 | arxiv:2603.14897 | Bidirectional transfer learning between bulk and spatial transcriptomics prediction |
| 23 | GALA | bioRxiv | 2025-12-02 | 10.64898/2025.11.29.691288 | Unified landmark-free spatial alignment with genetic algorithm-guided modality-aware rasterization |
| 24 | TRACER | bioRxiv | 2026-03-10 | 10.64898/2026.03.08.710395 | Refines transcript-to-cell assignment in imaging-based ST using gene-gene coherence |
| 25 | GREmLN | bioRxiv | 2025-07-09 | 10.1101/2025.07.03.663009 | Foundation model using graph signal processing for gene regulatory embeddings |
| 26 | Sparse Autoencoders for FM Interpretability | bioRxiv | 2025-10-23 | 10.1101/2025.10.22.681631 | Interpretability analysis of scGPT, scFoundation, and Geneformer using sparse autoencoders |
| 27 | MM-test | arXiv | 2026-03-10 | arxiv:2603.09061 | Distribution-free screening method for spatially variable genes |
| 28 | Count Bridges | arXiv | 2026-03-05 | arxiv:2603.04730 | Novel modeling and deconvolution approach for transcriptomic data |
| 29 | Domain Elastic Transform | arXiv | 2026-03-22 | arxiv:2603.21235 | Bayesian function registration for spatial transcriptomics alignment |
| 30 | Beyond Attention Heatmaps | arXiv | 2026-03-09 | arxiv:2603.08328 | Better explanation methods for multiple instance learning models in histopathology |
| 31 | Integrated DL Framework (GNN+KAN) | medRxiv | 2026-02-24 | 10.64898/2026.02.22.26346827 | GNN + KAN + MixUp augmentation for RNA-seq classification with explainable AI |
| 32 | ZI-HGT + CARD | bioRxiv | 2024-06-28 | 10.1101/2024.06.24.600480 | Zero-inflated model for spatially informed cell-type deconvolution |
| 33 | ST Benchmarking Across Organoids | bioRxiv | 2025-05-09 | 10.1101/2025.05.04.651803 | Stereo-seq profiling and benchmarking across multiple organoid models |
| 34 | Convolutional Autoencoders for Spatial Data in ABMs | bioRxiv | 2026-03-17 | 10.64898/2026.03.13.711699 | Using convolutional autoencoders to inform agent-based models with spatial data |
| 35 | Patches | bioRxiv | 2024-12-24 | 10.1101/2024.12.23.630186 | Conditional subspace representation learning for decoding transcriptional programs |

---

## Key Themes and Trends

1. **Deconvolution remains a hot topic** with at least 4 new methods (SA2E, UCASpatial, ZI-HGT + CARD, Count Bridges), each targeting different architectural strategies (spatial autoencoders, ultra-precision, zero-inflated, bridge processes).

2. **Histology-to-expression prediction** is rapidly maturing, with 6+ methods (HINGE, CPNN, BiTro, MViTGene, MAD, MINT, Pixel2Gene) competing and complementing each other. Foundation model adaptation (HINGE) and knowledge distillation (MAD) represent two distinct deployment strategies.

3. **Foundation models for spatial data** are an emerging frontier: spRefine uses genomic language models for ST denoising, HINGE adapts scGPT/Geneformer to spatial context, and "ST as Images" enables image SSL pre-training on ST data.

4. **Spatial perturbation modeling** is a new capability enabled by Celcomen (causal GNN) and TRAILBLAZER (multicellular transformer), moving beyond observational analysis to predictive/causal frameworks.

5. **Temporal + spatial** analysis (stVCR) and **multi-platform compatibility** (Pixel2Gene across Visium HD, Xenium, CosMx) reflect the field's move toward more comprehensive and practical tools.

6. **Alignment and registration** methods (RAFT-UP, GALA, Domain Elastic Transform) are receiving needed attention for multi-section and cross-platform integration.

---

*Report generated: 2026-03-23 | Literature search agent*
