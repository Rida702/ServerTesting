# Assuming result_image is your NumPy array
result_pil_image = Image.fromarray(result_image.astype('uint8'))

# Save the PIL Image to a BytesIO buffer
print("------2 FILE NOT READ, 500")
image_io = BytesIO()
result_pil_image.save(image_io, format='JPEG')
image_io.seek(0)

# Save paths to the database
print("------3 FILE NOT READ, 500")
my_model_instance = ImageModel()

# Save watch image
print("------4 FILE NOT READ, 500")
my_model_instance.watch_image = request.FILES['watchImage']
my_model_instance.watch_image.name = watch_image_path
my_model_instance.save()

# Save wrist image
print("------5 FILE NOT READ, 500")
my_model_instance.wrist_image = request.FILES['wristImage']
print("------5 FILE NOT READ, 500 1")
my_model_instance.wrist_image.name = wrist_image_path
print("------5 FILE NOT READ, 500 2")
my_model_instance.save()


# Save result image
print("------6 FILE NOT READ, 500")
my_model_instance.result_image.name = result_image_name
my_model_instance.result_image.save(result_image_name, ContentFile(image_io.read()), save=True)

print("------66 FILE NOT READ, 500")
# Prepare URLs for the template
context = {
    'watch_image_url': my_model_instance.watch_image.url,
    'wrist_image_url': my_model_instance.wrist_image.url,
    'result_image_url': my_model_instance.result_image.url,
}
print(f"Result Image Path: {{result_image_url}}")