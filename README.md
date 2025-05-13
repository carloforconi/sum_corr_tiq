# sum_corr_tiq
Sums data from multiple .tiq files, applies frequency drift correction and injection correction, and saves the result in .npz format with an automatically generated filename based on user settings.

## Requirements
Requires numpy and [IQTools](https://github.com/xaratustrah/iqtools)

## Usage
Set the desired settings in the config.toml file:
<pre lang="markdown">  folder_path = path to the data files
  saving_path = path to the folder where you want to save the .npz file
  start_datetime = date and time to start sum the data from (Format: YYYY.MM.DD.HH.MM). 
  end_datetime = date and time to end the sum.
  lframes = frame length (number of frequency bins).
  reference_freq = reference frequency
  peak_height_cut = 50.0 
  t_cut_start = 0.5 
  t_cut_stop = 2.0 
  left = 50 
  right = 50 ```
