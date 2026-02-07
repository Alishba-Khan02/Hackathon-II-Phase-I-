// frontend/src/app/page.tsx
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import AuthForm from "@/components/AuthForm";
import { apiFetch } from "@/lib/api";
import Link from "next/link"; // Import Link for navigation

export default function HomePage() {
  const { token, setToken } = useAuth();
  const router = useRouter();

  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (token) {
      router.push("/dashboard");
    }
  }, [token, router]);

  const handleSignup = async (username: string, password: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await apiFetch("/users/", {
        method: "POST",
        body: JSON.stringify({ username, password_hash: password }),
      });
      // After successful signup, redirect to login page as per user's flow
      router.push("/auth/login");
    } catch (err: any) {
      setError(err.detail || err.message || "Signup failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  if (token) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <p>Redirecting to dashboard...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full bg-gray-800 p-8 rounded-lg shadow-lg space-y-8 border border-emerald-400/30"> {/* Added card styling with neon border */}
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-white">
            Create your account
          </h2>
        </div>
        <AuthForm type="signup" onSubmit={handleSignup} error={error} isLoading={isLoading} />
        <div className="text-center">
          <p className="text-sm text-gray-300">
            Already have an account?{" "}
            <Link href="/auth/login" className="font-medium text-emerald-400 hover:text-emerald-300">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}