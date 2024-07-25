from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F
from django.db.models import Sum
from django.http import JsonResponse
from rest_framework import status

from donatello.apps.finanzas.serializer import FinanzaSerializer


from .models import Finanza

from datetime import date
from django.utils import timezone


class FinanzaListCreate(generics.ListCreateAPIView):
    serializer_class = FinanzaSerializer
    def get_queryset(self):
        id_usuario = self.kwargs['id_usuario']
        return Finanza.objects.filter(id_usuario=id_usuario)

class FinanzaDetail(generics.RetrieveAPIView):
    queryset = Finanza.objects.all()
    serializer_class = FinanzaSerializer

class FinanzaUpdate(generics.UpdateAPIView):
    queryset = Finanza.objects.all()
    serializer_class = FinanzaSerializer 

class FinanzaDelete(generics.DestroyAPIView):
    queryset = Finanza.objects.all()
    serializer_class = FinanzaSerializer
    

class IngresoTotal(APIView):
    def get(self, request, id_usuario):
        try:
            today = timezone.now().date()
            # Calcular fechas
            inicio_semana = today - timezone.timedelta(days=today.weekday())  # Lunes de la semana actual
            inicio_mes = today.replace(day=1)  # Primer día del mes actual

            # Calcular total de ingresos en la semana
            total_ingresos_semana = Finanza.objects.filter(
                fecha__range=[inicio_semana, today], 
                tipo='income', id_usuario=id_usuario
            ).aggregate(total=Sum('monto'))['total'] or 0
            
            # Calcular total de ingresos en el mes
            total_ingresos_mes = Finanza.objects.filter(
                fecha__range=[inicio_mes, today], 
                tipo='income', id_usuario=id_usuario
            ).aggregate(total=Sum('monto'))['total'] or 0

            # Preparar respuesta
            response_data = {
                'total_ingresos_semana': total_ingresos_semana,
                'total_ingresos_mes': total_ingresos_mes,
            }

            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class FinanceReport(APIView):
    def get(self, request):
        try:
            # Cálculos para el reporte
            today = date.today()
            current_year = today.year
            current_month = today.month

            # Ventas del mes actual
            ventas_mes_actual = Finanza.objects.filter(fecha__year=current_year, fecha__month=current_month,tipo='income').aggregate(total_ventas_mes=Sum('monto'))['total_ventas_mes'] or 0

            # Ventas del día actual
            ventas_dia_actual = Finanza.objects.filter(fecha=today,tipo='income').aggregate(total_ventas_dia=Sum('monto'))['total_ventas_dia'] or 0

            ventas_temporada_actual = Finanza.objects.filter(fecha__year=current_year,tipo='income').aggregate(total_ventas_temporada=Sum('monto'))['total_ventas_temporada'] or 0

            mes_mas_vendido = Finanza.objects.filter(fecha__year=current_year,tipo='income').values('fecha__month').annotate(total_ventas_mes=Sum('monto')).order_by('-total_ventas_mes').first()
            if mes_mas_vendido:
              mes_mas_vendido = mes_mas_vendido['fecha__month']
            else:
              mes_mas_vendido = None

            # Validar si los costos superaron las ventas en algún mes
            costos_por_mes = Finanza.objects.filter(tipo='spend').values('fecha__year', 'fecha__month').annotate(total_costos_mes=Sum('monto'))
            ventas_por_mes = Finanza.objects.filter(tipo='income').values('fecha__year', 'fecha__month').annotate(total_ventas_mes=Sum('monto'))
        
            mes_costos_superaron_ventas = None
            for costos in costos_por_mes:
                ventas = next((venta for venta in ventas_por_mes if venta['fecha__year'] == costos['fecha__year'] and venta['fecha__month'] == costos['fecha__month']), None)
                if ventas and costos['total_costos_mes'] > ventas['total_ventas_mes']:
                    mes_costos_superaron_ventas = costos['fecha__month']
                break

            report_data = {
            'ventas_mes_actual': ventas_mes_actual,
            'ventas_dia_actual': ventas_dia_actual,
            'ventas_temporada_actual': ventas_temporada_actual,
            'mes_mas_vendido': mes_mas_vendido,
            'mes_costo_superaron_ventas': mes_costos_superaron_ventas,
            }
            return JsonResponse(report_data)
        except Exception as e:
           return JsonResponse({'error': str(e)}, status=500)
        

class FinanzaCreateView(APIView):
    def post(self, request, format=None):
        serializer = FinanzaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)