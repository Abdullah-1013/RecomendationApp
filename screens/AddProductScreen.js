import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert, ScrollView, StyleSheet } from 'react-native';
import { addProduct } from '../services/productService';

export default function AddProductScreen({ route, navigation }) {
  const { table, query } = route.params;

  const [name, setName] = useState(query);

  // You can add more state variables here for other columns if needed
  const [price, setPrice] = useState('');

  const handleAdd = async () => {
    if (!name) return Alert.alert('Error', 'Please enter product name');

    const productData = { name };

    // Add price if exists
    if (price) productData.price_pkr = price;

    try {
      await addProduct(table, productData);
      Alert.alert('Success', 'Product added successfully');
      navigation.goBack();
    } catch (err) {
      console.log(err);
      Alert.alert('Error', 'Failed to add product.');
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Add New Product ({table})</Text>
      <TextInput
        style={styles.input}
        value={name}
        onChangeText={setName}
        placeholder="Enter product name"
      />
      <TextInput
        style={styles.input}
        value={price}
        onChangeText={setPrice}
        placeholder="Enter price (optional)"
        keyboardType="numeric"
      />
      <Button title="Add Product" onPress={handleAdd} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flexGrow: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  title: { fontSize: 18, marginBottom: 10, textAlign: 'center' },
  input: { borderWidth: 1, borderColor: '#ccc', width: '100%', padding: 10, marginBottom: 20 },
});
