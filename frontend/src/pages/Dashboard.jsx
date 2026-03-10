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

    const handleDragOver = useCallback((e) => {
        e.preventDefault();
    }, []);

    const handleDrop = useCallback((e) => {
        e.preventDefault();
        const droppedFile = e.dataTransfer.files[0];
        if (droppedFile && droppedFile.type.startsWith('image/')) {
            setFile(droppedFile);
            setPreview(URL.createObjectURL(droppedFile));
        }
    }, []);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            setPreview(URL.createObjectURL(selectedFile));
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) {
            setError('Please upload an image first.');
            return;
        }

        setLoading(true);
        setError('');

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
            setError(err.response?.data?.detail || 'An error occurred during enhancement.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex-1 max-w-4xl mx-auto w-full px-4 py-12">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-white mb-2">Enhance Imagery</h1>
                <p className="text-gray-400">Upload a low-resolution satellite image patch to see SRCNN upscaling in action.</p>
            </div>

            <div className="glassmorphism rounded-3xl p-8 shadow-2xl">
                {error && (
                    <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl mb-6">
                        {typeof error === 'string' ? error : JSON.stringify(error)}
                    </div>
                )}

                <div className="grid md:grid-cols-2 gap-8">
                    {/* Upload Section */}
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">Input Image</label>
                        <div
                            onDragOver={handleDragOver}
                            onDrop={handleDrop}
                            className={`border-2 border-dashed rounded-2xl p-8 text-center h-64 flex flex-col items-center justify-center transition-all ${preview ? 'border-primary/50 bg-primary/5' : 'border-gray-600 hover:border-primary/50 hover:bg-white/5'
                                }`}
                        >
                            {preview ? (
                                <div className="relative w-full h-full">
                                    <img src={preview} alt="Upload preview" className="object-contain w-full h-full rounded-lg" />
                                    <button
                                        type="button"
                                        onClick={() => { setFile(null); setPreview(null); }}
                                        className="absolute top-2 right-2 bg-black/50 text-white p-1 rounded hover:bg-red-500/80 transition-colors"
                                    >
                                        ×
                                    </button>
                                </div>
                            ) : (
                                <>
                                    <UploadCloud className="w-12 h-12 text-gray-400 mb-4" />
                                    <p className="text-gray-300 font-medium mb-1">Drag and drop your image</p>
                                    <p className="text-sm text-gray-500 mb-4">PNG, JPG up to 10MB</p>
                                    <label className="bg-white/10 hover:bg-white/20 text-white px-4 py-2 rounded-lg cursor-pointer transition-colors text-sm font-medium">
                                        Browse Files
                                        <input type="file" className="hidden" accept="image/*" onChange={handleFileChange} />
                                    </label>
                                </>
                            )}
                        </div>
                    </div>

                    {/* Settings Section */}
                    <div className="flex flex-col">
                        <div className="space-y-6 flex-1">
                            <div>
                                <label className="block text-sm font-medium text-gray-300 mb-3">Model Type</label>
                                <div className="grid grid-cols-2 gap-3">
                                    <button
                                        type="button"
                                        onClick={() => setModelType('bicubic')}
                                        className={`flex items-center gap-2 p-3 rounded-xl border transition-all ${modelType === 'bicubic'
                                                ? 'border-primary bg-primary/10 text-white'
                                                : 'border-white/10 text-gray-400 hover:bg-white/5'
                                            }`}
                                    >
                                        <ImageIcon className="w-5 h-5" /> Bicubic (Baseline)
                                    </button>
                                    <button
                                        type="button"
                                        onClick={() => setModelType('srcnn')}
                                        className={`flex items-center gap-2 p-3 rounded-xl border transition-all ${modelType === 'srcnn'
                                                ? 'border-accent bg-accent/10 text-white'
                                                : 'border-white/10 text-gray-400 hover:bg-white/5'
                                            }`}
                                    >
                                        <Cpu className="w-5 h-5" /> SRCNN (AI)
                                    </button>
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-300 mb-3">Scale Factor</label>
                                <div className="grid grid-cols-3 gap-3">
                                    {[2, 3, 4].map((scale) => (
                                        <button
                                            key={scale}
                                            type="button"
                                            onClick={() => setScaleFactor(scale)}
                                            className={`py-3 rounded-xl border text-center font-medium transition-all ${scaleFactor === scale
                                                    ? 'border-primary bg-primary/10 text-white'
                                                    : 'border-white/10 text-gray-400 hover:bg-white/5'
                                                }`}
                                        >
                                            {scale}x
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>

                        <button
                            onClick={handleSubmit}
                            disabled={loading || !file}
                            className="mt-8 w-full bg-primary hover:bg-primary-hover text-white py-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all disabled:opacity-50"
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="w-5 h-5 animate-spin" /> Processing Image...
                                </>
                            ) : (
                                <>Enhance Image</>
                            )}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
