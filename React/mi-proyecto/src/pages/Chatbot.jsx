import React, { useState } from "react";
import { auth } from "../firebaseConfig";

const Chatbot = () => {
  const [mensaje, setMensaje] = useState("");
  const [respuesta, setRespuesta] = useState("");
  const [loading, setLoading] = useState(false);

  const enviarMensaje = async () => {
    setLoading(true);
    setRespuesta("");

    try {
      const user = auth.currentUser;
      if (!user) {
        throw new Error("Usuario no autenticado");
      }

      const token = await user.getIdToken();

      const response = await fetch("https://lumiapi-luzj.onrender.com/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ mensaje }),
      });

      const data = await response.json();
      if (response.ok) {
        setRespuesta(data.respuesta);
      } else {
        setRespuesta(`Error: ${data.error}`);
        console.error("Detalles:", data.detail);
      }
    } catch (error) {
      console.error("Error al enviar mensaje:", error);
      setRespuesta("No se pudo enviar el mensaje.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Chat con OpenAI</h1>
      <textarea
        className="w-full p-2 border rounded mb-4"
        rows={4}
        placeholder="Escribe tu mensaje..."
        value={mensaje}
        onChange={(e) => setMensaje(e.target.value)}
      />
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        onClick={enviarMensaje}
        disabled={loading}
      >
        {loading ? "Enviando..." : "Enviar"}
      </button>
      {respuesta && (
        <div className="mt-4 p-3 border rounded bg-gray-50">
          <strong>Respuesta:</strong>
          <p>{respuesta}</p>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
