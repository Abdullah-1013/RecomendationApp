import React, { useState, useEffect } from 'react';
import { View, Text, Alert } from 'react-native';
import { Camera } from 'expo-camera';
import { checkProduct } from '../services/productService';

export default function ScannerScreen({ navigation }) {
  const [hasPermission, setHasPermission] = useState(null);
  const [scanned, setScanned] = useState(false);

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  const handleBarcode = async ({ data }) => {
    if (scanned) return;
    setScanned(true);

    try {
      const result = await checkProduct(data); // backend check
      if (result.exists) {
        Alert.alert('Product Exists', 'This product is already in the database.');
      } else {
        navigation.navigate('AddProductScreen', { qrId: data });
      }
    } catch (err) {
      Alert.alert('Error', 'Backend connection failed.');
    }
  };

  if (hasPermission === null) return <Text>Requesting camera permission...</Text>;
  if (hasPermission === false) return <Text>No access to camera</Text>;

  return (
    <Camera
      style={{ flex: 1 }}
      onBarCodeScanned={handleBarcode}
    />
  );
}
