// frontend/src/app/dashboard/page.tsx
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
}

export default function DashboardPage() {
  const { token, logout } = useAuth();
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // State for editing a task
  const [editTaskId, setEditTaskId] = useState<number | null>(null);
  const [editTaskTitle, setEditTaskTitle] = useState("");
  const [editTaskDescription, setEditTaskDescription] = useState("");

  const [newTaskTitle, setNewTaskTitle] = useState("");

  useEffect(() => {
    if (!token) {
      router.push("/auth/login");
      return;
    }
    fetchTasks();
  }, [token, router]);

  const fetchTasks = async () => {
    setLoading(true);
    setError(null);
    try {
      if (!token) return;
      const data = await apiFetch<Task[]>("/tasks/", { token });
      setTasks(data);
    } catch (err: any) {
      console.error(err);
      setError(err.detail || "Failed to fetch tasks.");
      logout();
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTaskTitle.trim() || !token) return;

    try {
      await apiFetch<Task>("/tasks/", {
        method: "POST",
        token,
        body: JSON.stringify({ title: newTaskTitle, completed: false }),
      });
      setNewTaskTitle("");
      fetchTasks();
    } catch (err: any) {
      console.error(err);
      setError(err.detail || "Failed to create task.");
    }
  };

  const handleToggleCompleted = async (taskId: number, currentStatus: boolean) => {
    if (!token) return;
    try {
      await apiFetch<Task>(`/tasks/${taskId}/${currentStatus ? "uncomplete" : "complete"}`, {
        method: "PATCH",
        token,
      });
      fetchTasks();
    } catch (err: any) {
      console.error(err);
      setError(err.detail || "Failed to update task status.");
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    if (!token) return;
    try {
      await apiFetch(`/tasks/${taskId}`, { method: "DELETE", token });
      fetchTasks();
    } catch (err: any) {
      console.error(err);
      setError(err.detail || "Failed to delete task.");
    }
  };

  // Start editing a task
  const handleEditTask = (task: Task) => {
    setEditTaskId(task.id);
    setEditTaskTitle(task.title);
    setEditTaskDescription(task.description || "");
  };

  // Save updated task
  const handleUpdateTask = async (taskId: number) => {
    if (!token || !editTaskTitle.trim()) return;
    try {
      await apiFetch(`/tasks/${taskId}`, {
        method: "PATCH",
        token,
        body: JSON.stringify({ title: editTaskTitle, description: editTaskDescription }),
      });
      setEditTaskId(null);
      setEditTaskTitle("");
      setEditTaskDescription("");
      fetchTasks();
    } catch (err: any) {
      console.error(err);
      setError(err.detail || "Failed to update task.");
    }
  };

  if (!token) return <p>Redirecting...</p>;
  if (loading) return <p>Loading tasks...</p>;
  if (error) return <p className="text-red-500">Error: {error}</p>;

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-4">
      <div className="container mx-auto max-w-2xl bg-gray-800 p-6 rounded-lg shadow-lg border border-emerald-400/30">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-extrabold text-white">Your Tasks</h1>
          <button
            onClick={logout}
            className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded transition duration-200"
          >
            Logout
          </button>
        </div>

        {error && <p className="text-red-400 mb-4">Failed to edit, 0 occurrences found for old_string (  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Your Tasks</h1>
      <button onClick={logout} className="bg-red-500 text-white px-4 py-2 rounded mb-4">
        Logout
      </button>

      <form onSubmit={handleCreateTask} className="mb-4 flex">
        <input
          type="text"
          placeholder="New task title"
          value={newTaskTitle}
          onChange={(e) => setNewTaskTitle(e.target.value)}
          className="flex-grow p-2 border border-gray-300 rounded-l-md"
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded-r-md">
          Add Task
        </button>
      </form>

      {tasks.length === 0 ? (
        <p>No tasks yet. Add one above!</p>
      ) : (
        <ul>
          {tasks.map((task) => (
            <li
              key={task.id}
              className="flex items-center justify-between bg-gray-100 p-3 rounded shadow-sm mb-2"
            >
              <div className="flex flex-col gap-1">
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={task.completed}
                    onChange={() => handleToggleCompleted(task.id, task.completed)}
                  />
                  {editTaskId === task.id ? (
                    <input
                      type="text"
                      value={editTaskTitle}
                      onChange={(e) => setEditTaskTitle(e.target.value)}
                      className="border p-1 rounded"
                    />
                  ) : (
                    <span className={task.completed ? "line-through text-gray-500" : ""}>
                      {task.title}
                    </span>
                  )}
                </div>
                {editTaskId === task.id ? (
                  <textarea
                    value={editTaskDescription}
                    onChange={(e) => setEditTaskDescription(e.target.value)}
                    className="mt-1 p-2 border border-gray-600 rounded-md bg-gray-800 text-white w-full"
                    placeholder="Description (optional)"
                    rows={2}
                  />
                ) : (
                  task.description && (
                    <span className="text-sm text-gray-600">({task.description})</span>
                  )
                )}
              </div>

              <div className="flex gap-2 ml-4">
                {editTaskId === task.id ? (
                  <button
                    onClick={() => handleUpdateTask(task.id)}
                    className="bg-green-500 text-white px-2 py-1 rounded"
                  >
                    Save
                  </button>
                ) : (
                  <button
                    onClick={() => handleEditTask(task)}
                    className="bg-yellow-400 text-white px-2 py-1 rounded"
                  >
                    Edit
                  </button>
                )}
                <button
                  onClick={() => handleDeleteTask(task.id)}
                  className="bg-red-400 text-white px-2 py-1 rounded"
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );). Original old_string was (  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Your Tasks</h1>
      <button onClick={logout} className="bg-red-500 text-white px-4 py-2 rounded mb-4">
        Logout
      </button>

      <form onSubmit={handleCreateTask} className="mb-4 flex">
        <input
          type="text"
          placeholder="New task title"
          value={newTaskTitle}
          onChange={(e) => setNewTaskTitle(e.target.value)}
          className="flex-grow p-2 border border-gray-300 rounded-l-md"
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded-r-md">
          Add Task
        </button>
      </form>

      {tasks.length === 0 ? (
        <p>No tasks yet. Add one above!</p>
      ) : (
        <ul>
          {tasks.map((task) => (
            <li
              key={task.id}
              className="flex items-center justify-between bg-gray-100 p-3 rounded shadow-sm mb-2"
            >
              <div className="flex flex-col gap-1">
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={task.completed}
                    onChange={() => handleToggleCompleted(task.id, task.completed)}
                  />
                  {editTaskId === task.id ? (
                    <input
                      type="text"
                      value={editTaskTitle}
                      onChange={(e) => setEditTaskTitle(e.target.value)}
                      className="border p-1 rounded"
                    />
                  ) : (
                    <span className={task.completed ? "line-through text-gray-500" : ""}>
                      {task.title}
                    </span>
                  )}
                </div>
                {editTaskId === task.id ? (
                  <textarea
                    value={editTaskDescription}
                    onChange={(e) => setEditTaskDescription(e.target.value)}
                    className="mt-1 p-2 border border-gray-600 rounded-md bg-gray-800 text-white w-full"
                    placeholder="Description (optional)"
                    rows={2}
                  />
                ) : (
                  task.description && (
                    <span className="text-sm text-gray-600">({task.description})</span>
                  )
                )}
              </div>

              <div className="flex gap-2 ml-4">
                {editTaskId === task.id ? (
                  <button
                    onClick={() => handleUpdateTask(task.id)}
                    className="bg-green-500 text-white px-2 py-1 rounded"
                  >
                    Save
                  </button>
                ) : (
                  <button
                    onClick={() => handleEditTask(task)}
                    className="bg-yellow-400 text-white px-2 py-1 rounded"
                  >
                    Edit
                  </button>
                )}
                <button
                  onClick={() => handleDeleteTask(task.id)}
                  className="bg-red-400 text-white px-2 py-1 rounded"
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );) in F:\Hackathon-II\Todo-app\frontend\src\app\dashboard\page.tsx. No edits made. The exact text in old_string was not found. Ensure you're not escaping content incorrectly and check whitespace, indentation, and context.</p>}

        <form onSubmit={handleCreateTask} className="mb-6 flex gap-2">
          <input
            type="text"
            placeholder="New task title"
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            className="flex-grow p-3 border border-gray-700 rounded-md bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-400"
          />
          <button
            type="submit"
            className="bg-emerald-600 hover:bg-emerald-500 text-gray-900 font-bold py-3 px-6 rounded-md transition duration-200"
          >
            Add Task
          </button>
        </form>

        {tasks.length === 0 ? (
          <p className="text-gray-400 text-center">No tasks yet. Add one above!</p>
        ) : (
          <ul className="space-y-3">
            {tasks.map((task) => (
              <li
                key={task.id}
                className="flex items-center justify-between bg-gray-700 p-4 rounded-lg shadow-md border border-gray-600"
              >
                <div className="flex flex-col flex-grow gap-1">
                  <div className="flex items-center gap-3">
                    <input
                      type="checkbox"
                      checked={task.completed}
                      onChange={() => handleToggleCompleted(task.id, task.completed)}
                      className="form-checkbox h-5 w-5 text-emerald-500 rounded border-gray-600 bg-gray-800 focus:ring-emerald-400 transition duration-150"
                    />
                    {editTaskId === task.id ? (
                      <input
                        type="text"
                        value={editTaskTitle}
                        onChange={(e) => setEditTaskTitle(e.target.value)}
                        className="flex-grow p-2 border border-gray-600 rounded-md bg-gray-800 text-white focus:outline-none focus:ring-1 focus:ring-emerald-400"
                      />
                    ) : (
                      <span className={`text-lg ${task.completed ? "line-through text-gray-500" : "text-white"}`}>
                        {task.title}
                      </span>
                    )}
                  </div>
                  {editTaskId === task.id ? (
                    <textarea
                      value={editTaskDescription}
                      onChange={(e) => setEditTaskDescription(e.target.value)}
                      className="mt-1 p-2 border border-gray-600 rounded-md bg-gray-800 text-white w-full focus:outline-none focus:ring-1 focus:ring-emerald-400"
                      placeholder="Description (optional)"
                      rows={2}
                    />
                  ) : (
                    task.description && (
                      <span className="text-sm text-gray-400 ml-8">({task.description})</span>
                    )
                  )}
                </div>

                <div className="flex gap-2 ml-4">
                  {editTaskId === task.id ? (
                    <button
                      onClick={() => handleUpdateTask(task.id)}
                      className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-3 rounded transition duration-200"
                    >
                      Save
                    </button>
                  ) : (
                    <button
                      onClick={() => handleEditTask(task)}
                      className="bg-yellow-600 hover:bg-yellow-700 text-white font-bold py-2 px-3 rounded transition duration-200"
                    >
                      Edit
                    </button>
                  )}
                  <button
                    onClick={() => handleDeleteTask(task.id)}
                    className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-3 rounded transition duration-200"
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );

}
