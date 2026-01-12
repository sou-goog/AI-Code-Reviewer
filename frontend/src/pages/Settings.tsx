import { useState, useEffect } from "react";
import { Github, ExternalLink, Check, X } from "lucide-react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface Repository {
    id: number;
    name: string;
    full_name: string;
    private: boolean;
    description: string | null;
    url: string;
    language: string | null;
    updated_at: string;
    auto_review_enabled?: boolean;
}

interface GitHubUser {
    id: number;
    username: string;
    avatar_url: string;
    name: string | null;
}

export default function Settings() {
    const [connected, setConnected] = useState(false);
    const [loading, setLoading] = useState(false);
    const [user, setUser] = useState<GitHubUser | null>(null);
    const [repos, setRepos] = useState<Repository[]>([]);

    useEffect(() => {
        // Check if user is already connected (from localStorage)
        const savedUser = localStorage.getItem("github_user");
        if (savedUser) {
            const userData = JSON.parse(savedUser);
            setUser(userData);
            setConnected(true);
            fetchRepos(userData.username);
        }

        // Handle OAuth callback
        const params = new URLSearchParams(window.location.search);
        const code = params.get("code");
        if (code) {
            handleOAuthCallback(code);
        }
    }, []);

    const connectGitHub = async () => {
        try {
            const response = await fetch(`${API_URL}/auth/github/login`);
            const data = await response.json();
            window.location.href = data.auth_url;
        } catch (error) {
            console.error("Failed to initiate GitHub OAuth:", error);
        }
    };

    const handleOAuthCallback = async (code: string) => {
        setLoading(true);
        try {
            const response = await fetch(
                `${API_URL}/auth/github/callback?code=${code}`
            );
            const data = await response.json();

            if (data.success) {
                setUser(data.user);
                setConnected(true);
                localStorage.setItem("github_user", JSON.stringify(data.user));

                // Clear URL params
                window.history.replaceState({}, document.title, "/settings");

                // Fetch repositories
                await fetchRepos(data.user.username);
            }
        } catch (error) {
            console.error("OAuth callback failed:", error);
        } finally {
            setLoading(false);
        }
    };

    const fetchRepos = async (username: string) => {
        try {
            const response = await fetch(
                `${API_URL}/auth/github/repos?username=${username}`
            );
            const data = await response.json();

            // Fetch auto-review status for each repo
            const reposWithSettings = await Promise.all(
                data.repos.map(async (repo: Repository) => {
                    try {
                        const settingsResponse = await fetch(
                            `${API_URL}/repos/settings/${encodeURIComponent(repo.full_name)}`
                        );
                        const settings = await settingsResponse.json();
                        return { ...repo, auto_review_enabled: settings.auto_review_enabled };
                    } catch {
                        return { ...repo, auto_review_enabled: false };
                    }
                })
            );

            setRepos(reposWithSettings);
        } catch (error) {
            console.error("Failed to fetch repos:", error);
        }
    };

    const toggleAutoReview = async (repo: Repository) => {
        const newStatus = !repo.auto_review_enabled;

        try {
            await fetch(`${API_URL}/repos/settings`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    repo_full_name: repo.full_name,
                    auto_review_enabled: newStatus,
                }),
            });

            // Update local state
            setRepos(
                repos.map((r) =>
                    r.id === repo.id ? { ...r, auto_review_enabled: newStatus } : r
                )
            );
        } catch (error) {
            console.error("Failed to update repo settings:", error);
        }
    };

    const disconnect = () => {
        localStorage.removeItem("github_user");
        setUser(null);
        setConnected(false);
        setRepos([]);
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <div className="w-16 h-16 border-4 border-t-blue-500 border-gray-200 rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-gray-600">Connecting to GitHub...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-6xl mx-auto p-6">
            <div className="mb-8">
                <h1 className="text-4xl font-bold mb-2">Settings</h1>
                <p className="text-gray-600">Connect GitHub and manage auto-review settings</p>
            </div>

            {!connected ? (
                <div className="bg-white rounded-xl shadow-lg p-8 text-center">
                    <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                        <Github className="w-10 h-10 text-gray-600" />
                    </div>
                    <h2 className="text-2xl font-bold mb-2">Connect GitHub</h2>
                    <p className="text-gray-600 mb-6 max-w-md mx-auto">
                        Connect your GitHub account to enable automatic PR reviews and inline
                        comments
                    </p>
                    <button
                        onClick={connectGitHub}
                        className="inline-flex items-center gap-2 px-8 py-3 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors font-medium"
                    >
                        <Github className="w-5 h-5" />
                        Connect with GitHub
                    </button>
                </div>
            ) : (
                <div className="space-y-6">
                    {/* Connected Account */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-4">
                                {user?.avatar_url && (
                                    <img
                                        src={user.avatar_url}
                                        alt={user.username}
                                        className="w-16 h-16 rounded-full"
                                    />
                                )}
                                <div>
                                    <h3 className="text-xl font-bold">{user?.name || user?.username}</h3>
                                    <p className="text-gray-600">@{user?.username}</p>
                                </div>
                            </div>
                            <button
                                onClick={disconnect}
                                className="px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                            >
                                Disconnect
                            </button>
                        </div>
                    </div>

                    {/* Repositories */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-2xl font-bold">Repositories</h2>
                            <p className="text-gray-600">{repos.length} repositories</p>
                        </div>

                        <div className="space-y-3">
                            {repos.map((repo) => (
                                <div
                                    key={repo.id}
                                    className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors"
                                >
                                    <div className="flex-1">
                                        <div className="flex items-center gap-2">
                                            <a
                                                href={repo.url}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="text-lg font-semibold hover:text-blue-600 flex items-center gap-1"
                                            >
                                                {repo.name}
                                                <ExternalLink className="w-4 h-4" />
                                            </a>
                                            {repo.private && (
                                                <span className="px-2 py-1 text-xs bg-gray-200 rounded">
                                                    Private
                                                </span>
                                            )}
                                            {repo.language && (
                                                <span className="px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded">
                                                    {repo.language}
                                                </span>
                                            )}
                                        </div>
                                        {repo.description && (
                                            <p className="text-sm text-gray-600 mt-1">
                                                {repo.description}
                                            </p>
                                        )}
                                    </div>

                                    <button
                                        onClick={() => toggleAutoReview(repo)}
                                        className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${repo.auto_review_enabled
                                                ? "bg-green-100 text-green-700 hover:bg-green-200"
                                                : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                                            }`}
                                    >
                                        {repo.auto_review_enabled ? (
                                            <>
                                                <Check className="w-4 h-4" />
                                                Auto-review ON
                                            </>
                                        ) : (
                                            <>
                                                <X className="w-4 h-4" />
                                                Auto-review OFF
                                            </>
                                        )}
                                    </button>
                                </div>
                            ))}
                        </div>

                        {repos.length === 0 && (
                            <div className="text-center py-12 text-gray-500">
                                <Github className="w-12 h-12 mx-auto mb-2 opacity-50" />
                                <p>No repositories found</p>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}
