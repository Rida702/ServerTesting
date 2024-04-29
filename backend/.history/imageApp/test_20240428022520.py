watch_image = request.FILES.get('watchImage')
wrist_image = request.FILES.get('wristImage')


my_model_instance.watch_image = request.FILES['watchImage']
            my_model_instance.watch_image.name = watch_image_path
            my_model_instance.save()