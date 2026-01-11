import { useState } from "react";
import Navbar from "@/components/Navbar";
import {
    History as HistoryIcon,
    Search,
    Filter,
    ChevronRight,
    AlertCircle,
    AlertTriangle,
    CheckCircle,
    Clock,
    FileCode
} from "lucide-react";

const historyData = [
    {
        id: 1,
        filename: "src/auth/login.py",
        language: "Python",
        timestamp: "2025-01-11 14:32",
        status: "critical",
        critical: 2,
        warnings: 3,
        suggestions: 5,
        summary: "Security vulnerabilities in authentication flow detected."
    },
    {
        id: 2,
        filename: "api/routes/users.ts",
        language: "TypeScript",
        timestamp: "2025-01-11 13:15",
        status: "warning",
        critical: 0,
        warnings: 4,
        suggestions: 2,
        summary: "Minor type safety improvements recommended."
    },
    {
        id: 3,
        filename: "lib/database.go",
        language: "Go",
        timestamp: "2025-01-11 11:48",
        status: "clean",
        critical: 0,
        warnings: 0,
        suggestions: 3,
        summary: "Clean code with minor style suggestions."
    },
    {
        id: 4,
        filename: "components/Dashboard.tsx",
        language: "TypeScript",
        timestamp: "2025-01-11 10:22",
        status: "warning",
        critical: 0,
        warnings: 2,
        suggestions: 4,
        summary: "Performance optimizations available for render cycles."
    },
    {
        id: 5,
        filename: "utils/validation.js",
        language: "JavaScript",
        timestamp: "2025-01-10 16:45",
        status: "critical",
        critical: 1,
        warnings: 2,
        suggestions: 1,
        summary: "Input validation bypass vulnerability found."
    },
    {
        id: 6,
        filename: "models/user.py",
        language: "Python",
        timestamp: "2025-01-10 15:30",
        status: "clean",
        critical: 0,
        warnings: 1,
        suggestions: 2,
        summary: "Well-structured data model with minor docs improvement."
    },
];

export default function History() {
    const [search, setSearch] = useState("");
    const [filter, setFilter] = useState("all");

    const filteredHistory = historyData.filter(item => {
        const matchesSearch = item.filename.toLowerCase().includes(search.toLowerCase());
        const matchesFilter = filter === "all" || item.status === filter;
        return matchesSearch && matchesFilter;
    });

    return (
        <div className="min-h-screen bg-background bg-grid relative">
            <div className="absolute inset-0 bg-gradient-radial pointer-events-none" />
            <Navbar />

            <main className="relative pt-28 pb-20 px-6">
                <div className="max-w-6xl mx-auto">
                    <div className="mb-10">
                        <h1 className="font-display text-4xl font-bold text-foreground mb-2 flex items-center gap-3">
                            <HistoryIcon className="w-10 h-10 text-primary" />
                            Review History
                        </h1>
                        <p className="text-muted-foreground">
                            Browse and search through your past code reviews
                        </p>
                    </div>

                    <div className="flex flex-col sm:flex-row gap-4 mb-8">
                        <div className="relative flex-1">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                            <input
                                placeholder="Search files..."
                                value={search}
                                onChange={(e) => setSearch(e.target.value)}
                                className="w-full pl-10 pr-4 py-2 text-sm bg-card border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                            />
                        </div>
                        <div className="relative">
                            <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground pointer-events-none" />
                            <select
                                value={filter}
                                onChange={(e) => setFilter(e.target.value)}
                                className="w-full sm:w-40 pl-10 pr-8 py-2 text-sm bg-card border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary appearance-none cursor-pointer"
                            >
                                <option value="all">All Reviews</option>
                                <option value="critical">Critical</option>
                                <option value="warning">Warnings</option>
                                <option value="clean">Clean</option>
                            </select>
                            <svg className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                            </svg>
                        </div>
                    </div>

                    <div className="space-y-4">
                        {filteredHistory.map((item) => (
                            <div
                                key={item.id}
                                className="glass rounded-xl p-5 hover:bg-white/5 transition-all cursor-pointer group"
                            >
                                <div className="flex items-start justify-between">
                                    <div className="flex items-start gap-4">
                                        <div className={`p-3 rounded-xl ${item.status === "critical" ? "bg-red-500/20" :
                                            item.status === "warning" ? "bg-yellow-500/20" :
                                                "bg-emerald-500/20"
                                            }`}>
                                            <FileCode className={`w-5 h-5 ${item.status === "critical" ? "text-red-400" :
                                                item.status === "warning" ? "text-yellow-400" :
                                                    "text-emerald-400"
                                                }`} />
                                        </div>
                                        <div>
                                            <h3 className="font-mono text-sm font-medium text-foreground mb-1">
                                                {item.filename}
                                            </h3>
                                            <div className="flex items-center gap-3 text-xs text-muted-foreground mb-2">
                                                <span className="px-2 py-0.5 rounded bg-white/10">{item.language}</span>
                                                <span className="flex items-center gap-1">
                                                    <Clock className="w-3 h-3" />
                                                    {item.timestamp}
                                                </span>
                                            </div>
                                            <p className="text-sm text-muted-foreground">{item.summary}</p>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-6">
                                        <div className="flex items-center gap-4 text-sm">
                                            {item.critical > 0 && (
                                                <div className="flex items-center gap-1 text-red-400">
                                                    <AlertCircle className="w-4 h-4" />
                                                    <span>{item.critical}</span>
                                                </div>
                                            )}
                                            {item.warnings > 0 && (
                                                <div className="flex items-center gap-1 text-yellow-400">
                                                    <AlertTriangle className="w-4 h-4" />
                                                    <span>{item.warnings}</span>
                                                </div>
                                            )}
                                            {item.suggestions > 0 && (
                                                <div className="flex items-center gap-1 text-emerald-400">
                                                    <CheckCircle className="w-4 h-4" />
                                                    <span>{item.suggestions}</span>
                                                </div>
                                            )}
                                        </div>
                                        <ChevronRight className="w-5 h-5 text-muted-foreground group-hover:text-foreground group-hover:translate-x-1 transition-all" />
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>

                    {filteredHistory.length === 0 && (
                        <div className="glass rounded-xl p-12 text-center">
                            <HistoryIcon className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                            <p className="text-muted-foreground">No reviews match your search</p>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}
