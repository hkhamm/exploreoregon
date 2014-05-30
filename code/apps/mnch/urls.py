from django.conf.urls import patterns, include, url

from mnch.views import *


urlpatterns = patterns('',

    url(r'^$', KioskView.as_view()),
    url(r'^photo/add/$', MobileSubmitPhotoView.as_view(), name='mobile_submit_photo'),

    url(r'^geological-site/comments', GeologicalSiteCommentsView.as_view(), name='geologicalsite_comments'),
    url(r'^geological-site/like/comment$', LikeCommentView.as_view(), name='like_comment'),
    url(r'^geological-site/submit/comment$', SubmitGeologicalSiteCommentView.as_view(), name='geologicalsite_submit_comment'),
    url(r'^geological-site/submit/photo$', SubmitGeologicalSitePhotoView.as_view(), name='geologicalsite_submit_photo'),

)

