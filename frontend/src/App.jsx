import { Navigate, Route, Routes, NavLink, useNavigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./AuthContext";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Products from "./pages/Products";
import Orders from "./pages/Orders";
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

function PrivateRoute({ children }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" replace />;
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
              <PrivateRoute>
                <Orders />
              </PrivateRoute>
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
