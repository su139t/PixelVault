import { useState } from "react";

import api from "./services/api";
import { createUser as createUserRequest } from "./services/userService";

function App() {
  const [message, setMessage] = useState("");

  const testBackend = async () => {
    try {
      const response = await api.get("/health");

      setMessage(response.data.status);
    } catch (error) {
      console.error(error);
      setMessage("Backend connection failed");
    }
  };

  const handleCreateUser = async () => {
    try {
      const response = await createUserRequest({
        telegram_user_id: 1234567589,
        name: "Sumit",
        username: "sumit",
        email: "sumit@example.com",
      });

      console.log(response.data);

      setMessage(response.data.message);
    } catch (error) {
      console.error(error);
      setMessage("User creation failed");
    }
  };

  return (
    <div>
      <h1>PixelVault</h1>

      <button onClick={testBackend}>Test Backend</button>

      <button onClick={handleCreateUser}>Create Test User</button>

      <p>{message}</p>
    </div>
  );
}

export default App;
