import React, { useEffect, useState, useCallback } from "react";
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  Alert,
  RefreshControl,
  Modal,
  TextInput,
} from "react-native";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { api } from "../../src/api/client";
import { useAuth } from "../../src/context/AuthContext";

interface HomeData {
  student_name: string;
  weight: {
    current_kg: number | null;
    recorded_on: string | null;
  };
  today_workout: {
    assignment_id: number;
    plan_name: string;
    day_label: string;
  } | null;
  today_diet: {
    plan_name: string;
    target_kcal: number;
  } | null;
  summary: {
    workouts_done_month: number;
    workouts_target_month: number;
    meals_done_today: number;
    meals_total_today: number;
    last_photo_upload: string | null;
  };
}

export default function HomeScreen() {
  const { logout } = useAuth();
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [data, setData] = useState<HomeData | null>(null);
  const [showWeightModal, setShowWeightModal] = useState(false);
  const [weightInput, setWeightInput] = useState("");

  const loadHome = useCallback(async () => {
    try {
      const res = await api.get("/api/v1/student/home/");
      setData(res.data);
    } catch (err: any) {
      Alert.alert("Erro", "Não foi possível carregar a home.");
      console.error(err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    loadHome();
  }, [loadHome]);

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    loadHome();
  }, [loadHome]);

  async function handleRegisterWeight() {
    if (!weightInput.trim()) {
      Alert.alert("Atenção", "Digite seu peso.");
      return;
    }

    const weight = parseFloat(weightInput);
    if (isNaN(weight) || weight <= 0) {
      Alert.alert("Atenção", "Peso inválido.");
      return;
    }

    try {
      const res = await api.post("/api/v1/student/weight/", {
        weight_kg: weight,
      });
      setData((prev) => {
        if (!prev) return null;
        return {
          ...prev,
          weight: res.data,
        };
      });
      setShowWeightModal(false);
      setWeightInput("");
      Alert.alert("Sucesso", "Peso registrado com sucesso!");
    } catch (err: any) {
      Alert.alert("Erro", "Não foi possível registrar o peso.");
      console.error(err);
    }
  }

  async function handleLogout() {
    Alert.alert("Confirmar", "Deseja fazer logout?", [
      { text: "Cancelar", style: "cancel" },
      {
        text: "Sair",
        onPress: async () => {
          await logout();
        },
        style: "destructive",
      },
    ]);
  }

  if (loading || !data) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#FF6B35" />
      </View>
    );
  }

  const workoutProgress = data.summary.workouts_target_month
    ? Math.round(
        (data.summary.workouts_done_month / data.summary.workouts_target_month) *
          100
      )
    : 0;

  const mealProgress =
    data.summary.meals_total_today > 0
      ? Math.round(
          (data.summary.meals_done_today / data.summary.meals_total_today) * 100
        )
      : 0;

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* Header com nome e logout */}
      <View style={styles.header}>
        <View>
          <Text style={styles.greeting}>Olá,</Text>
          <Text style={styles.userName}>{data.student_name}</Text>
        </View>
        <TouchableOpacity
          onPress={handleLogout}
          style={styles.logoutButton}
        >
          <MaterialCommunityIcons name="logout" size={24} color="#FF6B35" />
        </TouchableOpacity>
      </View>

      {/* Card de Peso */}
      <TouchableOpacity
        style={styles.weightCard}
        onPress={() => setShowWeightModal(true)}
      >
        <View>
          <Text style={styles.weightValue}>
            {data.weight.current_kg
              ? `${data.weight.current_kg.toFixed(1)} kg`
              : "-- kg"}
          </Text>
          {data.weight.recorded_on && (
            <Text style={styles.weightDate}>
              Registrado em {data.weight.recorded_on}
            </Text>
          )}
        </View>
        <TouchableOpacity
          onPress={() => setShowWeightModal(true)}
          style={styles.registerWeightButton}
        >
          <Text style={styles.registerWeightButtonText}>
            {data.weight.current_kg ? "Atualizar" : "Registrar"} Peso
          </Text>
        </TouchableOpacity>
      </TouchableOpacity>

      {/* Card de Treino de Hoje */}
      {data.today_workout && (
        <View style={styles.card}>
          <View style={styles.cardHeader}>
            <MaterialCommunityIcons
              name="dumbbell"
              size={20}
              color="#FF6B35"
            />
            <Text style={styles.cardTitle}>Treino de Hoje</Text>
          </View>
          <View style={styles.cardContent}>
            <Text style={styles.workoutPlanName}>
              {data.today_workout.plan_name}
            </Text>
            <Text style={styles.workoutDay}>
              {data.today_workout.day_label}
            </Text>
          </View>
          <TouchableOpacity style={styles.cardButton}>
            <Text style={styles.cardButtonText}>Iniciar Treino</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* Card de Dieta */}
      {data.today_diet && (
        <View style={styles.card}>
          <View style={styles.cardHeader}>
            <MaterialCommunityIcons name="apple" size={20} color="#FF6B35" />
            <Text style={styles.cardTitle}>Dieta de Hoje</Text>
          </View>
          <View style={styles.cardContent}>
            <Text style={styles.dietPlanName}>
              {data.today_diet.plan_name}
            </Text>
            <Text style={styles.dietKcal}>
              {data.today_diet.target_kcal} kcal
            </Text>
            <View style={styles.progressBar}>
              <View
                style={[
                  styles.progressFill,
                  {
                    width: `${Math.min(mealProgress, 100)}%`,
                    backgroundColor: mealProgress === 100 ? "#4CAF50" : "#FF6B35",
                  },
                ]}
              />
            </View>
            <Text style={styles.progressText}>
              {data.summary.meals_done_today}/{data.summary.meals_total_today}{" "}
              refeições
            </Text>
          </View>
          <TouchableOpacity style={styles.cardButton}>
            <Text style={styles.cardButtonText}>Ver Refeições</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* Card de Resumo */}
      <View style={styles.summaryContainer}>
        <View style={styles.summaryCard}>
          <MaterialCommunityIcons
            name="dumbbell"
            size={24}
            color="#FF6B35"
          />
          <Text style={styles.summaryValue}>
            {data.summary.workouts_done_month}/{data.summary.workouts_target_month}
          </Text>
          <Text style={styles.summaryLabel}>Treinos no mês</Text>
        </View>
        <View style={styles.summaryCard}>
          <MaterialCommunityIcons name="camera" size={24} color="#FF6B35" />
          <Text style={styles.summaryValue}>
            {data.summary.last_photo_upload ? "✓" : "-"}
          </Text>
          <Text style={styles.summaryLabel}>Última foto</Text>
        </View>
      </View>

      {/* Modal de Registrar Peso */}
      <Modal visible={showWeightModal} transparent animationType="fade">
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Registrar Peso</Text>
            <TextInput
              style={styles.weightInput}
              placeholder="Digite seu peso (kg)"
              placeholderTextColor="#999"
              keyboardType="decimal-pad"
              value={weightInput}
              onChangeText={setWeightInput}
            />
            <View style={styles.modalButtons}>
              <TouchableOpacity
                style={[styles.modalButton, styles.cancelButton]}
                onPress={() => {
                  setShowWeightModal(false);
                  setWeightInput("");
                }}
              >
                <Text style={styles.cancelButtonText}>Cancelar</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.modalButton, styles.confirmButton]}
                onPress={handleRegisterWeight}
              >
                <Text style={styles.confirmButtonText}>Registrar</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F8F8F8",
    paddingHorizontal: 16,
    paddingTop: 16,
  },
  centerContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 24,
  },
  greeting: {
    fontSize: 14,
    color: "#999",
    fontWeight: "400",
  },
  userName: {
    fontSize: 24,
    fontWeight: "700",
    color: "#222",
    marginTop: 4,
  },
  logoutButton: {
    padding: 8,
  },
  weightCard: {
    backgroundColor: "#FF6B35",
    borderRadius: 12,
    padding: 20,
    marginBottom: 16,
    flexDirection: "column",
    justifyContent: "space-between",
  },
  weightValue: {
    fontSize: 32,
    fontWeight: "700",
    color: "#FFFFFF",
  },
  weightDate: {
    fontSize: 12,
    color: "#FFCCB3",
    marginTop: 4,
  },
  registerWeightButton: {
    backgroundColor: "rgba(255,255,255,0.3)",
    borderRadius: 8,
    paddingVertical: 10,
    paddingHorizontal: 16,
    marginTop: 12,
    alignSelf: "flex-start",
  },
  registerWeightButtonText: {
    color: "#FFFFFF",
    fontSize: 12,
    fontWeight: "600",
  },
  card: {
    backgroundColor: "#FFFFFF",
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    shadowColor: "#000",
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  cardHeader: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 12,
  },
  cardTitle: {
    fontSize: 14,
    fontWeight: "600",
    color: "#222",
    marginLeft: 8,
  },
  cardContent: {
    marginBottom: 12,
  },
  workoutPlanName: {
    fontSize: 16,
    fontWeight: "600",
    color: "#222",
  },
  workoutDay: {
    fontSize: 14,
    color: "#666",
    marginTop: 4,
  },
  dietPlanName: {
    fontSize: 16,
    fontWeight: "600",
    color: "#222",
    marginBottom: 4,
  },
  dietKcal: {
    fontSize: 14,
    color: "#666",
    marginBottom: 8,
  },
  progressBar: {
    height: 6,
    backgroundColor: "#E0E0E0",
    borderRadius: 3,
    overflow: "hidden",
    marginBottom: 8,
  },
  progressFill: {
    height: "100%",
    borderRadius: 3,
  },
  progressText: {
    fontSize: 12,
    color: "#999",
    fontWeight: "500",
  },
  cardButton: {
    backgroundColor: "#FF6B35",
    borderRadius: 8,
    paddingVertical: 12,
    alignItems: "center",
  },
  cardButtonText: {
    color: "#FFFFFF",
    fontSize: 14,
    fontWeight: "600",
  },
  summaryContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 24,
  },
  summaryCard: {
    flex: 1,
    backgroundColor: "#FFFFFF",
    borderRadius: 12,
    padding: 16,
    alignItems: "center",
    marginHorizontal: 6,
    shadowColor: "#000",
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  summaryValue: {
    fontSize: 20,
    fontWeight: "700",
    color: "#FF6B35",
    marginVertical: 8,
  },
  summaryLabel: {
    fontSize: 12,
    color: "#999",
    fontWeight: "500",
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.5)",
    justifyContent: "center",
    alignItems: "center",
  },
  modalContent: {
    backgroundColor: "#FFFFFF",
    borderRadius: 16,
    padding: 24,
    width: "80%",
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: "700",
    color: "#222",
    marginBottom: 16,
    textAlign: "center",
  },
  weightInput: {
    borderWidth: 1,
    borderColor: "#E0E0E0",
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 12,
    fontSize: 16,
    marginBottom: 16,
    color: "#222",
  },
  modalButtons: {
    flexDirection: "row",
    gap: 12,
  },
  modalButton: {
    flex: 1,
    borderRadius: 8,
    paddingVertical: 12,
    alignItems: "center",
  },
  cancelButton: {
    backgroundColor: "#E0E0E0",
  },
  cancelButtonText: {
    color: "#666",
    fontSize: 14,
    fontWeight: "600",
  },
  confirmButton: {
    backgroundColor: "#FF6B35",
  },
  confirmButtonText: {
    color: "#FFFFFF",
    fontSize: 14,
    fontWeight: "600",
  },
});
