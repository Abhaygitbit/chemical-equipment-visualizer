import os
import pandas as pd
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from .models import Dataset, Equipment
from .serializers import DatasetSerializer

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_csv(request):
    """Handle CSV file upload"""
    print("📥 Upload request received")  # Debug print
    
    try:
        # Check if file is present
        if 'file' not in request.FILES:
            print("❌ No file in request")
            return Response({'error': 'No file uploaded'}, status=400)
        
        csv_file = request.FILES['file']
        print(f"✅ File received: {csv_file.name}")
        
        # Validate file type
        if not csv_file.name.endswith('.csv'):
            print("❌ Not a CSV file")
            return Response({'error': 'File must be CSV format'}, status=400)
        
        # Read CSV with pandas
        try:
            df = pd.read_csv(csv_file)
            print(f"✅ CSV read successfully: {len(df)} rows")
        except Exception as e:
            print(f"❌ Error reading CSV: {str(e)}")
            return Response({'error': f'Error reading CSV: {str(e)}'}, status=400)
        
        # Validate required columns
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ Missing columns: {missing_columns}")
            return Response(
                {'error': f'Missing required columns: {", ".join(missing_columns)}'},
                status=400
            )
        
        # Calculate statistics
        total_count = len(df)
        avg_flowrate = df['Flowrate'].mean()
        avg_pressure = df['Pressure'].mean()
        avg_temperature = df['Temperature'].mean()
        type_counts = df['Type'].value_counts().to_dict()
        
        print(f"📊 Statistics calculated: {total_count} equipment, {len(type_counts)} types")
        
        # Save file
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{csv_file.name}"
        file_path = os.path.join(upload_dir, filename)
        
        with open(file_path, 'wb+') as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)
        
        print(f"💾 File saved: {file_path}")
        
        # Create dataset record
        dataset = Dataset.objects.create(
            filename=csv_file.name,
            total_count=total_count,
            avg_flowrate=float(avg_flowrate),
            avg_pressure=float(avg_pressure),
            avg_temperature=float(avg_temperature),
            type_distribution=type_counts,
            file_path=file_path
        )
        
        print(f"✅ Dataset created with ID: {dataset.id}")
        
        # Create equipment records
        equipment_objects = []
        for _, row in df.iterrows():
            equipment_objects.append(
                Equipment(
                    dataset=dataset,
                    name=row['Equipment Name'],
                    equipment_type=row['Type'],
                    flowrate=float(row['Flowrate']),
                    pressure=float(row['Pressure']),
                    temperature=float(row['Temperature'])
                )
            )
        
        Equipment.objects.bulk_create(equipment_objects)
        print(f"✅ Created {len(equipment_objects)} equipment records")
        
        # Keep only last 5 datasets
        old_datasets = Dataset.objects.all().order_by('-upload_date')[5:]
        if old_datasets.exists():
            for old_dataset in old_datasets:
                if old_dataset.file_path and os.path.exists(old_dataset.file_path):
                    os.remove(old_dataset.file_path)
            old_datasets.delete()
            print(f"🗑️ Cleaned up old datasets, keeping last 5")
        
        # Return response
        serializer = DatasetSerializer(dataset)
        print("✅ Upload successful!")
        return Response({
            'message': 'File uploaded successfully',
            'data': serializer.data
        }, status=201)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response(
            {'error': f'Server error: {str(e)}'},
            status=500
        )

@api_view(['GET'])
def get_dataset(request, dataset_id):
    """Get dataset details"""
    try:
        dataset = Dataset.objects.get(id=dataset_id)
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)
    except Dataset.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

@api_view(['GET'])
def get_history(request):
    """Get last 5 uploads"""
    datasets = Dataset.objects.all().order_by('-upload_date')[:5]
    serializer = DatasetSerializer(datasets, many=True)
    return Response({'count': len(datasets), 'datasets': serializer.data})

@api_view(['GET'])
def generate_pdf(request, dataset_id):
    """Generate PDF report"""
    try:
        dataset = Dataset.objects.get(id=dataset_id)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{dataset_id}.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        elements.append(Paragraph("Equipment Report", styles['Title']))
        elements.append(Spacer(1, 12))
        
        # Summary
        summary_data = [
            ['Total Equipment', str(dataset.total_count)],
            ['Avg Flowrate', f"{dataset.avg_flowrate:.2f}"],
            ['Avg Pressure', f"{dataset.avg_pressure:.2f}"],
            ['Avg Temperature', f"{dataset.avg_temperature:.2f}"]
        ]
        t = Table(summary_data)
        t.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.grey)
        ]))
        elements.append(t)
        
        doc.build(elements)
        return response
    except Dataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=404)
    except Exception as e:
        return Response({'error': f'Error generating PDF: {str(e)}'}, status=500)

@api_view(['GET'])
def health_check(request):
    """Check if API is running"""
    return Response({'status': 'healthy', 'datasets': Dataset.objects.count()})

@api_view(['GET'])
def get_summary(request, dataset_id):
    """Get dataset summary"""
    return JsonResponse({
        "dataset_id": dataset_id,
        "summary": "summary endpoint working"
    })