# views.py
from django.shortcuts import render
from .forms import ImageUploadForm
from PIL import Image
from .models import ImageModel

def index_view(request):
    return render(request, 'index.html')

def upload_view(request):
    return render(request, 'upload.html')

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance1_image = form.cleaned_data['image']

            # Convert instance1 image to greyscale
            instance1_image_obj = Image.open(instance1_image)
            instance2_image = instance1_image_obj.convert('L')  # 'L' mode is for greyscale

            my_model_instance = ImageModel()
            my_model_instance.image.save(instance1_image.name, instance1_image)
            my_model_instance.grayscale_image.save(f"{instance1_image.name.split('.')[0]}_grayscale.jpg", instance2_image)

            
            context = {
                'original_image_url': my_model_instance.image.url,
                'grayscale_image_url': my_model_instance.grayscale_image.url,
            }

            return render(request, 'result.html', context)
    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})

















#Previous Implmenetation

"""def grayscale_image(image_path):
    img = Image.open(image_path).convert('L')
    save_path = os.path.join(settings.MEDIA_ROOT, 'grayscaled')
    os.makedirs(save_path, exist_ok=True)
    grayscale_filename = f"grayscaled_{os.path.basename(image_path)}"
    grayscale_path = os.path.join(save_path, grayscale_filename)

    with open(grayscale_path, 'wb') as f:
        img.save(f, format="JPEG")
    return grayscale_path"""
    
"""def grayscale_image(image_path):
    img = Image.open(image_path).convert('L')
    with BytesIO() as f:
        img.save(f, format="JPEG")
        f.seek(0)
        return f

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save(commit=False)
            greyImage = grayscale_image(uploaded_image.image.path)
            
            uploaded_image.grayscale_image_url = f'/media/grayscaled/grayscaled_{os.path.basename(uploaded_image.image.path)}'

            uploaded_image.grayscale_image.save(os.path.basename(uploaded_image.grayscale_image_url), ContentFile(greyImage.getvalue()))

                        
            filename = os.path.basename(uploaded_image.image.path)
            uploaded_image.grayscale_image = f'/media/uploads/{filename}'
            original_image_url = f'/media/uploads/{filename}'

            filename = os.path.basename(uploaded_image.image.path)
            grayscale_image_url = f'/media/grayscaled/grayscaled_{filename}'
            
            uploaded_image.save()

            context = {
                'original_image_url': original_image_url,
                'grayscale_image_url': grayscale_image_url,
            }
            return render(request, 'result.html', context)
    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})"""