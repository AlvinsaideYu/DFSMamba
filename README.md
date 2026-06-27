# DFSMamba

**DFSMamba: A Spatial–Frequency Collaborative Modeling Framework for Remote Sensing Image Super-Resolution**

The paper has been officially accepted. We will release the complete source code and supporting dataset in this repository shortly.

---

## Paper Information

**Title**: DFSMamba: A Spatial–Frequency Collaborative Modeling Framework for Remote Sensing Image Super-Resolution

**Journal**: Remote Sensing, 2026, 18(12), 1910

**DOI**: https://doi.org/10.3390/rs18121910

---

## Abstract

Existing single-image super-resolution methods for remote sensing images suffer from insufficient global receptive fields, weak high-frequency texture recovery, and excessive computational complexity. To address these issues, this paper proposes **DFSMamba**, a novel spatial–frequency collaborative modeling framework.First, **Semantic Continuous-Sparse Attention** enhances semantic perception through dynamic chunking and sparse connections while maintaining linear complexity, effectively alleviating the semantic truncation problem caused by fixed window partitioning.Second, the **Adaptive State-Space Module** employs parallel forward and backward state-space model branches to achieve bidirectional long-range dependency modeling and introduces an activation-guided feature fusion mechanism to adaptively enhance semantically relevant regions.Third, the **Discrete Fourier Transform Module** maps images to the frequency domain, establishes a global lossless receptive field, and explicitly enhances high-frequency details, compensating for the insufficient utilization of frequency-domain information in pure spatial-domain methods.Experiments on five public datasets demonstrate that DFSMamba outperforms mainstream CNN-, Transformer-, and Mamba-based methods across ×2 to ×4 scales. On the AID×3 task, it achieves a PSNR of **31.48 dB**, exceeding MambaIRv2 by **1.07 dB**. Ablation studies verify the positive synergistic effect of the three modules, with the full configuration achieving a PSNR improvement of **0.85 dB** over the single-module setup. Fine-grained category, multi-scale input, and loss function experiments further confirm its robustness and generalization capability, particularly in edge and texture detail reconstruction.

---

## Framework Overview

DFSMamba is designed for remote sensing image super-resolution by jointly modeling spatial semantics and frequency-domain details. The framework mainly consists of three key components:

1. **Semantic Continuous-Sparse Attention**

   * Enhances semantic perception through dynamic chunking and sparse connections.
   * Maintains linear computational complexity.
   * Alleviates semantic truncation caused by fixed window partitioning.

2. **Adaptive State-Space Module**

   * Uses parallel forward and backward state-space branches.
   * Captures bidirectional long-range dependencies.
   * Introduces activation-guided feature fusion to strengthen semantically relevant regions.

3. **Discrete Fourier Transform Module**

   * Maps features into the frequency domain.
   * Establishes a global lossless receptive field.
   * Explicitly enhances high-frequency texture and edge details.

---

## Repository Status

The framework and codebase are still under continuous polishing.

The following materials will be released shortly:

* Complete source code
* Training and testing scripts
* Supporting dataset information
* Pre-trained models
* Experimental configuration files
* Detailed usage instructions

Please stay tuned for updates.

---

## Citation

If you find our work beneficial to your research, please cite our paper as follows:

```bibtex
@article{DFSMamba2026,
  title={DFSMamba: A Spatial–Frequency Collaborative Modeling Framework for Remote Sensing Image Super-Resolution},
  journal={Remote Sensing},
  volume={18},
  number={12},
  pages={1910},
  year={2026},
  doi={10.3390/rs18121910}
}
```

---

## Feedback & Discussion

The framework and codebase are still under continuous polishing. We sincerely welcome all valuable suggestions, questions, and constructive criticisms regarding our spatial–frequency collaborative modeling strategy, experimental settings, and remote sensing super-resolution tasks.

Feel free to open an issue in this repository if you have any confusion or thoughts for improvement.

---

## Contact

For questions, suggestions, or academic discussion, please open an issue in this repository.

---
