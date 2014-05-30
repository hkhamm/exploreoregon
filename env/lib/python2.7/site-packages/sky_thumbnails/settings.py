# -*- coding: utf-8 -*-
#
#  This file is part of django-sky-thumbnails.
#
#  django-sky-thumbnails adds thumbnail support to the default ImageField.
#
#  Copyright 2012 Concentric Sky, Inc. All Rights Reserved.
#  http://www.concentricsky.com
#  Written by: Kyle Rimkus [Mar 2012]
#  This code may not be used without permission.
#
#  Parts of this code are derivative of django-thumbnail-works.
#
#  Development Web Site:
#    - http://www.codetrax.org/projects/django-thumbnail-works
#  Public Source Code Repository:
#    - https://source.codetrax.org/hgroot/django-thumbnail-works
#
#  Copyright 2010 George Notaras <gnot [at] g-loaded.eu>


from django.conf import settings


# Anything supported by PIL
THUMBNAILS_FORMAT = getattr(settings, 'THUMBNAILS_FORMAT', 'JPEG')

# For JPEG format only
THUMBNAILS_QUALITY = getattr(settings, 'THUMBNAILS_QUALITY', 85)

# This is the name of the directory where the thumbnails will be stored
THUMBNAILS_DIRNAME = getattr(settings, 'THUMBNAILS_DIRNAME', 'thumbs')

# Generate the thumbnails on first access rather than at the time the
# original image is saved. 
THUMBNAILS_DELAYED_GENERATION = getattr(settings, 'THUMBNAILS_DELAYED_GENERATION', False)
