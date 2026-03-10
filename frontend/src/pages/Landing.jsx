import { Link, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Sparkles, Layers, Image as ImageIcon, Zap } from 'lucide-react';

export default function Landing() {
    const { user } = useAuth();
    if (user) return <Navigate to="/dashboard" />;

    return (
        <div className="flex-1 space-gradient-bg flex flex-col justify-center items-center py-20 px-4 text-center">
            <div className="max-w-4xl mx-auto space-y-8">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full glassmorphism text-xs font-medium text-primary mb-4">
                    <Sparkles className="w-4 h-4" /> State-of-the-Art Deep Learning
                </div>
                <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-white drop-shadow-lg leading-tight">
                    Super-Resolution for <span className="block text-gradient">Satellite Imagery</span>
                </h1>
                <p className="text-xl text-gray-300 max-w-2xl mx-auto leading-relaxed">
                    Enhance low-resolution satellite patches with SRCNN. Turn blurry orbital visuals into clear, sharp intelligence instantly.
                </p>
                <div className="pt-8 flex gap-4 justify-center">
                    <Link to="/register" className="flex items-center gap-2 bg-primary hover:bg-primary-hover text-white px-8 py-4 rounded-xl font-bold text-lg transition-all shadow-lg shadow-primary/25 hover:shadow-primary/40 hover:-translate-y-0.5">
                        Start Enhancing Images <Zap className="w-5 h-5" />
                    </Link>
                </div>
            </div>
        </div>
    );
}
