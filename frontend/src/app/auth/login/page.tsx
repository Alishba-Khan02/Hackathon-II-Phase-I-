"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import AuthForm from "@/components/AuthForm";
import Link from "next/link"; // Import Link for navigation
import { apiFetch } from "@/lib/api";

export default function LoginPage() {
  const { token, setToken } = useAuth();
  const router = useRouter();

  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (token) {
      router.push("/dashboard");
    }
  }, [token, router]);

  const handleLogin = async (username: string, password: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiFetch<{ access_token: string }>("/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `username=${username}&password=${password}`,
      });
      setToken(response.access_token);
      router.push("/dashboard"); // Redirect to dashboard after successful login
    } catch (err: any) {
      setError(err.detail || "Login failed. Please check your credentials.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full bg-gray-800 p-8 rounded-lg shadow-lg space-y-8 border border-emerald-400/30"> {/* Added card styling with neon border */}
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-white">
            Sign in to your account
          </h2>
        </div>
        <AuthForm type="login" onSubmit={handleLogin} error={error} isLoading={isLoading} />
        <div className="text-center">
          <p className="text-sm text-gray-300">
            Don't have an account?{" "}
            <Link href="/" className="font-medium text-emerald-400 hover:text-emerald-300">
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}