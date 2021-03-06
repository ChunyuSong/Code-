(* ::Package:: *)

%% flip the DBSI.nii maps 




function output = resize_images _PCa _comp _loop()  

    
   list = walkpath_wrapper('.');
                 

   for i = 1:length(list)
       folder = list{i};
       if length(folder) > 29
           break;
       end
       fprintf('Processing folder % s \n', folder);
       
       % b0
        nii = load_nii('b0_map.nii');
        img = nii.img;
 
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'b0_map.nii');

        % model_v _map
        nii = load_nii('model_v _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'model_v _map.nii');

        % dti_axial _map
        nii = load_nii('dti_axial _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'dti_axial _map.nii');

        % dti_radial _map
        nii = load_nii('dti_radial _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'dti_radial _map.nii');

        % DTI_ADC
        nii=load_nii('dti_adc _map.nii');
        img=nii.img;
         
        DTI_ADC=imresize(img,2); % interpolate iamgew with bicubic  method
        nii=make_nii(DTI_ADC);
        save_nii(nii,'DTI_ADC _map.nii');

        % DTI_FA
        nii=load_nii('dti_fa _map.nii');
        img=nii.img;
         
        DTI_FA=imresize(img,2); % interpolate iamgew with bicubic  method
        nii=make_nii(DTI_FA);
        save_nii(nii,'DTI_FA _map.nii');


        % dti_dirx _map
        nii = load_nii('dti_dirx _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'dti_dirx _map.nii');

        % dti_diry _map
        nii = load_nii('dti_diry _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'dti_diry _map.nii');

        % dti_dirz _map
        nii = load_nii('dti_dirz _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'dti_dirz _map.nii');

        % dti_rgba _map
        nii = load_nii('dti_rgba _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'dti_rgba _map.nii');

        % dti_rgba _map _itk
        nii = load_nii('dti_rgba _map _itk.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'dti_rgba _itk _map.nii');

        % dti_r _map
        nii = load_nii('dti_r _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'dti_r _map.nii');

        % dti_g _map
        nii = load_nii('dti_g _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'dti_g _map.nii');

        % dti_b _map
        nii = load_nii('dti_b _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'dti_b _map.nii');

        % fiber_ratio
        nii=load_nii('fiber_ratio _map.nii');
        img=nii.img;
         
        fiber=imresize(img,2); % interpolate iamgew with bicubic  method
        nii=make_nii(fiber);
        save_nii(nii,'fiber_ratio _map.nii');

        % fiber1_axial _map
        nii = load_nii('fiber1_axial _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'fiber1_axial _map.nii');

        % fiber1_radial _map
        nii = load_nii('fiber1_radial _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'fiber1_radial _map.nii');


        % fiber1_fa _map
        nii = load_nii('fiber1_fa _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'fiber1_fa _map.nii');


        % fiber1_fiber _ratio _map
        nii = load_nii('fiber1_fiber _ratio _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'fiber1_fiber _ratio _map.nii');


        % fiber1_rgba _map
        nii = load_nii('fiber1_rgba _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'fiber1_rgba _map.nii');

        % fiber1_dirx _map
        nii = load_nii('fiber1_dirx _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'fiber1_dirx _map.nii');

        % fiber1_diry _map
        nii = load_nii('fiber1_diry _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'fiber1_diry _map.nii');

        % fiber1_dirz _map
        nii = load_nii('fiber1_dirz _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'fiber1_dirz _map.nii');

        % fiber2_axial _map
        nii = load_nii('fiber2_axial _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'fiber2_axial _map.nii');

        % fiber2_radial _map
        nii = load_nii('fiber2_radial _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'fiber2_radial _map.nii');


        % fiber2_fa _map
        nii = load_nii('fiber2_fa _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'fiber2_fa _map.nii');


        % fiber2_fiber _ratio _map
        nii = load_nii('fiber2_fiber _ratio _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'fiber2_fiber _ratio _map.nii');

        % fiber2_dirx _map
        nii = load_nii('fiber2_dirx _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'fiber2_dirx _map.nii');

        % fiber2_diry _map
        nii = load_nii('fiber2_diry _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'fiber2_diry _map.nii');

        % fiber2_dirz _map
        nii = load_nii('fiber2_dirz _map.nii');
        img = nii.img;
         
        b0 = imresize(img,2); % interpolate iamge with bicubic  method
        nii = make_nii(b0);
        save_nii(nii,'fiber2_dirz _map.nii');

        % restricted_ratio _ 1;
        nii=load_nii('restricted_ratio _ 1_map.nii');
        img=nii.img;
         
        restricted=imresize(img,2); % interpolate iamgew with bicubic  method
        nii=make_nii(restricted);
        save_nii(nii,'restricted_ratio _ 1_map.nii');

        % restricted_adc _ 1;
        nii=load_nii('restricted_adc _ 1_map.nii');
        img=nii.img;
         
        restricted=imresize(img,2); % interpolate iamgew with bicubic  method
        nii=make_nii(restricted);
        save_nii(nii,'restricted_adc _ 1_map.nii');

        % restricted_ratio _ 2;
        nii=load_nii('restricted_ratio _ 2_map.nii');
        img=nii.img;
         
        restricted=imresize(img,2); % interpolate iamgew with bicubic  method
        nii=make_nii(restricted);
        save_nii(nii,'restricted_ratio _ 2_map.nii');

        % restricted_adc _ 2;
        nii=load_nii('restricted_adc _ 2_map.nii');
        img=nii.img;
         
        restricted=imresize(img,2); % interpolate iamgew with bicubic  method
        nii=make_nii(restricted);
        save_nii(nii,'restricted_adc _ 2_map.nii');

        % hindered_ratio
        nii=load_nii('hindered_ratio _map.nii');
        img=nii.img;
         
        hindered=imresize(img,2); % interpolate iamgew with bicubic  method
        nii=make_nii(hindered);
        save_nii(nii,'hindered_ratio _map.nii');

        % hindered_adc
        nii=load_nii('hindered_adc _map.nii');
        img=nii.img;
         
        hindered=imresize(img,2); % interpolate iamgew with bicubic  method
        nii=make_nii(hindered);
        save_nii(nii,'hindered_adc _map.nii');

        % water_ratio
        nii=load_nii('water_ratio _map.nii');
        img=nii.img;
         
        water=imresize(img,2); % interpolate iamgew with bicubic  method
        nii=make_nii(water);
        save_nii(nii,'water_ratio _map.nii');

        % water_adc
        nii=load_nii('water_adc _map.nii');
        img=nii.img;
         
        water=imresize(img,2); % interpolate iamgew with bicubic  method
        nii=make_nii(water);
        save_nii(nii,'water_adc _map.nii');

        % iso_adc
        nii=load_nii('iso_adc _map.nii');
        img=nii.img;
         
        water=imresize(img,2); % interpolate iamgew with bicubic  method
        nii=make_nii(water);
        save_nii(nii,'iso_adc _map.nii');

        % fraction_rgba _map
        nii=load_nii('fraction_rgba _map.nii');
        img=nii.img;
         
        water=imresize(img,2); % interpolate iamgew with bicubic  method
        nii=make_nii(water);
        save_nii(nii,'fraction_rgba _map.nii');

        % fiber1_rgba _map _itk
        nii=load_nii('fiber1_rgba _map _itk.nii');
        img=nii.img;
         
        water=imresize(img,2); % interpolate iamgew with bicubic  method
        nii=make_nii(water);
        save_nii(nii,'fiber1_rgba _itk _map.nii');

        disp('Generate DBSI Results: Completed!');
        
   end
end
 
function list = walkpath(list, current_path)
    fprintf('% d % s \n', length(list), current_path);
    names = dir(current_path);
    for i = 1:length(names)
        abspath = [current_path filesep names (i).name];
        % if prefix is DBSI_results
        if length(strfind(names (i).name,'DHISTO_results')) > 0
            list{end+1} = abspath;
            continue;
        end
        if exist(abspath) == 7 && strcmp(names (i).name, '.') == 0 && strcmp(names (i).name, '..') == 0            
            list = walkpath(list, abspath);
        end
    end
end


function list = walkpath_wrapper(basedir)
    list = walkpath({}, basedir);
end


















