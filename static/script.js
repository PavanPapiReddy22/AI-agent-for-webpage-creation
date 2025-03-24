document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    function sendMessage() {
        const userMessage = userInput.value.trim();
        if (!userMessage) return;

        // Display user message
        chatBox.innerHTML += `<div class="message user-message"><strong>You:</strong> ${userMessage}</div>`;
        userInput.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;

        // Show loading indicator
        chatBox.innerHTML += `<div id="loading" class="message ai-message">Typing...</div>`;
        
        // Send message to backend
        fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("loading").remove(); // Remove loading text
            chatBox.innerHTML += `<div class="message ai-message"><strong>AI:</strong> ${data.response}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll
        })
        .catch(error => console.error("Error:", error));
    }

    // Send message on button click
    sendBtn.addEventListener("click", sendMessage);

    // Send message when Enter is pressed
    userInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault(); // Prevent new lines
            sendMessage();
        }
    });
});
