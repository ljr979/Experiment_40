import os, re
from matplotlib import markers
from matplotlib.markers import MarkerStyle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.markers as markers
import pandas as pd
import seaborn as sns
import string
import glob 
from scipy.optimize import curve_fit

##read trajectory file csv and print out to check it
trajectory_data_files_path = 'ImageJ_Results/crosslinked-aBc-50uM/non-coloc/'

output_folder = 'python_results/tests_for_quenching/'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

##make this variable so that it can change depending on change-point on small molecules
single_mol_step = 199

##now set threshold for big vs small molecules based on this single molecule (greater than 6 molecules is deemed large)
threshold_for_filter = single_mol_step * 6
print(threshold_for_filter)


trajectories_paths = [filename for filename in os.listdir(trajectory_data_files_path) if ".csv" in filename]
all_trajectory_data = []
for filename in trajectories_paths:
    data = pd.read_csv(f'{trajectory_data_files_path}{filename}')
    # store DataFrame in list
    all_trajectory_data.append(data)
    # see pd.concat documentation for more info
   
all_trajectory_data = pd.concat(all_trajectory_data, axis=1)
all_trajectory_data.head()

#dropping first column (slice col)
all_trajectory_data.drop([col for col in all_trajectory_data.columns.tolist() if col == ' '], inplace=True, axis=1) 

#relabelling column names so there's no double names from different files
all_trajectory_data.columns = [f'mean_{x}' for x in np.arange(0,len(all_trajectory_data.columns.tolist()))]

#define function to normalise column data, to apply to filtered big and small data frames 
def normalise(df, datatype) : 

    # Get max of all columns
    max_vals = df.max() #automatically takes max of each column
    print(max_vals)

    # Normalise each column to maximum value
    norm_df = df / max_vals

    # average each row (the average of all molecule values at every slice)
    mean_per_slice = norm_df.mean(axis=1) #note axis=1 here allows you to take mean of the rows instead of the columns
    #write the file for plotting to a new csv file
    mean_per_slice.to_csv(f'{output_folder}{datatype}.csv')
    return mean_per_slice

##SMALL molecules
#filter for molecules smaller than the threshold intensity
small_stuff = [col for col in all_trajectory_data.columns.tolist() if np.max(list(all_trajectory_data[col]))< threshold_for_filter] 
smaller_molecules = all_trajectory_data[small_stuff]


#below line does same thing as above but in one line 
#smaller_molecules = all_trajectory_data.loc[:, all_trajectory_data.lt((threshold_for_filter)).any()]

#applies 'normalise' function defined above, to make data frame with row means and output small molecule info

small_molecules_mean = normalise(smaller_molecules, 'small molecules')

# Plot mean using pandas inbuilt connection with matplotlib

plt.plot(small_molecules_mean, 'seagreen', label='small molecules')
plt.ylabel('Mean normalised intensity (A.U.)')
plt.xlabel('Slice')


##LARGER molecules 
#filter for molecules brighter than threshold intensity
#bigger_molecules = all_trajectory_data.loc[:, all_trajectory_data.gt((threshold_for_filter)).any()]
#print(bigger_molecules)

big_stuff = [col for col in all_trajectory_data.columns.tolist() if np.max(list(all_trajectory_data[col]))> threshold_for_filter] 
bigger_molecules = all_trajectory_data[big_stuff]
big_molecules_mean = normalise(bigger_molecules, 'big molecules')

# #OR using seaborn to more formally define what you want to plot
# for_plotting_big = big_molecules_mean.reset_index()
# for_plotting_small = small_molecules_mean.reset_index()
# f, (ax1, ax2) = plt.subplots(1,2, sharex= 'all', sharey='all')
# ax1.sns.lineplot(data=for_plotting_big, x='index',y=0)
# ax2.sns.lineplot(data=for_plotting_small, x='index', y=0)
# plt.ylabel('Mean normalised intensity (A.U.)')
# plt.xlabel('Slice')

# #plt.savefig('')
# plt.show()



# Plot mean using pandas inbuilt connection with matplotlib
#big_mean_per_slice.plot() 
plt.plot(big_molecules_mean, 'darkorange', label='big molecules')
plt.ylabel('Mean normalised intensity (A.U.)')
plt.xlabel('Slice')
plt.title('mean fluorescence intensity per slice for molecules > 6 vs < 6')
plt.legend(loc='upper right')
plt.savefig(f'{output_folder}average_intensity_bigvssmall.png')
plt.show()




#alternatively READ IN 'STEP SIZES' which is saved here, which allows us to match molecule names from trajectories to the steps

def compare_initial_vs_stepsize(input_path):
    step_sizes = pd.read_csv(f'{input_path}')
    step_sizes.drop([col for col in step_sizes.columns.tolist() if 'Unnamed:' in col], inplace=True, axis=1) 

    last_steps_sizes= step_sizes[step_sizes['last_step']==1].copy()

    all_trajectories_raw = pd.read_csv('python_results/stoichiometries/TIRF_crosslinked_aBc/clean_data/cleaned_data.csv')
    all_trajectories_raw.drop([col for col in all_trajectories_raw.columns.tolist() if 'Unnamed:' in col], inplace=True, axis=1) 
    # collect (max) fluorescence values for each trajectory
    timepoint_columns = [col for col in all_trajectories_raw.columns.tolist() if col not in ['molecule_number']]

    max_value_dict = {}
    for molecule, df in all_trajectories_raw.groupby('molecule_number'):
        molecule, df
        max_fluorescence_value = np.max(sorted(df[timepoint_columns].values[0], reverse=True))
        key_value={molecule:max_fluorescence_value}
            # Calculate average number of molecules by mean fluorescence / step size
        max_value_dict.update(key_value)
            #calculate the average / median step size for each step type

    #now map the max values onto the step sizes dataframe
    last_steps_sizes['max_value'] = last_steps_sizes['molecule_name'].map(max_value_dict)

    wanted_cols = ['molecule_name', 'step_size', 'max_value']
    last_steps_sizes.drop(columns=[col for col in last_steps_sizes if col not in wanted_cols], inplace=True)
    return last_steps_sizes

mark=markers.MarkerStyle(marker='s')

input_path='python_results/stoichiometries/TIRF_crosslinked_aBc/fitting_changepoints/step_sizes.csv'
small_last_steps_sizes = compare_initial_vs_stepsize(input_path)

plt.subplot(1,2,1)
plt.scatter(small_last_steps_sizes["step_size"], small_last_steps_sizes["max_value"],color='darkorange', marker=mark, facecolors='none')
plt.xlabel('last photobleaching step size (A.U.)')
plt.ylabel('Initial fluorescence intensity (A.U)')
plt.title('Molecules defined as "small"')



input_path='python_results/stoichiometries/TIRF_crosslinked_aBc/ALL_MOLECULES/fitting_changepoints/step_sizes.csv'
all_last_steps_sizes = compare_initial_vs_stepsize(input_path)

plt.subplot(1,2,2)
plt.scatter(all_last_steps_sizes["step_size"], all_last_steps_sizes["max_value"],color='seagreen', marker=mark, facecolors='none')
plt.ylim(0,5000)
plt.xlabel('last photobleaching step size (A.U.)')
plt.ylabel('Initial fluorescence intensity (A.U)')
plt.title('ALL molecules')
plt.savefig(f'{output_folder}intensity_vs_laststepsize.png')
plt.show()
