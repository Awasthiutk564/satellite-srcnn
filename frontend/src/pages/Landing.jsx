import { Link, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Sparkles, Layers, Image as ImageIcon, Zap, ChevronRight, CheckCircle2, Globe, Shield } from 'lucide-react';

export default function Landing() {
    const { user } = useAuth();

    if (user) {
        return <Navigate to="/dashboard" />;
    }

    return (
        <div className="flex-1 overflow-x-hidden">
            {/* Hero Section */}
            <section className="relative min-h-[90vh] flex flex-col justify-center items-center py-20 px-4 text-center overflow-hidden">
                {/* Background Blobs */}
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full -z-10 bg-background">
                    <div className="absolute top-20 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-[120px] animate-pulse" />
                    <div className="absolute bottom-20 right-1/4 w-96 h-96 bg-accent/20 rounded-full blur-[120px] animate-pulse delay-700" />
                </div>

                <div className="max-w-5xl mx-auto space-y-10 relative z-10">
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glassmorphism text-sm font-semibold text-primary mb-2 shadow-xl shadow-primary/10">
                        <Sparkles className="w-4 h-4" />
                        <span className="tracking-wide uppercase">Next-Gen Satellite Intelligence</span>
                    </div>

                    <h1 className="text-6xl md:text-8xl font-black tracking-tighter text-white leading-[1.1] drop-shadow-2xl">
                        Unblur the <br />
                        <span className="text-gradient">Final Frontier.</span>
                    </h1>

                    <p className="text-xl md:text-2xl text-gray-400 max-w-3xl mx-auto leading-relaxed font-medium">
                        Transform low-resolution orbital captures into high-fidelity intelligence using state-of-the-art
                        <span className="text-white"> SRCNN Deep Learning</span>. Designed for clarity, speed, and precision.
                    </p>

                    <div className="pt-10 flex flex-col sm:flex-row gap-6 justify-center items-center">
                        <Link
                            to="/register"
                            className="group flex items-center gap-3 bg-primary hover:bg-primary-hover text-white px-10 py-5 rounded-2xl font-black text-xl transition-all shadow-2xl shadow-primary/30 hover:shadow-primary/50 hover:-translate-y-1"
                        >
                            Get Started Now <ChevronRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
                        </Link>
                        <a href="#features" className="text-gray-300 hover:text-white font-bold text-lg transition-colors py-4">
                            Explore Capabilities
                        </a>
                    </div>
                </div>

                {/* Dashboard Preview Mockup */}
                <div className="mt-20 max-w-5xl mx-auto w-full px-4 transform translate-y-10">
                    <div className="glassmorphism rounded-t-3xl border-b-0 p-2 shadow-2xl overflow-hidden aspect-[16/9] relative">
                        <div className="absolute inset-0 bg-gradient-to-t from-background via-transparent to-transparent z-10" />
                        <img
                            src="https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?auto=format&fit=crop&q=80&w=2000"
                            alt="Satellite Preview"
                            className="w-full h-full object-cover rounded-2xl opacity-60"
                        />
                        <div className="absolute inset-0 flex items-center justify-center z-20">
                            <div className="glassmorphism p-8 rounded-3xl border-white/20 scale-110">
                                <Zap className="w-16 h-16 text-primary animate-bounce" />
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section id="features" className="py-32 px-4 bg-background/50">
                <div className="max-w-7xl mx-auto">
                    <div className="text-center mb-20 space-y-4">
                        <h2 className="text-4xl md:text-5xl font-bold text-white">Advanced Processing Suite</h2>
                        <p className="text-gray-400 max-w-2xl mx-auto">Everything you need to analyze and enhance satellite patches with military-grade precision.</p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-8">
                        <div className="glassmorphism p-10 rounded-[32px] border-white/5 hover:border-primary/30 transition-all hover:-translate-y-2 group">
                            <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mb-8 group-hover:scale-110 transition-transform">
                                <Layers className="w-8 h-8 text-primary" />
                            </div>
                            <h3 className="text-2xl font-bold text-white mb-4">SRCNN Core</h3>
                            <p className="text-gray-400 leading-relaxed">A specialized 3-layer Convolutional Neural Network that learns the mapping between low and high resolution patches.</p>
                        </div>

                        <div className="glassmorphism p-10 rounded-[32px] border-white/5 hover:border-accent/30 transition-all hover:-translate-y-2 group">
                            <div className="w-16 h-16 bg-accent/10 rounded-2xl flex items-center justify-center mb-8 group-hover:scale-110 transition-transform">
                                <ImageIcon className="w-8 h-8 text-accent" />
                            </div>
                            <h3 className="text-2xl font-bold text-white mb-4">Metric Analysis</h3>
                            <p className="text-gray-400 leading-relaxed">Objective quality assessment using PSNR, SSIM, and MSE metrics to ensure data integrity across all upscales.</p>
                        </div>

                        <div className="glassmorphism p-10 rounded-[32px] border-white/5 hover:border-purple-500/30 transition-all hover:-translate-y-2 group">
                            <div className="w-16 h-16 bg-purple-500/10 rounded-2xl flex items-center justify-center mb-8 group-hover:scale-110 transition-transform">
                                <Globe className="w-8 h-8 text-purple-400" />
                            </div>
                            <h3 className="text-2xl font-bold text-white mb-4">Global Standards</h3>
                            <p className="text-gray-400 leading-relaxed">Compatible with standard satellite image formats and optimized for land-use classification imagery.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* How it Works */}
            <section className="py-32 px-4 relative overflow-hidden">
                <div className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-20 items-center">
                    <div className="space-y-8">
                        <h2 className="text-4xl md:text-6xl font-black text-white leading-tight">Simplified Workflow. <br />Powerful Results.</h2>
                        <div className="space-y-6">
                            {[
                                { title: "Step 1: Upload", desc: "Drag and drop your low-res satellite image patches into our secure vault." },
                                { title: "Step 2: Configure", desc: "Select between Bicubic or SRCNN models with up to 4x scaling factors." },
                                { title: "Step 3: Analyze", desc: "Instant inference with real-time performance metrics and side-by-side comparison." }
                            ].map((step, i) => (
                                <div key={i} className="flex gap-4">
                                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold">
                                        {i + 1}
                                    </div>
                                    <div>
                                        <h4 className="text-white font-bold text-lg">{step.title}</h4>
                                        <p className="text-gray-400">{step.desc}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="glassmorphism p-8 rounded-[40px] border-white/10 relative">
                        <div className="absolute -top-10 -right-10 w-40 h-40 bg-accent/20 rounded-full blur-3xl" />
                        <div className="space-y-4">
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-sm font-bold text-primary flex items-center gap-2">
                                    <CheckCircle2 className="w-4 h-4" /> AUTO_ENHANCE_ACTIVE
                                </span>
                                <span className="text-xs text-gray-500 font-mono">STATION_ID: ALPHA-09</span>
                            </div>
                            <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                                <div className="bg-primary h-full w-[85%] animate-[loading_2s_ease-in-out_infinite]" />
                            </div>
                            <div className="grid grid-cols-2 gap-4 pt-4">
                                <div className="bg-white/5 p-4 rounded-2xl border border-white/5">
                                    <div className="text-[10px] uppercase tracking-widest text-gray-500 mb-1">Inference Latency</div>
                                    <div className="text-xl font-bold text-white">42ms</div>
                                </div>
                                <div className="bg-white/5 p-4 rounded-2xl border border-white/5">
                                    <div className="text-[10px] uppercase tracking-widest text-gray-500 mb-1">Avg. PSNR</div>
                                    <div className="text-xl font-bold text-accent">34.82 dB</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA */}
            <section className="py-32 px-4 text-center">
                <div className="max-w-4xl mx-auto glassmorphism p-16 rounded-[48px] border-white/10 relative overflow-hidden">
                    <div className="absolute inset-0 bg-primary/5 -z-10" />
                    <h2 className="text-4xl md:text-5xl font-black text-white mb-6">Ready to see the earth in HD?</h2>
                    <p className="text-gray-400 text-lg mb-10 max-w-xl mx-auto">Join researchers and analysts worldwide using SatEnhance AI for clearer perspectives.</p>
                    <Link
                        to="/register"
                        className="inline-flex items-center gap-2 bg-white text-gray-900 px-10 py-5 rounded-2xl font-black text-xl hover:bg-gray-200 transition-all shadow-xl shadow-white/10"
                    >
                        Create Free Account <Shield className="w-6 h-6" />
                    </Link>
                </div>
            </section>
        </div>
    );
}
