from analysis_scripts.py4bleaching.py4bleaching import analysis


input_folder = 'ImageJ_Results/crosslinked-aBc-50uM/'
output_folder = 'python_results/stoichiometries/TIRF_crosslinked_aBc/'

#change this according to the model that you'd like to use (from the repo with all the models)
model_name = 'Model_3'


analysis.pipeline(input_folder, output_folder, probability_threshold=0.4, model_name=model_name)

#below script is to PLOT the distributions of the molecule sizes in a violin plot, for colocalised and non-colocalised hsp27 and CLIC


input_folder='python_results/stoichiometries/'
stoich_files =[[f'{root}/{filename}' for filename in files if 'molecule_counts.csv' in filename] for root, dirs, files in os.walk(f'{input_folder}')]
stoich_files=[item for sublist in stoich_files for item in sublist]

import pandas as pd
molecule_counts=[]

for filepath in stoich_files:
    data= pd.read_csv(filepath)
    treatments = data.treatment
    timepoints=[]
    for item in treatments:
        timepoint=item.split('-')[0]
        timepoints.append(timepoint)
    data['timepoint']=timepoints

    molecule_counts.append(data)

molecule_counts=pd.concat(molecule_counts)
molecule_counts.drop([col for col in molecule_counts.columns.tolist() if ' ' in col], axis=1, inplace=True)
molecule_counts.drop([col for col in molecule_counts.columns.tolist() if 'all_small_mol_count' in col], axis=1, inplace=True)
molecule_counts.drop([col for col in molecule_counts.columns.tolist() if 'single_step_mol_count' in col], axis=1, inplace=True)
molecule_counts.drop([col for col in molecule_counts.columns.tolist() if 'max_fluorescence' in col], axis=1, inplace=True)
molecule_counts['protein'] = molecule_counts['protein'].replace({'aB-c':'hsp27'})

def remove_outlier(dataFrame, col_name='last_step_mol_count', threshold=30):
    return dataFrame[dataFrame[col_name] < threshold]

molecule_counts=remove_outlier(molecule_counts)

coloc_molecules=molecule_counts[molecule_counts['colocalisation']=="Coloc"]


non_coloc_molecules=molecule_counts[molecule_counts['colocalisation']=="Non-coloc"]


import seaborn as sns
import matplotlib.pyplot as plt

output_folder='python_results/stoichiometries/'

for group, df in molecule_counts.groupby(['colocalisation']): 
    df=pd.melt(df, id_vars=['timepoint','protein', 'colocalisation', 'molecule_number', 'treatment'], value_vars=['last_step_mol_count'])
    fig, ax = plt.subplots()
    ax = sns.violinplot(x="timepoint", y="value", hue="protein", data=df, order=['zero', '20min', '40min', '60min', '4h', '7h'], palette='viridis')
    ax.set_ylabel('# of subunits')
    plt.title(f'{group}')
    plt.savefig(f'{output_folder}{group}_stoichiometries.png')
    plt.show()