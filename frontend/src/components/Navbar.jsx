import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Satellite, LogOut, User as UserIcon } from 'lucide-react';

export default function Navbar() {
    const { user, logout } = useAuth();

    return (
        <nav className="border-b border-white/10 glassmorphism sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    <Link to={user ? "/dashboard" : "/"} className="flex items-center gap-2 group">
                        <Satellite className="w-8 h-8 text-primary group-hover:text-primary-hover transition-colors" />
                        <span className="font-bold text-xl tracking-tight text-white">
                            SatEnhance <span className="text-primary text-gradient">AI</span>
                        </span>
                    </Link>

                    <div className="flex items-center gap-4">
                        {user ? (
                            <>
                                <Link to="/history" className="text-gray-300 hover:text-white transition-colors">
                                    History
                                </Link>
                                <div className="h-6 w-px bg-white/20 mx-2"></div>
                                <div className="flex items-center gap-2 text-sm text-gray-400">
                                    <UserIcon className="w-4 h-4" />
                                    <span className="hidden sm:inline">{user.full_name || user.email}</span>
                                </div>
                                <button
                                    onClick={logout}
                                    className="ml-4 p-2 text-gray-400 hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-all"
                                    title="Logout"
                                >
                                    <LogOut className="w-5 h-5" />
                                </button>
                            </>
                        ) : (
                            <>
                                <Link to="/login" className="text-gray-300 hover:text-white font-medium transition-colors">
                                    Log in
                                </Link>
                                <Link
                                    to="/register"
                                    className="bg-primary hover:bg-primary-hover text-white px-4 py-2 rounded-lg font-medium transition-colors"
                                >
                                    Get Started
                                </Link>
                            </>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
}
