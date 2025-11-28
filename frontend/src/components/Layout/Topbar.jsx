import React from "react";
import { Bell, Search, User } from "lucide-react";

const Topbar = () => {
  return (
    <header className="h-16 bg-slate-900/50 backdrop-blur-md border-b border-slate-800 flex items-center justify-between px-6 sticky top-0 z-10 ml-64">
      <div className="flex items-center gap-4">
        <h2 className="text-lg font-semibold text-slate-100">
          Dashboard Overview
        </h2>
      </div>

      <div className="flex items-center gap-4">
        <div className="relative">
          <Search
            className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"
            size={18}
          />
          <input
            type="text"
            placeholder="Search threats, IPs..."
            className="bg-slate-950 border border-slate-800 rounded-full pl-10 pr-4 py-1.5 text-sm text-slate-200 focus:outline-none focus:border-blue-500 w-64"
          />
        </div>

        <button className="relative p-2 text-slate-400 hover:text-slate-200 transition-colors">
          <Bell size={20} />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>
      </div>
    </header>
  );
};

export default Topbar;
