import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import SearchScreen from './screens/SearchScreen';
import AddProductScreen from './screens/AddProductScreen';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="SearchScreen">
        <Stack.Screen name="SearchScreen" component={SearchScreen} options={{ title: 'Search Product' }} />
        <Stack.Screen name="AddProductScreen" component={AddProductScreen} options={{ title: 'Add Product' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
