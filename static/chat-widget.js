// Floating Chat Widget JavaScript
function initChatWidget() {
    // Create chat widget HTML
    const chatWidgetHTML = `
        <button class="chat-widget-button" onclick="openChatWidget()">💬</button>
        
        <div id="chatWidgetModal" class="chat-widget-modal" style="display: none;">
            <div class="chat-widget-header">
                <h3>💬 Fitness Assistant</h3>
                <button class="chat-widget-close" onclick="closeChatWidget()">✕</button>
            </div>
            <div class="chat-widget-messages" id="chatWidgetMessages"></div>
            <div class="chat-widget-input-area">
                <div class="chat-widget-input-group">
                    <input type="text" id="chatWidgetInput" placeholder="Ask me anything..." onkeypress="if(event.key==='Enter') sendChatMessage()">
                    <button onclick="sendChatMessage()">Send</button>
                </div>
            </div>
        </div>
    `;

    // Append to body
    const div = document.createElement('div');
    div.innerHTML = chatWidgetHTML;
    document.body.appendChild(div);

    // Initialize chat history
    window.chatWidgetHistory = [];
    initializeChatWidget();
}

function openChatWidget() {
    const modal = document.getElementById('chatWidgetModal');
    modal.style.display = 'flex';
}

function closeChatWidget() {
    const modal = document.getElementById('chatWidgetModal');
    modal.style.display = 'none';
}

function addChatWidgetMessage(sender, message) {
    const messagesContainer = document.getElementById('chatWidgetMessages');
    const messageEl = document.createElement('div');
    messageEl.className = 'chat-widget-message ' + sender;
    messageEl.textContent = message;
    messagesContainer.appendChild(messageEl);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    window.chatWidgetHistory.push({ role: sender === 'user' ? 'user' : 'assistant', content: message });
}

function initializeChatWidget() {
    const messagesContainer = document.getElementById('chatWidgetMessages');
    messagesContainer.innerHTML = '';
    window.chatWidgetHistory = [];
    addChatWidgetMessage('bot', '👋 Hi! I\'m your fitness assistant. Ask me about workouts, nutrition, fitness tips, or anything health-related!');
}

async function sendChatMessage() {
    const input = document.getElementById('chatWidgetInput');
    const message = input.value.trim();

    if (!message) return;

    addChatWidgetMessage('user', message);
    input.value = '';

    // Show typing indicator
    const messagesContainer = document.getElementById('chatWidgetMessages');
    const typingEl = document.createElement('div');
    typingEl.className = 'chat-widget-typing';
    typingEl.innerHTML = '<span></span><span></span><span></span>';
    typingEl.id = 'typingIndicator';
    messagesContainer.appendChild(typingEl);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    try {
        const response = await fetch('/chat-with-bot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                chat_history: window.chatWidgetHistory
            })
        });

        const data = await response.json();

        // Remove typing indicator
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) typingIndicator.remove();

        addChatWidgetMessage('bot', data.reply);
    } catch (error) {
        // Remove typing indicator
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) typingIndicator.remove();

        addChatWidgetMessage('bot', '❌ Sorry, I couldn\'t process that. Please try again.');
        console.error('Error:', error);
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initChatWidget);
} else {
    initChatWidget();
}
