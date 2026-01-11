import { useState } from "react";
import { motion } from "framer-motion";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface ReviewFormProps {
  onSubmit: (review: any) => void;
  loading: boolean;
  setLoading: (loading: boolean) => void;
}

// ... rest of the code from ReviewForm.tsx user provided

export default function ReviewForm({ onSubmit, loading, setLoading }: ReviewFormProps) {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!code.trim()) return;

    setLoading(true);
    
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
      onSubmit(data);
    } catch (error) {
      console.error('Review failed:', error);
      alert(`Failed to review code: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  // ... rest stays the same
}
