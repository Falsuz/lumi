import { useNavigate } from "react-router-dom";

function Chatbot() {
  const navigate = useNavigate();

  return (
    <div>
      <h1>Conversa con Lumi</h1>
      <p>Tu acompañante psicológico con IA personalizado.</p>

    </div>
  );
}

export default Chatbot;
