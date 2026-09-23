// ==========================================
// AI VISUAL TEACHER
// Frontend MVP
// ==========================================


// ------------------------------------------
// SAMPLE LEARNING DATA
// ------------------------------------------

const learningData = {

    "newton laws": {
        title: "Newton's Laws of Motion",

        explanation:
            "Newton's laws describe how objects move and how forces affect their motion.",

        simple:
            "Think of a football. If you push it, it starts moving. A stronger push produces a greater change in its motion.",

        keyPoint:
            "Force = Mass × Acceleration",

        visual:
            "⚽ → 💨",

        question:
            "Which law states that force equals mass multiplied by acceleration?",

        options: [
            "Newton's First Law",
            "Newton's Second Law",
            "Newton's Third Law",
            "Law of Gravitation"
        ],

        answer: 1
    },


    "photosynthesis": {
        title: "Photosynthesis",

        explanation:
            "Photosynthesis is the process by which green plants convert light energy into chemical energy.",

        simple:
            "Plants use sunlight, water and carbon dioxide to produce glucose and oxygen.",

        keyPoint:
            "Sunlight + CO₂ + Water → Glucose + Oxygen",

        visual:
            "☀️ + 🌱 + 💧 → 🍃 + O₂",

        question:
            "Which gas do plants take in during photosynthesis?",

        options: [
            "Oxygen",
            "Nitrogen",
            "Carbon dioxide",
            "Hydrogen"
        ],

        answer: 2
    },


    "dna": {
        title: "DNA",

        explanation:
            "DNA is the molecule that stores genetic information in living organisms.",

        simple:
            "Think of DNA as an instruction book that contains information used to build and maintain an organism.",

        keyPoint:
            "DNA carries hereditary genetic information.",

        visual:
            "🧬",

        question:
            "What does DNA primarily store?",

        options: [
            "Electrical energy",
            "Genetic information",
            "Water",
            "Oxygen"
        ],

        answer: 1
    }

};


// ------------------------------------------
// SET TOPIC
// ------------------------------------------

function setTopic(topic) {

    document.getElementById("topicInput").value = topic;

    document.getElementById("topicInput").focus();

}


// ------------------------------------------
// START LEARNING
// ------------------------------------------

function startLearning() {

    const input =
        document.getElementById("topicInput");

    const button =
        document.getElementById("learnButton");

    const topic =
        input.value.trim();

    if (!topic) {

        alert("Please enter a topic first.");

        input.focus();

        return;
    }


    button.disabled = true;

    button.innerText = "Learning...";


    // Small delay to simulate AI processing

    setTimeout(() => {

        generateLearning(topic);

        button.disabled = false;

        button.innerText = "Learn with AI →";

    }, 700);

}


// ------------------------------------------
// GENERATE LEARNING
// ------------------------------------------

function generateLearning(topic) {

    const normalizedTopic =
        topic.toLowerCase();

    let data =
        learningData[normalizedTopic];


    // If topic is not in our sample database

    if (!data) {

        data = {

            title: topic,

            explanation:
                `Let's start learning about ${topic}. This is a demo explanation from the AI Visual Teacher MVP.`,

            simple:
                `Imagine ${topic} as something you can understand step by step. The real AI backend will generate a personalized explanation here.`,

            keyPoint:
                "The AI backend will provide important points about this topic.",

            visual:
                "🧠 → 📚 → 💡",

            question:
                `Which option represents the best way to learn about ${topic}?`,

            options: [
                "Understand the basic concept",
                "Memorize everything without understanding",
                "Skip the fundamentals",
                "Do nothing"
            ],

            answer: 0

        };

    }


    displayExplanation(data);

    displayVisual(data);

    displayQuiz(data);

}


// ------------------------------------------
// DISPLAY EXPLANATION
// ------------------------------------------

function displayExplanation(data) {

    const container =
        document.getElementById("explanation");


    container.innerHTML = `

        <div class="explanation-content">

            <h3>${data.title}</h3>

            <p>
                ${data.explanation}
            </p>

            <p>
                <strong>Simple explanation:</strong>
            </p>

            <p>
                ${data.simple}
            </p>

            <div class="key-point">

                <strong>💡 Key Point</strong>

                <br>

                ${data.keyPoint}

            </div>

        </div>

    `;

}


// ------------------------------------------
// DISPLAY VISUAL
// ------------------------------------------

function displayVisual(data) {

    const container =
        document.getElementById("visualContent");


    container.innerHTML = `

        <div class="visual-placeholder">

            <div class="visual-circle">

                ${data.visual}

            </div>

            <h3>${data.title}</h3>

            <p>
                Interactive visualization will be
                connected to the AI/3D engine next.
            </p>

        </div>

    `;

}


// ------------------------------------------
// DISPLAY QUIZ
// ------------------------------------------

function displayQuiz(data) {

    const container =
        document.getElementById("quizContainer");


    let optionsHTML = "";


    data.options.forEach((option, index) => {

        optionsHTML += `

            <button
                class="option"
                onclick="checkAnswer(${index}, ${data.answer}, this)"
            >

                ${String.fromCharCode(65 + index)}.
                ${option}

            </button>

        `;

    });


    container.innerHTML = `

        <div class="question">

            ${data.question}

        </div>

        <div>

            ${optionsHTML}

        </div>

        <div id="quizResult"></div>

    `;

}


// ------------------------------------------
// CHECK ANSWER
// ------------------------------------------

function checkAnswer(
    selected,
    correct,
    button
) {

    const result =
        document.getElementById("quizResult");


    const options =
        document.querySelectorAll(".option");


    options.forEach(option => {

        option.disabled = true;

    });


    if (selected === correct) {

        button.classList.add("correct");

        result.innerHTML = `

            <div class="key-point">

                🎉 Correct!

                <br>

                Great job. You understood the concept.

            </div>

        `;

    } else {

        button.classList.add("wrong");

        options[correct].classList.add("correct");

        result.innerHTML = `

            <div class="key-point">

                ❌ Not quite.

                <br>

                The highlighted option is the correct answer.

            </div>

        `;

    }

}


// ------------------------------------------
// ENTER KEY
// ------------------------------------------

document
    .getElementById("topicInput")
    .addEventListener(
        "keydown",
        function(event) {

            if (event.key === "Enter") {

                startLearning();

            }

        }
    );
