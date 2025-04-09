// src/pages/Preferencias.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getAuth } from "firebase/auth";

// Debemos implementar una opcion para actualizar preferencias

function Preferences() {
  const [form, setForm] = useState({
    fueATerapia: "",
    estiloDeComunicacion: "",
    nivelAnsiedad: "",
    motivoDeUso: ""
  });

  const navigate = useNavigate();
  const auth = getAuth();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const user = auth.currentUser;

    if (user) {
      const idToken = await user.getIdToken(); // Obtenemos el token del usuario

      try {
        const response = await fetch("http://localhost:5000/api/preferencias", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${idToken}`, // Enviamos el token en los headers
          },
          body: JSON.stringify(form),
        });

        const data = await response.json();
        if (response.ok) {
          alert("Preferencias guardadas correctamente");
          navigate("/chat"); 
        } else {
          console.error("Error al guardar preferencias:", data.error);
        }
      } catch (error) {
        console.error("Error de comunicación con el backend:", error);
      }
    }
  };

  return (
    <div>
      <h2>Personaliza tu experiencia</h2>
      <form onSubmit={handleSubmit}>
        <label>
          ¿Has ido a terapia psicológica antes?
          <select name="fueATerapia" onChange={handleChange} required>
            <option value="">Seleccione</option>
            <option value="si">Sí</option>
            <option value="no">No</option>
          </select>
        </label>

        <label>
          ¿Cuál es tu estilo de comunicación preferido?
          <select name="estiloDeComunicacion" onChange={handleChange} required>
            <option value="">Seleccione</option>
            <option value="empatico">Empático y comprensivo</option>
            <option value="directo">Directo y al grano</option>
            <option value="reflexivo">Reflexivo y pausado</option>
          </select>
        </label>

        <label>
          ¿Cómo describirías tu nivel actual de ansiedad?
          <select name="nivelAnsiedad" onChange={handleChange} required>
            <option value="">Seleccione</option>
            <option value="bajo">Bajo</option>
            <option value="medio">Medio</option>
            <option value="alto">Alto</option>
          </select>
        </label>

        <label>
          ¿Cuál es el principal motivo por el que usas Lumi?
          <input
            type="text"
            name="motivoDeUso"
            placeholder="Ej. hablar con alguien, procesar emociones, etc."
            onChange={handleChange}
            required
          />
        </label>

        <button type="submit">Guardar preferencias</button>
      </form>
    </div>
  );
}

export default Preferences;
