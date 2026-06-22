import { Stack } from "expo-router";
import { AuthProvider, useAuth } from "../src/context/AuthContext";

function RootNavigator() {
  const { isLoggedIn, isLoading } = useAuth();

  // Enquanto carrega a sessão, mostra loading. Isso previne flickering da tela de login.
  if (isLoading) {
    return null;
  }

  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Protected guard={!isLoggedIn}>
        <Stack.Screen name="login" />
      </Stack.Protected>
      <Stack.Protected guard={isLoggedIn}>
        <Stack.Screen name="(tabs)" />
      </Stack.Protected>
    </Stack>
  );
}

export default function AppLayout() {
  return (
    <AuthProvider>
      <RootNavigator />
    </AuthProvider>
  );
}
