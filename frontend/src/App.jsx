import { Navigate, Route, Routes, Link, useNavigate } from "react-router-dom";
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

  return (
    <nav>
      <Link to="/products">Products</Link>
      {isAuthenticated && <Link to="/orders">My Orders</Link>}
      {isAuthenticated ? (
        <button onClick={handleLogout}>Log out</button>
      ) : (
        <>
          <Link to="/login">Log in</Link>
          <Link to="/register">Register</Link>
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
