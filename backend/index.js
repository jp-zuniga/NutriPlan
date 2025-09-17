import { GoogleGenAI } from "@google/genai";
import cors from "cors"
import express from "express"

const app = express();
const port = 3000;

let conversations = {};

// API_KEY Environment Variable must be set
const API_KEY = process.env.API_KEY;

// Currently using a GEMINI Api key so let's go for that
// You can get yours for free at https://aistudio.google.com/apikey

// The client gets the API key from the environment variable `GEMINI_API_KEY`.
const ai = new GoogleGenAI({apiKey: API_KEY});

async function callAI(message, user_id) {
  console.log(`Request to speak to AI with message: ${message}`)

  if(!conversations[user_id]) {
    console.log(`Opening conversation with user ${user_id}`)
    conversations[user_id] = [];
  }
  else {
    console.log(`Conversation length with the user ${user_id}: ${conversations[user_id].length}`)
  }

  conversations[user_id].push({
    role: 'user',
    message: message
  })

  console.log(`Contents sent to gemini: ${JSON.stringify(conversations[user_id])}`)

  const response = await ai.models.generateContent({
    model: "gemini-2.5-pro",
    contents: JSON.stringify(conversations[user_id]),
  });

  conversations[user_id].push({
    role: 'ai',
    message: response.text
  })

  return response.text;
}

app.use(express.json());
app.use(cors());

app.post('/ai-endpoint', async (req, res) => {
    console.log(`Incoming request!`);

    const { user_id, message } = req.body; // Get message

    if(!message || message == "") {
        res.json({
            error: "The messsage field is null",
            answer: null
        })
        return;
    }

    const answer = await callAI(message, user_id);
    console.log(`Server answered with: ${answer}`);
    res.json({
        error: null,
        answer: answer
    });
});

app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});