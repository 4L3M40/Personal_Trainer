import { useState } from "react";
import LoginScreen from "../src/screens/LoginScreen";
import WorkoutTodayScreen from "../src/screens/WorkoutTodayScreen";

export default function Index() {
  const [loggedIn, setLoggedIn] = useState(false);

  if (loggedIn) {
    return <WorkoutTodayScreen onLogout={() => setLoggedIn(false)} />;
  }

  return <LoginScreen onLoginSuccess={() => setLoggedIn(true)} />;
}