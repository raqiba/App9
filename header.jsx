// src/components/Header.jsx
import React from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate,useLocation } from "react-router-dom";

const Header = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
    if (location.pathname === "/auth-page") return null;

  const handleLogout = () => {
    logout();
    navigate("/auth-page");
  };

  if (!user) return null; // Don’t show header if no user is logged in

  return (
    <div className="w-full bg-indigo-600 text-white px-4 py-2 flex justify-between items-center">
      <span className="text-lg font-semibold">{user.username}</span>
      <button
        onClick={handleLogout}
        className="bg-white text-indigo-600 px-3 py-1 rounded hover:bg-gray-100"
      >
        Logout
      </button>
    </div>
  );
};

export default Header;
