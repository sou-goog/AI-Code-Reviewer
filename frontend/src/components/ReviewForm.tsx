import { useState } from "react";
import { Send, Code } from "lucide-react";

interface ReviewFormProps {
    onSubmit: (code: string, language: string) => void;
    loading: boolean;
}

const sampleCode = `def authenticate_user(username, password):
    # Security vulnerability: SQL injection risk
    query = f"SELECT * FROM users WHERE username = '{username}'"
    
    # Missing: Password hashing
    if user.password == password:
        return create_token(user)`;

export default function ReviewForm({ onSubmit, loading }: ReviewFormProps) {
    const [code, setCode] = useState("");
    const [language, setLanguage] = useState("python");

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!code.trim()) return;
        onSubmit(code, language);
    };

    const handleLoadSample = () => {
        setCode(sampleCode);
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <label className="text-sm font-medium text-muted-foreground">Language</label>
                    <select
                        value={language}
                        onChange={(e) => setLanguage(e.target.value)}
                        className="w-40 h-10 bg-card border border-border rounded-lg px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                    >
                        <option value="python">Python</option>
                        <option value="javascript">JavaScript</option>
                        <option value="typescript">TypeScript</option>
                        <option value="java">Java</option>
                        <option value="go">Go</option>
                        <option value="rust">Rust</option>
                    </select>
                </div>
                <button
                    type="button"
                    onClick={handleLoadSample}
                    className="h-10 px-4 text-sm text-muted-foreground hover:text-foreground flex items-center gap-2 rounded-lg hover:bg-white/5 transition-colors"
                >
                    <Code className="w-4 h-4" />
                    Load Sample
                </button>
            </div>

            <div className="relative">
                <textarea
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    placeholder="Paste your code or git diff here..."
                    className="w-full h-80 p-5 bg-card border border-border rounded-xl font-mono text-sm resize-none focus:outline-none focus:ring-2 focus:ring-primary/50 placeholder:text-muted-foreground/50"
                    required
                />
            </div>

            <div className="flex items-center justify-between">
                <p className="text-sm text-muted-foreground">
                    {code.length > 0 ? `${code.split('\n').length} lines` : "No code entered"}
                </p>
                <button
                    type="submit"
                    disabled={loading || !code.trim()}
                    className="px-8 py-3 bg-gradient-to-r from-primary to-blue-500 text-white font-semibold rounded-xl glow-primary transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                    {loading ? (
                        <>
                            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                            Analyzing...
                        </>
                    ) : (
                        <>
                            <Send className="w-5 h-5" />
                            Review Code
                        </>
                    )}
                </button>
            </div>
        </form>
    );
}
