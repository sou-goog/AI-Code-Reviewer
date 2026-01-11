import { useState } from "react";
import Navbar from "@/components/Navbar";
import ReviewForm from "@/components/ReviewForm";
import ReviewResult from "@/components/ReviewResult";
import { Sparkles, Zap, Shield, Code2 } from "lucide-react";

export default function Home() {
    const [loading, setLoading] = useState(false);
    const [review, setReview] = useState<any>(null);

    const handleSubmit = (reviewData: any) => {
        setReview(reviewData);
    };

    return (
        <div className="min-h-screen bg-background bg-grid relative">
            <div className="absolute inset-0 bg-gradient-radial pointer-events-none" />
            <Navbar />

            <main className="relative pt-28 pb-20 px-6">
                <div className="max-w-6xl mx-auto">
                    <div className="text-center mb-12">
                        <h1 className="font-display text-5xl md:text-6xl font-bold mb-4">
                            <span className="text-gradient">AI-Powered</span>
                            <br />
                            Code Review
                        </h1>
                        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                            Get instant, intelligent feedback on your code changes.
                            Catch bugs, security issues, and improve code quality before you merge.
                        </p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-4 mb-12">
                        {[
                            { icon: Zap, title: "Instant Analysis", desc: "Get feedback in seconds" },
                            { icon: Shield, title: "Security Focus", desc: "Catch vulnerabilities early" },
                            { icon: Code2, title: "Multi-Language", desc: "Python, JS, Go & more" },
                        ].map((feature, i) => (
                            <div key={feature.title} className="glass rounded-xl p-5 flex items-center gap-4">
                                <div className="p-3 rounded-lg bg-primary/20">
                                    <feature.icon className="w-5 h-5 text-primary" />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-foreground">{feature.title}</h3>
                                    <p className="text-sm text-muted-foreground">{feature.desc}</p>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="grid lg:grid-cols-2 gap-8">
                        <div className="space-y-4">
                            <h2 className="font-display text-2xl font-semibold text-foreground flex items-center gap-2">
                                <Sparkles className="w-6 h-6 text-primary" />
                                Submit Code for Review
                            </h2>
                            <ReviewForm onSubmit={handleSubmit} loading={loading} setLoading={setLoading} />
                        </div>

                        <div className="space-y-4">
                            <h2 className="font-display text-2xl font-semibold text-foreground">
                                Review Results
                            </h2>
                            {loading ? (
                                <div className="glass rounded-xl p-12 flex flex-col items-center justify-center">
                                    <div className="w-12 h-12 border-3 border-primary/30 border-t-primary rounded-full animate-spin mb-4" />
                                    <p className="text-muted-foreground">Analyzing your code...</p>
                                </div>
                            ) : review ? (
                                <ReviewResult review={review} />
                            ) : (
                                <div className="glass rounded-xl p-12 flex flex-col items-center justify-center text-center">
                                    <div className="w-16 h-16 rounded-2xl bg-muted/50 flex items-center justify-center mb-4">
                                        <Code2 className="w-8 h-8 text-muted-foreground" />
                                    </div>
                                    <p className="text-muted-foreground">
                                        Submit code to see AI-powered review results
                                    </p>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
