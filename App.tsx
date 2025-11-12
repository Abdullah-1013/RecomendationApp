// App.tsx
import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import LoginScreen from "./screens/LoginScreen";
import SignupScreen from "./screens/SignupScreen";
import RecommendationScreen from "./screens/RecommendationScreen";

export type RootStackParamList = {
  Login: undefined;
  Signup: undefined;
  Recommendations: { userId: string };
};

const Stack = createStackNavigator<RootStackParamList>();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Signup">
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Signup" component={SignupScreen} />
        <Stack.Screen name="Recommendations" component={RecommendationScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
