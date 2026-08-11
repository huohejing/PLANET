import os
import numpy as np
import pandas as pd
import torch
import pickle
import sys
sys.path.append(os.path.dirname(os.path.abspath(file)))
from rdkit import Chem
from PLANET_data import load_protein_and_mols
from PLANET_model import PlanetEstimator as _PlanetEstimator # Import the original class
import argparse
class PlanetEstimator:
def init(self, device=torch.device('cpu')):
self.device = device
self.model = _PlanetEstimator() # Use the original model class
# Load parameters, ensuring they go to the specified device
self.model.load_parameters('PLANET.param', map_location=self.device)
self.model.to(self.device) # Move the model to the specified device
self.model.eval()
text

编辑



def workflow(self, protein_file, mol_file, prefix, center_x=None, center_y=None, center_z=None):
    # Ensure device is CPU here as well
    device = torch.device('cpu')

    print(f'Loading data from {mol_file} and {protein_file}')
    data_loader = load_protein_and_mols(protein_file, mol_file, center_x=center_x, center_y=center_y, center_z=center_z)

    results = []
    smiles_list = []

    print('Start predicting...')
    for i, batch in enumerate(data_loader):
        print(f'Processing molecule {i+1}/{len(data_loader.dataset)}', end='\r')
        try:
            # The batch should already be on the correct device (CPU) based on load_protein_and_mols
            # If load_protein_and_mols doesn't handle device, you might need to move it here:
            # batch = batch.to(device) # Uncomment if necessary, but ideally handled in data loading

            with torch.no_grad():
                output = self.model(batch)
                pred = torch.sigmoid(output).item() # Apply sigmoid and get scalar value

            smiles = batch.smiles # Assuming batch has a smiles attribute
            results.append(pred)
            smiles_list.append(smiles)

        except Exception as e:
            print(f"\nError processing molecule {i+1}: {e}")
            # Append NaN or a specific flag for failed molecules
            results.append(np.nan)
            smiles_list.append("FAILED") # Or append the original SMILES if available from input list

    print('\nSaving results...')
    df = pd.DataFrame({'SMILES': smiles_list, 'Score': results})
    csv_name = f'{prefix}.csv'
    sdf_name = f'{prefix}.sdf'

    df.to_csv(csv_name, index=False)

    # Write SDF with scores
    supplier = Chem.SDMolSupplier(mol_file)
    writer = Chem.SDWriter(sdf_name)
    for i, mol in enumerate(supplier):
        if mol is not None:
            # Add the score as a property
            score_val = results[i] if i < len(results) else np.nan
            mol.SetProp('PLANET_Score', str(score_val))
            writer.write(mol)
    writer.close()

    print(f'Results saved to {csv_name} and {sdf_name}')
def main():
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--protein', type=str, required=True)
parser.add_argument('-l', '--ligand', type=str, default=None) # Optional ligand for pocket definition
parser.add_argument('-x', '--center_x', type=float, default=None)
parser.add_argument('-y', '--center_y', type=float, default=None)
parser.add_argument('-z', '--center_z', type=float, default=None)
parser.add_argument('-m', '--mol_file', type=str, required=True)
parser.add_argument('--prefix', type=str, required=True)
args = parser.parse_args()
text

编辑



# Note: This simplified version doesn't use -l argument directly within this script.
# It relies on PLANET_data.load_protein_and_mols to handle pocket definition,
# potentially using the ligand info internally if provided alongside the protein file
# or via center coordinates.

protein_file = args.protein
mol_file = args.mol_file
prefix = args.prefix
center_x, center_y, center_z = args.center_x, args.center_y, args.center_z

estimator = PlanetEstimator()
estimator.workflow(protein_file, mol_file, prefix, center_x, center_y, center_z)
if name == 'main':
main()