import { useState, useEffect } from 'react';
import { useLocation, useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Download, Image as ImageIcon, Zap, Activity } from 'lucide-react';

export default function Results() {
    const { id } = useParams();
    const location = useLocation();
    const navigate = useNavigate();
    const [data, setData] = useState(location.state?.resultData || null);

    const API_URL = 'http://localhost:8000';

    useEffect(() => {
        // If we land here without state, we'd normally fetch the result by ID.
        // Since our backend returns it in the upload, we just use local state for simplicity.
        if (!data) {
            navigate('/history');
        }
    }, [data, navigate]);

    if (!data) return null;

    const { result, original_image_url, enhanced_image_url } = data;

    const handleDownload = async () => {
        try {
            const response = await fetch(`${API_URL}${enhanced_image_url}`);
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `enhanced_${result.model_type}_x${result.scale_factor}.png`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        } catch (err) {
            console.error('Failed to download image', err);
        }
    };

    return (
        <div className="flex-1 max-w-6xl mx-auto w-full px-4 py-8">
            <button
                onClick={() => navigate('/dashboard')}
                className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors mb-8"
            >
                <ArrowLeft className="w-4 h-4" /> Back to Dashboard
            </button>

            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                        Enhancement Results
                        <span className="px-3 py-1 bg-white/10 rounded-full text-sm font-medium text-primary border border-white/10">
                            {result.model_type.toUpperCase()}
                        </span>
                    </h1>
                    <p className="text-gray-400 mt-2">Scale Factor: {result.scale_factor}x</p>
                </div>

                <button
                    onClick={handleDownload}
                    className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 border border-white/20 text-white rounded-lg transition-colors"
                >
                    <Download className="w-4 h-4" /> Download
                </button>
            </div>

            <div className="grid lg:grid-cols-3 gap-8 mb-8">
                {/* Images */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="grid md:grid-cols-2 gap-6">
                        <div className="space-y-3">
                            <div className="flex items-center gap-2 text-gray-300 font-medium">
                                <ImageIcon className="w-4 h-4" /> Original Image (Low Res)
                            </div>
                            <div className="glassmorphism rounded-2xl p-2 aspect-square flex items-center justify-center overflow-hidden">
                                <img
                                    src={`${API_URL}${original_image_url}`}
                                    alt="Original"
                                    className="max-w-full max-h-full object-contain"
                                    style={{ imageRendering: 'pixelated' }}
                                />
                            </div>
                        </div>

                        <div className="space-y-3">
                            <div className="flex items-center gap-2 text-gray-300 font-medium">
                                <Zap className="w-4 h-4 text-accent" /> Enhanced Image
                            </div>
                            <div className="glassmorphism rounded-2xl p-2 aspect-square flex items-center justify-center overflow-hidden border border-accent/20">
                                <img
                                    src={`${API_URL}${enhanced_image_url}`}
                                    alt="Enhanced"
                                    className="max-w-full max-h-full object-contain"
                                />
                            </div>
                        </div>
                    </div>
                </div>

                {/* Metrics Sidebar */}
                <div className="space-y-6">
                    <div className="glassmorphism rounded-2xl p-6 border border-white/5">
                        <h3 className="text-xl font-bold text-white flex items-center gap-2 mb-6">
                            <Activity className="w-5 h-5 text-primary" /> Image Metrics
                        </h3>

                        <div className="space-y-6">
                            <div className="border-b border-white/10 pb-4">
                                <p className="text-sm text-gray-400 mb-1">PSNR (Peak Signal-to-Noise Ratio)</p>
                                <p className="text-3xl font-light text-white">
                                    {result.psnr.toFixed(2)} <span className="text-xl text-gray-500">dB</span>
                                </p>
                                <div className="w-full bg-white/5 h-1.5 mt-3 rounded-full overflow-hidden">
                                    <div className="bg-primary h-full rounded-full" style={{ width: `${Math.min(result.psnr / 40 * 100, 100)}%` }} />
                                </div>
                            </div>

                            <div className="border-b border-white/10 pb-4">
                                <p className="text-sm text-gray-400 mb-1">SSIM (Structural Similarity)</p>
                                <p className="text-3xl font-light text-white">
                                    {result.ssim.toFixed(4)}
                                </p>
                                <div className="w-full bg-white/5 h-1.5 mt-3 rounded-full overflow-hidden">
                                    <div className="bg-accent h-full rounded-full" style={{ width: `${result.ssim * 100}%` }} />
                                </div>
                            </div>

                            <div>
                                <p className="text-sm text-gray-400 mb-1">MSE (Mean Squared Error)</p>
                                <p className="text-2xl font-light text-white">
                                    {result.mse.toFixed(2)}
                                </p>
                            </div>
                        </div>

                        <div className="mt-8 pt-4 border-t border-white/10">
                            <p className="text-xs text-center text-gray-500">
                                Processed in {result.processing_time_ms} ms
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
