import React from "react";
import { View, Text } from "react-native";

export default function ProductFoundScreen({ route }) {
  const { product } = route.params;

  return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 22 }}>Product Found!</Text>
      <Text>Name: {product.name}</Text>
      <Text>Brand: {product.brand}</Text>
      <Text>Model: {product.model}</Text>
      <Text>Year: {product.year}</Text>
      <Text>Engine: {product.engine}</Text>
      <Text>Price: {product.price}</Text>
    </View>
  );
}
