// frontend/src/lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

interface RequestOptions extends RequestInit {
  token?: string;
}

async function apiFetch<T>(
  endpoint: string,
  { token, headers, ...customConfig }: RequestOptions = {}
): Promise<T> {
  const config: RequestInit = {
    method: customConfig.method || "GET",
    headers: {
      "Content-Type": "application/json",
      ...headers,
    },
    ...customConfig,
  };

  if (token) {
    config.headers = {
      ...config.headers,
      Authorization: `Bearer ${token}`,
    } as HeadersInit;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

  if (!response.ok) {
    const error = await response.json();
    return Promise.reject(error);
  }

  if (response.status === 204) {
    return {} as T; // No Content
  }

  return await response.json();
}

export { apiFetch };
