import os
import numpy as np
import matplotlib.pyplot as plt
import toml
from iqtools import get_iq_object, plotters
import math
from datetime import datetime

def extract_datetime_from_filename(filename):
    """Extracts datetime object from a filename of format RSA01-YYYY.MM.DD.HH.MM.SS.*"""
    try:
        parts = filename.split('-')[1].split('.')
        dt_str = '.'.join(parts[:6])
        return datetime.strptime(dt_str, "%Y.%m.%d.%H.%M.%S")
    except Exception:
        return None

def get_files_in_range(folder_path, start_dt_str, end_dt_str):
    """Gets files within a datetime range (inclusive)"""
    start_dt = datetime.strptime(start_dt_str, "%Y.%m.%d.%H.%M")
    end_dt = datetime.strptime(end_dt_str, "%Y.%m.%d.%H.%M")

    file_list = sorted(os.listdir(folder_path))
    matching_files = []

    for file in file_list:
        if not file.startswith("RSA01-"):
            continue
        file_dt = extract_datetime_from_filename(file)
        if file_dt and start_dt <= file_dt <= end_dt:
            matching_files.append(os.path.join(folder_path, file))

    return matching_files

def main():
    config = toml.load("config.toml")
    folder_path = config["folder_path"]
    saving_path = config["saving_path"]
    start_datetime = config["start_datetime"]
    end_datetime = config["end_datetime"]
    lframes = config["lframes"]
    reference_freq = config["reference_freq"]
    peak_height_cut = config["peak_height_cut"]
    t_cut_start = config["t_cut_start"]
    t_cut_stop = config["t_cut_stop"]
    left = config["left"]
    right = config["right"]

    files = get_files_in_range(folder_path, start_datetime, end_datetime)
    if not files:
        print("No matching files found.")
        return

    filename_1 = os.path.basename(files[0])
    filename_2 = os.path.basename(files[-1])
    parts_1 = filename_1.split('.')
    parts_2 = filename_2.split('.')
    date_part = '.'.join(parts_1[:3])
    start_time = f"{parts_1[3]}:{parts_1[4]}"
    end_time = f"{parts_2[3]}:{parts_2[4]}"
    combined_name = f"{date_part}_{start_time}_{end_time}"

    iq = get_iq_object(files[0])
    nframes = math.floor(iq.nsamples_total / lframes)
    iq.read(lframes=lframes, nframes=nframes)
    iq.method = "fftw"
    xx0, yy0, zz0 = iq.get_power_spectrogram(lframes=lframes, nframes=nframes)

    zz_sum = np.zeros_like(zz0)
    zz_freq_corr_sum = np.zeros_like(zz0)
    zz_inj_corr = np.zeros_like(zz0)
    zz_inj_corr_sum = np.zeros_like(zz0)

    freq_bin_size = iq.fs / lframes
    t_bin_size = 1 / freq_bin_size
    nsamples_total = iq.nsamples_total
    fs = nsamples_total / yy0[-1][0]
    center_freq = iq.center

    x_cut_start = int(lframes/2) - left
    x_cut_stop = int(lframes/2) - right
    y_bin_start = int(t_cut_start / t_bin_size)
    y_bin_stop = int(t_cut_stop / t_bin_size)
    peak_height_list = []

    bandwidth = lframes * freq_bin_size
    reference_bin = int((reference_freq - center_freq + bandwidth/2) / freq_bin_size)

    for file in files:
        iq = get_iq_object(file)
        iq.read(lframes=lframes, nframes=nframes)
        iq.method = "fftw"
        xx, yy, zz = iq.get_power_spectrogram(lframes=lframes, nframes=nframes)

        zz_sum += zz
        zz_window = zz[y_bin_start:, x_cut_start:x_cut_stop]
        proj_x = zz_window.sum(axis=0)
        max_idx = np.argmax(proj_x)
        peak_height = proj_x[max_idx]
        index = x_cut_start + max_idx
        bin_shift = int(round(index - reference_bin))
        peak_height_list.append(peak_height)

        if peak_height > peak_height_cut:
            zz_shifted = np.roll(zz, shift=-bin_shift, axis=1)
            zz_freq_corr_sum += zz_shifted
            ref_idx = np.argmax(zz_shifted[y_bin_start:, x_cut_start:x_cut_stop].sum(axis=0))
            for i in range(len(zz)):
                bin_diff = np.argmax(zz_shifted[i, x_cut_start:x_cut_stop]) - ref_idx
                zz_inj_corr[i] = np.roll(zz_shifted[i], shift=-bin_diff)
            zz_inj_corr_sum += zz_inj_corr

    np.savez(f"{saving_path}summed_{combined_name}_cut={peak_height_cut}.npz", xx=xx+iq.center, yy=yy, zz_sum=zz_sum, zz_freq_corr_sum=zz_freq_corr_sum, zz_inj_corr_sum=zz_inj_corr_sum)
    np.savez(f"{saving_path}PID/{combined_name}_cut={peak_height_cut}.npz", arr_0=(xx+iq.center).flatten(), arr_1=(zz_freq_corr_sum).flatten())
    
    # Histogram
    fig, ax = plt.subplots()
    counts, bins, patches = ax.hist(peak_height_list, bins=50, edgecolor='black', alpha=0.7)
    ax.axvline(x=peak_height_cut, color='red', linestyle='dotted', linewidth=2)
    textstr = '\n'.join([
        f'Entries   : {len(peak_height_list):>8}',
        f'Mean      : {np.mean(peak_height_list):>8.2f}',
        f'Std Dev   : {np.std(peak_height_list):>8.2f}',
        f'Integral  : {np.sum(peak_height_list):>8.2f}'
    ])
    props = dict(boxstyle='square', facecolor='white', edgecolor='black')
    ax.text(0.95, 0.95, textstr, transform=ax.transAxes, fontsize=10,
            fontfamily='monospace', verticalalignment='top', horizontalalignment='right', bbox=props)
    ax.set_xlim(0, 300)
    plt.xlabel(r'Height of $^{194}Pb^{82+}$')
    plt.ylabel('Number of Occurrences')
    plt.title('Histogram of Quantity')
    plt.grid(True)
    plt.savefig(f"{saving_path}Histogram_{combined_name}_cut={peak_height_cut}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    main()
