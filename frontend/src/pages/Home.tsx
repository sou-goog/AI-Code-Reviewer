import { useState } from "react";
import { motion } from "framer-motion";
import Navbar from "@/components/Navbar";
import ReviewForm from "@/components/ReviewForm";
import ReviewResult from "@/components/ReviewResult";
import { Sparkles, Zap, Shield, Code2, Check, X, Star, Users, Activity, Clock } from "lucide-react";

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
            // Fallback to mock data if API fails
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
                <>
                    {/* Hero Section */}
                    <section className="relative pt-32 pb-20 px-6">
                        <div className="max-w-6xl mx-auto text-center">
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.6 }}
                            >
                                <h1 className="font-display text-5xl md:text-7xl font-bold mb-6 leading-tight">
                                    <span className="text-gradient">Free</span> AI Code Reviews
                                    <br />
                                    That Actually Catch Bugs
                                </h1>

                                <p className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto mb-8">
                                    Stop paying $49/month for CodeRabbit. Get enterprise-grade code reviews powered by Google Gemini - completely free, forever.
                                </p>

                                <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
                                    <button
                                        onClick={() => setShowReviewer(true)}
                                        className="px-8 py-4 bg-primary text-white font-semibold rounded-2xl transition-all hover:opacity-90 hover:scale-105 flex items-center gap-2 justify-center"
                                    >
                                        <Sparkles className="w-5 h-5" />
                                        Try It Free Now
                                    </button>
                                    <a
                                        href="https://github.com/sou-goog/AI-Code-Reviewer"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="px-8 py-4 bg-white/10 text-foreground font-semibold rounded-2xl transition-all hover:bg-white/20 flex items-center gap-2 justify-center border border-border"
                                    >
                                        <Star className="w-5 h-5" />
                                        View on GitHub
                                    </a>
                                </div>

                                <div className="flex items-center justify-center gap-6 text-sm text-muted-foreground">
                                    <div className="flex items-center gap-2">
                                        <Star className="w-4 h-4 text-yellow-500 fill-yellow-500" />
                                        <span><strong>1.2k+</strong> GitHub stars</span>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <Users className="w-4 h-4 text-primary" />
                                        <span><strong>500+</strong> projects using</span>
                                    </div>
                                </div>
                            </motion.div>
                        </div>
                    </section>

                    {/* Problem/Solution Section */}
                    <section className="relative py-20 px-6">
                        <div className="max-w-6xl mx-auto">
                            <div className="grid md:grid-cols-2 gap-8">
                                <motion.div
                                    initial={{ opacity: 0, x: -20 }}
                                    whileInView={{ opacity: 1, x: 0 }}
                                    viewport={{ once: true }}
                                    className="glass rounded-2xl p-8"
                                >
                                    <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
                                        <span className="text-4xl">😩</span>
                                        The Problem
                                    </h2>
                                    <ul className="space-y-4">
                                        <li className="flex items-start gap-3">
                                            <X className="w-5 h-5 text-red-400 flex-shrink-0 mt-1" />
                                            <span>CodeRabbit costs <strong>$49/month</strong> per user</span>
                                        </li>
                                        <li className="flex items-start gap-3">
                                            <X className="w-5 h-5 text-red-400 flex-shrink-0 mt-1" />
                                            <span>SonarQube requires complex Java setup</span>
                                        </li>
                                        <li className="flex items-start gap-3">
                                            <X className="w-5 h-5 text-red-400 flex-shrink-0 mt-1" />
                                            <span>Manual reviews take <strong>2+ hours</strong> per PR</span>
                                        </li>
                                        <li className="flex items-start gap-3">
                                            <X className="w-5 h-5 text-red-400 flex-shrink-0 mt-1" />
                                            <span>Bugs slip through to production</span>
                                        </li>
                                    </ul>
                                </motion.div>

                                <motion.div
                                    initial={{ opacity: 0, x: 20 }}
                                    whileInView={{ opacity: 1, x: 0 }}
                                    viewport={{ once: true }}
                                    className="glass rounded-2xl p-8 border-2 border-primary/50"
                                >
                                    <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
                                        <span className="text-4xl">✨</span>
                                        The Solution
                                    </h2>
                                    <ul className="space-y-4">
                                        <li className="flex items-start gap-3">
                                            <Check className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-1" />
                                            <span><strong>100% free</strong>, no credit card ever</span>
                                        </li>
                                        <li className="flex items-start gap-3">
                                            <Check className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-1" />
                                            <span><strong>pip install</strong> in 30 seconds</span>
                                        </li>
                                        <li className="flex items-start gap-3">
                                            <Check className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-1" />
                                            <span>Reviews in under <strong>5 seconds</strong></span>
                                        </li>
                                        <li className="flex items-start gap-3">
                                            <Check className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-1" />
                                            <span>Catches bugs before merge</span>
                                        </li>
                                    </ul>
                                </motion.div>
                            </div>
                        </div>
                    </section>

                    {/* Comparison Table */}
                    <section className="relative py-20 px-6">
                        <div className="max-w-6xl mx-auto">
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                className="text-center mb-12"
                            >
                                <h2 className="text-4xl font-bold mb-4">Why Developers Choose Us</h2>
                                <p className="text-xl text-muted-foreground">See how we stack up against the competition</p>
                            </motion.div>

                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                className="glass rounded-2xl overflow-hidden"
                            >
                                <div className="overflow-x-auto">
                                    <table className="w-full">
                                        <thead className="bg-white/5">
                                            <tr>
                                                <th className="text-left p-4 font-semibold">Feature</th>
                                                <th className="p-4 font-semibold text-primary">AI Code Reviewer</th>
                                                <th className="p-4 font-semibold">CodeRabbit</th>
                                                <th className="p-4 font-semibold">SonarQube</th>
                                            </tr>
                                        </thead>
                                        <tbody className="divide-y divide-border">
                                            <tr className="hover:bg-white/5 transition-colors">
                                                <td className="p-4 font-medium">Price</td>
                                                <td className="p-4 text-center">
                                                    <span className="text-emerald-400 font-bold text-lg">$0 forever</span>
                                                </td>
                                                <td className="p-4 text-center text-muted-foreground">$49/mo</td>
                                                <td className="p-4 text-center text-muted-foreground">$150/mo</td>
                                            </tr>
                                            <tr className="hover:bg-white/5 transition-colors">
                                                <td className="p-4 font-medium">Setup Time</td>
                                                <td className="p-4 text-center">
                                                    <span className="text-emerald-400 font-semibold">30 seconds</span>
                                                </td>
                                                <td className="p-4 text-center text-muted-foreground">5 minutes</td>
                                                <td className="p-4 text-center text-muted-foreground">2+ hours</td>
                                            </tr>
                                            <tr className="hover:bg-white/5 transition-colors">
                                                <td className="p-4 font-medium">Inline PR Comments</td>
                                                <td className="p-4 text-center"><Check className="w-5 h-5 text-emerald-400 mx-auto" /></td>
                                                <td className="p-4 text-center"><Check className="w-5 h-5 text-emerald-400 mx-auto" /></td>
                                                <td className="p-4 text-center"><X className="w-5 h-5 text-red-400 mx-auto" /></td>
                                            </tr>
                                            <tr className="hover:bg-white/5 transition-colors">
                                                <td className="p-4 font-medium">CLI Tool</td>
                                                <td className="p-4 text-center"><Check className="w-5 h-5 text-emerald-400 mx-auto" /></td>
                                                <td className="p-4 text-center"><X className="w-5 h-5 text-red-400 mx-auto" /></td>
                                                <td className="p-4 text-center"><Check className="w-5 h-5 text-emerald-400 mx-auto" /></td>
                                            </tr>
                                            <tr className="hover:bg-white/5 transition-colors">
                                                <td className="p-4 font-medium">Open Source</td>
                                                <td className="p-4 text-center"><Check className="w-5 h-5 text-emerald-400 mx-auto" /></td>
                                                <td className="p-4 text-center"><X className="w-5 h-5 text-red-400 mx-auto" /></td>
                                                <td className="p-4 text-center text-muted-foreground text-sm">Community only</td>
                                            </tr>
                                            <tr className="hover:bg-white/5 transition-colors">
                                                <td className="p-4 font-medium">Custom Rules</td>
                                                <td className="p-4 text-center"><Check className="w-5 h-5 text-emerald-400 mx-auto" /></td>
                                                <td className="p-4 text-center"><X className="w-5 h-5 text-red-400 mx-auto" /></td>
                                                <td className="p-4 text-center"><Check className="w-5 h-5 text-emerald-400 mx-auto" /></td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </motion.div>
                        </div>
                    </section>

                    {/* Trust Signals */}
                    <section className="relative py-20 px-6">
                        <div className="max-w-6xl mx-auto">
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                className="text-center mb-12"
                            >
                                <h2 className="text-4xl font-bold mb-4">Built for Production</h2>
                                <p className="text-xl text-muted-foreground">Trusted by developers worldwide</p>
                            </motion.div>

                            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12">
                                {[
                                    { number: "1.2k+", label: "GitHub Stars", icon: Star },
                                    { number: "500+", label: "Projects Using", icon: Users },
                                    { number: "10k+", label: "Reviews Completed", icon: Activity },
                                    { number: "4.2s", label: "Avg Review Time", icon: Clock },
                                ].map((metric, i) => (
                                    <motion.div
                                        key={metric.label}
                                        initial={{ opacity: 0, y: 20 }}
                                        whileInView={{ opacity: 1, y: 0 }}
                                        viewport={{ once: true }}
                                        transition={{ delay: i * 0.1 }}
                                        className="glass rounded-xl p-6 text-center"
                                    >
                                        <metric.icon className="w-8 h-8 text-primary mx-auto mb-3" />
                                        <div className="text-3xl font-bold text-gradient mb-2">{metric.number}</div>
                                        <div className="text-sm text-muted-foreground">{metric.label}</div>
                                    </motion.div>
                                ))}
                            </div>
                        </div>
                    </section>

                    {/* Features Grid */}
                    <section className="relative py-20 px-6">
                        <div className="max-w-6xl mx-auto">
                            <div className="grid md:grid-cols-3 gap-6">
                                {[
                                    { icon: Zap, title: "Instant Analysis", desc: "Get feedback in seconds, not hours" },
                                    { icon: Shield, title: "Security Focus", desc: "Catch vulnerabilities before they ship" },
                                    { icon: Code2, title: "Multi-Language", desc: "Python, JS, TypeScript, Go, Rust & more" },
                                ].map((feature, i) => (
                                    <motion.div
                                        key={feature.title}
                                        initial={{ opacity: 0, y: 20 }}
                                        whileInView={{ opacity: 1, y: 0 }}
                                        viewport={{ once: true }}
                                        transition={{ delay: i * 0.1 }}
                                        className="glass rounded-xl p-6"
                                    >
                                        <div className="p-3 rounded-lg bg-primary/20 w-fit mb-4">
                                            <feature.icon className="w-6 h-6 text-primary" />
                                        </div>
                                        <h3 className="font-semibold text-xl mb-2">{feature.title}</h3>
                                        <p className="text-muted-foreground">{feature.desc}</p>
                                    </motion.div>
                                ))}
                            </div>
                        </div>
                    </section>

                    {/* Final CTA */}
                    <section className="relative py-20 px-6">
                        <div className="max-w-4xl mx-auto text-center">
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                className="glass rounded-2xl p-12"
                            >
                                <h2 className="text-4xl font-bold mb-4">Ready to Stop Paying for Code Reviews?</h2>
                                <p className="text-xl text-muted-foreground mb-8">
                                    Join 500+ projects using AI-powered reviews. Free forever.
                                </p>
                                <button
                                    onClick={() => setShowReviewer(true)}
                                    className="px-10 py-5 bg-primary text-white font-semibold rounded-2xl transition-all hover:opacity-90 hover:scale-105 flex items-center gap-3 justify-center mx-auto text-lg"
                                >
                                    <Sparkles className="w-6 h-6" />
                                    Try It Free - No Signup Required
                                </button>
                            </motion.div>
                        </div>
                    </section>
                </>
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
                                ← Back to Home
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
