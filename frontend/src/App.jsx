import { Navigate, Route, Routes, NavLink, useNavigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./AuthContext";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Products from "./pages/Products";
import Orders from "./pages/Orders";
import ProtectedRoute from "./components/ProtectedRoute";
import "./App.css";

function Nav() {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  const getNavStyle = ({ isActive }) => (isActive ? { fontWeight: "bold", textDecoration: "underline" } : {});

  return (
    <nav>
      <NavLink to="/products" style={getNavStyle}>Products</NavLink>
      {isAuthenticated && <NavLink to="/orders" style={getNavStyle}>My Orders</NavLink>}
      {isAuthenticated ? (
        <button onClick={handleLogout}>Log out</button>
      ) : (
        <>
          <NavLink to="/login" style={getNavStyle}>Log in</NavLink>
          <NavLink to="/register" style={getNavStyle}>Register</NavLink>
        </>
      )}
    </nav>
  );
}

function AppRoutes() {
  return (
    <>
      <Nav />
      <main>
        <Routes>
          <Route path="/" element={<Navigate to="/products" replace />} />
          <Route path="/products" element={<Products />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/orders"
            element={
              <ProtectedRoute>
                <Orders />
              </ProtectedRoute>
            }
          />
        </Routes>
      </main>
    </>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}
