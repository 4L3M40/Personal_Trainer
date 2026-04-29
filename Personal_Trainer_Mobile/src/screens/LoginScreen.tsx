import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import axios from "axios";
import { BASE_URL } from "../api/client";
import { saveTokens } from "../storage/token";

interface Props {
  onLoginSuccess: () => void;
}

export default function LoginScreen({ onLoginSuccess }: Props) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleLogin() {
    if (!username.trim() || !password.trim()) {
      Alert.alert("Atenção", "Preencha usuário e senha.");
      return;
    }
    setLoading(true);
    try {
      const res = await axios.post(`${BASE_URL}/api/v1/auth/login/`, {
        username: username.trim(),
        password,
      });
      await saveTokens(res.data.access, res.data.refresh);
      onLoginSuccess();
    } catch (err: any) {
      const msg =
        err.response?.status === 401
          ? "Usuário ou senha incorretos."
          : "Erro ao conectar. Verifique o servidor.";
      Alert.alert("Erro", msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <View style={styles.card}>
        <Text style={styles.logo}>💪</Text>
        <Text style={styles.title}>Personal Trainer</Text>
        <Text style={styles.subtitle}>Entre com sua conta</Text>

        <TextInput
          style={styles.input}
          placeholder="Usuário"
          placeholderTextColor="#888"
          autoCapitalize="none"
          value={username}
          onChangeText={setUsername}
        />

        <TextInput
          style={styles.input}
          placeholder="Senha"
          placeholderTextColor="#888"
          secureTextEntry
          value={password}
          onChangeText={setPassword}
        />

        <TouchableOpacity
          style={[styles.btn, loading && styles.btnDisabled]}
          onPress={handleLogin}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.btnText}>Entrar</Text>
          )}
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#0f1117",
    justifyContent: "center",
    alignItems: "center",
    padding: 24,
  },
  card: {
    width: "100%",
    maxWidth: 360,
    backgroundColor: "#1c1f2e",
    borderRadius: 16,
    padding: 32,
    alignItems: "center",
    shadowColor: "#000",
    shadowOpacity: 0.4,
    shadowRadius: 12,
    elevation: 8,
  },
  logo: {
    fontSize: 48,
    marginBottom: 8,
  },
  title: {
    fontSize: 24,
    fontWeight: "700",
    color: "#fff",
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 14,
    color: "#888",
    marginBottom: 28,
  },
  input: {
    width: "100%",
    backgroundColor: "#2a2d3e",
    borderRadius: 10,
    padding: 14,
    color: "#fff",
    fontSize: 15,
    marginBottom: 14,
    borderWidth: 1,
    borderColor: "#3a3d50",
  },
  btn: {
    width: "100%",
    backgroundColor: "#4f6ef7",
    borderRadius: 10,
    padding: 15,
    alignItems: "center",
    marginTop: 6,
  },
  btnDisabled: {
    opacity: 0.6,
  },
  btnText: {
    color: "#fff",
    fontWeight: "700",
    fontSize: 16,
  },
});
