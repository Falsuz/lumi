import { useNavigate } from "react-router-dom";

function Welcome() {
  const navigate = useNavigate();

  return (
    <div>
      <h1>Bienvenido a Lumi</h1>
      <p>Tu acompañante psicológico con IA personalizado.</p>
      <button onClick={() => navigate("/auth")}>Empezar</button>
    </div>
  );
}

export default Welcome;
