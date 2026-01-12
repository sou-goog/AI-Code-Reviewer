import { useState } from "react";
import { motion } from "framer-motion";
import Navbar from "@/components/Navbar";
import ReviewForm from "@/components/ReviewForm";
import ReviewResult from "@/components/ReviewResult";
import { Sparkles, Zap, Shield, Code2 } from "lucide-react";

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

const API_URL = "https://ai-code-reviewer-ea6x.onrender.com";

export default function Home() {
    const [loading, setLoading] = useState(false);
    const [review, setReview] = useState<typeof mockReview | null>(null);

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
            // Fallback to mock data if API fails
            setReview(mockReview);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-background bg-grid relative">
            <div className="absolute inset-0 bg-gradient-radial pointer-events-none" />
            <Navbar />

            <main className="relative pt-28 pb-20 px-6">
                <div className="max-w-6xl mx-auto">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-center mb-12"
                    >
                        <h1 className="font-display text-5xl md:text-6xl font-bold mb-4">
                            <span className="text-gradient">AI-Powered</span>
                            <br />
                            Code Review
                        </h1>
                        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                            Get instant, intelligent feedback on your code changes.
                            Catch bugs, security issues, and improve code quality before you merge.
                        </p>
                    </motion.div>

                    <div className="grid md:grid-cols-3 gap-4 mb-12">
                        {[
                            { icon: Zap, title: "Instant Analysis", desc: "Get feedback in seconds" },
                            { icon: Shield, title: "Security Focus", desc: "Catch vulnerabilities early" },
                            { icon: Code2, title: "Multi-Language", desc: "Python, JS, Go & more" },
                        ].map((feature, i) => (
                            <motion.div
                                key={feature.title}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.2 + i * 0.1 }}
                                className="glass rounded-xl p-5 flex items-center gap-4"
                            >
                                <div className="p-3 rounded-lg bg-primary/20">
                                    <feature.icon className="w-5 h-5 text-primary" />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-foreground">{feature.title}</h3>
                                    <p className="text-sm text-muted-foreground">{feature.desc}</p>
                                </div>
                            </motion.div>
                        ))}
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
        </div>
    );
}
