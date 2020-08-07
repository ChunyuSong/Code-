%% flip the DBSI.nii maps by yzz on 04/13/2016

% b0
nii = load_nii('b0.nii')
A = nii.img
b0_reg = imresize(A,2.13) % interpolate iamge with bicubic method
nii = make_nii(b0_reg)
save_nii(nii,'b0_reg.nii')

% DTI_ADC
nii=load_nii('DTI_ADC.nii')
B=nii.img
DTI_ADC_reg=imresize(B,2.13) % interpolate iamgew with bicubic method
nii=make_nii(DTI_ADC_reg)
save_nii(nii,'DTI_ADC_reg.nii')

% DTI_FA
nii=load_nii('DTI_FA.nii')
B=nii.img
DTI_FA=imresize(B,2.13) % interpolate iamgew with bicubic method
nii=make_nii(DTI_FA)
save_nii(nii,'DTI_FA_reg.nii')

% Fiber_ratio
nii=load_nii('fiber_ratio_map.nii')
B=nii.img
BPH_reg=imresize(B,2.13) % interpolate iamgew with bicubic method
nii=make_nii(BPH_reg)
save_nii(nii,'BPH_reg.nii')

% restricted_ratio
nii=load_nii('restricted_ratio_map.nii')
B=nii.img
Lymphocytes_reg=imresize(B,2.13) % interpolate iamgew with bicubic method
nii=make_nii(Lymphocytes_reg)
save_nii(nii,'Lymphocytes_reg.nii')

% hindered_ratio
nii=load_nii('hindered_ratio_map.nii')
B=nii.img
PCa_reg=imresize(B,2.13) % interpolate iamgew with bicubic method
nii=make_nii(PCa_reg)
save_nii(nii,'PCa_reg.nii')

% water_ratio
nii=load_nii('water_ratio_map.nii')
B=nii.img
prostate_reg=imresize(B,2.13) % interpolate iamgew with bicubic method
nii=make_nii(prostate_reg)
save_nii(nii,'prostate_reg.nii')

% generate DWI_1500 image
nii = load_nii('dwi_1500.nii')
c=nii.img
dwi_1500_reg=imresize(C,2.13) % interpolate iamgew with bicubic method
nii = make_nii(dwi_1500_reg)
save_nii(nii,'dwi_1500_reg.nii')
















