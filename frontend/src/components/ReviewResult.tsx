import { AlertCircle, AlertTriangle, Lightbulb, CheckCircle, ChevronDown } from "lucide-react";
import { useState } from "react";

interface ReviewResultProps {
    review: {
        critical: string[];
        warnings: string[];
        suggestions: string[];
        positive: string[];
        summary: string;
    };
}

export default function ReviewResult({ review }: ReviewResultProps) {
    const sections = [
        {
            title: "Critical Issues",
            emoji: "🔴",
            icon: AlertCircle,
            color: "text-red-400 border-red-500/30 bg-red-500/10",
            glowClass: "glow-critical",
            items: review.critical,
        },
        {
            title: "Warnings",
            emoji: "🟡",
            icon: AlertTriangle,
            color: "text-yellow-400 border-yellow-500/30 bg-yellow-500/10",
            glowClass: "glow-warning",
            items: review.warnings,
        },
        {
            title: "Suggestions",
            emoji: "🟢",
            icon: Lightbulb,
            color: "text-emerald-400 border-emerald-500/30 bg-emerald-500/10",
            glowClass: "glow-success",
            items: review.suggestions,
        },
        {
            title: "Positive Notes",
            emoji: "✅",
            icon: CheckCircle,
            color: "text-blue-400 border-blue-500/30 bg-blue-500/10",
            glowClass: "glow-info",
            items: review.positive,
        },
    ];

    return (
        <div className="space-y-6">
            <div className="glass rounded-xl p-6 border border-white/10">
                <h3 className="font-display text-lg font-semibold mb-3">Summary</h3>
                <p className="text-muted-foreground leading-relaxed">{review.summary}</p>
            </div>

            <div className="grid gap-4">
                {sections.map((section, index) => (
                    <Section key={section.title} section={section} index={index} />
                ))}
            </div>
        </div>
    );
}

function Section({ section, index }: { section: any; index: number }) {
    const [isOpen, setIsOpen] = useState(section.items.length > 0);
    const Icon = section.icon;

    if (section.items.length === 0) {
        return null;
    }

    return (
        <div>
            <div className={`rounded-xl border ${section.color} ${section.glowClass} overflow-hidden`}>
                <button
                    onClick={() => setIsOpen(!isOpen)}
                    className="w-full flex items-center justify-between p-4 hover:bg-white/5 transition-colors"
                >
                    <div className="flex items-center gap-3">
                        <Icon className="w-5 h-5" />
                        <span className="font-display font-semibold">{section.title}</span>
                        <span className="text-sm opacity-70">({section.items.length})</span>
                    </div>
                    <ChevronDown className={`w-5 h-5 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
                </button>
                {isOpen && (
                    <div className="px-4 pb-4 space-y-3">
                        {section.items.map((item: string, i: number) => (
                            <div key={i} className="flex gap-3 p-3 rounded-lg bg-black/20">
                                <span className="text-lg">{section.emoji}</span>
                                <p className="text-sm text-foreground/90 leading-relaxed">{item}</p>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
