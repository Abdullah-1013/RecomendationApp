import React, { useState } from 'react';
import { View, TextInput, Button, Alert } from 'react-native';

export default function SignupScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignup = async () => {
    try {
      const res = await fetch("http://192.168.1.104:5000/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (data.error) {
        Alert.alert("Error", data.error);
      } else {
        Alert.alert("Success", "User signed up successfully!");
        navigation.navigate("Login");
      }
    } catch (err) {
      console.log(err);
      Alert.alert("Error", "Something went wrong during signup.");
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <TextInput placeholder="Email" value={email} onChangeText={setEmail} autoCapitalize="none" />
      <TextInput placeholder="Password" value={password} onChangeText={setPassword} secureTextEntry />
      <Button title="Sign Up" onPress={handleSignup} />
    </View>
  );
}
