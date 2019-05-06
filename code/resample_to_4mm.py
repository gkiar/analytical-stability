#!/usr/bin/env python

from argparse import ArgumentParser
from glob import glob
import os.path as op

from nilearn.image import resample_img
from nilearn import datasets
import nibabel as nib
import numpy as np


shapes = {1: (182, 218, 182),
          2: (91, 109, 91),
          3: (62, 74, 62),
          4: (48, 56, 48)}

def resample_images(images, outdir, resolution=4):
    # Get file list 
    if op.isdir(images):
        files = glob(op.join(images, "**", "*.nii*"), recursive=True)
        inpdir = True
    else:
        files = [images]
        inpdir = False



    if 1 <= resolution <= 4:
        target_affine = datasets.load_mni152_brain_mask().affine.copy()
        target_affine[:3,:3] = np.sign(target_affine[:3,:3]) * resolution
        target_shape = shapes[resolution]
    else:
        raise ValueError("Resolution must be between 1 mm and 4 mm, inclusive.")

    im1 = nib.load(f1)
    def _resample_to_resolution(orig_img):
        return resample_img(orig_img,
                            target_affine=target_affine,
                            target_shape=target_shape)
    


def main():
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
    parser.add_argument("resolution", action="store", type=int, default=4,
                        help="Resulting resolution in mm. Default is 4 mm.")

    results = parser.parse_args()
    resample_images(results.data, results.outdir, results.resolution)


if __name__ == "__main__":
    main()


