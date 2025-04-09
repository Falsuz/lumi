import './App.css'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Welcome from "./pages/Welcome";
import AuthForm from "./pages/AuthForm";
import Preferences from "./pages/Preferences";
import Chatbot from "./pages/Chatbot"; 

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Welcome />} />
        <Route path="/auth" element={<AuthForm />} />
        <Route path="/chat" element={<Chatbot />} />
        <Route path="/preferencias" element={<Preferences />} />
      </Routes>
    </Router>
  );
}

export default App;
