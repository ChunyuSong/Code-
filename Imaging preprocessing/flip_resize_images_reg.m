(* ::Package:: *)


% b0
nii = load_nii('b0_map.nii');
A = nii.img;
A1 = flipdim(A,2); % flip iamges vertically;
b0 = imresize(A1,4.27); % interpolate iamge with bicubic method;
nii = make_nii(b0);
save_nii(nii,'b0_reg.nii');

% DTI_ADC
nii=load_nii('dti_adc _map.nii');
B=nii.img;
B1=flipdim(B,2); % flip iamges vertically;
DTI_ADC=imresize(B1,4.27);% interpolate iamgew with bicubic method;
nii=make_nii(DTI_ADC);
save_nii(nii,'DTI_ADC _reg.nii');

% DTI_FA;
nii=load_nii('dti_fa _map.nii');
B=nii.img;
B1=flipdim(B,2); % flip iamges vertically;
DTI_FA=imresize(B1,4.27);% interpolate iamgew with bicubic method;
nii=make_nii(DTI_FA);
save_nii(nii,'DTI_FA _reg.nii');

% Fiber_ratio
nii=load_nii('fiber_ratio _map.nii');
B=nii.img;
B1=flipdim(B,2); % flip iamges vertically;
BPH=imresize(B1,4.27); % interpolate iamgew with bicubic method;
nii=make_nii(BPH);
save_nii(nii,'BPH_reg.nii');

% restricted_ratio
nii=load_nii('restricted_ratio _map.nii');
B=nii.img;
B1=flipdim(B,2); % flip iamges vertically;
Lymphocytes=imresize(B1,4.27); % interpolate iamgew with bicubic method;
nii=make_nii(Lymphocytes);
save_nii(nii,'Lymphocytes_reg.nii');

% hindered_ratio
nii=load_nii('hindered_ratio _map.nii');
B=nii.img;
B1=flipdim(B,2); % flip iamges vertically;
PCa=imresize(B1,4.27); % interpolate iamgew with bicubic method;
nii=make_nii(PCa);
save_nii(nii,'PCa_reg.nii');

% water_ratio
nii=load_nii('water_ratio _map.nii');
B=nii.img;
B1=flipdim(B,2); % flip iamges vertically;
prostate=imresize(B1,4.27); % interpolate iamgew with bicubic method;
nii=make_nii(prostate);
save_nii(nii,'prostate_reg.nii');

% generate DWI_ 1500 image
nii = load_nii('dti_adc _map.nii');
adc=nii.img;
b0=load_nii('b0_map.nii');
b0=b0.img;
C=b0.*exp(-1.5*adc);
C1=flipdim(C,2); % flip iamges vertically
dwi_ 1500=imresize(C1,4.27); % interpolate iamgew with bicubic method
nii = make_nii(dwi_ 1500);
save_nii(nii,'dwi_ 1500_reg.nii');
















