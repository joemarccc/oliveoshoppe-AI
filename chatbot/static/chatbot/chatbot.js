document.addEventListener('DOMContentLoaded', function() {
    const widget = document.querySelector('.chatbot-widget');
    const button = document.querySelector('.chatbot-button');
    const window = document.querySelector('.chatbot-window');
    const messages = document.querySelector('.chatbot-messages');
    const input = document.querySelector('.chatbot-input input');
    const sendButton = document.querySelector('.chatbot-input button');

    // Toggle chatbot window
    button.addEventListener('click', () => {
        const isVisible = window.style.display === 'flex';
        window.style.display = isVisible ? 'none' : 'flex';
        if (!isVisible) {
            input.focus();
        }
    });

    // Send message function
    function sendMessage() {
        const message = input.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage(message, 'user');
        input.value = '';

        // Send to backend
        fetch('/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            addMessage(data.response, 'bot');
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Sorry, I encountered an error. Please try again later.', 'bot');
        });
    }

    // Add message to chat window
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        messageDiv.textContent = text;
        messages.appendChild(messageDiv);
        messages.scrollTop = messages.scrollHeight;
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});