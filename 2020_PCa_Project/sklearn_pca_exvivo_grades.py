
#------------------------------------------------------------------------------------------
# deep learning classifier using sklearn framework
# TensorBoard support:
#   :scalars:
#     - accuracy
#     - wieghts and biases
#     - cost/cross entropy
#     - dropout
#   :images:
#     - reshaped input
#     - conv layers outputs
#     - conv layers weights visualisation
#   :graph:
#     - full graph of the network
#   :distributions and histograms:
#     - weights and biases
#     - activations
#   :checkpoint saving:
#     - checkpoints/saving model
#     - weights embeddings
#
#   :to be implemented:
#     - image embeddings (as in https://www.tensorflow.org/get_started/embedding_viz)
#     - ROC curve calculation (as in http://blog.csdn.net/mao_feng/article/details/54731098)
#--------------------------------------------------------------------------------------------

import os
import csv
import pandas as pd
import glob2 as glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn

from sklearn import datasets
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler


# ----------------------------------------------------------------------------------
# DNN paramters
# ----------------------------------------------------------------------------------
# key model parameters
n_classes = 5
solver = 'adam'                               # optimized funciton: "adam", "SGD"
activation = 'tanh'                           # "relu", "sigmoid", "tanh"
learning_rate = 'adaptive'                    # "constant", "adaptive"
learning_rate_init = 0.00008
batch_size = 'auto'                           # "auto"
momentum = 0.97
hidden_layer = (200, 200, 200, 200, 200, 200, 200, 200, 200, 200)
# routine parameters
d = 3
test_size = 0.5
random_state = 42
val_test_size = 0.3
max_iteration = 500

# ----------------------------------------------------------------------------------
# preparing data and folders
# ----------------------------------------------------------------------------------
print("PCa DNN classification ROC analysis: start...")

# # data path for windows system
# project_dir = r'\\10.39.42.102\temp\Prostate_Cancer_ex_vivo\Deep_Learning'
# result_dir = r'\\10.39.42.102\temp\Deep_Learning\pca_exvivo_grading\result'
# log_dir = r'\\10.39.42.102\temp\Deep_Learning\pca_exvivo_grading\log'

# data path for linux or mac system
project_dir = '/bmrp092temp/Prostate_Cancer_ex_vivo/Deep_Learning/'
result_dir = '/bmrp092temp/Deep_Learning/pca_exvivo_grading/result/'
log_dir = '/bmrp092temp/Deep_Learning/pca_exvivo_grading/log/'

if not os.path.exists(result_dir):
    print('result directory does not exist - creating...')
    os.makedirs(result_dir)
    print('log directory created.')
else:
    print('result directory already exists ...')

if not os.path.exists(log_dir):
       print('log directory does not exist - creating...')
       os.makedirs(log_dir)
       os.makedirs(log_dir + '/train')
       os.makedirs(log_dir + '/validation')
       print('log directory created.')
else:
    print('log directory already exists ...')

# ----------------------------------------------------------------------------------
# construct train, validation and test dataset
# ----------------------------------------------------------------------------------
maps_list = [
             'b0_map.nii',                       #07
             'dti_adc_map.nii',                  #08
             'dti_axial_map.nii',                #09
             'dti_fa_map.nii',                   #10
             'dti_radial_map.nii',               #11
             'fiber_ratio_map.nii',              #12
             'fiber1_axial_map.nii',             #13
             'fiber1_fa_map.nii',                #14
             'fiber1_fiber_ratio_map.nii',       #15
             'fiber1_radial_map.nii',            #16
             'fiber2_axial_map.nii',             #17
             'fiber2_fa_map.nii',                #18
             'fiber2_fiber_ratio_map.nii',       #19
             'fiber2_radial_map.nii',            #20
             'hindered_ratio_map.nii',           #21
             'hindered_adc_map.nii',             #22
             'iso_adc_map.nii',                  #23
             'restricted_adc_1_map.nii',         #24
             'restricted_adc_2_map.nii',         #25
             'restricted_ratio_1_map.nii',       #26
             'restricted_ratio_2_map.nii',       #27
             'water_adc_map.nii',                #28
             'water_ratio_map.nii',              #29
]

# load data from csv files and define x and y
df = pd.read_csv(os.path.join(project_dir, 'Gleason.csv'))
# df = df[~df['Sub_ID'].str.contains("SH")]

# define label class
df.loc[df['ROI_Class'] == 'G1', 'y_cat'] = 0
df.loc[df['ROI_Class'] == 'G2', 'y_cat'] = 1
df.loc[df['ROI_Class'] == 'G3', 'y_cat'] = 2
df.loc[df['ROI_Class'] == 'G5', 'y_cat'] = 3
df.loc[df['ROI_Class'] == 'G4', 'y_cat'] = 4

# balance train and validation data from each class
class0 = df[df['y_cat'] == 0]
class0_sample = class0.sample(int(class0.shape[0]))
class1 = df[df['y_cat'] == 1]
class1_sample = class1.sample(int(class1.shape[0]))
class2 = df[df['y_cat'] == 2]
class2_sample = class2.sample(int(class2.shape[0]*0.7))
class3 = df[df['y_cat'] == 3]
class3_sample = class3.sample(int(class3.shape[0]*0.12))
class4 = df[df['y_cat'] == 4]
class4_sample = class3.sample(int(class4.shape[0]))

# reconstruct dataset from balanced data
df_2 = pd.concat([class0_sample, class1_sample, class2_sample, class3_sample])

# select train, validation and test features 
X = df_2.iloc[:, [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 22, 23, 24, 25, 26, 27, 28, 29]]

# define train, validation and test labels
Y = df_2.y_cat.astype('int')

# normalize data using standard scalar 
scaler = StandardScaler()
x = scaler.fit_transform(X.astype(np.float64))

# construct train dataset with 70% slpit
x_train, x_val_test, y_train, y_val_test = train_test_split(
                                                            x,
                                                            Y,
                                                            test_size=val_test_size,
                                                            random_state=random_state
)

# construct validation and test dataset with 50% split
x_val, x_test, y_val, y_test = train_test_split(
                                                x_val_test,
                                                y_val_test,
                                                test_size=test_size,
                                                random_state=random_state
)

train_size = len(x_train)
print("data loading: complete!")
print("train set size:", len(x_train))
print("validation set size:", len(x_val))
print("test set size:", len(x_test))
print("loading data from csv file: complete!!!")
print("deep neuronetwork construction: start...")

# ----------------------------------------------------------------------------------
# construct DNN model with batch normalization layers and dropout layers
# ----------------------------------------------------------------------------------

DNN_model = OneVsRestClassifier(
                                MLPClassifier(
                                              activation=activation,
                                              hidden_layer_sizes=hidden_layer,
                                              beta_1=0.9,
                                              beta_2=0.999,
                                              alpha=0.0001,
                                              batch_size=batch_size,
                                              early_stopping=False,
                                              epsilon=1e-08,
                                              learning_rate=learning_rate,
                                              learning_rate_init=learning_rate_init,
                                              max_iter=max_iteration,
                                              momentum=momentum,
                                              nesterovs_momentum=True,
                                              power_t=0.5,
                                              random_state=None,
                                              shuffle=True,
                                              solver=solver,
                                              tol=0.0001,
                                              validation_fraction=0.1,
                                              verbose=False,
                                              warm_start=False
                                              )
)

DNN_model.fit(x_train, y_train)
print("training a DNN classifier: complete!")

# ----------------------------------------------------------------------------------
# evaluate DNN model
# ----------------------------------------------------------------------------------
y_pred = DNN_model.predict(x_val)
accuracy = accuracy_score(y_val, y_pred)
print("overall accuracy:", np.around(accuracy, d))
cm = confusion_matrix(y_val, y_pred)
print("normalized confusion matrix:")
cm_2 = cm.astype('float')/cm.sum(axis=1)[:, np.newaxis]
cm_2 = np.around(cm_2, 2)
print(cm_2)

print(classification_report(y_val, y_pred, digits=d))

# ----------------------------------------------------------------------------------
# plot confusion matrix
# ----------------------------------------------------------------------------------
ax_2 = sn.heatmap(cm_2, annot=True, annot_kws={"size": 15}, cmap="Blues", linewidths=.5)
# plt.figure(figsize = (10,7))
# sn.set(font_scale=1.4) #for label size
# plt.ylabel('True label', fontsize=13, fontweight='bold')
# plt.xlabel('Predicted label',fontsize=13, fontweight='bold')
ax_2.axhline(y=0, color='k', linewidth=3)
ax_2.axhline(y=4, color='k', linewidth=3)
ax_2.axvline(x=0, color='k', linewidth=3)
ax_2.axvline(x=4, color='k', linewidth=3)
ax_2.set_aspect('equal')
plt.savefig(os.path.join(result_dir, 'confusion_matrix.png'), format='png', dpi=600)
plt.tight_layout()
# plt.show()
# plt.close()
print("plotting confusion matrix_2: complete!")



