import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Satellite, Lock, Mail, ArrowRight } from 'lucide-react';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            await login(email, password);
            navigate('/dashboard');
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to login.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex-1 flex justify-center items-center px-4">
            <div className="max-w-md w-full glassmorphism p-8 rounded-3xl shadow-2xl relative overflow-hidden">
                <div className="text-center mb-10">
                    <div className="inline-flex justify-center items-center w-16 h-16 rounded-full bg-white/5 border border-white/10 mb-4 shadow-xl">
                        <Satellite className="w-8 h-8 text-primary" />
                    </div>
                    <h2 className="text-3xl font-bold text-white mb-2">Welcome Back</h2>
                </div>
                <form onSubmit={handleSubmit} className="space-y-6">
                    {error && <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-3 rounded-lg text-sm text-center">{error}</div>}
                    <div className="space-y-4">
                        <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-4 text-white" placeholder="Email" />
                        <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-4 text-white" placeholder="Password" />
                    </div>
                    <button type="submit" disabled={loading} className="w-full bg-primary hover:bg-primary-hover text-white py-4 rounded-xl font-bold flex items-center justify-center gap-2">
                        {loading ? 'Authenticating...' : 'Sign In'} <ArrowRight className="w-5 h-5" />
                    </button>
                </form>
                <p className="text-center mt-8 text-gray-400">Need an account? <Link to="/register" className="text-primary hover:text-white font-medium">Create one now</Link></p>
            </div>
        </div>
    );
}
