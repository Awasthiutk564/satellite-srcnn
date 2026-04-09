import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Satellite, Lock, Mail, User, ArrowRight, Eye, EyeOff, CheckCircle2 } from 'lucide-react';

const getFirebaseErrorMessage = (code) => {
    switch (code) {
        case 'auth/email-already-in-use':
            return 'An account with this email already exists.';
        case 'auth/weak-password':
            return 'Password must be at least 6 characters long.';
        case 'auth/invalid-email':
            return 'Please enter a valid email address.';
        case 'auth/operation-not-allowed':
            return 'Email/password sign-up is not enabled.';
        case 'auth/network-request-failed':
            return 'Network error. Check your connection.';
        default:
            return 'Registration failed. Please try again.';
    }
};

export default function Register() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [fullName, setFullName] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { register } = useAuth();
    const navigate = useNavigate();

    const passwordStrength = () => {
        if (password.length === 0) return { level: 0, label: '', color: '' };
        if (password.length < 6) return { level: 1, label: 'Too short', color: 'bg-red-500' };
        if (password.length < 8) return { level: 2, label: 'Weak', color: 'bg-orange-500' };
        const hasUpper = /[A-Z]/.test(password);
        const hasNumber = /[0-9]/.test(password);
        const hasSpecial = /[^A-Za-z0-9]/.test(password);
        const score = [hasUpper, hasNumber, hasSpecial].filter(Boolean).length;
        if (score >= 2) return { level: 4, label: 'Strong', color: 'bg-green-500' };
        return { level: 3, label: 'Fair', color: 'bg-yellow-500' };
    };

    const strength = passwordStrength();

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (password.length < 6) {
            setError('Password must be at least 6 characters long.');
            return;
        }
        setLoading(true);
        setError('');
        try {
            await register(email, password, fullName);
            navigate('/dashboard');
        } catch (err) {
            setError(getFirebaseErrorMessage(err.code));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex-1 flex justify-center items-center px-4 py-12">
            <div className="max-w-md w-full glassmorphism p-8 rounded-3xl shadow-2xl relative overflow-hidden">
                <div className="absolute top-0 left-0 w-64 h-64 bg-accent/10 rounded-full blur-3xl -translate-y-1/2 -translate-x-1/2" />
                <div className="absolute bottom-0 right-0 w-48 h-48 bg-purple-500/10 rounded-full blur-3xl translate-y-1/2 translate-x-1/2" />

                <div className="relative z-10">
                    <div className="text-center mb-10">
                        <div className="inline-flex justify-center items-center w-16 h-16 rounded-full bg-white/5 border border-white/10 mb-4 shadow-xl">
                            <Satellite className="w-8 h-8 text-accent" />
                        </div>
                        <h2 className="text-3xl font-bold text-white mb-2">Create Account</h2>
                        <p className="text-gray-400">Start processing high-res satellite imagery</p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-6">
                        {error && (
                            <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-3 rounded-lg text-sm text-center animate-[shake_0.5s_ease-in-out]">
                                {error}
                            </div>
                        )}

                        <div className="space-y-4">
                            <div className="relative group">
                                <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500 group-focus-within:text-accent transition-colors" />
                                <input
                                    id="register-fullname"
                                    type="text"
                                    required
                                    value={fullName}
                                    onChange={(e) => setFullName(e.target.value)}
                                    className="w-full bg-white/5 border border-white/10 rounded-xl px-11 py-4 text-white placeholder-gray-500 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-all"
                                    placeholder="Full Name"
                                />
                            </div>

                            <div className="relative group">
                                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500 group-focus-within:text-accent transition-colors" />
                                <input
                                    id="register-email"
                                    type="email"
                                    required
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full bg-white/5 border border-white/10 rounded-xl px-11 py-4 text-white placeholder-gray-500 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-all"
                                    placeholder="Email address"
                                />
                            </div>

                            <div className="relative group">
                                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500 group-focus-within:text-accent transition-colors" />
                                <input
                                    id="register-password"
                                    type={showPassword ? 'text' : 'password'}
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="w-full bg-white/5 border border-white/10 rounded-xl px-11 py-4 pr-12 text-white placeholder-gray-500 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-all"
                                    placeholder="Password (min 6 chars)"
                                    minLength={6}
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white transition-colors"
                                >
                                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                                </button>
                            </div>

                            {/* Password Strength Indicator */}
                            {password.length > 0 && (
                                <div className="space-y-2 px-1">
                                    <div className="flex gap-1.5">
                                        {[1, 2, 3, 4].map((i) => (
                                            <div
                                                key={i}
                                                className={`h-1.5 flex-1 rounded-full transition-all duration-300 ${
                                                    i <= strength.level ? strength.color : 'bg-white/10'
                                                }`}
                                            />
                                        ))}
                                    </div>
                                    <p className={`text-xs font-medium ${
                                        strength.level <= 1 ? 'text-red-400' :
                                        strength.level <= 2 ? 'text-orange-400' :
                                        strength.level <= 3 ? 'text-yellow-400' :
                                        'text-green-400'
                                    }`}>
                                        {strength.label}
                                    </p>
                                </div>
                            )}
                        </div>

                        {/* Requirements Checklist */}
                        <div className="space-y-2 px-1">
                            {[
                                { met: password.length >= 6, text: 'At least 6 characters' },
                                { met: /[A-Z]/.test(password), text: 'One uppercase letter' },
                                { met: /[0-9]/.test(password), text: 'One number' },
                            ].map((req, i) => (
                                <div key={i} className={`flex items-center gap-2 text-xs transition-colors ${req.met ? 'text-green-400' : 'text-gray-500'}`}>
                                    <CheckCircle2 className={`w-3.5 h-3.5 transition-all ${req.met ? 'scale-100' : 'scale-90 opacity-50'}`} />
                                    {req.text}
                                </div>
                            ))}
                        </div>

                        <button
                            id="register-submit"
                            type="submit"
                            disabled={loading}
                            className="w-full bg-accent hover:bg-cyan-400 text-gray-900 py-4 rounded-xl font-bold flex items-center justify-center gap-2 group transition-all disabled:opacity-50"
                        >
                            {loading ? (
                                <span className="flex items-center gap-2">
                                    <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                    </svg>
                                    Creating Account...
                                </span>
                            ) : (
                                <>
                                    Register
                                    <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                                </>
                            )}
                        </button>
                    </form>

                    <p className="text-center mt-8 text-gray-400">
                        Already have an account?{' '}
                        <Link to="/login" className="text-accent hover:text-cyan-300 font-medium transition-colors">
                            Log in instead
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}
