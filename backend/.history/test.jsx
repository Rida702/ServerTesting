import React, { Component } from 'react';
import { View, Button } from 'react-native';

export default class MyApp extends Component {
  
  uploadImageToDjango = async () => {
    const watchpicturePath = await axios.get('https://www.shutterstock.com/image-photo/luxury-watch-isolated-on-white-260nw-1528296152.jpg');
    const wristpicturePath = await axios.get('https://img.freepik.com/premium-photo/female-hand-holds-something-isolated-white-wall_270100-481.jpg');
    const URLpath = "https://94a0-103-4-95-6.ngrok-free.app/api/uploadWristImage/"; // Your Django backend URL

    const formData = new FormData();
    formData.append("watchImage", { uri: watchpicturePath.uri, name: 'watchImage.jpg', type: 'image/jpeg' }); // Use unique name for watch image
    formData.append("wristImage", { uri: wristpicturePath.uri, name: 'wristImage.jpg', type: 'image/jpeg' }); // Use unique name for wrist image
    formData.append("remark", "Hello");

    try {
      const response = await fetch(URLpath, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'multipart/form-data',
        },
        body: formData
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const responseJson = await response.json();
      console.log(responseJson);
      // Handle success, if needed
    } catch (error) {
      console.error('Error uploading image:', error);
      // Handle error, if needed
    }
  }

  render() {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <Button       
          title="Upload Image"
          onPress={this.uploadImageToDjango}
        />
      </View>
    );
  }
}
