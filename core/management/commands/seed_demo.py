from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta

from crm.models import Client, Plan
from library.models import Exercise, Food
from workouts.models import WorkoutPlan, WorkoutDay, WorkoutExercise
from diets.models import DietPlan, Meal, MealItem
from agenda.models import Alert, Appointment

class Command(BaseCommand):
    help = "Cria dados de exemplo para navegar no protótipo."

    def handle(self, *args, **options):
        # Planos
        cutting, _ = Plan.objects.get_or_create(name="Cutting")
        bulking, _ = Plan.objects.get_or_create(name="Bulking")
        manut, _ = Plan.objects.get_or_create(name="Manutenção")

        # Clientes
        Client.objects.get_or_create(
            full_name="João Silva",
            defaults=dict(age=32, weight_kg=80.2, height_m=1.78, plan=cutting, last_activity_at=date.today()-timedelta(days=2)),
        )
        Client.objects.get_or_create(
            full_name="Maria Souza",
            defaults=dict(age=28, weight_kg=62.4, height_m=1.65, plan=bulking, last_activity_at=date.today()-timedelta(days=4)),
        )
        Client.objects.get_or_create(
            full_name="Pedro Lima",
            defaults=dict(age=35, weight_kg=91.0, height_m=1.82, plan=manut, status=Client.Status.PAUSED, last_activity_at=date.today()-timedelta(days=10)),
        )

        # Biblioteca
        supino, _ = Exercise.objects.get_or_create(name="Supino Reto", defaults={"muscle_group":"Peito"})
        agach, _ = Exercise.objects.get_or_create(name="Agachamento", defaults={"muscle_group":"Pernas"})
        pux, _ = Exercise.objects.get_or_create(name="Puxada Frontal", defaults={"muscle_group":"Costas"})
        desenv, _ = Exercise.objects.get_or_create(name="Desenvolvimento", defaults={"muscle_group":"Ombros"})
        Exercise.objects.get_or_create(name="Crossover", defaults={"muscle_group":"Peito"})
        Exercise.objects.get_or_create(name="Tríceps Pulley", defaults={"muscle_group":"Braços"})
        Exercise.objects.get_or_create(name="Leg Press", defaults={"muscle_group":"Pernas"})
        Exercise.objects.get_or_create(name="Stiff", defaults={"muscle_group":"Pernas"})
        Exercise.objects.get_or_create(name="Remada Baixa", defaults={"muscle_group":"Costas"})
        Exercise.objects.get_or_create(name="Rosca Direta", defaults={"muscle_group":"Braços"})

        frango, _ = Food.objects.get_or_create(name="Peito de Frango", defaults={"portion_label":"100g","kcal":165,"protein_g":31,"carbs_g":0,"fats_g":4})
        arroz, _ = Food.objects.get_or_create(name="Arroz Branco", defaults={"portion_label":"100g","kcal":130,"protein_g":2.7,"carbs_g":28,"fats_g":0.3})
        batata, _ = Food.objects.get_or_create(name="Batata Doce", defaults={"portion_label":"100g","kcal":86,"protein_g":1.6,"carbs_g":20,"fats_g":0.1})
        whey, _ = Food.objects.get_or_create(name="Whey Protein", defaults={"portion_label":"30g","kcal":120,"protein_g":24,"carbs_g":3,"fats_g":1.5})

        # Treino modelo
        wp, _ = WorkoutPlan.objects.get_or_create(name="ABC Cutting", defaults={"tags":"Hipertrofia, ABC"})
        if not wp.days.exists():
            d1 = WorkoutDay.objects.create(plan=wp, label="Dia A", order=1)
            d2 = WorkoutDay.objects.create(plan=wp, label="Dia B", order=2)
            d3 = WorkoutDay.objects.create(plan=wp, label="Dia C", order=3)
            WorkoutExercise.objects.create(day=d1, exercise=supino, sets=4, reps="10-12", rest_seconds=60)
            WorkoutExercise.objects.create(day=d2, exercise=agach, sets=4, reps="8-10", rest_seconds=90)
            WorkoutExercise.objects.create(day=d3, exercise=pux, sets=4, reps="10-12", rest_seconds=60)

        # Dieta modelo
        dp, _ = DietPlan.objects.get_or_create(name="Cutting 1800kcal", defaults={"total_kcal":1800})
        if not dp.meals.exists():
            cafe = Meal.objects.create(plan=dp, name="Café da manhã", order=1)
            lanche = Meal.objects.create(plan=dp, name="Lanche", order=2)
            almoco = Meal.objects.create(plan=dp, name="Almoço", order=3)
            jantar = Meal.objects.create(plan=dp, name="Jantar", order=4)

            MealItem.objects.create(meal=cafe, food=whey, quantity_label="30g", kcal=120, protein_g=24, carbs_g=3, fats_g=1.5)
            MealItem.objects.create(meal=lanche, food=frango, quantity_label="100g", kcal=165, protein_g=31, carbs_g=0, fats_g=4)
            MealItem.objects.create(meal=almoco, food=arroz, quantity_label="100g", kcal=130, protein_g=2.7, carbs_g=28, fats_g=0.3)
            MealItem.objects.create(meal=jantar, food=batata, quantity_label="100g", kcal=86, protein_g=1.6, carbs_g=20, fats_g=0.1)

        # Alertas e agenda
        Alert.objects.get_or_create(title="7 pendências de acompanhamento", defaults={"is_open": True})
        if not Appointment.objects.exists():
            now = timezone.now()
            Appointment.objects.create(title="Consulta João", starts_at=now+timedelta(days=1, hours=10), ends_at=now+timedelta(days=1, hours=11))
            Appointment.objects.create(title="Atualizar treino Maria", starts_at=now+timedelta(days=2, hours=15), ends_at=now+timedelta(days=2, hours=16))
            Appointment.objects.create(title="Avaliação Pedro", starts_at=now+timedelta(days=4, hours=17), ends_at=now+timedelta(days=4, hours=18))

        self.stdout.write(self.style.SUCCESS("Dados de exemplo criados/atualizados com sucesso."))
