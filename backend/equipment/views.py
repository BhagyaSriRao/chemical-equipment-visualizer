from .models import UploadHistory
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import FileResponse
from .utils.pdf_report import generate_pdf
import io
from reportlab.pdfgen import canvas
from django.http import HttpResponse, FileResponse


@api_view(['POST'])
def upload_csv(request):
    file = request.FILES.get('file')
    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    df = pd.read_csv(file)

    required_cols = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    for col in required_cols:
        if col not in df.columns:
            return Response({"error": f"Missing column: {col}"}, status=400)

    total_equipment = len(df)
    avg_flowrate = round(df['Flowrate'].mean(), 2)
    avg_pressure = round(df['Pressure'].mean(), 2)
    avg_temperature = round(df['Temperature'].mean(), 2)

    equipment_type_distribution = df['Type'].value_counts().to_dict()
    table_data = df.to_dict(orient='records')

    history = UploadHistory.objects.create(
        filename=file.name,
        total_equipment=total_equipment,
        avg_flowrate=avg_flowrate,
        avg_pressure=avg_pressure,
        avg_temperature=avg_temperature
    )

    # keep only last 5 uploads
    old = UploadHistory.objects.order_by('-uploaded_at')[5:]
    for o in old:
        o.delete()

    return Response({
        "total_equipment": total_equipment,
        "average_flowrate": avg_flowrate,
        "average_pressure": avg_pressure,
        "average_temperature": avg_temperature,
        "equipment_type_distribution": equipment_type_distribution,
        "table_data": table_data
    })


@api_view(['GET'])
def upload_history(request):
    history = UploadHistory.objects.order_by('-uploaded_at')[:5]
    return Response([
        {
            "id": h.id,
            "filename": h.filename,
            "total_equipment": h.total_equipment,
            "uploaded_at": h.uploaded_at.strftime("%Y-%m-%d %H:%M")
        }
        for h in history
    ])


@api_view(['GET'])
# equipment/views.py


def download_pdf(request):
    # get ID from query parameters
    record_id = request.GET.get("id")
    if not record_id:
        return HttpResponse("Missing ID", status=400)

    try:
        record = UploadHistory.objects.get(id=record_id)
    except UploadHistory.DoesNotExist:
        return HttpResponse("Record not found", status=404)

    # Generate PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, f"Filename: {record.filename}")
    p.drawString(100, 780, f"Total Equipment: {record.total_equipment}")
    p.drawString(100, 760, f"Average Flowrate: {record.avg_flowrate}")
    p.drawString(100, 740, f"Average Pressure: {record.avg_pressure}")
    p.drawString(100, 720, f"Average Temperature: {record.avg_temperature}")
    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{record.filename}.pdf"'
    return response
