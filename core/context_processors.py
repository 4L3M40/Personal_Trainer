from crm.models import Client
from workouts.models import WorkoutPlan
from diets.models import DietPlan
from agenda.models import Alert

def nav_counts(request):
    """Contadores no menu lateral (usados como destaque de métricas no protótipo)."""
    try:
        return {
            "nav_clients_count": Client.objects.filter(status=Client.Status.ACTIVE).count(),
            "nav_workouts_today": WorkoutPlan.objects.filter(is_active=True).count(),
            "nav_diets_active": DietPlan.objects.filter(is_active=True).count(),
            "nav_alerts_count": Alert.objects.filter(is_open=True).count(),
        }
    except Exception:
        # Durante migrações (ou banco vazio) não queremos quebrar o layout.
        return {"nav_clients_count": 0, "nav_workouts_today": 0, "nav_diets_active": 0, "nav_alerts_count": 0}
