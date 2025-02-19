from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd

#Post request responsible for generating suggestions
class ProcessSalesReport(APIView):
    def get(self, request, *args, **kwargs):
        return Response("API Base URL", status=status.HTTP_200_OK)
    

    def post(self, request, format=None):
        sales_file = request.FILES.get('sales_report')
        if not sales_file:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Check the file extension to determine how to read it
            file_name = sales_file.name.lower()
            if file_name.endswith('.csv'):
                df = pd.read_csv(sales_file, encoding='utf-8-sig')
            elif file_name.endswith('.xls') or file_name.endswith('.xlsx'):
                df = pd.read_excel(sales_file, encoding='utf-8-sig')
            else:
                return Response({'error': 'Unsupported file format.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Process the DataFrame to generate order suggestions.
            report = self.generate_order_suggestions(df)
            return Response(report, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def generate_order_suggestions(self, df):
        """
        Example: Group sales by 'product_name' and calculate a suggested order amount 
        as 10% more than the total sold quantity.
        Expected columns: 'product_name', 'quantity_sold'
        """
        df.columns = df.columns.str.strip()
        if 'product_name' not in df.columns or 'quantity_sold' not in df.columns:
            return {'error': 'Missing required columns: product_name and/or quantity_sold.'}
        
        suggestions = {}
        grouped = df.groupby('product_name')['quantity_sold'].sum().reset_index()
        for _, row in grouped.iterrows():
            product = row['product_name']
            sold = row['quantity_sold']
            suggested_order = int(sold * 1.1)  # Order 10% more
            suggestions[product] = {
                'total_sold': sold,
                'suggested_order': suggested_order
            }
        return suggestions

#Returns home screen for uploading the CSV file
class FrontendAppView(TemplateView):
    template_name = 'index.html'



