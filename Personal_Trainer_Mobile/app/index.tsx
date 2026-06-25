import { useEffect } from "react";
import { useAuth } from "../src/context/AuthContext";
import { router } from "expo-router";

export default function Index() {
  const { isLoggedIn, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading) {
      if (isLoggedIn) {
        router.replace("/(tabs)");
      } else {
        router.replace("/login");
      }
    }
  }, [isLoggedIn, isLoading]);

  return null;
}