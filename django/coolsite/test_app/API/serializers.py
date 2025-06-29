# serializers
from test_app.views import *
from rest_framework import serializers
from test_app.models import *

class librarySerializer(serializers.ModelSerializer):
    class Meta:
        model = library
        fields = ('title','slug','content', 'cat')
