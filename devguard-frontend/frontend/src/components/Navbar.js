// src/components/Navbar.js
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-blue-500 p-4 text-white">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-xl font-bold">DevGuard</h1>
        <div className="space-x-4">
          <a href="/" className="hover:underline">Home</a>
          <a href="/dashboard" className="hover:underline">Dashboard</a>
          <a href="/settings" className="hover:underline">Settings</a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
