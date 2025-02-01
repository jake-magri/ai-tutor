// src/components/OpenAIForm.tsx

import React, { useState } from 'react';
import { askTutor } from '../utils/API.ts';

const OpenAIForm: React.FC = () => {
    const [prompt, setPrompt] = useState('');
    const [response, setResponse] = useState<string | null>(null);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        try {
            const res = await askTutor(prompt);
            const data = await res.json();
            setResponse(data.answer); // Assuming the API returns an object with an `answer` field
        } catch (error) {
            console.error("Error fetching response:", error);
            setResponse("An error occurred while fetching the response.");
        }
    };

    return (
        <div>
            {response && (
                <div>
                    <h3>Response:</h3>
                    <p>{response}</p>
                </div>
            )}
            <form onSubmit={handleSubmit}>
                <label>
                    Ask OpenAI:
                    <input
                        type="text"
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                    />
                </label>
                <button type="submit">Submit</button>
            </form>
        </div>
    );
};

export default OpenAIForm;