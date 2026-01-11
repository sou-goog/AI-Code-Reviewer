'use client';

import { useState } from 'react';

interface ReviewFormProps {
    onSubmit: (code: string, language: string) => Promise<void>;
    isLoading: boolean;
}

const SAMPLE_CODE = `def process_user_data(user_input):
    # Potential SQL injection vulnerability
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    
    # Missing error handling
    result = database.execute(query)
    
    # Hardcoded credentials
    api_key = "sk-1234567890abcdef"
    
    return result`;

export default function ReviewForm({ onSubmit, isLoading }: ReviewFormProps) {
    const [code, setCode] = useState('');
    const [language, setLanguage] = useState('python');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit(code, language);
    };

    const loadSample = () => {
        setCode(SAMPLE_CODE);
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            {/* Language Selection */}
            <div>
                <label className="block text-sm font-semibold uppercase tracking-wide text-grey-secondary mb-3">
                    Language
                </label>
                <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-purple-accent"
                >
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                    <option value="typescript">TypeScript</option>
                    <option value="java">Java</option>
                    <option value="go">Go</option>
                    <option value="rust">Rust</option>
                </select>
            </div>

            {/* Code Input */}
            <div>
                <div className="flex items-center justify-between mb-3">
                    <label className="block text-sm font-semibold uppercase tracking-wide text-grey-secondary">
                        Code / Git Diff
                    </label>
                    <button
                        type="button"
                        onClick={loadSample}
                        className="text-sm text-purple-accent hover:text-blue-accent transition-colors"
                    >
                        Load Sample
                    </button>
                </div>
                <textarea
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    placeholder="Paste your code or git diff here..."
                    className="w-full h-80 bg-white/5 border border-white/10 rounded-lg px-4 py-3 font-mono text-sm text-white placeholder-grey-secondary/50 focus:outline-none focus:ring-2 focus:ring-purple-accent resize-none"
                    required
                />
            </div>

            {/* Submit Button */}
            <button
                type="submit"
                disabled={isLoading}
                className="w-full gradient-button py-4 px-6 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
                {isLoading ? (
                    <div className="flex items-center justify-center gap-3">
                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        <span>Analyzing code...</span>
                    </div>
                ) : (
                    'Review Code'
                )}
            </button>
        </form>
    );
}
