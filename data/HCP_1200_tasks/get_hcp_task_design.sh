#!/bin/bash

source ~/code/env/gp3/bin/activate

task=${1}
nsubs=${2}

# Get subject list
# N.B.: replace `head` with `tail` if you want the last N instead...
subjs=$(aws --profile=hcp \
            s3 ls \
            s3://hcp-openaccess/HCP_1200/ | \
            awk '{ print $2 }' | \
            cut -d '/' -f 1 | \
            head -${nsubs})

# Download corresponding fsf and event files for the task
for sub in ${subjs};
do
  echo ${sub}
  mkdir -p ${sub}
  aws --profile=hcp \
      s3 cp --recursive \
      --exclude="*" \
      --include="tfMRI_${task}*fsf" \
      --include="tfMRI_${task}*EVs*" \
      s3://hcp-openaccess/HCP_1200/${sub}/MNINonLinear/Results/ \
      ${sub}
done

