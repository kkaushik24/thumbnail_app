from PIL import Image
import urllib2
import uuid
import io

from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse

# Create your views here.

def create_thumbnail(request):
	"""
	This view creates the thumbnail for the imageurl given in get
	query.
	"""
	# get query for image processing
	image_url = request.GET.get('image_url')
	height = request.GET.get('height')
	width = request.GET.get('width')
	error_list_str = []
	# response dict for the image
	response_dict = {'image_url': image_url,
					  'height': height,
					  'width': width}
	
	# sanity check for correct get params
	if image_url is None:
		error_msg = "No image url in get parameter"
		error_list_str.append(error_msg)
	if height is None:
		error_msg = "No height is provided"
		error_list_str.append(error_msg)
	if width is None:
		error_list_str.append(error_msg)
	size = width, height
	# if there is no error try to process the image url
	if not error_list_str:
		try:
			image_data = urllib2.urlopen(image_url)
			image_file = io.BytesIO(image_data.read())
			img = Image.open(image_file)
			
		except:
			error_msg = "Image could not be loaded"
			error_list_str.append(error_msg)

		try:
			img.thumbnail(size)
		except:
			error_msg = "Thumbnail could not be created"
			error_list_str.append(error_msg)
	if error_list_str:
		# if there is error 
		# send the json response for the error
		response_dict.update({"errors": error_list_str})
		return JsonResponse(response_dict)
	else:
		response = HttpResponse(content_type="image/jpeg")
		img.save(response, img.format)
		return response
