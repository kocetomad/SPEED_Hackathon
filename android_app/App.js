import React, { Component } from "react";
import { StyleSheet, View } from "react-native";
import CupertinoButtonWarning from "./components/CupertinoButtonWarning";
import MaterialHeader12 from "./components/MaterialHeader12";
import MaterialSlider from "./components/MaterialSlider";

function Untitled(props) {
  return (
    <View style={styles.container}>
      <View style={styles.cupertinoButtonWarning3Row}>
        <CupertinoButtonWarning
          style={styles.cupertinoButtonWarning3}
        ></CupertinoButtonWarning>
        <View style={styles.cupertinoButtonWarning3Filler}></View>
        <CupertinoButtonWarning
          style={styles.cupertinoButtonWarning4}
        ></CupertinoButtonWarning>
      </View>
      <View style={styles.cupertinoButtonWarning5Row}>
        <CupertinoButtonWarning
          style={styles.cupertinoButtonWarning5}
        ></CupertinoButtonWarning>
        <View style={styles.cupertinoButtonWarning5Filler}></View>
        <CupertinoButtonWarning
          style={styles.cupertinoButtonWarning6}
        ></CupertinoButtonWarning>
      </View>
      <MaterialHeader12 style={styles.materialHeader12}></MaterialHeader12>
      <MaterialSlider style={styles.materialSlider}></MaterialSlider>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1
  },
  cupertinoButtonWarning3: {
    height: 138,
    width: 161,
    shadowColor: "rgba(0,0,0,1)",
    shadowOffset: {
      width: 3,
      height: 3
    },
    elevation: 5,
    shadowOpacity: 0.27,
    shadowRadius: 0
  },
  cupertinoButtonWarning3Filler: {
    flex: 1,
    flexDirection: "row"
  },
  cupertinoButtonWarning4: {
    height: 138,
    shadowColor: "rgba(0,0,0,1)",
    shadowOffset: {
      width: 3,
      height: 3
    },
    elevation: 5,
    shadowOpacity: 0.27,
    shadowRadius: 0,
    width: 161
  },
  cupertinoButtonWarning3Row: {
    height: 138,
    flexDirection: "row",
    marginTop: 103,
    marginLeft: 9,
    marginRight: 12
  },
  cupertinoButtonWarning5: {
    height: 138,
    width: 161,
    shadowColor: "rgba(0,0,0,1)",
    shadowOffset: {
      width: 3,
      height: 3
    },
    elevation: 5,
    shadowOpacity: 0.27,
    shadowRadius: 0
  },
  cupertinoButtonWarning5Filler: {
    flex: 1,
    flexDirection: "row"
  },
  cupertinoButtonWarning6: {
    height: 138,
    shadowColor: "rgba(0,0,0,1)",
    shadowOffset: {
      width: 3,
      height: 3
    },
    elevation: 5,
    shadowOpacity: 0.27,
    shadowRadius: 0,
    width: 161
  },
  cupertinoButtonWarning5Row: {
    height: 138,
    flexDirection: "row",
    marginTop: 18,
    marginLeft: 9,
    marginRight: 12
  },
  materialHeader12: {
    height: 51,
    width: 360,
    marginTop: -397,
    alignSelf: "center"
  },
  materialSlider: {
    height: 30,
    width: 307,
    marginTop: 488,
    marginLeft: 28
  }
});

export default Untitled;