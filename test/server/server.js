// radhe radhe
const express = require("express");
const http = require("http");
const { Server } = require("socket.io");

const app = express();
const server = http.createServer(app);
const io = new Server(server);

// EJS setup
app.set("view engine", "ejs");

// Route
app.get("/", (req, res) => {
  res.render("index");
});

// WebSocket logic
io.on("connection", (socket) => {
  console.log("Client connected:", socket.id);

  // listen for custom event
  socket.on("socket_test_event", (data) => {
    console.log("Received from client:", data);

    // reply back to client
    socket.emit("socket_test_event", {
      message: "Hello from server 👋",
      received: data
    });
  });

  socket.on("disconnect", () => {
    console.log("Client disconnected:", socket.id);
  });
});

// Start server
server.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
});

