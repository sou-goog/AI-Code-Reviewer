'use client';

import Link from 'next/link';

interface NavbarProps {
    currentPage: 'review' | 'stats' | 'history';
}

export default function Navbar({ currentPage }: NavbarProps) {
    return (
        <nav className="border-b border-white/10 backdrop-blur-lg bg-white/5 sticky top-0 z-50">
            <div className="container mx-auto px-4 py-4 max-w-7xl">
                <div className="flex items-center justify-between">
                    {/* Logo */}
                    <Link href="/" className="text-2xl font-heading font-bold bg-gradient-purple-blue bg-clip-text text-transparent">
                        AI Code Reviewer
                    </Link>

                    {/* Navigation Buttons */}
                    <div className="flex gap-2">
                        <Link href="/">
                            <button className={`nav-pill ${currentPage === 'review' ? 'nav-pill-active' : 'nav-pill-inactive'}`}>
                                Review
                            </button>
                        </Link>

                        <Link href="/stats">
                            <button className={`nav-pill ${currentPage === 'stats' ? 'nav-pill-active' : 'nav-pill-inactive'}`}>
                                Analytics
                            </button>
                        </Link>

                        <Link href="/history">
                            <button className={`nav-pill ${currentPage === 'history' ? 'nav-pill-active' : 'nav-pill-inactive'}`}>
                                History
                            </button>
                        </Link>
                    </div>
                </div>
            </div>
        </nav>
    );
}
