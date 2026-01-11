'use client';

import { useState } from 'react';
import Navbar from '../components/Navbar';
import ReviewForm from '../components/ReviewForm';
import ReviewResults from '../components/ReviewResults';

export default function Home() {
    const [reviewResult, setReviewResult] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleReviewSubmit = async (code: string, language: string) => {
        setIsLoading(true);

        try {
            // Call your backend API
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/review`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code_diff: code, language })
            });

            const data = await response.json();
            setReviewResult(data.review);
        } catch (error) {
            console.error('Review failed:', error);
            alert('Failed to review code. Check your API connection.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen">
            <Navbar currentPage="review" />

            <main className="container mx-auto px-4 py-8 max-w-7xl">
                <div className="grid lg:grid-down gap-8">
                    {/* Left Column - Review Form */}
                    <div className="glass-card p-8">
                        <h2 className="text-3xl font-heading font-bold mb-6 bg-gradient-purple-blue bg-clip-text text-transparent">
                            Submit Code for Review
                        </h2>
                        <ReviewForm onSubmit={handleReviewSubmit} isLoading={isLoading} />
                    </div>

                    {/* Right Column - Results */}
                    <div className="glass-card p-8 lg:col-span-1">
                        <h2 className="text-3xl font-heading font-bold mb-6">
                            Review Results
                        </h2>
                        {reviewResult ? (
                            <ReviewResults result={reviewResult} />
                        ) : (
                            <div className="text-center py-16 text-grey-secondary">
                                <p className="text-lg">Submit code to see AI-powered review results</p>
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
}
