# sum_corr_tiq
Sums data from multiple .tiq files, applies frequency drift correction and injection correction, and saves the result in .npz format with an automatically generated filename based on user settings.

## Requirements
Requires numpy and [IQTools](https://github.com/xaratustrah/iqtools)

## Run
After setting properly the config.toml file, run the script:
<pre lang="markdown"> python sum_corr_tiq.py </pre>

The output name is generated in this format:
<pre lang="markdown"> summed_(RSA_name)-(start_date)_(start_time)_(end_time)_cut=(cut).npz </pre>


## Usage
Set the desired settings in the config.toml file:
<pre lang="markdown">  folder_path = path to the data files
  saving_path = path to the folder where you want to save the .npz file
  start_datetime = date and time to start sum the data from (Format: YYYY.MM.DD.HH.MM). 
  end_datetime = date and time to end the sum.
  lframes = frame length (number of frequency bins).
  reference_freq = reference frequency
  peak_height_cut = minimum intensity level for applying the cut  
  t_cut_start = time after injection effect on frequency
  t_cut_stop = final time
  left = frequency bin at the left of the main peak to isolate it (default: 50)
  right = frequency bin at the right of the main peak to isolate it (default: 50)</pre>
