#!/usr/bin/env python

from argparse import ArgumentParser
from glob import glob
import os.path as op
import os

from nilearn.image import resample_img
from nilearn import datasets
from scipy import ndimage
import nibabel as nib
import numpy as np

import matplotlib.pyplot as plt


shapes = {1: (182, 218, 182),
          2: (91, 109, 91),
          3: (62, 74, 62),
          4: (48, 56, 48)}

def _get_imlist(images):
    if op.isdir(images):
        files = glob(op.join(images, "**", "*.nii*"), recursive=True)
        inpdir = True
    else:
        files = [images]
        inpdir = False
    return files, inpdir


def resample_images(images, outdir, resolution=4):
    # Get file list
    files, inpdir = _get_imlist(images)

    # Determine target affine transform
    if 1 <= resolution <= 4:
        target_affine = datasets.load_mni152_brain_mask().affine.copy()
        target_affine[:3,:3] = np.sign(target_affine[:3,:3]) * resolution
        target_shape = shapes[resolution]
    else:
        raise ValueError("Resolution must be between 1 mm and 4 mm, inclusive.")

    # Define resampling function for images with the determined afine and shape
    def _resample_to_resolution(orig_img):
        return resample_img(orig_img,
                            target_affine=target_affine,
                            target_shape=target_shape,
                            interpolation='nearest')

    for idx, imfile in enumerate(files):
        try:
            if inpdir:
                fout = op.join(outdir, op.relpath(imfile, images))
            else:
                fout = op.join(outdir, op.basename(imfile))

            if op.isfile(fout):
                continue

            print("Resampling image {0} of {1}...".format(idx + 1, len(files)))
            os.system("mkdir -p {0}".format(op.dirname(fout)))
            newim = _resample_to_resolution(nib.load(imfile))
            nib.save(newim, fout)
        except Exception as e:
            print("Failed!")
            print(e)
            continue


def visualize_voxel_maps(images, outdir, resolution=4):
    # Plotting the image matrices, intentionally avoiding nilearn utils
    # because I want to see how the matrices overlap without any fanciness,
    # just like the network will receive them.

    # Get file list
    files, inpdir = _get_imlist(images)

    # load brain mask from nilearn
    mask = datasets.load_mni152_brain_mask()
    target_affine = mask.affine.copy()
    target_affine[:3,:3] = np.sign(target_affine[:3,:3]) * resolution
    target_shape = shapes[resolution]

    # resample mask image to resolution
    mask = resample_img(mask,
                        target_affine=target_affine,
                        target_shape=target_shape,
                        interpolation='nearest')
    dtype = mask.get_data_dtype()
    mask = mask.get_data().astype(int)

    # convert to boundary
    mask = ndimage.binary_closing(mask, iterations=3).astype(int)
    outer = ndimage.binary_dilation(mask, iterations=2).astype(int)
    mask = (outer - mask).astype('<f4')
    nib.save(nib.Nifti1Image(mask, affine=target_affine), 'boundary.nii.gz')

    cloud = np.zeros_like(mask)
    for idx, imfile in enumerate(files):
        try:
            print("Loading image {0} of {1}...".format(idx + 1, len(files)))
            # load map and binarize
            immap = nib.load(imfile).get_data()
            immap = (immap > 0).astype(int).astype('<f4')

            # add value to map
            cloud += immap
        except Exception as e:
            print("Failed!")
            print(e)
            continue

    # add boundary to image as largest intensity
    # cloud[mask > 0] = np.max(cloud) + 10

    cloud_img = nib.Nifti1Image(cloud, affine=target_affine)
    nib.save(cloud_img, op.join(outdir, 'pointcloud.nii.gz'))


def main():
    description = "Utility to resample nifti images in MNI space."
    parser = ArgumentParser(__file__, description=description)
    parser.add_argument("data", action="store",
                        help="Either single Nifti image file or directory to be"
                             "recursively searched for Nifti images. These "
                             "images will be resampled to the target "
                             "resolution in MNI standard space.")
    parser.add_argument("outdir", action="store",
                        help="Directory (that must exist prior to running) for "
                             "storing the resampled images. Images will be "
                             "stored in the same directory structure and name "
                             "convention as provided input(s).")
    parser.add_argument("--resolution", action="store", type=int, default=4,
                        choices=[1, 2, 3, 4],
                        help="Resulting resolution in mm. Default is 4 mm.")
    parser.add_argument("--visualize", action="store_true")

    results = parser.parse_args()
    if not results.visualize:
        resample_images(results.data, results.outdir, results.resolution)
    else:
        visualize_voxel_maps(results.data, results.outdir)


if __name__ == "__main__":
    main()
