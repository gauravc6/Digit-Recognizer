# Digit Recognizer
### Description
* A Convolutional Neural Network model built into a script to work on real life digit images.
* Model has been trained with data augmentation using keras' ImageDataGenerator to make it more robust on real life images.
* The script uses various image processing techniques such grayscale, threshold, dilate and resize to get overall better performance
* The script also has a GUI based thresholding option to adapt to different lighting conditions.


![Screenshot](https://raw.githubusercontent.com/gauravc6/Digit-Recognizer/master/Screenshot.png)

### Get it running
* First create a conda enviroment using `conda create --name env python=3.7`
* Activate the environment using `source activate env` for mac/linux users or `activate env` for windows users.
* Install requirements using `conda install tensorflow keras opencv` for CPU only or `conda install tensorflow-gpu keras opencv` for GPU acceleration support.
* Next to run the script simply do `python recognizeDigits.py`.

### Other Info
* `DigitsMNIST.ipynb` contains code used to create the model.
* Dataset - https://www.kaggle.com/c/digit-recognizer
* `recognizeDigitsExp.py` contains prototype code for GUI based custom ROI setting. Feel free to experiment with it. It **will** crash if ROI points are set out of frame or if are set incoherently.
