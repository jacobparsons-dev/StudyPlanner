import { useEffect, useState } from "react";
import {
    getStudyItems,
    createStudyItem,
    updateStudyItem,
    deleteStudyItem,
} from "../api";
const emptyForm = {
    subject: "",
    topic: "",
    question: "",
    answer: "",
    difficulty: 1,
};

function StudyItemsManager(){
    const [items, setItems] = useState([]);
    const [form, setForm] = useState(emptyForm);
    const [editingId, setEditingId] = useState(null);
    const [editForm, setEditForm] = useState(emptyForm);
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState("");

    const fetchItems = async () => {
        try {
            setLoading(true);
            setError("");
            const data = await getStudyItems();
            setItems(data);
        } catch (err) {
            console.error("Failed to fetch study item:", err);
            setError("Failed to load study items.");
        } finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        fetchItems();
    }, []);
    const handleCreateChange = (event) => {
        const { name, value } = event.target;
        setForm((prev) => ({
            ...prev,
            [name]: name === "difficulty" ? Number(value) : value,
        }));
    };
    const handleCreateSubmit = async (event) => {
        event.preventDefault();
        try {
            setSubmitting(true);
            setError("")
            const createdItem = await createStudyItem(form);
            setItems((prev) => [createdItem, ...prev]);
            setForm(emptyForm);
        } catch (err) {
            console.error("Failed to create study item:", err);
            setError("Failed to create study item.");
        } finally {
            setSubmitting(false);
        }
    };
    const handleDelete = async (itemId) => {
        try {
            setError("");
            await deleteStudyItem(itemId);
            setItems((prev) => prev.filter((item) => item.item_id !== itemId));
        } catch (err) {
            console.error("Failed to delete study item:", err);
            setError("Failed to delete study item.");
        }
    };
    const startEditing = (item) => {
        setEditingId(item.item_id);
        setEditForm({
            subject: item.subject,
            topic: item.topic,
            question: item.question,
            answer: item.answer,
            difficulty: item.difficulty,
        });
    };
    const cancelEditing = () => {
        setEditingId(null);
            setEditForm(emptyForm);
    };
    const handleEditChange = (event) => {
        const { name, value } = event.target;
        setEditForm((prev) => ({
            ...prev,
            [name]: name === "difficulty" ? Number(value) : value,
        }));
    };
    const handleEditSubmit = async (itemId) => {
        try {
            setError("");
            console.log("Sending editform:", editForm);
            const updatedItem = await updateStudyItem(itemId, editForm);
            console.log("returned from backend:", updatedItem)
            setItems((prev) =>
                prev.map((item) => (item.item_id === itemId ? updatedItem : item))
            );
            cancelEditing();
        } catch (err) {
            console.error("Failed to update study item:", err);
            setError("Failed to update study item.");
        }
    };
    return (
        <section className="rounded-3x1 bg-white/90 p-6 shadow-lg ring-1 ring-sky-100 backdrop-blur-sm">
            <div className="mb-6">
                <h2 className="text-2x1 font-semibold text-slate-800">Manage study items</h2>
                <p className="mt-1 text-sm text-slate-500">
                    Add, edit and delete your cards.
                </p>
            </div>
            {error ? (
                <div className="mb-4 rounded-2x1 bg-red-50 px-4 py-3 text-sm text-red-600 ring-1 ring-red-100">
                    {error}
                </div>
            ) : null}
            <form
                onSubmit={handleCreateSubmit}
                className="grid gap-4 rounded-2x1 bg-slate-50/80 p-4 ring-1 ring-slate-100"
            >
                <div className="grid gap-4 sm:grid-cols-2">
                    <input
                        name="subject"
                        value={form.subject}
                        onChange={handleCreateChange}
                        placeholder="Subject"
                        className="rounded-2x1 border border-slate-200 bg-white px-4 py-3 text-slate-700 outline-none"
                        required
                    />
                    <input
                        name="topic"
                        value={form.topic}
                        onChange={handleCreateChange}
                        placeholder="Topic"
                        className="rounded-2x1 border border-slate-200 bg-white px-4 py-3 text-slate-700 outline-none"
                        required
                    />
                </div>
                <input
                    name="question"
                    value={form.question}
                    onChange={handleCreateChange}
                    placeholder="Question"
                    className="rounded-2x1 border border-slate-200 bg-white px-4 py-3 text-slate-700 outline-none"
                    required
                />
                <textarea
                    name="answer"
                    value={form.answer}
                    onChange={handleCreateChange}
                    placeholder="Answer"
                    rows="4"
                    className="rounded-2x1 border border-slate-200 bg-white px-4 py-3 text-slate-700 outline-none"
                    required
                />
                <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
                    <label className="block">
                        <span className="mb-2 block text-sm font-medium text-slate-600">
                            Difficulty
                        </span>
                        <select
                            name="difficulty"
                            value={form.difficulty}
                            onChange={handleCreateChange}
                            className="rounded-2x1 border border-slate-200 bg-white px-4 py-3 text-slate-700 outline-none"
                        >
                            <option value={1}>1</option>
                            <option value={2}>2</option>
                            <option value={3}>3</option>
                        </select>
                    </label>
                    <button
                        type="submit"
                        disabled={submitting}
                        className="rounded-2x1 bg-sky-300 px-5 py-3 font-medium text-slate-800 shadow-sm transition hover:bg-sky-400 disabled:cursor-not-allowed disabled:opacity-70"
                    >
                        {submitting ? "Adding..." : "Add study item"}
                    </button>
                </div>
            </form>
            <div className="mt-8 space-y-4">
                {loading ? (
                    <p className="text-slate-500">Loading study items...</p>

                ) : items.length === 0 ? (
                    <div className="rounded-2x1 bg-slate-50 p-6 text-center text-slate-500">
                        No study items found.
                    </div>

                ) : (
                    items.map((item) => (
                        <div
                            key={item.item_id}
                            className="rounded-2x1 border border-slate-100 bg-slate-50/80 p-4"
                        >
                            {editingId === item.item_id ? (
                                <div className="grid gap-3">
                                    <div className="grid gap-3 sm:grid-cols-2">
                                        <input
                                            name="subject"
                                            value={editForm.subject}
                                            onChange={handleEditChange}
                                            className="rounded2x1 border border-slate-200 bg-white px-4 py-3 text-slate-700 outline-none"
                                        />
                                        <input
                                            name="topic"
                                            value={editForm.topic}
                                            onChange={handleEditChange}
                                            className="rounded-2x1 border border-slate-200 bg-white px-4 py-3 text-slate-700 outline-none"
                                        />
                                    </div>
                                    <input
                                        name="question"
                                        value={editForm.question}
                                        onChange={handleEditChange}
                                        className="rounded-2x1 border border-slate-200 bg-white px-4 py-3 text-slate-700 outline-none"
                                    />
                                    <textarea
                                        name="answer"
                                        value={editForm.answer}
                                        onChange={handleEditChange}
                                        rows="4"
                                        className="rounded-2x1 border border-slate-200 bg-white px-4 py-3 text-slate-700 outline-none"
                                    />
                                    <select
                                        name="difficulty"
                                        value={editForm.difficulty}
                                        onChange={handleEditChange}
                                        className="w-fit rounded-2x1 border border-slate-200 bg-white px-4 py-3 text-slate-700 outline-none"
                                    >
                                        <option value={1}>1</option>
                                        <option value={2}>2</option>
                                        <option value={3}>3</option>
                                    </select>
                                    <div className="flex flex-wrap gap-3">
                                        <button
                                            type="button"
                                            onClick={() => handleEditSubmit(item.item_id)}
                                            className="rounded-2x1 bg-pink-300 px-5 py-3 font-medium text-slate-800 shadow-sm transition hover:bg-pink-400"
                                        >
                                            Save
                                        </button>
                                        <button
                                            type="button"
                                            onClick={cancelEditing}
                                            className="rounded-2x1 border border-slate-200 bg-white px-5 py-3 font-medium text-slate-700 transition hover:bg-slate-100"
                                        >
                                            Cancel
                                        </button>
                                    </div>
                                </div>
                            ) : (
                                <>
                                    <div className="flex items-start justify-between gap-4">
                                        <div>
                                            <p className="text-sm font-medium text-sky-400">{item.subject}</p>
                                            <p className="text-sm text-slate-400">{item.topic}</p>
                                        </div>

                                        <div className="rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-sky-500">
                                            Difficulty {item.difficulty}
                                        </div>
                                    </div>
                                    <p className="mt-4 text-lg font-semibold text-slate-800">
                                        {item.question}
                                    </p>
                                    <p className="mt-2 text-slate-600">{item.answer}</p>
                                    <div className="mt-4 flex flex-wrap gap-3">
                                        <button
                                            type="button"
                                            onClick={() => startEditing(item)}
                                            className="rounded-2x1 border border-sky-200 bg-white px-4 py-2 font-medium text-sky-500 transition hover:bg-sky-50"
                                        >
                                            Edit
                                        </button>
                                        <button
                                            type="button"
                                            onClick={() => handleDelete(item.item_id)}
                                            className="rounded-2x1 border border-pink-200 bg-white px-4 py-2 font-medium text-pink-500 transition hover:bg-pink-50"
                                        >
                                            Delete
                                        </button>
                                    </div>
                                </>
                            )}
                        </div>
                    ))
                )}
            </div>
        </section>
    );
}
export default StudyItemsManager;