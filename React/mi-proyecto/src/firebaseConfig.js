// firebaseConfig.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyAOxXknLjV-nVbL5cdp0-i3SRfFZXeGyg8",
  authDomain: "lumi-5f571.firebaseapp.com",
  projectId: "lumi-5f571",
  storageBucket: "lumi-5f571.firebasestorage.app",
  messagingSenderId: "189031354741",
  appId: "1:189031354741:web:7a4dfccedca35e0589033c"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
