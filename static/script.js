let mediaRecorder;
let audioChunks = [];
let isListening = false;

async function toggleVoiceInput() {
    const btn = document.getElementById("voice-btn");

    if (!btn) {
        return;
    }

    if (!isListening) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            isListening = true;
            btn.classList.add("listening");
            btn.textContent = "Listening...";

            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
                await processAudio(audioBlob);
                stream.getTracks().forEach((track) => track.stop());
            };

            mediaRecorder.start();
        } catch (error) {
            alert("Please allow microphone access.");
        }
    } else {
        isListening = false;
        btn.classList.remove("listening");
        btn.textContent = "Mic";
        mediaRecorder.stop();
    }
}

async function processAudio(audioBlob) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.lang = "en-US";

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        const input = document.getElementById("user-input");
        if (input) {
            input.value = transcript;
            sendMessage();
        }
    };
}

function formatResponse(text) {
    const sections = {
        breakfast: "Breakfast",
        lunch: "Lunch",
        dinner: "Dinner",
        snacks: "Snacks",
        tips: "Tips",
        workout: "Workout",
        exercise: "Exercise",
        "warm-up": "Warm-up",
        "cool-down": "Cool-down",
        hydration: "Hydration",
        calories: "Calories",
        protein: "Protein",
        carbs: "Carbs",
        fat: "Fat",
        notes: "Notes"
    };

    let result = '<div class="formatted-response">';
    const lines = String(text || "").split("\n").filter((line) => line.trim() !== "");
    let inSection = false;

    for (const line of lines) {
        const trimmed = line.trim();
        let foundSection = false;

        for (const [key, title] of Object.entries(sections)) {
            if (trimmed.toLowerCase().includes(key)) {
                if (inSection) {
                    result += "</div>";
                }
                result += `<div class="response-section"><h3 class="section-header">${title}</h3>`;
                inSection = true;
                foundSection = true;
                break;
            }
        }

        if (!foundSection && trimmed) {
            if (trimmed.startsWith("• ") || trimmed.match(/^\d+\./)) {
                result += `<div class="list-item">- ${trimmed.replace(/^[•\d+.]+\s*/, "")}</div>`;
            } else if (trimmed.startsWith("-")) {
                result += `<div class="list-item">- ${trimmed.substring(1).trim()}</div>`;
            } else if (!inSection) {
                result += `<div class="response-text">${trimmed}</div>`;
            } else {
                result += `<div class="list-item">- ${trimmed}</div>`;
            }
        }
    }

    if (inSection) {
        result += "</div>";
    }
    result += "</div>";
    return result;
}

function appendBotMessage(html) {
    const chatBox = document.getElementById("chat-box");
    if (!chatBox) {
        return;
    }
    chatBox.innerHTML += `<div class="bot">${html}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    if (!input || !chatBox) {
        return;
    }

    const message = input.value.trim();
    if (!message) {
        return;
    }

    const age = document.getElementById("age")?.value;
    const goal = document.getElementById("goal")?.value;

    chatBox.innerHTML += `<div class="user">${message}</div>`;
    input.value = "";
    appendBotMessage('<span class="typing-indicator">...</span> Generating response...');

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message, age, goal })
        });

        const data = await res.json();
        const bots = document.querySelectorAll(".bot");
        bots[bots.length - 1]?.remove();
        appendBotMessage(formatResponse(data.response));
    } catch (error) {
        const bots = document.querySelectorAll(".bot");
        bots[bots.length - 1]?.remove();
        appendBotMessage("Error - Please try again.");
        console.error(error);
    }
}

async function generateTips() {
    const chatBox = document.getElementById("chat-box");
    const goal = document.getElementById("goal")?.value;
    if (!chatBox) {
        return;
    }

    appendBotMessage('<span class="typing-indicator">...</span> Getting expert tips...');

    try {
        const res = await fetch("/goal-based-response", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                goal,
                question: `Give me 5 expert tips for ${goal}`
            })
        });

        const data = await res.json();
        const bots = document.querySelectorAll(".bot");
        bots[bots.length - 1]?.remove();
        appendBotMessage(formatResponse(data.response));
    } catch (error) {
        const bots = document.querySelectorAll(".bot");
        bots[bots.length - 1]?.remove();
        appendBotMessage("Error generating tips.");
    }
}

function showWorkoutModal() {
    document.getElementById("workout-modal")?.classList.add("show");
}

function closeWorkoutModal() {
    document.getElementById("workout-modal")?.classList.remove("show");
}

async function generateWorkout() {
    const duration = document.getElementById("workout-duration")?.value;
    const equipment = document.getElementById("workout-equipment")?.value;
    const experience = document.getElementById("workout-experience")?.value;
    const goal = document.getElementById("goal")?.value;

    closeWorkoutModal();
    appendBotMessage('<span class="typing-indicator">...</span> Creating your workout...');

    try {
        const res = await fetch("/generate-workout", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                goal,
                fitness_goal: goal,
                duration,
                equipment,
                experience,
                intensity: experience
            })
        });

        const data = await res.json();
        const bots = document.querySelectorAll(".bot");
        bots[bots.length - 1]?.remove();
        appendBotMessage(formatResponse(data.workout || data.error || "Workout generated."));
    } catch (error) {
        const bots = document.querySelectorAll(".bot");
        bots[bots.length - 1]?.remove();
        appendBotMessage("Error generating workout.");
    }
}

function showMealPlanModal() {
    document.getElementById("meal-modal")?.classList.add("show");
}

function closeMealPlanModal() {
    document.getElementById("meal-modal")?.classList.remove("show");
}

async function generateMealPlan() {
    const goal = document.getElementById("goal")?.value;
    const calories = document.getElementById("meal-calories")?.value;
    const dietary_preference = document.getElementById("meal-preference")?.value;
    const days = document.getElementById("meal-days")?.value;

    closeMealPlanModal();
    appendBotMessage('<span class="typing-indicator">...</span> Creating your meal plan...');

    try {
        const res = await fetch("/generate-meal-plan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ goal, calories, dietary_preference, days })
        });

        const data = await res.json();
        const bots = document.querySelectorAll(".bot");
        bots[bots.length - 1]?.remove();
        appendBotMessage(formatResponse(data.meal_plan || data.error || "Meal plan generated."));
    } catch (error) {
        const bots = document.querySelectorAll(".bot");
        bots[bots.length - 1]?.remove();
        appendBotMessage("Error generating meal plan.");
    }
}

async function loadChatHistory() {
    const chatBox = document.getElementById("chat-box");
    if (!chatBox) {
        return;
    }

    try {
        const res = await fetch("/get-chat-history");
        const data = await res.json();

        appendBotMessage("Loading your conversation history...");

        if (data.history && data.history.length > 0) {
            data.history.forEach((chat) => {
                const date = new Date(chat.timestamp).toLocaleString();
                appendBotMessage(`<strong>${date}</strong><br>${chat.user}<br><small>${chat.assistant.substring(0, 100)}...</small>`);
            });
        } else {
            appendBotMessage("No conversation history found. Start chatting.");
        }
    } catch (error) {
        appendBotMessage("Error loading history.");
    }
}

async function clearChatHistory() {
    if (confirm("Are you sure you want to clear all chat history?")) {
        try {
            await fetch("/clear-chat-history", { method: "POST" });
            alert("Chat history cleared.");
        } catch (error) {
            alert("Error clearing history.");
        }
    }
}

function goToCalculator() {
    window.location.href = "/calculator";
}

function goToTimer() {
    window.location.href = "/workout-timer";
}

function goToPersonality() {
    window.location.href = "/personality-mode";
}

function goToMoodWorkout() {
    window.location.href = "/mood-workout";
}

function goToAchievements() {
    window.location.href = "/achievements";
}

document.addEventListener("keypress", (event) => {
    if (event.key === "Enter" && document.getElementById("user-input")) {
        sendMessage();
    }
});

async function askTips() {
    const age = document.getElementById("age")?.value;
    const goal = document.getElementById("goal")?.value;

    appendBotMessage('<span class="typing-indicator">...</span> Getting fitness tips...');

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: "Give me expert fitness tips and advice for achieving my goals",
                age,
                goal
            })
        });

        const data = await res.json();
        const bots = document.querySelectorAll(".bot");
        bots[bots.length - 1]?.remove();
        appendBotMessage(formatResponse(data.response));
    } catch (error) {
        const bots = document.querySelectorAll(".bot");
        bots[bots.length - 1]?.remove();
        appendBotMessage("Error getting tips.");
        console.error(error);
    }
}
