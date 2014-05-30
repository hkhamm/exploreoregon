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


class ImageSizeError(Exception):
    pass

class ThumbnailOptionError(Exception):
    pass

class ThumbnailWorksError(Exception):
    """Internal sky_thumbnails error.
    
    Should be raised any time a method encounters an argument having a bad type
    or bad value. Write as many such checks as necessary in order to catch any
    changes in the underlying framework.
    
    This is important, since this app is built on Django internal structures,
    which might change without notice.
    
    """
    pass
