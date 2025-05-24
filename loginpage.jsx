import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { axiosInstance } from "../../api/axiosInstance";
import { useAuth } from "../../context/AuthContext"; // Import AuthContext

const LoginSignUp = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [UserName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const { login } = useAuth(); // Get login function from AuthContext

  const handleToggle = () => {
    setIsLogin(!isLogin);
    setEmail("");
    setUserName("");
    setPassword("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isLogin && !email.endsWith("@curemd.com")) {
      alert("Email must end with @curemd.com");
      return;
    }

    try {
      const endpoint = isLogin ? "/check-user" : "/sign-up";
      const response = await axiosInstance.post(endpoint, {
        UserName,
        email,
        password,
      });

      console.log("RESPONSE DATA: ", response.data.user_collection);

      if (isLogin) {
        if (response.data.exists) {
          // Update authentication state
          login({
            dbname: response.data.user_collection,
            username: UserName, // or response.data.username if your API returns it
          });          
          navigate("/nctid-input", {
            state: {
              dbname: response.data.user_collection,
            },
          });
        } else {
          alert("User does not exist. Please sign up.");
        }
      } else {
        login({
          dbname: response.data.user_collection,
          username: UserName, // or response.data.username if your API returns it
        }); 
        navigate("/nctid-input", {
          state: {
            dbname: response.data.user_collection_name,
          },
        });
      }
    } catch (err) {
      const errorMessage = err?.response?.data?.detail || "Something went wrong.";
      alert(errorMessage);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-center text-indigo-700 mb-6">
          {isLogin ? "Login" : "Sign Up"}
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="User Name"
            value={UserName}
            onChange={(e) => setUserName(e.target.value)}
            required
          />

          {!isLogin && (
            <input
              type="email"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="Email (must end with @curemd.com)"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          )}

          <input
            type="password"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button
            type="submit"
            className="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition duration-200"
          >
            {isLogin ? "Login" : "Sign Up"}
          </button>
        </form>

        <p
          onClick={handleToggle}
          className="mt-4 text-center text-indigo-600 cursor-pointer hover:underline"
        >
          {isLogin ? "Don't have an account? Sign Up" : "Already have an account? Login"}
        </p>
      </div>
    </div>
  );
};

export default LoginSignUp;
