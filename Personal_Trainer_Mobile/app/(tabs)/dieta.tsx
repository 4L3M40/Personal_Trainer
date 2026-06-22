import React from "react";
import { View, Text, StyleSheet } from "react-native";

export default function DietaScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Dieta</Text>
      <Text style={styles.placeholder}>Em desenvolvimento...</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#F8F8F8",
  },
  title: {
    fontSize: 24,
    fontWeight: "700",
    color: "#222",
    marginBottom: 16,
  },
  placeholder: {
    fontSize: 16,
    color: "#999",
  },
});
