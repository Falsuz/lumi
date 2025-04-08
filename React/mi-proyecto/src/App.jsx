import './App.css'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Welcome from "./pages/Welcome";
import AuthForm from "./pages/AuthForm";
import Preferencias from "./pages/Preferences";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Welcome />} />
        <Route path="/auth" element={<AuthForm />} />
        <Route path="/preferencias" element={<Preferencias />} />
      </Routes>
    </Router>
  );
}

export default App;
