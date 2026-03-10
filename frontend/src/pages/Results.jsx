import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { ArrowLeft, Download, Activity } from 'lucide-react';

export default function Results() {
    const location = useLocation();
    const navigate = useNavigate();
    const data = location.state?.resultData;
    const API_URL = 'http://localhost:8000';

    useEffect(() => { if (!data) navigate('/history'); }, [data, navigate]);
    if (!data) return null;

    const { result, original_image_url, enhanced_image_url } = data;

    return (
        <div className="flex-1 max-w-6xl mx-auto w-full px-4 py-8">
            <button onClick={() => navigate('/dashboard')} className="flex items-center gap-2 text-gray-400 mb-8">&larr; Back</button>
            <div className="grid lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 grid md:grid-cols-2 gap-6">
                    <div className="glassmorphism rounded-2xl p-4 aspect-square flex flex-col items-center">
                        <span className="text-sm text-gray-400 mb-2">Original</span>
                        <img src={`${API_URL}${original_image_url}`} style={{ imageRendering: 'pixelated' }} className="max-h-[90%] object-contain" />
                    </div>
                    <div className="glassmorphism rounded-2xl p-4 aspect-square flex flex-col items-center border-accent/20">
                        <span className="text-sm text-accent mb-2">Enhanced ({result.model_type})</span>
                        <img src={`${API_URL}${enhanced_image_url}`} className="max-h-[90%] object-contain" />
                    </div>
                </div>
                <div className="glassmorphism rounded-2xl p-6">
                    <h3 className="text-xl font-bold mb-6 flex items-center gap-2 text-primary"><Activity /> Metrics</h3>
                    <div className="space-y-4">
                        <div><p className="text-xs text-gray-400">PSNR</p><p className="text-2xl font-bold">{result.psnr.toFixed(2)} dB</p></div>
                        <div><p className="text-xs text-gray-400">SSIM</p><p className="text-2xl font-bold">{result.ssim.toFixed(4)}</p></div>
                        <div><p className="text-xs text-gray-400">MSE</p><p className="text-2xl font-bold">{result.mse.toFixed(2)}</p></div>
                        <div className="pt-4 border-t border-white/10 text-xs text-gray-500">Processed in {result.processing_time_ms}ms</div>
                    </div>
                </div>
            </div>
        </div>
    );
}
