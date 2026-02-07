"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import AuthForm from "@/components/AuthForm";
import { apiFetch } from "@/lib/api";

export default function SignupPage() {
  const { token, setToken } = useAuth();
  const router = useRouter();

  const [error, setError] = useState<string | undefined>();
  const [isLoading, setIsLoading] = useState(false);

  // Auto logout if logged in
  useEffect(() => {
    if (token) setToken(null);
  }, [token, setToken]);

  const handleSignup = async (username: string, password: string) => {
    setIsLoading(true);
    setError(undefined);

    try {
      await apiFetch("/users/", {
        method: "POST",
        body: JSON.stringify({ username, password_hash: password }),
      });
      router.push("/auth/login"); // Redirect to login after signup
    } catch (err: any) {
      setError(err.detail || err.message || "Signup failed.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4">
      <div className="max-w-md w-full space-y-8">
        <h2 className="text-3xl font-extrabold text-center text-gray-900">Create your account</h2>
        <AuthForm type="signup" onSubmit={handleSignup} error={error} isLoading={isLoading} />
      </div>
    </div>
  );
}
