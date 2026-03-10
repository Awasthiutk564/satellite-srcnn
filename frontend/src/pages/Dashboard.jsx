import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { UploadCloud, Image as ImageIcon, Cpu, Loader2 } from 'lucide-react';
import api from '../services/api';

export default function Dashboard() {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [modelType, setModelType] = useState('srcnn');
    const [scaleFactor, setScaleFactor] = useState(2);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            setPreview(URL.createObjectURL(selectedFile));
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) { setError('Please upload an image.'); return; }
        setLoading(true); setError('');
        const formData = new FormData();
        formData.append('file', file);
        formData.append('model_type', modelType);
        formData.append('scale_factor', scaleFactor);

        try {
            const res = await api.post('/enhance/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            navigate(`/results/${res.data.result.id}`, { state: { resultData: res.data } });
        } catch (err) {
            setError(err.response?.data?.detail || 'An error occurred.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex-1 max-w-4xl mx-auto w-full px-4 py-12">
            <h1 className="text-3xl font-bold text-white mb-8">Enhance Imagery</h1>
            <div className="glassmorphism rounded-3xl p-8 shadow-2xl overflow-hidden">
                {error && <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl mb-6">{error}</div>}
                <div className="grid md:grid-cols-2 gap-8">
                    <div className="border-2 border-dashed rounded-2xl p-8 text-center h-64 flex flex-col items-center justify-center border-gray-600">
                        {preview ? <img src={preview} className="object-contain w-full h-full" /> :
                            <label className="cursor-pointer">
                                <UploadCloud className="w-12 h-12 text-gray-400 mx-auto" />
                                <span className="text-gray-300 block mt-2">Click to Upload</span>
                                <input type="file" className="hidden" accept="image/*" onChange={handleFileChange} />
                            </label>
                        }
                    </div>
                    <div className="space-y-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-2">Model</label>
                            <div className="grid grid-cols-2 gap-2">
                                <button onClick={() => setModelType('bicubic')} className={`p-2 rounded-lg border ${modelType === 'bicubic' ? 'border-primary bg-primary/20' : 'border-white/10'}`}>Bicubic</button>
                                <button onClick={() => setModelType('srcnn')} className={`p-2 rounded-lg border ${modelType === 'srcnn' ? 'border-accent bg-accent/20' : 'border-white/10'}`}>SRCNN</button>
                            </div>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-2">Scale</label>
                            <div className="grid grid-cols-3 gap-2">
                                {[2, 3, 4].map(s => <button key={s} onClick={() => setScaleFactor(s)} className={`p-2 rounded-lg border ${scaleFactor === s ? 'border-primary bg-primary/20' : 'border-white/10'}`}>{s}x</button>)}
                            </div>
                        </div>
                        <button onClick={handleSubmit} disabled={loading || !file} className="w-full bg-primary py-4 rounded-xl font-bold flex justify-center items-center gap-2">
                            {loading ? <Loader2 className="animate-spin" /> : 'Enhance'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
