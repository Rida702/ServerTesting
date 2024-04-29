watch_image = request.FILES.get('watchImage')
wrist_image = request.FILES.get('wristImage')


my_model_instance.watch_image = request.FILES['watchImage']
my_model_instance.watch_image.name = watch_image_path
my_model_instance.save()


print("------5 FILE NOT READ, 500")
my_model_instance.wrist_image = request.FILES['wristImage']
print("------5 FILE NOT READ, 500 1")
my_model_instance.wrist_image.name = wrist_image_path
print("------5 FILE NOT READ, 500 2")
my_model_instance.save()

<------------------------>
print("Here 1")
            wrist_image_data = request.data.get('wristImage')
            watch_image_data = request.data.get('watchImage')

print("Here 44")
my_model_instance.watch_image = request.FILES['watchImage']
my_model_instance.watch_image.name = watch_image_path
my_model_instance.save()

# Save wrist image
print("Here 55")
my_model_instance.wrist_image = request.FILES['wristImage']
my_model_instance.wrist_image.name = wrist_image_path
my_model_instance.save()



