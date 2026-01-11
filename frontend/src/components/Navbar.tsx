import { Link, useLocation } from "wouter";
import { Code2, BarChart3, History, Sparkles } from "lucide-react";

export default function Navbar() {
    const [location] = useLocation();

    const links = [
        { href: "/", label: "Review", icon: Code2 },
        { href: "/stats", label: "Analytics", icon: BarChart3 },
        { href: "/history", label: "History", icon: History },
    ];

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 glass">
            <div className="max-w-6xl mx-auto px-6 py-4">
                <div className="flex items-center justify-between">
                    <Link href="/">
                        <div className="flex items-center gap-3 cursor-pointer">
                            <div className="w-10 h-10 rounded-2xl bg-primary flex items-center justify-center">
                                <Sparkles className="w-5 h-5 text-white -scale-x-100" strokeWidth={2} />
                            </div>
                            <span className="font-display text-xl font-semibold text-foreground">
                                AI Code Reviewer
                            </span>
                        </div>
                    </Link>

                    <div className="flex items-center gap-1">
                        {links.map((link) => {
                            const isActive = location === link.href;
                            const Icon = link.icon;
                            return (
                                <Link key={link.href} href={link.href}>
                                    <button
                                        className={`relative px-4 py-2 rounded-lg font-medium text-sm flex items-center gap-2 transition-all duration-200 ${isActive
                                            ? "bg-primary text-white"
                                            : "text-muted-foreground hover:text-foreground hover:bg-white/5"
                                            }`}
                                    >
                                        <Icon className="w-4 h-4" />
                                        <span>{link.label}</span>
                                    </button>
                                </Link>
                            );
                        })}
                    </div>
                </div>
            </div>
        </nav>
    );
}
