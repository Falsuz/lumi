import { useState } from "react";
import { auth } from '../firebaseConfig';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword } from "firebase/auth";

function AuthForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isRegistering, setIsRegistering] = useState(false); // Estado para alternar entre login y registro

  const handleAuth = async (e) => {
    e.preventDefault();
    try {
      let userCredential;

      if (isRegistering) {
        userCredential = await createUserWithEmailAndPassword(auth, email, password);
      } else {
        userCredential = await signInWithEmailAndPassword(auth, email, password);
      }

      const token = await userCredential.user.getIdToken();

      // Enviar token al backend
      const response = await fetch("http://localhost:5000/protected", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();
      console.log(`${isRegistering ? "Registro" : "Login"} exitoso, respuesta del backend:`, data);
    } catch (error) {
      console.error(`Error al ${isRegistering ? "registrar" : "iniciar sesión"}:`, error.message);
    }
  };

  return (
    <div>
      <h2>{isRegistering ? "Registrarse" : "Iniciar sesión"}</h2>
      <form onSubmit={handleAuth}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Correo"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Contraseña"
        />
        <button type="submit">{isRegistering ? "Registrarse" : "Iniciar sesión"}</button>
      </form>
      <button onClick={() => setIsRegistering(!isRegistering)}>
        {isRegistering ? "¿Ya tienes cuenta? Inicia sesión" : "¿No tienes cuenta? Regístrate"}
      </button>
    </div>
  );
}

export default AuthForm;
