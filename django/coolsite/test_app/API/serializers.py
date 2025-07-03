# serializers
from test_app.views import *
from rest_framework import serializers
from test_app.models import *

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = library
        fields = ('title','slug','content', 'cat')
