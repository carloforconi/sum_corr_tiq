# sum_corr_tiq
Sums data from multiple `.tiq` files, applies frequency drift correction and injection correction, and saves the result in `.npz` format with an automatically generated filename based on user settings.

## Installation
- Download and install [IQTools](https://github.com/xaratustrah/iqtools) from [@xaratustrah](https://github.com/xaratustrah).  
- Download or clone the repository:  
```
git clone https://github.com/carloforconi/sum_corr_tiq.git
```
- Then, in the cloned repository:
```
pip install .
```


## Usage
Set the config.toml file:
``` folder_path = path to the data files
  saving_path = path to the folder where you want to save the .npz file
  start_datetime = date and time to start sum the data from (Format: YYYY.MM.DD.HH.MM) 
  end_datetime = date and time to end the sum
  lframes = frame length (number of frequency bins)
  reference_freq = reference frequency [Hz]
  peak_height_cut = minimum intensity level for applying the cut 
  t_cut_start = time after which there is no injection effect on frequency
  t_cut_stop = final time
  left = frequency bin at the left of the main peak to isolate it (default: 50)
  right = frequency bin at the right of the main peak to isolate it (default: 50)
```

Run the script:
```
python sum_corr_tiq.py 
```
### Results
The output file name is generated in this format: `summed_(RSA_name)-(start_date)_(start_time)_(end_time)_cut=(cut).npz` (for example: `summed_RSA01-2024.05.16_00:30_00:40_cut=51.npz`).   
The `npz` file contains data of the frequency, time, and intensities (raw summed intensities, summed intensities with frequency drift correction, summed intensities with frequency drift and injection correction).

## License 
Please see the file [LICENSE](https://github.com/carloforconi/sum_corr_tiq/blob/main/LICENSE) for further information about how the content is licensed.




