from bottle import run, request, route, abort
import os
from PIL import Image
import tempfile

# What each header should be on incoming request
headers = {
  'content-type': 'multipart/form-data'
}

# Each header to check for incoming request
header = ['content-type']

# Save state of a successful image upload and color request
# Keys: imagePath, color
imageUpload = {}

@route('/rockLibrary/imageupload', method='POST')
def getImageUploadAndColor():
    """Recieves request of image to be uploaded along with the
    respective color to be found on the image

    Example request: 
        {
            "image": <image_file>,
            "color": pink
        }

    Returns:
        Successful json request message with the rocks places and types provided.
    """
    for head in header:
        print(request.get_header(head))
        if headers.get(head) not in request.get_header(head):
            abort(406, 'Incorrect headers')
    colorRequest = request.forms.get('color')
    imageRequest = request.files.get('image')
    if not (colorRequest or imageRequest):
        abort(400, 'Bad request')

    imageName = imageRequest.filename.split('.')
    if len(imageName) > 2 or imageName[len(imageName)-1] not in ('jpeg', 'jpg', 'png'):
        abort(400, 'Bad Request on image input')

    tempdirectory = tempfile.gettempdir()
    if not os.path.exists(tempdirectory):
        abort(512, 'server fault')
    
    file_path = r'{path}/{file}'.format(path=tempdirectory, file=imageRequest.filename)
    imageRequest.save(file_path, overwrite=True)
    im = Image.open(file_path)
    im.show()

    imageUpload = {'imagePath': file_path, 'color': colorRequest}

    return {'Message': 'Request successful, requested image saved'}

run(host='localhost', port=8002, reloader=True, debug=True)