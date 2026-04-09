import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCunosmRaGDy07nmaqKUXqDUO4j9AjmsQM",
  authDomain: "we-care-hospitals-6ab3d.firebaseapp.com",
  projectId: "we-care-hospitals-6ab3d",
  storageBucket: "we-care-hospitals-6ab3d.firebasestorage.app",
  messagingSenderId: "1036047451432",
  appId: "1:1036047451432:web:3052f1ec508eda785d7c1d"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export default app;
