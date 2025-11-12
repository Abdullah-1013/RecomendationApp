// screens/RecommendationScreen.js
import React, { useEffect, useState } from "react";
import { View, Text, FlatList, ActivityIndicator, StyleSheet } from "react-native";

const API_BASE = "http://192.168.0.104:8000";

export default function RecommendationScreen({ route }) {
  const { userId } = route.params;
  const [loading, setLoading] = useState(true);
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/recommendations`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, top_n: 8 }),
      });
      const data = await res.json();
      if (res.ok) setProducts(data.recommendations || []);
      else {
        console.error("Recommendation error:", data);
      }
    } catch (err) {
      console.error("Fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <ActivityIndicator style={{ flex: 1 }} size="large" />;

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Recommendations</Text>
      <FlatList
        data={products}
        keyExtractor={(item) => item.id}
        contentContainerStyle={{ paddingBottom: 30 }}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.name}>{item.name}</Text>
            <Text>Price: {item.price}</Text>
            <Text>Sustainable: {item.is_sustainable ? "Yes" : "No"}</Text>
          </View>
        )}
        ListEmptyComponent={<Text>No recommendations available.</Text>}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  header: { fontSize: 20, fontWeight: "bold", marginBottom: 12, textAlign: "center" },
  card: { padding: 12, borderRadius: 8, backgroundColor: "#f2f2f2", marginBottom: 10 },
  name: { fontSize: 16, fontWeight: "600" },
});
