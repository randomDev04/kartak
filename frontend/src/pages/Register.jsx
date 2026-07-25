import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { api } from "../api";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      await api.register(email, password);
      navigate("/login");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Register</h2>
      {error && <p className="error">{error}</p>}
      <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button type="submit">Create account</button>
      <p>
        Already have an account? <Link to="/login">Log in</Link>
      </p>
    </form>
  );
}
