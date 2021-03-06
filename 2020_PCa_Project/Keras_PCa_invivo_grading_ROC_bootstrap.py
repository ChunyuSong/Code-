#----------------------------------------------------------------------
# deep learning classifier using a multiple layer perceptron (MLP)
# batch normalization was used
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
#-------------------------------------------------------------------------------------------

import os
import timeit
import numpy as np
import pandas as pd
import seaborn as sn
import glob2 as glob
import nibabel as nib
from functools import partial
from datetime import datetime
import matplotlib.pyplot as plt
from scipy import interp
from itertools import cycle
from time import gmtime, strftime

import keras
from keras import initializers
from keras.optimizers import RMSprop
from keras.models import Sequential, Model
from keras.layers import Input, Dense, Reshape, Activation, Dropout
from keras.layers.normalization import BatchNormalization
from keras.wrappers.scikit_learn import KerasClassifier
from keras.layers.advanced_activations import ELU, LeakyReLU

import tensorflow

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.metrics import precision_recall_curve, auc
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import label_binarize
from sklearn.metrics import f1_score
from sklearn.metrics import auc
from sklearn.utils import resample



# ----------------------------------------------------------------------------------
# preparing data and folders
# ----------------------------------------------------------------------------------
def data_path():

    if not os.path.exists(result_dir):
        print('result directory does not exist - creating...')
        os.makedirs(result_dir)
        print('log directory created...')
    else:
        print('result directory already exists ...')

    if not os.path.exists(log_dir):
           print('log directory does not exist - creating...')
           os.makedirs(log_dir)
           os.makedirs(log_dir + '/train')
           os.makedirs(log_dir + '/validation')
           print('log directory created.')
    else:
        print('log directory already exists...')

# ----------------------------------------------------------------------------------
# construct train, validation and test dataset
# ----------------------------------------------------------------------------------
class PCa_data(object):
    
    '''
    calculate DNN statisical results
    '''
    
    def __init__(
                 self,
                 project_dir,
                 random_state,
                 train_split,
                 test_split,
                 ratio_1, 
                 ratio_2,
                 ratio_3, 
                 ratio_4,
                 ratio_5,
                 x_input
                 ):
                        
        self.project_dir  = project_dir
        self.random_state = random_state
        self.train_split  = train_split
        self.test_split   = test_split
        self.ratio_1      = ratio_1
        self.ratio_2      = ratio_2
        self.ratio_3      = ratio_3
        self.ratio_4      = ratio_4
        self.ratio_5      = ratio_5
        self.x_input      = x_input

    def map_list():

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
        
        return map_list
        
    def data_loading(self):

        files = glob.glob(self.project_dir + "/*.xlsx")
        
        df = pd.DataFrame()
        
        for f in files:
            data = pd.read_excel(f, 'Sheet1', header=None)
            data.iloc[:, 1:] = (data.iloc[:, 1:])/(data.iloc[:, 1:].max())
            data = data.iloc[data[data.iloc[:, 0] != 0].index]
            df = df.append(data)
        
        return df
    
    def data_balancing(self):

        df = self.data_loading()

        df.loc[df.iloc[:, 0] == 1, 'y_cat'] = 0
        df.loc[df.iloc[:, 0] == 2, 'y_cat'] = 1
        df.loc[df.iloc[:, 0] == 3, 'y_cat'] = 2
        df.loc[df.iloc[:, 0] == 4, 'y_cat'] = 3
        df.loc[df.iloc[:, 0] == 5, 'y_cat'] = 4

        class1        = df[df['y_cat'] == 0]
        class1_sample = class1.sample(int(class1.shape[0]*self.ratio_1))
        
        class2        = df[df['y_cat'] == 1]
        class2_sample = class2.sample(int(class2.shape[0]*self.ratio_2))
        
        class3        = df[df['y_cat'] == 2]
        class3_sample = class3.sample(int(class3.shape[0]*self.ratio_3))
        
        class4        = df[df['y_cat'] == 3]
        class4_sample = class4.sample(int(class4.shape[0]*self.ratio_4))
        
        class5        = df[df['y_cat'] == 4]
        class5_sample = class5.sample(int(class5.shape[0]*self.ratio_5))

        df_2 = pd.concat([
                          class1_sample,
                          class2_sample,
                          class3_sample,
                          class4_sample,
                          class5_sample
                          ])

        return df_2

    def dataset_construction(self):
        
        df_2 = self.data_balancing()

        X    = df_2.iloc[:, self.x_input]

        Y    = df_2.y_cat.astype('int')

        Y_2  = label_binarize(Y, classes=[0, 1, 2, 3, 4])

        x_train, x_test_1, y_train, y_test_1 = train_test_split(
                                                                X,
                                                                Y_2,
                                                                test_size=self.train_split,
                                                                random_state=self.random_state,
                                                                stratify=Y_2
                                                                )

        x_val, x_test, y_val, y_test = train_test_split(
                                                        x_test_1,
                                                        y_test_1,
                                                        test_size=self.test_split,
                                                        random_state=self.random_state,
                                                        stratify=y_test_1
                                                        )

        return x_train, x_val, x_test, y_train, y_val, y_test
    
# ----------------------------------------------------------------------------------
# construct DNN model with batch normalization layers and dropout layers
# ----------------------------------------------------------------------------------
class Keras_model(object):
    
    def __init__(
                 self,
                 init,
                 optimizer,
                 loss,
                 activation,
                 dropout_rate,
                 batch_momentum, 
                 n_inputs,
                 n_outputs
                 ):
        
        self.init           = init
        self.optimizer      = optimizer
        self.loss           = loss
        self.dropout_rate   = dropout_rate
        self.batch_momentum = batch_momentum
        self.n_inputs       = n_inputs
        self.n_outputs      = n_outputs
        self.activation     = activation
           
    def build_model(self):
    
        model = Sequential()

        dense_layer = partial(
                              Dense,
                              init=self.init, 
                              use_bias=False,
                              activation=None,
                              )

        batch_normalization = partial(
                                      BatchNormalization,
                                      axis=-1,
                                      momentum=self.batch_momentum,
                                      epsilon=0.001,
                                      beta_initializer='zeros',
                                      gamma_initializer='ones',
                                      beta_regularizer=None,
                                      gamma_regularizer=None                             
                                      )
                                                                  
        # input layer                              
        model.add(dense_layer(self.n_inputs, input_dim=self.n_inputs))
        model.add(batch_normalization())
        model.add(self.activation)
        model.add(Dropout(self.dropout_rate))

        # hidden layer 1
        model.add(dense_layer(n_hidden1))
        model.add(batch_normalization())
        model.add(self.activation)
        model.add(Dropout(self.dropout_rate))

        # hidden layer 2
        model.add(dense_layer(n_hidden2))
        model.add(batch_normalization())
        model.add(self.activation)
        model.add(Dropout(self.dropout_rate))

        # hidden layer 3
        model.add(dense_layer(n_hidden3))
        model.add(batch_normalization())
        model.add(self.activation)
        model.add(Dropout(self.dropout_rate))

        # hidden layer 4
        model.add(dense_layer(n_hidden4))
        model.add(batch_normalization())
        model.add(self.activation)
        model.add(Dropout(self.dropout_rate))

        # hidden layer 5
        model.add(dense_layer(n_hidden5))
        model.add(batch_normalization())
        model.add(self.activation)
        model.add(Dropout(self.dropout_rate))

        # hidden layer 6
        model.add(dense_layer(n_hidden6))
        model.add(batch_normalization())
        model.add(self.activation)
        model.add(Dropout(self.dropout_rate))

        # hidden layer 7
        model.add(dense_layer(n_hidden7))
        model.add(batch_normalization())
        model.add(self.activation)
        model.add(Dropout(self.dropout_rate))

        # hidden layer 8
        model.add(dense_layer(n_hidden8))
        model.add(batch_normalization())
        model.add(self.activation)
        model.add(Dropout(self.dropout_rate))

        # hidden layer 9
        model.add(dense_layer(n_hidden9))
        model.add(batch_normalization())
        model.add(self.activation)
        model.add(Dropout(self.dropout_rate))
                  
        # hidden layer 10
        model.add(dense_layer(n_hidden10))
        model.add(batch_normalization())
        model.add(self.activation)
        model.add(Dropout(self.dropout_rate))

        # output layer
        model.add(dense_layer(self.n_outputs))
        model.add(batch_normalization())
        model.add(Activation(output_activation))

        # optimizer functions

        #model.summary()

        model.compile(
                      loss=self.loss,
                      optimizer=self.optimizer,
                      metrics=['accuracy']
                      )
        
        return model

# ----------------------------------------------------------------------------------
# trainning DNN model
# ----------------------------------------------------------------------------------
def model_training():
    
    history = model.fit(
                        x=x_train,
                        y=y_train,
                        batch_size=batch_size,
                        epochs=epochs,
                        verbose=0,
                        callbacks=None,
                        validation_split=None,
                        validation_data=(x_val, y_val),
                        shuffle=True,
                        class_weight=None,
                        sample_weight=None,
                        initial_epoch=0,
                        steps_per_epoch=None,
                        validation_steps=None            
                        )

    score = model.evaluate(
                           x_test,
                           y_test,
                           verbose=0
                           )
    
    y_pred       = model.predict(x_test)  
    y_pred_label = np.argmax(y_pred, axis=1)

    test_loss     = score[0]
    test_accuracy = score[1]

    test_loss     = np.around(test_loss, 3)
    test_accuracy = np.around(test_accuracy, 3)
    
    return score, y_pred, test_loss, test_accuracy

# ----------------------------------------------------------------------------------
# AUC, sensitivity, specificity with 1000 bootstrap itertations
# ----------------------------------------------------------------------------------

def ROC_AUC_bootstrap(y_test, y_pred):

    """
    calculate AUC, TPR, TNR with 1000 iterations
    """
    
    AUC  = []
    THRE = []
    TNR  = []
    TPR  = []

    for i in range(n_classes):
        
        aucs  = []
        tprs  = []
        fprs  = []
        tnrs  = []
        thres = []
        
        for j in range(n_bootstrap):
            
            #print("bootstrap iteration: " + str(j+1) + " out of " + str(n_bootstrap))
            
            index = range(len(y_pred[:, i]))
            
            indices = resample(
                               index,
                               replace=True,
                               n_samples=int(len(y_pred[:, i]))
                               )

            fpr, tpr, thre = roc_curve(y_test[indices, i], y_pred[indices, i])

            q = np.arange(len(tpr))
            
            roc = pd.DataFrame(
                               {
                                'fpr' : pd.Series(fpr, index=q),
                                'tpr' : pd.Series(tpr, index=q),
                                'tnr' : pd.Series(1-fpr, index=q),
                                'tf'  : pd.Series(tpr-(1-fpr), index=q),
                                'thre': pd.Series(thre, index=q)
                                }
                               )
            
            roc_opt = roc.loc[(roc['tpr']-roc['fpr']).idxmax(),:]
       
            aucs.append(roc_auc_score(y_test[indices, i], y_pred[indices, i]))
            tprs.append(roc_opt['tpr'])
            tnrs.append(roc_opt['tnr'])
            thres.append(roc_opt['thre'])

        AUC.append(aucs)
        TPR.append(tprs)
        TNR.append(tnrs)

        total = sum([AUC, TPR, TNR], [])

    return total
        
# ----------------------------------------------------------------------------------
# mean, 95% CI
# ----------------------------------------------------------------------------------
def mean_CI(stat, confidence=0.95):
    
    alpha  = 0.95
    mean   = np.mean(np.array(stat))
    
    p_up   = (1.0 - alpha)/2.0*100
    lower  = max(0.0, np.percentile(stat, p_up))
    
    p_down = ((alpha + (1.0 - alpha)/2.0)*100)
    upper  = min(1.0, np.percentile(stat, p_down))
    
    return mean, lower, upper

def stat_summary():

    stat_sum = []
    
    ROC_AUC = np.array(total)

    for i in range(len(ROC_AUC)):
        
        stat = ROC_AUC[i]
        stat = mean_CI(stat)
        stat_sum.append(stat)
        
    stat_sum = np.array(stat_sum)
    stat_sum = np.round(stat_sum, decimals=3)
    
    return stat_sum

def stat_report():

    stat_sum = stat_summary()

    stat_df = pd.DataFrame(
                           stat_sum,
                           index=[                           
                                  'AUC_1',  
                                  'AUC_2',
                                  'AUC_3', 
                                  'AUC_4', 
                                  'AUC_5',
                                  'TPR_1',
                                  'TPR_2',
                                  'TPR_3',
                                  'TPR_4',
                                  'TPR_5',
                                  'TNR_1',
                                  'TNR_2',
                                  'TNR_3',
                                  'TNR_4',
                                  'TNR_5'
                                  ],                            
                           columns=[
                                    'mean',
                                    '95% CI -',
                                    '95% CI +'
                                    ]
                           )

    filename = str('grading_invivo') + '_' + \
               str(n_bootstrap) + '_' + \
               str(epochs) + '_' + \
               str(strftime("%d-%b-%Y-%H-%M-%S", gmtime())) + \
               '.csv'

    stat_df.to_csv(os.path.join(result_dir, filename))

    return stat_df

# ----------------------------------------------------------------------------------
# model hyper parameters
# ---------------------------------------------------------------------------------- 
if __name__ == '__main__':

    # model paramters
    n_bootstrap   = 1000
    alpha         = 0.3
    random_state  = 42
    ELU_alpha     = 1.0
    digit         = 3
    train_split   = 0.2
    test_split    = 0.5
    ratio_1       = 1
    ratio_2       = 1
    ratio_3       = 1
    ratio_4       = 1
    ratio_5       = 1
    count         = 0
    x_input       = [1, 2, 3, 8, 11, 13, 14, 18, 19, 20, 22, 26,
                     27, 28, 29, 31, 32, 33, 35, 36, 37, 38, 39, 40]
    n_inputs      = len(x_input)
    n_outputs     = 5
    n_classes     = n_outputs
    
    Learning_Rate = [0.01, 0.001, 0.1]
    Momentum      = [0.97]
    Dropout_Rate  = [0]
    Batch_Size    = [200]
    Epochs        = [10, 20]
    
    n_neurons     = 100
    n_hidden1     = n_neurons
    n_hidden2     = n_neurons
    n_hidden3     = n_neurons
    n_hidden4     = n_neurons
    n_hidden5     = n_neurons
    n_hidden6     = n_neurons
    n_hidden7     = n_neurons
    n_hidden8     = n_neurons
    n_hidden9     = n_neurons
    n_hidden10    = n_neurons

    # model functions
    init              = 'he_uniform' 
    optimizer         = 'adam'          
    loss              = 'categorical_crossentropy'
    output_activation = 'softmax'
    activation        = ELU(alpha=ELU_alpha)     
    
    '''
    keranl initializer: 'he_uniform', 'lecun_normal', 'lecun_uniform'
    optimizer function: 'adam', 'adamax', 'nadam', 'sgd'
    loss function: 'categorical_crossentropy'
    activation function: LeakyReLU(alpha=alpha)
    '''

    # data and results path 
    project_dir = r'\\10.39.42.102\temp\Prostate_Cancer_Project_Shanghai\PCa_Machine_Learning\PCA_in_vivo_data_excel'
    result_dir = r'\\10.39.42.102\temp\2019_PCa_AI\invivo_grading\result'
    log_dir = r'\\10.39.42.102\temp\2019_PCa_AI\invivo_grading\log'

    # ----------------------------------------------------------------------------------
    # run the model
    # ----------------------------------------------------------------------------------
    
    print("Deep Neural Network for PCa grade classification: start...")

    start = timeit.default_timer()
    
    data_path()

    PCa_Data = PCa_data(
                        project_dir,
                        random_state,
                        train_split,
                        test_split,
                        ratio_1, 
                        ratio_2,
                        ratio_3, 
                        ratio_4,
                        ratio_5,
                        x_input
                        )

    x_train, x_val, x_test, y_train, y_val, y_test = PCa_Data.dataset_construction()

    total_run = len(Momentum)*len(Epochs)*len(Batch_Size)*len(Learning_Rate)
    
    breaking = False

    for i in Batch_Size:
        
        for j in Momentum:
            
            for k in Epochs:

                for l in Learning_Rate:

                    for m in Dropout_Rate:

                        count += 1

                        print('\niteration: ' + str(count) + '/' + str(total_run))

                        batch_size     = i
                        batch_momentum = j
                        epochs         = k
                        learning_rate  = l
                        dropout_rate   = m
                            
                        model = Keras_model(
                                            init,
                                            optimizer,
                                            loss,
                                            activation,
                                            dropout_rate,
                                            batch_momentum,
                                            n_inputs,
                                            n_outputs
                                            ).build_model()
                        
                        score, y_pred, test_loss, test_accuracy = model_training()
                                                                
                        total = ROC_AUC_bootstrap(y_test, y_pred)

                        stat_df = stat_report()

                        print(stat_df)

                        print('\noverall test loss:  ', test_loss)
                        print('overall test accuracy:', test_accuracy)                        
                        print('epochs:        ', epochs)
                        print('batch size:    ', batch_size)
                        print('dropout rate:  ', dropout_rate)
                        print('batch momentum:', batch_momentum)
                        print('learning rate: ', learning_rate)
                        print('neuron numbers:', n_neurons)
                    
                        if test_accuracy > 0.99:
                            breaking = True

                    if breaking == True:
                        break

                if breaking == True:
                    break

            if breaking == True:
                break
            
        if breaking == True:
            break

    print('train size:     ', len(x_train))
    print('validation size:', len(x_val))
    print('test size:      ', len(x_test))
    print('bootstrap iter: ', n_bootstrap)
    
    stop = timeit.default_timer()
    running_seconds = np.around(stop - start, -1)
    running_minutes = np.around(running_seconds/60, 1)
    print('DNN running time:', running_seconds, 'sec')
    print('DNN running time:', running_minutes, 'min')


