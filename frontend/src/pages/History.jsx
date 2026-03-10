import { useState, useEffect } from 'react';
import api from '../services/api';
import { History as HistoryIcon, Clock, Activity, Zap } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function History() {
    const [images, setImages] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const res = await api.get('/images/');
                // We'll map each image to row items for all of its results
                const items = [];
                for (const img of res.data) {
                    try {
                        const detailRes = await api.get(`/images/${img.id}`);
                        const detail = detailRes.data;
                        if (detail.results && detail.results.length > 0) {
                            for (const r of detail.results) {
                                items.push({
                                    image: detail,
                                    result: r,
                                });
                            }
                        }
                    } catch (e) {
                        console.error("Failed fetching detail for", img.id, e);
                    }
                }

                // Sort by created_at desc
                items.sort((a, b) => new Date(b.result.created_at) - new Date(a.result.created_at));
                setImages(items);
            } catch (err) {
                console.error('Failed to load history', err);
            } finally {
                setLoading(false);
            }
        };
        fetchHistory();
    }, []);

    const handleClick = (item) => {
        // Reconstruct required payload for Results.jsx state
        const data = {
            result: item.result,
            original_image_url: `/files/${item.image.storage_path}`,
            enhanced_image_url: `/files/${item.result.output_path}`,
        };
        navigate(`/results/${item.result.id}`, { state: { resultData: data } });
    };

    return (
        <div className="flex-1 max-w-5xl mx-auto w-full px-4 py-12">
            <div className="flex items-center gap-3 mb-8">
                <div className="p-3 bg-white/5 rounded-xl border border-white/10">
                    <HistoryIcon className="w-6 h-6 text-primary" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold text-white">Enhancement History</h1>
                    <p className="text-gray-400">View all your past satellite image upscales.</p>
                </div>
            </div>

            <div className="glassmorphism rounded-3xl overflow-hidden border border-white/10 shadow-xl">
                {loading ? (
                    <div className="p-12 text-center text-gray-400 animate-pulse">
                        Loading your history...
                    </div>
                ) : images.length === 0 ? (
                    <div className="p-12 text-center text-gray-500">
                        No enhancements found. Go to the dashboard to process an image!
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr className="bg-white/5 border-b border-white/10 text-gray-400 text-sm">
                                    <th className="p-4 font-medium">Date</th>
                                    <th className="p-4 font-medium">Model</th>
                                    <th className="p-4 font-medium">Scale</th>
                                    <th className="p-4 font-medium">Metrics</th>
                                    <th className="p-4 font-medium text-right">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {images.map((item, i) => (
                                    <tr
                                        key={`${item.image.id}-${item.result.id}-${i}`}
                                        className="border-b border-white/5 hover:bg-white/5 transition-colors group cursor-pointer"
                                        onClick={() => handleClick(item)}
                                    >
                                        <td className="p-4 text-gray-300">
                                            <div className="flex items-center gap-2">
                                                <Clock className="w-4 h-4 text-gray-500" />
                                                {new Date(item.result.created_at).toLocaleDateString()}
                                            </div>
                                        </td>
                                        <td className="p-4">
                                            <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border ${item.result.model_type === 'srcnn'
                                                    ? 'bg-accent/10 text-accent border-accent/20'
                                                    : 'bg-primary/10 text-primary border-primary/20'
                                                }`}>
                                                {item.result.model_type.toUpperCase()}
                                            </span>
                                        </td>
                                        <td className="p-4 text-gray-300">{item.result.scale_factor}x</td>
                                        <td className="p-4">
                                            <div className="flex flex-col gap-1 text-xs">
                                                <span className="text-gray-400">PSNR: <span className="text-white">{item.result.psnr.toFixed(2)} dB</span></span>
                                                <span className="text-gray-400">SSIM: <span className="text-white">{item.result.ssim.toFixed(4)}</span></span>
                                            </div>
                                        </td>
                                        <td className="p-4 text-right">
                                            <button className="text-sm text-primary hover:text-white font-medium transition-colors opacity-0 group-hover:opacity-100">
                                                View Result &rarr;
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
}
