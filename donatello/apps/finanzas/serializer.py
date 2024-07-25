from rest_framework import serializers
from .models import Finanza

class FinanzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finanza
        fields = ('id_finanza', 'tipo', 'monto', 'fecha', 'id_usuario', 'motivo', 'descripcion')

    def validate(self, data):
            if data['tipo'] == 'spend':
                if not data.get('motivo'):
                    raise serializers.ValidationError("Motivo es requerido si el tipo es 'Gasto'.")
                if not data.get('descripcion'):
                    raise serializers.ValidationError("Descripcion es requerida si el tipo es 'Gasto'.")
            return data