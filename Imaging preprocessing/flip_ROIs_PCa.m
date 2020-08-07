%% flip the DBSI.nii maps by yzz on 04/13/2016
%% edited on 05/05/2016 interpolate maps by twice
%% edited by JLin on 08/10/2017 for complete dbsi parameters
%% edited by JLin on 09/15/2017 to subsitute bicubic interpolation to nearest neighbor interpolation
function output = flip_ROIs_PCa()  

    list = cellstr(ls('*_*'));

    for i = 1:length(list)
           mask = list{i};
           if length(mask) > 67
               break;
           end
           fprintf('Processing %s\n', mask);

           % b0
           loadingNifti(mask);
 
          
       
   end
        disp('Generate ROI: Completed!');
        
end

function loadingNifti(mask)

    nii = load_nii(mask);
    img = nii.img;
    img_1 = fliplr(img);
    nii = make_nii(img_1);
    save_nii(nii,mask);

end

    
        
     


















