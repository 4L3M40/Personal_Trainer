import AsyncStorage from "@react-native-async-storage/async-storage";

const ACCESS_KEY = "@pt:access_token";
const REFRESH_KEY = "@pt:refresh_token";

export async function saveTokens(access: string, refresh: string) {
  await AsyncStorage.multiSet([
    [ACCESS_KEY, access],
    [REFRESH_KEY, refresh],
  ]);
}

export async function getToken(type: "access" | "refresh"): Promise<string | null> {
  return AsyncStorage.getItem(type === "access" ? ACCESS_KEY : REFRESH_KEY);
}

export async function clearTokens() {
  await AsyncStorage.multiRemove([ACCESS_KEY, REFRESH_KEY]);
}

export async function hasSession(): Promise<boolean> {
  const token = await getToken("access");
  return !!token;
}
