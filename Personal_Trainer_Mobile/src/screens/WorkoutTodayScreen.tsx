import React, { useEffect, useState, useCallback } from "react";
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  Alert,
  ScrollView,
  RefreshControl,
} from "react-native";
import api from "../api/client";
import { clearTokens } from "../storage/token";

// ─── Tipos ──────────────────────────────────────────────────────────────────

interface Exercise {
  id: number;
  exercise_name: string;
  sets: number;
  reps: string;
  suggested_load: string;
  rest_seconds: number;
  notes: string;
}

interface WorkoutDay {
  id: number;
  label: string;
  order: number;
  items: Exercise[];
}

interface WorkoutPlan {
  id: number;
  name: string;
  days: WorkoutDay[];
}

interface Assignment {
  id: number;
  start_date: string;
}

interface Session {
  id: number;
  finished_at: string | null;
  set_logs: SetLog[];
}

interface SetLog {
  id: number;
  workout_exercise: number;
  set_number: number;
  reps_done: number;
  load_used: string;
}

// ─── Componente ─────────────────────────────────────────────────────────────

interface Props {
  onLogout: () => void;
}

export default function WorkoutTodayScreen({ onLogout }: Props) {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [assignment, setAssignment] = useState<Assignment | null>(null);
  const [plan, setPlan] = useState<WorkoutPlan | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [activeDay, setActiveDay] = useState(0);
  const [loggingSet, setLoggingSet] = useState<number | null>(null);

  const loadToday = useCallback(async () => {
    try {
      const res = await api.get("/api/v1/student/workouts/today/");
      setAssignment(res.data.assignment);
      setPlan(res.data.workout);
    } catch (err: any) {
      if (err.response?.status === 404) {
        setAssignment(null);
        setPlan(null);
      } else {
        Alert.alert("Erro", "Não foi possível carregar o treino.");
      }
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    loadToday();
  }, []);

  async function handleLogout() {
    await clearTokens();
    onLogout();
  }

  async function handleStartWorkout() {
    if (!assignment) return;
    try {
      const res = await api.post(
        `/api/v1/student/workouts/${assignment.id}/start/`
      );
      setSession(res.data.session);
      Alert.alert("✅ Treino iniciado!", "Registre suas séries abaixo.");
    } catch {
      Alert.alert("Erro", "Não foi possível iniciar o treino.");
    }
  }

  async function handleLogSet(exercise: Exercise, setNumber: number) {
    if (!session) {
      Alert.alert("Atenção", "Inicie o treino primeiro.");
      return;
    }
    setLoggingSet(exercise.id * 100 + setNumber);
    try {
      const res = await api.post(`/api/v1/student/sessions/${session.id}/log-set/`, {
        workout_exercise: exercise.id,
        set_number: setNumber,
        reps_done: parseInt(exercise.reps) || 0,
        load_used: exercise.suggested_load || "0",
        is_done: true,
      });
      setSession(res.data.session);
    } catch {
      Alert.alert("Erro", "Não foi possível registrar a série.");
    } finally {
      setLoggingSet(null);
    }
  }

  async function handleFinish() {
    if (!session) return;
    Alert.alert("Finalizar treino?", "Você confirma que terminou?", [
      { text: "Cancelar", style: "cancel" },
      {
        text: "Finalizar ✅",
        onPress: async () => {
          try {
            const res = await api.post(
              `/api/v1/student/sessions/${session.id}/finish/`
            );
            setSession(res.data.session);
          } catch {
            Alert.alert("Erro", "Não foi possível finalizar.");
          }
        },
      },
    ]);
  }

  function isSetDone(exerciseId: number, setNumber: number): boolean {
    if (!session) return false;
    return session.set_logs.some(
      (log) => log.workout_exercise === exerciseId && log.set_number === setNumber
    );
  }

  // ─── Render ───────────────────────────────────────────────────────────────

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#4f6ef7" />
      </View>
    );
  }

  if (!plan) {
    return (
      <View style={styles.center}>
        <Text style={styles.emptyIcon}>😴</Text>
        <Text style={styles.emptyTitle}>Nenhum treino hoje</Text>
        <Text style={styles.emptyText}>
          Seu personal ainda não atribuiu um treino ativo.
        </Text>
        <TouchableOpacity style={styles.logoutBtn} onPress={handleLogout}>
          <Text style={styles.logoutText}>Sair</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const days = plan.days ?? [];
  const currentDay = days[activeDay];
  const isFinished = !!session?.finished_at;

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.headerTitle}>{plan.name}</Text>
          <Text style={styles.headerSub}>
            {isFinished
              ? "✅ Treino finalizado!"
              : session
              ? "🔥 Treino em andamento"
              : "Pronto para treinar?"}
          </Text>
        </View>
        <TouchableOpacity onPress={handleLogout}>
          <Text style={styles.logoutIcon}>⎋</Text>
        </TouchableOpacity>
      </View>

      {/* Day tabs */}
      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.tabs}>
        {days.map((day, idx) => (
          <TouchableOpacity
            key={day.id}
            style={[styles.tab, activeDay === idx && styles.tabActive]}
            onPress={() => setActiveDay(idx)}
          >
            <Text style={[styles.tabText, activeDay === idx && styles.tabTextActive]}>
              {day.label}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* Exercise list */}
      <FlatList
        data={currentDay?.items ?? []}
        keyExtractor={(item) => String(item.id)}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={() => { setRefreshing(true); loadToday(); }} />
        }
        contentContainerStyle={styles.list}
        ListHeaderComponent={
          !session && !isFinished ? (
            <TouchableOpacity style={styles.startBtn} onPress={handleStartWorkout}>
              <Text style={styles.startBtnText}>▶  Iniciar Treino</Text>
            </TouchableOpacity>
          ) : isFinished ? null : (
            <TouchableOpacity style={styles.finishBtn} onPress={handleFinish}>
              <Text style={styles.finishBtnText}>🏁  Finalizar Treino</Text>
            </TouchableOpacity>
          )
        }
        renderItem={({ item: ex }) => (
          <View style={styles.card}>
            <Text style={styles.exName}>{ex.exercise_name}</Text>
            <View style={styles.exMeta}>
              <Text style={styles.exMetaText}>
                {ex.sets} séries × {ex.reps} reps
              </Text>
              {ex.suggested_load ? (
                <Text style={styles.exMetaText}>🏋️ {ex.suggested_load}</Text>
              ) : null}
              {ex.rest_seconds > 0 ? (
                <Text style={styles.exMetaText}>⏱ {ex.rest_seconds}s</Text>
              ) : null}
            </View>
            {ex.notes ? (
              <Text style={styles.exNotes}>📝 {ex.notes}</Text>
            ) : null}

            {/* Series buttons */}
            {session && !isFinished && (
              <View style={styles.setsRow}>
                {Array.from({ length: ex.sets }, (_, i) => i + 1).map((setNum) => {
                  const done = isSetDone(ex.id, setNum);
                  const key = ex.id * 100 + setNum;
                  return (
                    <TouchableOpacity
                      key={setNum}
                      style={[styles.setBtn, done && styles.setBtnDone]}
                      onPress={() => !done && handleLogSet(ex, setNum)}
                      disabled={done || loggingSet === key}
                    >
                      {loggingSet === key ? (
                        <ActivityIndicator size="small" color="#fff" />
                      ) : (
                        <Text style={styles.setBtnText}>
                          {done ? "✓" : `S${setNum}`}
                        </Text>
                      )}
                    </TouchableOpacity>
                  );
                })}
              </View>
            )}
          </View>
        )}
        ListEmptyComponent={
          <Text style={styles.emptyText}>Nenhum exercício neste dia.</Text>
        }
      />
    </View>
  );
}

// ─── Styles ──────────────────────────────────────────────────────────────────

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0f1117" },
  center: {
    flex: 1,
    backgroundColor: "#0f1117",
    justifyContent: "center",
    alignItems: "center",
    padding: 24,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingTop: 56,
    paddingHorizontal: 20,
    paddingBottom: 16,
    backgroundColor: "#1c1f2e",
  },
  headerTitle: { color: "#fff", fontSize: 20, fontWeight: "700" },
  headerSub: { color: "#888", fontSize: 13, marginTop: 2 },
  logoutIcon: { color: "#888", fontSize: 22 },
  tabs: {
    paddingHorizontal: 16,
    paddingVertical: 10,
    backgroundColor: "#1c1f2e",
    borderBottomWidth: 1,
    borderBottomColor: "#2a2d3e",
    flexGrow: 0,
  },
  tab: {
    paddingHorizontal: 14,
    paddingVertical: 6,
    borderRadius: 20,
    marginRight: 8,
    backgroundColor: "#2a2d3e",
  },
  tabActive: { backgroundColor: "#4f6ef7" },
  tabText: { color: "#888", fontSize: 13, fontWeight: "600" },
  tabTextActive: { color: "#fff" },
  list: { padding: 16, paddingBottom: 40 },
  startBtn: {
    backgroundColor: "#4f6ef7",
    borderRadius: 12,
    padding: 16,
    alignItems: "center",
    marginBottom: 16,
  },
  startBtnText: { color: "#fff", fontWeight: "700", fontSize: 16 },
  finishBtn: {
    backgroundColor: "#27ae60",
    borderRadius: 12,
    padding: 14,
    alignItems: "center",
    marginBottom: 16,
  },
  finishBtnText: { color: "#fff", fontWeight: "700", fontSize: 15 },
  card: {
    backgroundColor: "#1c1f2e",
    borderRadius: 14,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: "#2a2d3e",
  },
  exName: { color: "#fff", fontSize: 16, fontWeight: "700", marginBottom: 6 },
  exMeta: { flexDirection: "row", gap: 12, flexWrap: "wrap", marginBottom: 4 },
  exMetaText: { color: "#888", fontSize: 13 },
  exNotes: { color: "#666", fontSize: 12, marginTop: 4, fontStyle: "italic" },
  setsRow: {
    flexDirection: "row",
    gap: 8,
    marginTop: 12,
    flexWrap: "wrap",
  },
  setBtn: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: "#2a2d3e",
    justifyContent: "center",
    alignItems: "center",
    borderWidth: 2,
    borderColor: "#3a3d50",
  },
  setBtnDone: { backgroundColor: "#27ae60", borderColor: "#27ae60" },
  setBtnText: { color: "#fff", fontSize: 13, fontWeight: "700" },
  emptyIcon: { fontSize: 48, marginBottom: 12 },
  emptyTitle: { color: "#fff", fontSize: 20, fontWeight: "700", marginBottom: 8 },
  emptyText: { color: "#888", fontSize: 14, textAlign: "center" },
  logoutBtn: {
    marginTop: 24,
    backgroundColor: "#2a2d3e",
    borderRadius: 10,
    paddingHorizontal: 24,
    paddingVertical: 12,
  },
  logoutText: { color: "#fff", fontWeight: "600" },
});
