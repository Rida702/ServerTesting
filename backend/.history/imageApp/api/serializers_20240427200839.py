from rest_framework import serializers
from imageApp.models import ImageModel

class ImageModelSerializer(serializers.ModelSerializer):
    watch_image_url = serializers.SerializerMethodField()
    wrist_image_url = serializers.SerializerMethodField()
    result_image_url = serializers.SerializerMethodField()

    def get_watch_image_url(self, obj):
        return obj.watch_image.url if obj.watch_image else None

    def get_wrist_image_url(self, obj):
        return obj.wrist_image.url if obj.wrist_image else None

    def get_result_image_url(self, obj):
        return obj.result_image.url if obj.result_image else None

    class Meta:
        model = ImageModel
        print('Here 1')
        fields = ['id', 'watch_image', 'wrist_image', 'result_image', 'watch_image_url', 'wrist_image_url', 'result_image_url']
