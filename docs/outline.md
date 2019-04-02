# Analytical Stability

The goal of this project is to better understand the variability and stability of commonly used processing tools in functional MRI.
First, this requires understanding properties of statistical parametric maps (SPMs), such as a low-dimensional representiation, and the relationships between maps developed by various software packages.
Second, we need to develop understanding of the stability of these tools and maps so that we can verify the trustworthiness of these mappings.

The main steps which need to be completed for this project to be successful are:

***Understanding Variability***

1. Identify a low-dimensional representation (LDR) for publicly available functional SPMs
2. Generate SPMs using known data + tool combinations
3. Learn LDR for each tool
4. Learn mapping from tool-LDRs to the common LDR 


***Characterizing Stability***

1. Generate noisy SPM estimates
2. Re-learn LDRs for noisy settings
3. Learn mapping from noisy-LDR settings to noiseless-LDR in each tool
4. Evaluate the stability of the mapping within tools


### Understanding Variability

#### 1. Identify LDR

- [ ] Crawl Neurovault for all SPMs
- [ ] Determine model for generating LDR (i.e. PCA? tSNE?)
- [ ] Learn LDR using split-half resampling to prevent overfitting

#### 2. Generate SPMs

- [ ] Create Boutiques descriptors for:
  - [ ] FSL
  - [ ] AFNI
  - [ ] SPM (if possible?)
- [ ] Determine pipelines & parameters for generating SPMs
- [ ] Process datasets:
  - [ ] CoRR
  - [ ] HCP
  - [ ] OpenNeuro

#### 3. Learn Tool-LDRs

- [ ] Re-train the model in 1. above using tool-partitioned subsets
- [ ] Re-train the model in 1. above using data-partitioned subsets

#### 4. Learn Tool-LDR to Common-LDR Mapping

- [ ] Determine method for mapping between all LDR-spaces
- [ ] Train method
- [ ] Evaluate

### Characterizing Stability

#### 1. Generate Noisy SPMs

- [ ] Add variable noise levels to images
- [ ] Generate SPMs using the same methods as above

#### 2. Learn Tool-LDR for Each Noise Setting

- [ ] Learn more LDRs using the same method as above

#### 3. Learn Noisy-LDR to Tool-LDR (noiseless) Mapping

- [ ] Learn mapping using the samd method as above

#### 4. Evaluate Stability of Mapping Within Tools

- [ ] Compute condition number of maps
- [ ] Compute the variance of the differences between maps

