import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert, StyleSheet, Picker } from 'react-native';
import { checkProduct } from '../services/productService';

export default function SearchScreen({ navigation }) {
  const [query, setQuery] = useState('');
  const [table, setTable] = useState('air_conditioners');

  const handleSearch = async () => {
    if (!query) return Alert.alert('Error', 'Please enter a product name');

    try {
      const result = await checkProduct(table, query);
      if (result.exists) {
        Alert.alert('Product Exists', 'This product is already in the database.');
      } else {
        navigation.navigate('AddProductScreen', { table, query });
      }
    } catch (err) {
      console.log(err);
      Alert.alert('Error', 'Failed to connect to database.');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Select Table:</Text>
      <Picker
        selectedValue={table}
        style={{ height: 50, width: 200 }}
        onValueChange={(itemValue) => setTable(itemValue)}
      >
        <Picker.Item label="Air Conditioners" value="air_conditioners" />
        <Picker.Item label="Cars" value="cars" />
        <Picker.Item label="Bikes" value="bikes" />
        <Picker.Item label="Records" value="records" />
      </Picker>

      <Text style={styles.title}>Search Product:</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter product name"
        value={query}
        onChangeText={setQuery}
      />
      <Button title="Search" onPress={handleSearch} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  title: { fontSize: 18, marginBottom: 10 },
  input: { borderWidth: 1, borderColor: '#ccc', width: '100%', padding: 10, marginBottom: 20 },
});
