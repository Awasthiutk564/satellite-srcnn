import { useState, useEffect } from 'react';
import api from '../services/api';
import { History as HistoryIcon, Clock } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function History() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        (async () => {
            try {
                const res = await api.get('/images/');
                const allItems = [];
                for (const img of res.data) {
                    const detail = (await api.get(`/images/${img.id}`)).data;
                    detail.results?.forEach(r => allItems.push({ image: detail, result: r }));
                }
                setItems(allItems.sort((a, b) => new Date(b.result.created_at) - new Date(a.result.created_at)));
            } catch (e) { console.error(e); } finally { setLoading(false); }
        })();
    }, []);

    return (
        <div className="flex-1 max-w-5xl mx-auto w-full px-4 py-12">
            <h1 className="text-3xl font-bold text-white mb-8 flex items-center gap-2"><HistoryIcon /> History</h1>
            <div className="glassmorphism rounded-3xl overflow-hidden">
                {loading ? <div className="p-12 text-center text-gray-400">Loading...</div> :
                    <table className="w-full text-left">
                        <thead className="bg-white/5 border-b border-white/10">
                            <tr><th className="p-4">Date</th><th className="p-4">Model</th><th className="p-4">Scale</th><th className="p-4">Action</th></tr>
                        </thead>
                        <tbody>
                            {items.map((item, i) => (
                                <tr key={i} className="border-b border-white/5 hover:bg-white/5 cursor-pointer" onClick={() => navigate(`/results/${item.result.id}`, { state: { resultData: { result: item.result, original_image_url: `/files/${item.image.storage_path}`, enhanced_image_url: `/files/${item.result.output_path}` } } })}>
                                    <td className="p-4 text-sm text-gray-400">{new Date(item.result.created_at).toLocaleDateString()}</td>
                                    <td className="p-4"><span className="px-2 py-0.5 rounded-full text-xs bg-primary/20 text-primary">{item.result.model_type}</span></td>
                                    <td className="p-4 text-sm">{item.result.scale_factor}x</td>
                                    <td className="p-4 text-sm text-primary">View &rarr;</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                }
            </div>
        </div>
    );
}
