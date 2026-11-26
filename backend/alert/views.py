
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from config.permissions import IsOperator, IsVictim, IsVictimOrOperator
from alert.models import Alert
from alert.serializers import AlertSerializer


class AlertViewSet(ModelViewSet):
    serializer_class = AlertSerializer

    # Déterminer les alertes accessibles selon le rôle
    def get_queryset(self):
        user = self.request.user

        try:
            profile = user.profile
        except Exception:
            return Alert.objects.none()

        if profile.role in ["SUPERADMIN", "ADMIN", "OPERATEUR"]:
            return Alert.objects.all()

        if profile.role == "VICTIM":
            return Alert.objects.filter(profile=profile)

        return Alert.objects.none()

    # Permissions selon l'action
    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, IsVictim]

        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsOperator]

        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, IsVictimOrOperator]
        
        elif self.action == "update_location":
            permission_classes = [IsAuthenticated, IsVictim]
            
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    # Création d'une alerte
    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    # Annulation logique d'une alerte
    def perform_destroy(self, instance):
        profile = self.request.user.profile

        # Une victime peut annuler uniquement une alerte en attente
        if profile.role == "VICTIM":
            if instance.status != Alert.Status.PENDING:
                raise PermissionDenied(
                    "Vous ne pouvez pas annuler une alerte déjà prise en charge."
                )

        # On conserve l'alerte dans la base de données
        instance.status = Alert.Status.CANCELLED
        instance.save(update_fields=["status", "updated_at"])

    # Historique des alertes
    @action(detail=False, methods=["get"], url_path="history")
    def history(self, request):
        profile = request.user.profile

        alerts = Alert.objects.filter(
            profile=profile
        ).order_by("-created_at")

        serializer = self.get_serializer(alerts, many=True)

        return Response(serializer.data)
    
    # Modifier la géolocalisation d'une alerte
    @action(detail=True, methods=["patch"], url_path="update-location")
    def update_location(self, request, pk=None):
        alert = self.get_object()

        # Vérifier que l'alerte n'est pas terminée
        if alert.status in ["RESOLVED", "CANCELLED", "CLOSED"]:
            raise PermissionDenied(
                "Impossible de modifier la position d'une alerte terminée."
            )

        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
        address = request.data.get("address")

        if latitude is None or longitude is None:
            return Response(
                {"error": "La latitude et la longitude sont obligatoires."},
                status=status.HTTP_400_BAD_REQUEST
            )

        alert.latitude = latitude
        alert.longitude = longitude

        if address is not None:
            alert.address = address

        alert.save()

        return Response({
            "message": "Géolocalisation mise à jour avec succès.",
            "alert_id": alert.id,
            "latitude": alert.latitude,
            "longitude": alert.longitude,
            "address": alert.address
        })
