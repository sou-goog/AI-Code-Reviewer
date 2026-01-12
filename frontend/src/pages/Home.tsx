import { useState } from "react";
import { motion } from "framer-motion";
import Navbar from "@/components/Navbar";
import ReviewForm from "@/components/ReviewForm";
import ReviewResult from "@/components/ReviewResult";
import { Sparkles, Zap, Shield, Code2, Github } from "lucide-react";

const API_URL = "https://ai-code-reviewer-ea6x.onrender.com";

const mockReview = {
    critical: [
        "Security vulnerability: The `validate_token` function catches all exceptions with a bare `except:` clause, which can hide critical errors and make debugging difficult. Use specific exception types like `jwt.ExpiredSignatureError` and `jwt.InvalidTokenError`.",
        "The JWT decode is missing the `algorithms` parameter, which is required in PyJWT 2.0+. Add `algorithms=['HS256']` to prevent algorithm confusion attacks.",
    ],
    warnings: [
        "The `logger.warning` call uses an f-string which could log sensitive information. Consider sanitizing the username or using structured logging.",
        "Missing rate limiting on authentication attempts could allow brute force attacks.",
    ],
    suggestions: [
        "Consider adding a `max_age` parameter to the token validation to handle token expiration.",
        "The password checking logic could be moved to a separate `verify_credentials` method for better separation of concerns.",
        "Add type hints to function parameters and return types for better code documentation.",
    ],
    positive: [
        "Good improvement switching from plain password comparison to `check_password_hash` - this is a crucial security fix.",
        "Adding logging for failed login attempts is excellent for security monitoring and audit trails.",
        "Clean function naming conventions that clearly describe the purpose.",
    ],
    summary: "This diff shows security improvements to the authentication flow. The switch to hashed password comparison and addition of logging are positive changes. However, there are critical security issues in the token validation that should be addressed before merging.",
};

export default function Home() {
    const [loading, setLoading] = useState(false);
    const [review, setReview] = useState<typeof mockReview | null>(null);
    const [showReviewer, setShowReviewer] = useState(false);

    const handleSubmit = async (code: string, language: string) => {
        setLoading(true);
        setReview(null);

        try {
            const response = await fetch(`${API_URL}/api/review`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    code_diff: code,
                    language
                })
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            const data = await response.json();
            setReview(data);
        } catch (error: any) {
            console.error('Review failed:', error);
            setReview(mockReview);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-background relative overflow-hidden">
            <div className="absolute inset-0 bg-grid pointer-events-none" />
            <div className="absolute inset-0 bg-gradient-radial pointer-events-none" />

            <Navbar />

            {!showReviewer ? (
                <main className="relative pt-32 pb-20 px-6">
                    <div className="max-w-5xl mx-auto">
                        {/* Hero Section */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="text-center mb-16"
                        >
                            <h1 className="font-display text-5xl md:text-6xl font-bold mb-6 leading-tight">
                                <span className="text-gradient">AI Code Reviewer</span>
                            </h1>

                            <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-8">
                                Get AI-powered code reviews using Google Gemini. Catches bugs, security issues, and suggests improvements.
                            </p>

                            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-6">
                                <button
                                    onClick={() => setShowReviewer(true)}
                                    className="px-8 py-4 bg-primary text-white font-semibold rounded-2xl transition-all hover:opacity-90 flex items-center gap-2 justify-center"
                                >
                                    <Sparkles className="w-5 h-5" />
                                    Try It Now
                                </button>
                                <a
                                    href="https://github.com/sou-goog/AI-Code-Reviewer"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="px-8 py-4 bg-white/10 text-foreground font-semibold rounded-2xl transition-all hover:bg-white/20 flex items-center gap-2 justify-center border border-border"
                                >
                                    <Github className="w-5 h-5" />
                                    View on GitHub
                                </a>
                            </div>
                        </motion.div>

                        {/* Features */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.2 }}
                            className="grid md:grid-cols-3 gap-6 mb-16"
                        >
                            {[
                                { icon: Zap, title: "Instant Analysis", desc: "Get feedback in seconds" },
                                { icon: Shield, title: "Security Focus", desc: "Catch vulnerabilities early" },
                                { icon: Code2, title: "Multi-Language", desc: "Python, JS, Go & more" },
                            ].map((feature, i) => (
                                <div
                                    key={feature.title}
                                    className="glass rounded-xl p-6 text-center"
                                >
                                    <div className="p-3 rounded-lg bg-primary/20 w-fit mx-auto mb-4">
                                        <feature.icon className="w-6 h-6 text-primary" />
                                    </div>
                                    <h3 className="font-semibold text-lg mb-2">{feature.title}</h3>
                                    <p className="text-sm text-muted-foreground">{feature.desc}</p>
                                </div>
                            ))}
                        </motion.div>

                        {/* How it Works */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.3 }}
                            className="glass rounded-2xl p-8 mb-16"
                        >
                            <h2 className="text-3xl font-bold mb-6 text-center">How It Works</h2>
                            <div className="space-y-4 max-w-2xl mx-auto">
                                <div className="flex items-start gap-4">
                                    <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 mt-1">
                                        <span className="text-primary font-bold">1</span>
                                    </div>
                                    <div>
                                        <h3 className="font-semibold mb-1">Paste Your Code</h3>
                                        <p className="text-muted-foreground">Submit code snippets or diffs for review</p>
                                    </div>
                                </div>
                                <div className="flex items-start gap-4">
                                    <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 mt-1">
                                        <span className="text-primary font-bold">2</span>
                                    </div>
                                    <div>
                                        <h3 className="font-semibold mb-1">AI Analysis</h3>
                                        <p className="text-muted-foreground">Google Gemini reviews your code for issues</p>
                                    </div>
                                </div>
                                <div className="flex items-start gap-4">
                                    <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 mt-1">
                                        <span className="text-primary font-bold">3</span>
                                    </div>
                                    <div>
                                        <h3 className="font-semibold mb-1">Get Feedback</h3>
                                        <p className="text-muted-foreground">Receive categorized suggestions and improvements</p>
                                    </div>
                                </div>
                            </div>
                        </motion.div>

                        {/* Final CTA */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.4 }}
                            className="text-center"
                        >
                            <button
                                onClick={() => setShowReviewer(true)}
                                className="px-10 py-5 bg-primary text-white font-semibold rounded-2xl transition-all hover:opacity-90 hover:scale-105 inline-flex items-center gap-3 text-lg"
                            >
                                <Sparkles className="w-6 h-6" />
                                Get Started
                            </button>
                            <p className="text-sm text-muted-foreground mt-4">Free to use • No signup required</p>
                        </motion.div>
                    </div>
                </main>
            ) : (
                <main className="relative pt-28 pb-20 px-6">
                    <div className="max-w-6xl mx-auto">
                        <div className="mb-8 flex items-center justify-between">
                            <h1 className="font-display text-4xl font-bold">
                                <span className="text-gradient">AI Code Reviewer</span>
                            </h1>
                            <button
                                onClick={() => setShowReviewer(false)}
                                className="text-muted-foreground hover:text-foreground transition-colors"
                            >
                                ← Back
                            </button>
                        </div>

                        <div className="grid lg:grid-cols-2 gap-8">
                            <div className="space-y-4">
                                <h2 className="font-display text-2xl font-semibold text-foreground flex items-center gap-2">
                                    <Sparkles className="w-5 h-5 text-primary -scale-x-100" />
                                    Submit Code for Review
                                </h2>
                                <ReviewForm onSubmit={handleSubmit} loading={loading} />
                            </div>

                            <div className="space-y-4">
                                <h2 className="font-display text-2xl font-semibold text-foreground">
                                    Review Results
                                </h2>
                                {loading ? (
                                    <motion.div
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        className="glass rounded-xl p-12 flex flex-col items-center justify-center"
                                    >
                                        <motion.div
                                            animate={{ rotate: 360 }}
                                            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                                            className="w-12 h-12 border-3 border-primary/30 border-t-primary rounded-full mb-4"
                                        />
                                        <p className="text-muted-foreground">Analyzing your code...</p>
                                    </motion.div>
                                ) : review ? (
                                    <ReviewResult review={review} />
                                ) : (
                                    <motion.div
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        className="glass rounded-xl p-12 flex flex-col items-center justify-center text-center"
                                    >
                                        <div className="w-16 h-16 rounded-2xl bg-muted/50 flex items-center justify-center mb-4">
                                            <Code2 className="w-8 h-8 text-muted-foreground" />
                                        </div>
                                        <p className="text-muted-foreground">
                                            Submit code to see AI-powered review results
                                        </p>
                                    </motion.div>
                                )}
                            </div>
                        </div>
                    </div>
                </main>
            )}
        </div>
    );
}
