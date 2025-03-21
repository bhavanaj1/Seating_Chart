from django.shortcuts import render, redirect
from .form import SeatingChartForm
# from pdf2image import convert_from_path

# Create your views here.
def home(request):
    return render(request, 'seating_chart_main_page.html')

def seating_chart_upload(request):
    if request.method == "POST":
        # print("✅ Received POST request")  # Debugging
        # print("📂 Uploaded files:", request.FILES)  # Debugging

        form = SeatingChartForm(request.POST, request.FILES)
        # print("📋 Form initialized:", form)
        if form.is_valid():
            # print("✅ Form is valid")
            instance = form.save()
            # print(f"✅ File saved: {instance.file.path}")
            form.make_everything()
            # print("✅ Seating chart and PDFs created")
            return redirect("together")
        # else:
            # print("❌ Form is invalid:", form.errors)
    else:
        form = SeatingChartForm()
    context = {'form': form}
    return render(request, 'seating_chart_upload.html', context)

def seating_chart_type(request):
    if request.method == "POST":
        form = SeatingChartForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form.make_everything()
            return redirect("together")
    else:
        form = SeatingChartForm()
    context = {'form': form}
    return render(request, 'seating_chart_type.html', context)


def together(request):
    return render(request, 'together.html')


def seating_chart_webpage(request):
    return render(request, 'seating_chart_webpage.html')







