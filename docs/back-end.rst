back-end
============

.. automodule:: Back-end
   :members:




Contents
----------

The back-end was created using Django. It contains two folders called:
Core, ImageWeave

Core
----------
admin
~~~~~~~~~~
.. code-block:: python

   from django.contrib import admin
   from .models import Image

   admin.site.register(Image)

This code registers the Image model with the Django admin site. This allows you to manage Image instances through the admin site.

The from django.contrib import admin statement imports the admin module from the django.contrib package, which provides tools for managing data in your Django project.

The Image model is imported from the same module as the admin.site.register function call. The Image model represents an image and its associated metadata, such as the file name, file size, and creation date.

The admin.site.register(Image) statement registers the Image model with the Django admin site. This makes it possible to manage Image instances through the admin site, including adding, editing, and deleting them.

Once you have registered a model with the admin site, you can access it by navigating to the admin site URL in your web browser and logging in as an admin user. You should then be able to see the Image model listed on the admin site's home page and manage its instances.

apps
~~~~~~~~~~~
.. code-block:: python
   
   from django.apps import AppConfig

   class CoreConfig(AppConfig):
      default_auto_field = 'django.db.models.BigAutoField'
      name = 'core'

This is an AppConfig class in Django. An AppConfig class is a configuration object that provides metadata for an application. It allows you to customize certain aspects of the application and provides a way to interact with the Django framework.

To be more specific, the CoreConfig class is defining the configuration for an app called core. Here are the different components of this configuration:

default_auto_field: This setting specifies the default primary key field for models that are defined in this app. In this case, it is set to django.db.models.BigAutoField, which is a 64-bit integer field that is automatically incremented.

name: This setting specifies the name of the app. This is the name that will be used to refer to the app throughout the Django framework. In this case, the app is named core.

Note that there can be multiple AppConfig classes defined for a single app, each with its own set of configuration options. These classes can be used to customize various aspects of the app, such as the app's models, views, templates, and so on.   

models
~~~~~~~~

.. code-block:: python

   from django.db import models

   class Image(models.Model):
      name = models.CharField(max_length=100)
      caption = models.TextField()
      category = models.CharField(max_length=100)
      image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name

This is a Django model class called Image. A model represents a database table and its associated data, and it defines the fields that make up the data for that table.

To be more specific, the Image model has four fields:

name: This field represents the name of the image and is a CharField with a maximum length of 100 characters.

caption: This field represents the caption for the image and is a TextField that can hold an unlimited amount of text.

category: This field represents the category of the image and is a CharField with a maximum length of 100 characters.

image: This field represents the actual image file and is an ImageField that will upload the image to the "images/" subdirectory of the media directory.

The __str__ method is also defined, which returns the name of the image as a string. This is useful for debugging and for displaying the name of the image in the Django admin interface.

serializers
~~~~~~~~

.. code-block:: python

   from rest_framework import serializers
   from .models import Image

   class ImageSerializer(serializers.ModelSerializer):
      class Meta:
         model = Image
         fields = '__all__'

This is a Django REST Framework serializer class called ImageSerializer. A serializer is a component that converts complex data types, such as Django model instances, into Python data types that can be easily rendered into JSON or other content types.

To be more specific, the ImageSerializer class is defining the serialization for the Image model. It is using the ModelSerializer class provided by Django REST Framework, which automatically generates a set of fields based on the model definition.

The Meta class inside ImageSerializer is used to specify the metadata for the serializer. In this case, it specifies that the Image model should be used and all of its fields should be included in the serialization. The fields attribute can also be set to a list of specific field names if you only want to include certain fields.

By default, the ModelSerializer will generate a set of read-only fields based on the model definition, but you can override or customize these fields by defining them explicitly in the serializer class.   


urls
~~~~
.. code-block:: python

   from django.urls import path
   from . import views

   urlpatterns = [
      path('image-upload/', views.image_upload_view, name='image_upload'),
      path('image-list/', views.image_list_view, name='image_list'),
      path('image-detail/<int:pk>/', views.image_detail_view, name='image_detail'),
   ]

This is a Django URL configuration for an app called core. URL configuration determines how URLs should be handled by the Django framework.

To be more specific, there are three URL patterns defined using the path function:

image-upload/: This URL pattern maps to the image_upload_view view function and is used to handle requests to upload new images.

image-list/: This URL pattern maps to the image_list_view view function and is used to handle requests to list all images that have been uploaded.

image-detail/<int:pk>/: This URL pattern maps to the image_detail_view view function and is used to handle requests to retrieve the details of a specific image, where the pk parameter is the primary key of the image in the database.

Each URL pattern is given a name using the name parameter, which can be used to reference the URL pattern in other parts of the code. For example, you could use the reverse function to generate a URL for a specific view based on its name.

To use these URL patterns in your Django app, you need to include them in the app's urls.py file by calling the include function and passing in the URL patterns for that app. This allows the main project-level urls.py file to route requests to the appropriate app based on the URL path.

views
~~~~
.. code-block:: python
   
   from django.shortcuts import render
   from django.http import JsonResponse
   from rest_framework.parsers import MultiPartParser, FormParser
   from rest_framework.decorators import api_view
   from rest_framework.response import Response
   from .models import Image
   from .serializers import ImageSerializer

   @api_view(['POST'])
   def image_upload_view(request):
      serializer = ImageSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=201)
      return Response(serializer.errors, status=400)

   @api_view(['GET'])
   def image_list_view(request):
      images = Image.objects.all()
      serializer = ImageSerializer(images, many=True)
      return Response(serializer.data)

   @api_view(['GET'])
   def image_detail_view(request, pk):
      image = Image.objects.get(pk=pk)
      serializer = ImageSerializer(image)
      return Response(serializer.data)


This is a Django view module that defines three view functions for handling HTTP requests related to image uploads and retrieval. Views are the main way in which Django handles HTTP requests and responses.

To be more specific, there are three view functions defined using the api_view decorator provided by the Django REST Framework:

image_upload_view: This view function handles HTTP POST requests to upload new images. It uses the ImageSerializer to serialize the incoming data and create a new Image object in the database. If the data is valid, it returns a JSON response with the serialized data and an HTTP status code of 201 (Created). If the data is invalid, it returns a JSON response with the serialization errors and an HTTP status code of 400 (Bad Request).

image_list_view: This view function handles HTTP GET requests to retrieve a list of all uploaded images. It fetches all Image objects from the database, serializes them using the ImageSerializer, and returns a JSON response with the serialized data.

image_detail_view: This view function handles HTTP GET requests to retrieve the details of a specific image, identified by its primary key (pk). It fetches the Image object with the specified primary key from the database, serializes it using the ImageSerializer, and returns a JSON response with the serialized data.

In each view function, the Response class is used to create and return the HTTP response. This class takes a Python object as its first argument and automatically converts it to a JSON response. The status parameter can be used to set the HTTP status code for the response.

The api_view decorator is used to ensure that the view functions only accept HTTP requests that match the specified HTTP methods. In this example, the image_upload_view function only accepts HTTP POST requests, while the image_list_view and image_detail_view functions only accept HTTP GET requests.

ImageWeave
-----------

asgi
~~~~~~
.. code-block:: python

   """
   ASGI config for ImageWeave project.

   It exposes the ASGI callable as a module-level variable named ``application``.

   For more information on this file, see
   https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
   """

   import os

   from django.core.asgi import get_asgi_application

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ImageWeave.settings')

   application = get_asgi_application()

This is the ASGI (Asynchronous Server Gateway Interface) configuration file for the Django project called ImageWeave. ASGI is a specification for asynchronous web servers that enables Django to handle long-lived connections and real-time applications.

This specific ASGI configuration file is generated automatically by Django when you create a new project using the django-admin startproject command. It contains the following elements:

import os: This imports the os module, which is used to access environment variables and other system-specific functionality.

from django.core.asgi import get_asgi_application: This imports the get_asgi_application function from the django.core.asgi module. This function returns an ASGI callable that can be used to handle HTTP and WebSocket connections for a Django application.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ImageWeave.settings'): This sets the DJANGO_SETTINGS_MODULE environment variable to the path of the project's settings module (ImageWeave.settings). This tells Django which settings module to use for the project.

application = get_asgi_application(): This calls the get_asgi_application function to create a new ASGI callable for the project and assigns it to the application variable. This callable can then be used by an ASGI server to handle HTTP and WebSocket connections for the project.

In summary, this ASGI configuration file sets up the environment and creates an ASGI callable for a Django project, which can then be used by an ASGI server to handle incoming connections.


settings
~~~~~~~~
.. code-block:: python

   from pathlib import Path

   # Build paths inside the project like this: BASE_DIR / 'subdir'.
   BASE_DIR = Path(__file__).resolve().parent.parent


   # Quick-start development settings - unsuitable for production
   # See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

   # SECURITY WARNING: keep the secret key used in production secret!
   SECRET_KEY = 'django-insecure-%r*##-#@=uu68qll)uschz+$%y&$9$-+qekb_4r1ajuz9bs=pn'

   # SECURITY WARNING: don't run with debug turned on in production!
   DEBUG = True

   ALLOWED_HOSTS = []


   # Application definition

   INSTALLED_APPS = [
      'core',
      
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',

      'rest_framework',
   ]

   MIDDLEWARE = [
      'django.middleware.security.SecurityMiddleware',
      'django.contrib.sessions.middleware.SessionMiddleware',
      'django.middleware.common.CommonMiddleware',
      'django.middleware.csrf.CsrfViewMiddleware',
      'django.contrib.auth.middleware.AuthenticationMiddleware',
      'django.contrib.messages.middleware.MessageMiddleware',
      'django.middleware.clickjacking.XFrameOptionsMiddleware',
   ]

   ROOT_URLCONF = 'ImageWeave.urls'

   TEMPLATES = [
      {
         'BACKEND': 'django.template.backends.django.DjangoTemplates',
         'DIRS': [],
         'APP_DIRS': True,
         'OPTIONS': {
               'context_processors': [
                  'django.template.context_processors.debug',
                  'django.template.context_processors.request',
                  'django.contrib.auth.context_processors.auth',
                  'django.contrib.messages.context_processors.messages',
               ],
         },
      },
   ]

   WSGI_APPLICATION = 'ImageWeave.wsgi.application'


   # Database
   # https://docs.djangoproject.com/en/4.1/ref/settings/#databases

   DATABASES = {
      'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': BASE_DIR / 'db.sqlite3',
      }
   }


   # Password validation
   # https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

   AUTH_PASSWORD_VALIDATORS = [
      {
         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
      },
      {
         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
      },
      {
         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
      },
      {
         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
      },
   ]


   # Internationalization
   # https://docs.djangoproject.com/en/4.1/topics/i18n/

   LANGUAGE_CODE = 'en-us'

   TIME_ZONE = 'UTC'

   USE_I18N = True

   USE_TZ = True


   # Static files (CSS, JavaScript, Images)
   # https://docs.djangoproject.com/en/4.1/howto/static-files/

   STATIC_URL = 'static/'

   # Default primary key field type
   # https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

   DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

This is settings file. It lets Django know how to be properly configured....

urls
~~~~
.. code-block:: python
   
   from django.contrib import admin
   from django.urls import path, include
   from django.conf import settings
   from django.conf.urls.static import static

   from django.contrib import admin
   from django.urls import path, include
   from django.conf import settings
   from django.conf.urls.static import static

   urlpatterns = [
      path('admin/', admin.site.urls),
      path('', include('core.urls')),
   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

   
The code defines the URL configuration for the Django backend application. The urlpatterns variable is a list of URL patterns that map URLs to views.

The first pattern maps the URL /admin/ to the admin.site.urls view, which provides access to the Django administration site. The second pattern maps the root URL (/) to the core.urls module, which contains the URL patterns for the core application.

The static() function is used to serve static files (such as images) during development. It is used to add a URL pattern for the MEDIA_URL setting, which maps to the MEDIA_ROOT directory where media files are stored. This allows the server to serve media files to clients who request them.

wsgi
~~~~
.. code-block:: python
   
   import os

   from django.core.wsgi import get_wsgi_application

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ImageWeave.settings')

   application = get_wsgi_application()


This is the WSGI (Web Server Gateway Interface) configuration file for the Django project named "ImageWeave". WSGI is a specification for a standardized interface between web servers and Python web applications or frameworks.

This file imports the get_wsgi_application() function from django.core.wsgi module. The get_wsgi_application() function returns a WSGI callable that can be used by a web server to serve the Django application.

The os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ImageWeave.settings') line sets the DJANGO_SETTINGS_MODULE environment variable to tell Django which settings module to use. In this case, it's set to 'ImageWeave.settings', which refers to the settings.py file in the ImageWeave project directory.

Finally, the application variable is assigned the WSGI callable returned by the get_wsgi_application() function. This is what a web server would use to serve the Django application.
