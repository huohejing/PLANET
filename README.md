# PLANET: Protein-Ligand Affinity prediction NETwork

> **Original work by [ComputArtCMCG](https://github.com/ComputArtCMCG/PLANET).**
> This is a bugfixed, CPU-ready version maintained for personal use and community convenience.
> All credit for the model architecture, training strategy, and research belongs to the original authors.

PLANET is a graph neural network for predicting protein-ligand binding affinity. It takes the 3D structure of a binding pocket (Cα coordinates + residue types) and the 2D graph of a ligand molecule as inputs, and predicts binding affinity without conformational sampling — making it ~100× faster than traditional docking for virtual screening.

## Key features

- **No 3D ligand conformation needed** — works directly from SMILES or 2D SDF
- **Multi-task training** — jointly learns binding affinity, protein-ligand contact maps, and intra-ligand distances
- **CASF-2016 benchmark** — comparable scoring power to 3D complex-based methods
- **DUD-E virtual screening** — outperforms GLIDE SP at <1% of the compute time

## Quick start

```bash
# Create environment
conda env create -f planet.yaml
conda activate planet

# Or use an existing env with torch + rdkit installed
cd PLANET
python PLANET_runn.py -p <protein.pdb> -l <crystal_ligand.sdf> -m <mols.sdf> --prefix result
```

### Parameters

| Flag | Description |
|------|-------------|
| `-p` / `--protein` | Protein structure file (.pdb) |
| `-l` / `--ligand` | Crystal ligand (.sdf) for defining binding pocket center |
| `-x, -y, -z` | Manual pocket center coordinates (alternative to `-l`) |
| `-m` / `--mol_file` | Molecules to score (.sdf or .smi) |
| `--prefix` | Output prefix (default: `result`) |

### Output

- `{prefix}.csv` — SMILES + PLANET affinity scores
- `{prefix}.sdf` — molecules with `PLANET_affinity` property

### Protein preparation

The protein .pdb must have correct Cα atoms. Use Maestro *prepwizard* or equivalent to fix broken residues and assign protonation states. Residues within 12 Å of the pocket center are included.

## Files

| File | Purpose |
|------|---------|
| `PLANET_runn.py` | **Inference entry point** (bugfixed, CPU-ready) |
| `PLANET_model.py` | Model architecture (PLANET class) |
| `layers.py` | GNN layers: ProteinEGNN, LigandGAT, ProLig |
| `chemutils.py` | Molecular featurization, protein pocket parsing |
| `DUDE.py` | DUD-E virtual screening evaluation |
| `PLANET_train.py` | Training script |
| `PLANET_datautils.py` | Data loading from PDBbind |
| `PLANET_test.py` | CASF-2016 benchmark evaluation |

## Fixes in this version

- Removed hardcoded `.cuda()` calls — runs on CPU by default
- Fixed `nnutils.create_var` to not force GPU transfer
- `PLANET_runn.py`: cleaned-up inference script with proper device handling
- Compatible with modern PyTorch (tested on 1.12+)

## Original paper

Zhang et al. *PLANET: A Multi-Objective Graph Neural Network Model for Protein-Ligand Binding Affinity Prediction.* (in preparation)

## License

This repository follows the license terms of the [original PLANET repository](https://github.com/ComputArtCMCG/PLANET).
