# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 19:30:38 2017

@author: stef
"""

import datetime
from haystack import indexes
from document.models import Document

#
class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    #text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title_full')
    text = indexes.CharField(model_attr='content_html',document=True)
    #slug = indexes.CharField(model_attr='slug')
    #birthdate = indexes.DateTimeField(model_attr='birthdate')


    def get_model(self):
        return Document

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()