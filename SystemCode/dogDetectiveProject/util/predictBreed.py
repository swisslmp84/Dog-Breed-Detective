import os
from flask import Flask, request, redirect, url_for, jsonify, render_template
from werkzeug.utils import secure_filename
import cv2
import keras
import numpy as np
import pandas as pd

from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from keras import backend as K
import tensorflow as tf
from tqdm import tqdm
from tensorflow.keras.preprocessing.image import load_img

from collections import defaultdict
from io import StringIO

from object_detection.utils import ops as utils_ops
from utils import label_map_util
from utils import visualization_utils as vis_util

import tensorflow.compat.v1 as tf1
 
UPLOAD_FOLDER = './static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
DEBUG = True

# featureExtractor = load_model('./models/feature_extractor.h5')
# dnn = load_model('./models/dogbreed.h5')

# What model to download.
MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_OBJECT_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
PATH_TO_BREED_LABELS = os.path.join('data', 'dog_breed_label_map.pbtxt')

detection_graph = tf1.Graph()
with detection_graph.as_default():
    od_graph_def = tf1.GraphDef()
    with tf1.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf1.import_graph_def(od_graph_def, name='')

def loadTargetClass():
    npzfile = np.load('./models/target_names.npz')
    labels_dataframe = pd.DataFrame(npzfile['arr_0'], columns = ['breed'])
    #Create list of alphabetically sorted labels.
    dog_breeds = sorted(list(set(labels_dataframe['breed'])))
    n_classes = len(dog_breeds)
    #Map each label string to an integer label.
    class_to_num = dict(zip(dog_breeds, range(n_classes)))

    for index, breedName in enumerate(dog_breeds):
        if index == 0:
            mode = 'w'
        else:
            mode = 'a'              
        customized_label_map(breedName, index+1, mode)  

    return class_to_num

def customized_label_map(breedName, id, mode):
    with open(PATH_TO_BREED_LABELS, mode) as the_file:
        the_file.write('item\n')
        the_file.write('{\n')
        the_file.write("name:'{0}'".format(str(breedName)))
        the_file.write('\n')
        the_file.write('id:{}'.format(int(id)))
        the_file.write('\n')
        the_file.write("display_name:'{0}'".format(str(breedName)))
        the_file.write('\n')
        the_file.write('}\n')

# load target labels
class_num = loadTargetClass()

breed_index = label_map_util.create_category_index_from_labelmap(PATH_TO_BREED_LABELS, use_display_name=True)
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_OBJECT_LABELS, use_display_name=True)

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

def run_inference_for_single_image(image, graph):
  with graph.as_default():
    with tf1.Session() as sess:
      # Get handles to input and output tensors
      ops = tf1.get_default_graph().get_operations()
      all_tensor_names = {output.name for op in ops for output in op.outputs}
      tensor_dict = {}
      for key in [
          'num_detections', 'detection_boxes', 'detection_scores',
          'detection_classes', 'detection_masks']:
          tensor_name = key + ':0'
          if tensor_name in all_tensor_names:
            tensor_dict[key] = tf1.get_default_graph().get_tensor_by_name(tensor_name)

      if 'detection_masks' in tensor_dict:
        # The following processing is only for single image
        detection_boxes = tf1.squeeze(tensor_dict['detection_boxes'], [0])
        detection_masks = tf1.squeeze(tensor_dict['detection_masks'], [0])
        # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
        real_num_detection = tf1.cast(tensor_dict['num_detections'][0], tf1.int32)
        detection_boxes = tf1.slice(detection_boxes, [0, 0], [real_num_detection, -1])
        detection_masks = tf1.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(detection_masks, detection_boxes, image.shape[0], image.shape[1])
        detection_masks_reframed = tf1.cast(tf1.greater(detection_masks_reframed, 0.5), tf1.uint8)
        # Follow the convention by adding back the batch dimension
        tensor_dict['detection_masks'] = tf1.expand_dims(detection_masks_reframed, 0)

      image_tensor = tf1.get_default_graph().get_tensor_by_name('image_tensor:0')

      # Run inference
      output_dict = sess.run(tensor_dict, feed_dict={image_tensor: np.expand_dims(image, 0)})

      # all outputs are float32 numpy arrays, so convert types as appropriate
      output_dict['num_detections'] = int(output_dict['num_detections'][0])
      output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.uint8)
      output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
      output_dict['detection_scores'] = output_dict['detection_scores'][0]

      filter_arr = []
      for i in range(len(output_dict['detection_classes'])):
        if category_index[output_dict['detection_classes'][i]]['name'] == 'dog' and output_dict['detection_scores'][i] > 0.5:
            filter_arr.append(True)
        else:
            filter_arr.append(False)

      output_dict['detection_boxes'] = output_dict['detection_boxes'][filter_arr]
      output_dict['detection_classes'] = output_dict['detection_classes'][filter_arr]
      output_dict['detection_scores'] = output_dict['detection_scores'][filter_arr]

      if 'detection_masks' in output_dict:
        output_dict['detection_masks'] = output_dict['detection_masks'][0]
        # output_dict['detection_masks'] = output_dict['detection_masks'][filter_arr]
        # if len(filter_arr) == len(output_dict['detection_masks']):
            # output_dict['detection_masks'] = output_dict['detection_masks'][filter_arr]
                
  return output_dict


def predictDogBreed(output_dict, image_np, filename, featureExtractor, dnn):
    (im_height, im_width) = image_np.shape[0:2]

    results = []

    for index, box in enumerate(output_dict['detection_boxes']):
        ymin, xmin, ymax, xmax = box
        box_img = image_np[int(ymin * im_height):int(ymax * im_height), int(xmin * im_width):int(xmax * im_width)]

        cv2.imwrite(os.path.join(UPLOAD_FOLDER, str(index)+"_"+filename), box_img)
        test_features = feature_extractor(os.path.join(UPLOAD_FOLDER, str(index)+"_"+filename), featureExtractor)

        y_pred = dnn.predict(test_features)
        pred_codes = np.argmax(y_pred, axis = 1)[0]

        for key, value in class_num.items(): 
            if pred_codes == value: 
                results.append([key, int(xmin * im_width), int(ymin * im_height), int(xmax * im_width), int(ymax * im_height)])
                break

        output_dict['detection_classes'][index] = pred_codes + 1
        output_dict['detection_scores'][index] = max(y_pred[0])

    return results

# for feature_extraction dataframe must have to contain file_name and  breed columns
def feature_extractor(filepath, featureExtractor):
    df = pd.DataFrame({'file_name':[filepath]})

    img_size = (224,224,3)
    data_size = len(df)
    batch_size = 1
    X = np.zeros([data_size,4128], dtype=np.uint8)

    datagen = ImageDataGenerator()
    generator = datagen.flow_from_dataframe(df, x_col = 'file_name', class_mode = None, 
        batch_size=1, shuffle = False,target_size = (img_size[:2]),color_mode = 'rgb')
    i = 0
    for input_batch in tqdm(generator):
        input_batch = featureExtractor.predict(input_batch)
        X[i * batch_size : (i + 1) * batch_size] = input_batch
        i += 1
        if i * batch_size >= data_size:
            break
    return X

def resizeImg(image_np):
    desired_size = 500
    old_size = image_np.shape[:2] # old_size is in (height, width) format
    ratio = float(desired_size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])

    # new_size should be in (width, height) format
    im = cv2.resize(image_np, (new_size[1], new_size[0]))

    delta_w = desired_size - new_size[1]
    delta_h = desired_size - new_size[0]
    top, bottom = delta_h//2, delta_h-(delta_h//2)
    left, right = delta_w//2, delta_w-(delta_w//2)

    color = [0, 0, 0]
    new_im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

    return new_im


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
def predict_image(request, featureExtractor, dnn):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            return "No file part"

        file = request.files['file']
        if file.filename == '':
            return "No image selected for uploading"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            image_np = cv2.imread(os.path.join(UPLOAD_FOLDER, filename))

            image_np = resizeImg(image_np)

            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)

            # Actual object detection of dog/s in image.
            output_dict = run_inference_for_single_image(image_np, detection_graph)

            # predict dog breed for detect dog object in image
            results = predictDogBreed(output_dict, image_np, filename, featureExtractor, dnn)

            # Visualization of the results of a detection.
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                output_dict['detection_boxes'],
                output_dict['detection_classes'],
                output_dict['detection_scores'],
                breed_index,
                instance_masks=output_dict.get('detection_masks'),
                use_normalized_coordinates=True, min_score_thresh=.01,
                line_thickness=5)

            cv2.imwrite(os.path.join(UPLOAD_FOLDER, filename), image_np)
            
            results.insert(0,os.path.join(UPLOAD_FOLDER, filename))
            return jsonify(results)
        else:
            return "Allowed image types are -> png, jpg, jpeg"
    return ""

