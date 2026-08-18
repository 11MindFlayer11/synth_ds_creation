# SynthDS Creation

A modular research pipeline for generating synthetic human pose datasets using
Gaussian Splatting, COLMAP and Unity.

---

## Project Goals

This project aims to build an end-to-end pipeline capable of

- Reconstructing real-world scenes using 3D Gaussian Splatting
- Inserting animated SMPL humans into reconstructed scenes
- Rendering realistic occlusions
- Automatically generating perfect 2D and 3D pose annotations

The long-term goal is to reproduce and extend the ideas proposed in VOccl3D.

---

## Pipeline

Video

↓

Frame Extraction

↓

COLMAP

↓

Gaussian Splatting

↓

Scene Reconstruction

↓

Unity Rendering

↓

Synthetic Dataset

---

## Repository Structure

```

synth_ds_creation/

├── notebook.ipynb

├── pipeline/

├── configs/

├── README.md

└── requirements.txt

```

---

## Current Progress

- [x] Repository created
- [x] Project architecture
- [ ] Installer
- [ ] Workspace manager
- [ ] Frame extraction
- [ ] COLMAP pipeline
- [ ] Gaussian training
- [ ] Rendering
- [ ] Unity export

---

## Future Features

- Resume interrupted runs
- Batch reconstruction
- Automatic checkpointing
- Unity integration
- Dataset generation





To add a new method, 
1. add its installation in the install.py and modify the install_pipeline function
2. add the repo to config.py
3. change render, scene, train, workspace
4. 