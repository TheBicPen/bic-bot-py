# test.py
#original code from https://github.com/MicrocontrollersAndMore/TensorFlow_Tut_2_Classification_Walk-through

import os
import tensorflow as tf
import numpy as np
import cv2

# module-level variables ##############################################################################################
RETRAINED_LABELS_TXT_FILE_LOC = os.getcwd() + "/image_classification/retrained_labels.txt"
RETRAINED_GRAPH_PB_FILE_LOC = os.getcwd() + "/image_classification/retrained_graph.pb"

TEST_IMAGES_DIR = os.getcwd() + "/image_classification/test_images"

SCALAR_RED = (0.0, 0.0, 255.0)
SCALAR_BLUE = (255.0, 0.0, 0.0)

#######################################################################################################################
def main():
    print("starting program . . .")

    if not checkIfNecessaryPathsAndFilesExist():
        return
    # end if

    sess = start_classify()
    if sess is not None:
        print("Started Successfully!")
        return sess
    return
# end main

def get_classifications():
    # get a list of classifications from the labels file
    classifications = []
    # for each line in the label file . . .
    for currentLine in tf.gfile.GFile(RETRAINED_LABELS_TXT_FILE_LOC):
        # remove the carriage return
        classification = currentLine.rstrip()
        # and append to the list
        classifications.append(classification)
    # end for
    return classifications

def start_classify():
    classifications = get_classifications()

    # show the classifications to prove out that we were able to read the label file successfully
    print("classifications = " + str(classifications))


    # load the graph from file
    with tf.gfile.FastGFile(RETRAINED_GRAPH_PB_FILE_LOC, 'rb') as retrainedGraphFile:
        # instantiate a GraphDef object
        graphDef = tf.GraphDef()
        # read in retrained graph into the GraphDef object
        graphDef.ParseFromString(retrainedGraphFile.read())
        # import the graph into the current default Graph, note that we don't need to be concerned with the return value
        _ = tf.import_graph_def(graphDef, name='')
    # end with

    return tf.Session()

def classify_image(fileName, sess, classifications):

    openCVImage = cv2.imdecode(np.fromstring(fileName, np.uint8), 1)

    # if we were not able to successfully open the image, return
    if openCVImage is None:
        print("unable to open " + fileName + " as an OpenCV image")
        return "unable to open " + fileName + " as an OpenCV image"
    # end if

    # get the final tensor from the graph
    finalTensor = sess.graph.get_tensor_by_name('final_result:0')

    # convert the OpenCV image (numpy array) to a TensorFlow image
    tfImage = np.array(openCVImage)[:, :, 0:3]

    # run the network to get the predictions
    predictions = sess.run(finalTensor, {'DecodeJpeg:0': tfImage})

    # sort predictions from most confidence to least confidence
    sortedPredictions = predictions[0].argsort()[-len(predictions[0]):][::-1]

    print("---------------------------------------")

    # keep track of if we're going through the next for loop for the first time so we can show more info about
    # the first prediction, which is the most likely prediction (they were sorted descending above)
    onMostLikelyPrediction = True
    # for each prediction . . .
    for prediction in sortedPredictions:
        strClassification = classifications[prediction]

        # if the classification (obtained from the directory name) ends with the letter "s", remove the "s" to change from plural to singular
        if strClassification.endswith("s"):
            strClassification = strClassification[:-1]
        # end if

        # get confidence, then get confidence rounded to 2 places after the decimal
        confidence = predictions[0][prediction]

        # if we're on the first (most likely) prediction, state what the object appears to be and show a % confidence to two decimal places
        if onMostLikelyPrediction:
            # get the score as a %
            scoreAsAPercent = confidence * 100.0
            # show the result to std out
            print("the object appears to be a " + strClassification + ", " + "{0:.2f}".format(scoreAsAPercent) + "% confidence")
            return (strClassification, scoreAsAPercent)
            # write the result on the image
            # writeResultOnImage(openCVImage, strClassification + ", " + "{0:.2f}".format(scoreAsAPercent) + "% confidence")
            # finally we can show the OpenCV image
            # cv2.imshow(fileName, openCVImage)
            
            # mark that we've show the most likely prediction at this point so the additional information in
            # this if statement does not show again for this image
            onMostLikelyPrediction = False
        # end if

#######################################################################################################################
def checkIfNecessaryPathsAndFilesExist():

    if not os.path.exists(RETRAINED_LABELS_TXT_FILE_LOC):
        print('ERROR: RETRAINED_LABELS_TXT_FILE_LOC "' + RETRAINED_LABELS_TXT_FILE_LOC + '" does not seem to exist')
        return False
    # end if

    if not os.path.exists(RETRAINED_GRAPH_PB_FILE_LOC):
        print('ERROR: RETRAINED_GRAPH_PB_FILE_LOC "' + RETRAINED_GRAPH_PB_FILE_LOC + '" does not seem to exist')
        return False
    # end if

    return True
# end function

#######################################################################################################################
def writeResultOnImage(openCVImage, resultText):
    # ToDo: this function may take some further fine-tuning to show the text well given any possible image size

    imageHeight, imageWidth, sceneNumChannels = openCVImage.shape

    # choose a font
    fontFace = cv2.FONT_HERSHEY_TRIPLEX

    # chose the font size and thickness as a fraction of the image size
    fontScale = 1.0
    fontThickness = 2

    # make sure font thickness is an integer, if not, the OpenCV functions that use this may crash
    fontThickness = int(fontThickness)

    upperLeftTextOriginX = int(imageWidth * 0.05)
    upperLeftTextOriginY = int(imageHeight * 0.05)

    textSize, baseline = cv2.getTextSize(resultText, fontFace, fontScale, fontThickness)
    textSizeWidth, textSizeHeight = textSize

    # calculate the lower left origin of the text area based on the text area center, width, and height
    lowerLeftTextOriginX = upperLeftTextOriginX
    lowerLeftTextOriginY = upperLeftTextOriginY + textSizeHeight

    # write the text on the image
    cv2.putText(openCVImage, resultText, (lowerLeftTextOriginX, lowerLeftTextOriginY), fontFace, fontScale, SCALAR_BLUE, fontThickness)
# end function

#######################################################################################################################
if __name__ == "__main__":
    main()
