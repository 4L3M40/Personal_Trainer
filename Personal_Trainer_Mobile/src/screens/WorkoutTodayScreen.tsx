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
  end_date?: string | null;
}

interface SetLog {
  id: number;
  workout_exercise: number;
  set_number: number;
  reps_done: number;
  load_used: string;
}

interface Session {
  id: number;
  finished_at: string | null;
  set_logs: SetLog[];
}

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
  const [currentExercise, setCurrentExercise] = useState(0);
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
  }, [loadToday]);

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
      Alert.alert("Treino iniciado", "Registre suas séries abaixo.");
    } catch {
      Alert.alert("Erro", "Não foi possível iniciar o treino.");
    }
  }

  async function handleLogSet(exercise: Exercise, setNumber: number) {
    if (!session) {
      Alert.alert("Atenção", "Inicie o treino primeiro.");
      return;
    }

    const key = exercise.id * 100 + setNumber;
    setLoggingSet(key);

    try {
      const res = await api.post(
        `/api/v1/student/sessions/${session.id}/log-set/`,
        {
          workout_exercise: exercise.id,
          set_number: setNumber,
          reps_done: parseInt(exercise.reps, 10) || 0,
          load_used: exercise.suggested_load || "0",
          is_done: true,
        }
      );

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
        text: "Finalizar",
        onPress: async () => {
          try {
            const res = await api.post(
              `/api/v1/student/sessions/${session.id}/finish/`
            );
            setSession(res.data.session);
            Alert.alert("Parabéns", "Treino finalizado com sucesso.");
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
      (log) =>
        log.workout_exercise === exerciseId && log.set_number === setNumber
    );
  }

  function handleRefresh() {
    setRefreshing(true);
    loadToday();
  }

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#4f6ef7" />
        <Text style={styles.loadingText}>Carregando treino...</Text>
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
  const exercises = currentDay?.items ?? [];
  const currentEx = exercises[currentExercise];
  const isFinished = !!session?.finished_at;

  const totalSets = exercises.reduce((acc, ex) => acc + ex.sets, 0);
  const doneSets = session?.set_logs?.length || 0;
  const progress = totalSets > 0 ? Math.round((doneSets / totalSets) * 100) : 0;

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View>
          <Text style={styles.headerTitle}>{plan.name}</Text>
          <Text style={styles.headerSub}>
            {isFinished
              ? "✅ Treino finalizado!"
              : session
              ? `🔥 ${progress}% concluído`
              : "Pronto para treinar?"}
          </Text>
        </View>

        <TouchableOpacity onPress={handleLogout}>
          <Text style={styles.logoutIcon}>⎋</Text>
        </TouchableOpacity>
      </View>

      {session && !isFinished && (
        <View style={styles.progressWrapper}>
          <View style={styles.progressInfo}>
            <Text style={styles.progressText}>
              Exercício {Math.min(currentExercise + 1, exercises.length)} de{" "}
              {exercises.length}
            </Text>
            <Text style={styles.progressText}>{progress}%</Text>
          </View>

          <View style={styles.progressBar}>
            <View style={[styles.progressFill, { width: `${progress}%` }]} />
          </View>
        </View>
      )}

      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        style={styles.tabs}
      >
        {days.map((day, idx) => (
          <TouchableOpacity
            key={day.id}
            style={[styles.tab, activeDay === idx && styles.tabActive]}
            onPress={() => {
              setActiveDay(idx);
              setCurrentExercise(0);
            }}
          >
            <Text
              style={[
                styles.tabText,
                activeDay === idx && styles.tabTextActive,
              ]}
            >
              {day.label}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      <FlatList
        data={session && !isFinished && currentEx ? [currentEx] : exercises}
        keyExtractor={(item) => String(item.id)}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={handleRefresh} />
        }
        contentContainerStyle={styles.list}
        ListHeaderComponent={
          <>
            {!session && !isFinished && (
              <TouchableOpacity
                style={styles.startBtn}
                onPress={handleStartWorkout}
              >
                <Text style={styles.startBtnText}>▶ Iniciar Treino</Text>
              </TouchableOpacity>
            )}

            {session && !isFinished && (
              <View style={styles.executionBox}>
                <Text style={styles.executionTitle}>Treino em execução</Text>
                <Text style={styles.executionSub}>
                  Complete as séries do exercício atual.
                </Text>
              </View>
            )}
          </>
        }
        renderItem={({ item: ex }) => (
          <View style={styles.card}>
            <Text style={styles.exName}>🏋️ {ex.exercise_name}</Text>

            <View style={styles.exMeta}>
              <Text style={styles.exMetaText}>
                {ex.sets} séries × {ex.reps} reps
              </Text>

              {ex.suggested_load ? (
                <Text style={styles.exMetaText}>Carga: {ex.suggested_load}</Text>
              ) : null}

              {ex.rest_seconds > 0 ? (
                <Text style={styles.exMetaText}>Descanso: {ex.rest_seconds}s</Text>
              ) : null}
            </View>

            {ex.notes ? <Text style={styles.exNotes}>📝 {ex.notes}</Text> : null}

            {session && !isFinished && (
              <View style={styles.setsBox}>
                <Text style={styles.setsTitle}>Séries</Text>

                <View style={styles.setsRow}>
                  {Array.from({ length: ex.sets }, (_, i) => i + 1).map(
                    (setNum) => {
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
                              {done ? "✓" : `${setNum}`}
                            </Text>
                          )}
                        </TouchableOpacity>
                      );
                    }
                  )}
                </View>
              </View>
            )}
          </View>
        )}
        ListFooterComponent={
          session && !isFinished ? (
            <View style={styles.footerActions}>
              {currentExercise < exercises.length - 1 ? (
                <TouchableOpacity
                  style={styles.nextBtn}
                  onPress={() => setCurrentExercise((prev) => prev + 1)}
                >
                  <Text style={styles.nextBtnText}>Próximo Exercício</Text>
                </TouchableOpacity>
              ) : null}

              <TouchableOpacity style={styles.finishBtn} onPress={handleFinish}>
                <Text style={styles.finishBtnText}>Finalizar Treino</Text>
              </TouchableOpacity>
            </View>
          ) : null
        }
        ListEmptyComponent={
          <Text style={styles.emptyText}>Nenhum exercício neste dia.</Text>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#0f1117",
  },
  center: {
    flex: 1,
    backgroundColor: "#0f1117",
    justifyContent: "center",
    alignItems: "center",
    padding: 24,
  },
  loadingText: {
    color: "#888",
    marginTop: 12,
    fontSize: 14,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingTop: 56,
    paddingHorizontal: 20,
    paddingBottom: 18,
    backgroundColor: "#1c1f2e",
  },
  headerTitle: {
    color: "#fff",
    fontSize: 24,
    fontWeight: "800",
  },
  headerSub: {
    color: "#9ca3af",
    fontSize: 14,
    marginTop: 4,
  },
  logoutIcon: {
    color: "#9ca3af",
    fontSize: 24,
  },
  progressWrapper: {
    backgroundColor: "#1c1f2e",
    paddingHorizontal: 20,
    paddingBottom: 16,
  },
  progressInfo: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 8,
  },
  progressText: {
    color: "#cbd5e1",
    fontSize: 13,
    fontWeight: "600",
  },
  progressBar: {
    height: 7,
    backgroundColor: "#2a2d3e",
    borderRadius: 99,
    overflow: "hidden",
  },
  progressFill: {
    height: "100%",
    backgroundColor: "#4f6ef7",
  },
  tabs: {
    paddingHorizontal: 16,
    paddingVertical: 12,
    backgroundColor: "#1c1f2e",
    borderBottomWidth: 1,
    borderBottomColor: "#2a2d3e",
    flexGrow: 0,
  },
  tab: {
    paddingHorizontal: 18,
    paddingVertical: 9,
    borderRadius: 999,
    marginRight: 10,
    backgroundColor: "#2a2d3e",
  },
  tabActive: {
    backgroundColor: "#4f6ef7",
  },
  tabText: {
    color: "#9ca3af",
    fontSize: 14,
    fontWeight: "700",
  },
  tabTextActive: {
    color: "#fff",
  },
  list: {
    padding: 16,
    paddingBottom: 50,
  },
  startBtn: {
    backgroundColor: "#4f6ef7",
    borderRadius: 14,
    padding: 18,
    alignItems: "center",
    marginBottom: 16,
  },
  startBtnText: {
    color: "#fff",
    fontWeight: "800",
    fontSize: 17,
  },
  executionBox: {
    backgroundColor: "#151827",
    borderWidth: 1,
    borderColor: "#2a2d3e",
    borderRadius: 14,
    padding: 14,
    marginBottom: 16,
  },
  executionTitle: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "800",
  },
  executionSub: {
    color: "#9ca3af",
    fontSize: 13,
    marginTop: 4,
  },
  card: {
    backgroundColor: "#1c1f2e",
    borderRadius: 18,
    padding: 18,
    marginBottom: 14,
    borderWidth: 1,
    borderColor: "#2a2d3e",
  },
  exName: {
    color: "#fff",
    fontSize: 20,
    fontWeight: "800",
    marginBottom: 10,
  },
  exMeta: {
    flexDirection: "row",
    gap: 12,
    flexWrap: "wrap",
    marginBottom: 4,
  },
  exMetaText: {
    color: "#9ca3af",
    fontSize: 14,
  },
  exNotes: {
    color: "#8b8f9f",
    fontSize: 13,
    marginTop: 8,
    fontStyle: "italic",
  },
  setsBox: {
    marginTop: 18,
    paddingTop: 14,
    borderTopWidth: 1,
    borderTopColor: "#2a2d3e",
  },
  setsTitle: {
    color: "#cbd5e1",
    fontSize: 13,
    fontWeight: "700",
    marginBottom: 10,
    textTransform: "uppercase",
    letterSpacing: 0.6,
  },
  setsRow: {
    flexDirection: "row",
    gap: 10,
    flexWrap: "wrap",
  },
  setBtn: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: "#2a2d3e",
    justifyContent: "center",
    alignItems: "center",
    borderWidth: 2,
    borderColor: "#3a3d50",
  },
  setBtnDone: {
    backgroundColor: "#22c55e",
    borderColor: "#22c55e",
  },
  setBtnText: {
    color: "#fff",
    fontSize: 15,
    fontWeight: "800",
  },
  footerActions: {
    marginTop: 2,
  },
  nextBtn: {
    backgroundColor: "#4f6ef7",
    borderRadius: 14,
    padding: 16,
    alignItems: "center",
    marginBottom: 10,
  },
  nextBtnText: {
    color: "#fff",
    fontWeight: "800",
    fontSize: 15,
  },
  finishBtn: {
    backgroundColor: "#22c55e",
    borderRadius: 14,
    padding: 16,
    alignItems: "center",
  },
  finishBtnText: {
    color: "#fff",
    fontWeight: "800",
    fontSize: 15,
  },
  emptyIcon: {
    fontSize: 48,
    marginBottom: 12,
  },
  emptyTitle: {
    color: "#fff",
    fontSize: 22,
    fontWeight: "800",
    marginBottom: 8,
  },
  emptyText: {
    color: "#9ca3af",
    fontSize: 14,
    textAlign: "center",
  },
  logoutBtn: {
    marginTop: 24,
    backgroundColor: "#2a2d3e",
    borderRadius: 12,
    paddingHorizontal: 26,
    paddingVertical: 13,
  },
  logoutText: {
    color: "#fff",
    fontWeight: "700",
  },
});