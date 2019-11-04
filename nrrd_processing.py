from os import path, mkdir
import nrrd
import numpy as np
import matplotlib.pyplot as plt


# sample code for opening PET and CT files in nrrd format, cutting the head region, printing some data from the header,
# and saving them again.


def sample_stack(stack, rows=6, cols=6, start_with=10, show_every=3):
    fig, ax = plt.subplots(rows, cols, figsize=[12, 12])
    for i in range(rows * cols):
        ind = start_with + i * show_every
        ax[int(i / rows), int(i % rows)].set_title('slice %d' % ind)
        ax[int(i / rows), int(i % rows)].imshow(stack[:, :, ind], cmap='gray')
        ax[int(i / rows), int(i % rows)].axis('off')


if __name__ == '__main__':
    # directory of patient data
    data_dir = 'D:\Christina\Data\PET-CT LKH'
    # directory to save outputs to
    dest_dir = 'D:\Christina\Data\PET-CT LKH\Database_for_upload'
    patient = 'Pat1'
    ct_path = path.join(data_dir, patient, 'PET-CT', patient + '_CT.nrrd')
    pet_path = path.join(data_dir, patient, 'PET-CT', patient + '_PET.nrrd')
    dest_dir = path.join(dest_dir, patient)

    # Create target Directory if it doesn't exist
    if not path.exists(dest_dir):
        mkdir(dest_dir)

    # read nrrd files
    print('reading files...')
    ct_data, ct_header = nrrd.read(ct_path)
    pet_data, pet_header = nrrd.read(pet_path)

    # parse nrrd header for spacing
    ct_spacing = np.asarray([ct_header['space directions'][0, 0],
                             ct_header['space directions'][1, 1],
                             ct_header['space directions'][2, 2]])

    pet_spacing = np.asarray([pet_header['space directions'][0, 0],
                              pet_header['space directions'][1, 1],
                              pet_header['space directions'][2, 2]])

    print('cut...')
    # cut the head region. if the head is approx 25 cm high, calculate the number of slices using the slice thickness
    height = 250
    num_slices_ct = int(height / ct_spacing[2])
    ct_data = ct_data[:, :, -num_slices_ct:]

    num_slices_pet = int(height / pet_spacing[2])
    pet_data = pet_data[:, :, -num_slices_pet:]

    # print data information
    print('CT: ')
    print(' Volume Size')
    print(ct_data.shape)
    print(' Resolution')
    print(ct_spacing)
    print('PET: ')
    print(' Volume Size')
    print(pet_data.shape)
    print(' Resolution')
    print(pet_spacing)

    # save the files
    print('writing files...')
    nrrd.write(path.join(dest_dir, patient + '_CT.nrrd'), ct_data, ct_header)
    nrrd.write(path.join(dest_dir, patient + '_PET.nrrd'), pet_data, pet_header)
    print('done.')
