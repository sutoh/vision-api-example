# encoding: utf-8
import argparse

from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials
import json

# https://cloud.google.com/vision/reference/rest/?hl=ja
DISCOVERY_URL='https://vision.googleapis.com/$discovery/rest?version=v1'

def get_vision_service():
    credentials = GoogleCredentials.get_application_default()
    return discovery.build('vision', 'v1', credentials=credentials,
                           discoveryServiceUrl=DISCOVERY_URL)

# https://syncer.jp/cloud-vision-api#section-6-6
def get_type_name(key):
    dict = {
        'label': 'LABEL_DETECTION',
        'face': 'FACE_DETECTION',
        'landmark': 'LANDMARK_DETECTION',
        'logo': 'LOGO_DETECTION',
        'text': 'TEXT_DETECTION',
        'safe': 'SAFE_SEARCH_DETECTION',
        'color': 'IMAGE_PROPERTIES'
    }
    ret = dict.get(key, None)
    if ret is None:
        raise Excetion('cant None Types. please check -h help.')
    return ret

# https://syncer.jp/cloud-vision-api#section-7-2
def get_responce_name(key):
    dict = {
        'label': 'labelAnnotations',
        'face': 'faceAnnotations',
        'landmark': 'landmarkAnnotations',
        'logo': 'logoAnnotations',
        'text': 'textAnnotations',
        'safe': 'safeSearchAnnotation',
        'color': 'imagePropertiesAnnotation'
    }
    ret = dict.get(key, None)
    if ret is None:
        raise Excetion('cant None Types. please check -h help.')
    return ret

def identify_landmark(gcs_uri, type_key, max_results=10):
    """Uses the Vision API to identify the landmark in the given image.
    Args:
        gcs_uri: A uri of the form: gs://bucket/object
        type_key: Request type
    Returns:
        Many array of dicts with infomation about the <type_key> in the picture.
    """

    batch_request = [{
        'image': {
            'source': {
                'gcs_image_uri': gcs_uri
            }
        },
        'features': [{
            'type': get_type_name(type_key),
            'maxResults': max_results,
            }]
        }]

    service = get_vision_service()
    request = service.images().annotate(body={
        'requests': batch_request,
        })
    response = request.execute()

    if response['responses'][0].get('error', None) is not None:
        print(response['responses'][0].get('error', None))

    ret = response['responses'][0].get(get_responce_name(type_key), None)
    return ret

def main(gcs_uri, type):
    if gcs_uri[:5] != 'gs://':
        raise Exception('Image uri must be of the form gs://bucket/object')
    annotations = identify_landmark(gcs_uri, type)
    if annotations is None:
        print json.dumps({})
    else:
        print json.dumps(annotations)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Identifies the landmark in the given image.')
    parser.add_argument(
        'gcs_uri', help=('The Google Cloud Storage uri to the image to identify'
                         ', of the form: gs://bucket_name/object_name.jpg'))
    parser.add_argument(
        '--type', help=('Default: label'
                       ', type: face, landmark, logo, text, safe, color')
                        , default='label')
    args = parser.parse_args()

    main(args.gcs_uri, args.type)
