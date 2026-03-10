import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Satellite, Lock, Mail, User, ArrowRight } from 'lucide-react';

export default function Register() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [fullName, setFullName] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { register } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            await register(email, password, fullName);
            navigate('/dashboard');
        } catch (err) {
            setError(err.response?.data?.detail || 'Registration failed.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex-1 flex justify-center items-center px-4 py-12">
            <div className="max-w-md w-full glassmorphism p-8 rounded-3xl shadow-2xl relative overflow-hidden">
                <h2 className="text-3xl font-bold text-white mb-6 text-center">Create Account</h2>
                <form onSubmit={handleSubmit} className="space-y-6">
                    {error && <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-3 rounded-lg text-sm">{error}</div>}
                    <div className="space-y-4">
                        <input type="text" required value={fullName} onChange={(e) => setFullName(e.target.value)} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-4 text-white" placeholder="Full Name" />
                        <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-4 text-white" placeholder="Email" />
                        <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-4 text-white" placeholder="Password" minLength={6} />
                    </div>
                    <button type="submit" disabled={loading} className="w-full bg-accent hover:bg-cyan-400 text-gray-900 py-4 rounded-xl font-bold">
                        {loading ? 'Creating Account...' : 'Register'}
                    </button>
                </form>
                <p className="text-center mt-8 text-gray-400">Already have an account? <Link to="/login" className="text-accent hover:text-cyan-300 font-medium">Log in instead</Link></p>
            </div>
        </div>
    );
}
