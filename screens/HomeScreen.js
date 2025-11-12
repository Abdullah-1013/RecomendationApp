import React, { useEffect, useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useNavigation, useRoute } from '@react-navigation/native';

const HomeScreen = () => {
  const navigation = useNavigation();
  const route = useRoute();
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    if (route.params?.userId) {
      setUserId(route.params.userId);
      AsyncStorage.setItem('loggedUserId', route.params.userId.toString());
    } else {
      AsyncStorage.getItem('loggedUserId').then((storedId) => {
        if (storedId) {
          setUserId(storedId);
        } else {
          navigation.replace('LoginScreen');
        }
      });
    }
  }, []);

  const handleLogout = async () => {
    await AsyncStorage.removeItem('loggedUserId');
    navigation.replace('LoginScreen');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome User: {userId}</Text>

      <TouchableOpacity
        style={styles.button}
        onPress={() => navigation.navigate('PurchaseScreen', { userId })}
      >
        <Text style={styles.buttonText}>Add Dummy Purchases</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.button}
        onPress={() => Alert.alert('Coming Soon', 'Recommendation logic will be added in Phase 3')}
      >
        <Text style={styles.buttonText}>Get Recommendations</Text>
      </TouchableOpacity>

      <TouchableOpacity style={[styles.button, styles.logoutButton]} onPress={handleLogout}>
        <Text style={styles.buttonText}>Logout</Text>
      </TouchableOpacity>
    </View>
  );
};

export default HomeScreen;

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  title: { fontSize: 22, fontWeight: 'bold', marginBottom: 30 },
  button: {
    width: '100%',
    backgroundColor: 'blue',
    padding: 15,
    borderRadius: 8,
    marginBottom: 15,
    alignItems: 'center',
  },
  logoutButton: {
    backgroundColor: 'red',
  },
  buttonText: { color: 'white', fontSize: 16, fontWeight: 'bold' },
});
