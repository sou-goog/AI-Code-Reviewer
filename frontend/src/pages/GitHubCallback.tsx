import { useEffect } from "react";
import { useLocation } from "wouter";

export default function GitHubCallback() {
    const [, setLocation] = useLocation();

    useEffect(() => {
        // Get the code and state from URL params
        const params = new URLSearchParams(window.location.search);
        const code = params.get("code");
        const state = params.get("state");

        if (code) {
            // Send to backend callback endpoint
            const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

            fetch(`${API_URL}/auth/github/callback?code=${code}&state=${state || ""}`)
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        // Store user data
                        localStorage.setItem("github_user", JSON.stringify(data.user));
                        // Redirect to settings
                        setLocation("/settings");
                    } else {
                        console.error("GitHub callback error:", data);
                        setLocation("/settings?error=auth_failed");
                    }
                })
                .catch(error => {
                    console.error("GitHub callback error:", error);
                    setLocation("/settings?error=auth_failed");
                });
        } else {
            // No code, redirect back
            setLocation("/settings");
        }
    }, [setLocation]);

    return (
        <div className="flex items-center justify-center min-h-screen">
            <div className="text-center">
                <div className="w-16 h-16 border-4 border-t-blue-500 border-gray-200 rounded-full animate-spin mx-auto mb-4"></div>
                <p className="text-gray-600">Connecting to GitHub...</p>
            </div>
        </div>
    );
}
