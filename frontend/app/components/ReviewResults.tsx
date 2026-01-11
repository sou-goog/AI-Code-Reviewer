'use client';

import ReactMarkdown from 'react-markdown';

interface ReviewResultsProps {
    result: string;
}

export default function ReviewResults({ result }: ReviewResultsProps) {
    // Parse result into sections
    const sections = parseMarkdown(result);

    return (
        <div className="space-y-6">
            {/* Summary */}
            {sections.summary && (
                <div className="pb-6 border-b border-white/10">
                    <h3 className="text-xl font-semibold mb-3">📋 Summary</h3>
                    <div className="prose prose-invert max-w-none text-grey-secondary">
                        <ReactMarkdown>{sections.summary}</ReactMarkdown>
                    </div>
                </div>
            )}

            {/* Critical Issues */}
            {sections.critical && (
                <IssueSection
                    title="Critical Issues"
                    emoji="🔴"
                    content={sections.critical}
                    color="red"
                />
            )}

            {/* Warnings */}
            {sections.warnings && (
                <IssueSection
                    title="Warnings"
                    emoji="🟡"
                    content={sections.warnings}
                    color="yellow"
                />
            )}

            {/* Suggestions */}
            {sections.suggestions && (
                <IssueSection
                    title="Suggestions"
                    emoji="🟢"
                    content={sections.suggestions}
                    color="green"
                />
            )}

            {/* Positive Notes */}
            {sections.positive && (
                <IssueSection
                    title="Positive Notes"
                    emoji="✅"
                    content={sections.positive}
                    color="blue"
                />
            )}
        </div>
    );
}

function IssueSection({ title, emoji, content, color }: {
    title: string;
    emoji: string;
    content: string;
    color: 'red' | 'yellow' | 'green' | 'blue';
}) {
    const borderColors = {
        red: 'border-critical-red/30',
        yellow: 'border-warning-yellow/30',
        green: 'border-success-green/30',
        blue: 'border-blue-accent/30',
    };

    const bgColors = {
        red: 'bg-critical-red/5',
        yellow: 'bg-warning-yellow/5',
        green: 'bg-success-green/5',
        blue: 'bg-blue-accent/5',
    };

    return (
        <div className={`border ${borderColors[color]} ${bgColors[color]} rounded-lg p-6`}>
            <h3 className="text-xl font-semibold mb-4">
                {emoji} {title}
            </h3>
            <div className="prose prose-invert max-w-none text-grey-secondary">
                <ReactMarkdown>{content}</ReactMarkdown>
            </div>
        </div>
    );
}

function parseMarkdown(text: string) {
    const sections: any = {};

    // Extract summary
    const summaryMatch = text.match(/##\s*🔍?\s*Summary(.*?)(?=##|$)/s);
    if (summaryMatch) sections.summary = summaryMatch[1].trim();

    // Extract critical
    const criticalMatch = text.match(/##\s*🔴\s*Critical[^#]*(.*?)(?=##|$)/s);
    if (criticalMatch) sections.critical = criticalMatch[1].trim();

    // Extract warnings
    const warningsMatch = text.match(/##\s*🟡\s*Warnings?(.*?)(?=##|$)/s);
    if (warningsMatch) sections.warnings = warningsMatch[1].trim();

    // Extract suggestions
    const suggestionsMatch = text.match(/##\s*🟢\s*Suggestions?(.*?)(?=##|$)/s);
    if (suggestionsMatch) sections.suggestions = suggestionsMatch[1].trim();

    // Extract positive
    const positiveMatch = text.match(/##\s*✅\s*Positive[^#]*(.*?)(?=##|$)/s);
    if (positiveMatch) sections.positive = positiveMatch[1].trim();

    return sections;
}
