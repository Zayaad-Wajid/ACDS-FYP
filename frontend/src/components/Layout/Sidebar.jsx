import React from "react";
import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  ShieldAlert,
  FileText,
  Settings,
  Activity,
  Lock,
} from "lucide-react";
import { cn } from "../../utils/cn";

const Sidebar = () => {
  const navItems = [
    { icon: LayoutDashboard, label: "Dashboard", path: "/" },
    { icon: ShieldAlert, label: "Email Phishing", path: "/phishing" },
    { icon: FileText, label: "Logs", path: "/logs" },
    { icon: Settings, label: "Settings", path: "/settings" },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col h-screen fixed left-0 top-0 z-10">
      <div className="p-6 border-b border-slate-800">
        <h1 className="text-xl font-bold text-blue-400 tracking-wider">ACDS</h1>
        <p className="text-xs text-slate-500 mt-1">Autonomous Cyber Defense</p>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors",
                isActive
                  ? "bg-blue-900/30 text-blue-400 border border-blue-900/50"
                  : "text-slate-400 hover:bg-slate-800/50 hover:text-slate-200"
              )
            }
          >
            <item.icon size={20} />
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-slate-800">
        <div className="flex items-center gap-3 px-4 py-2">
          <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-xs font-bold">
            AD
          </div>
          <div>
            <p className="text-sm font-medium text-slate-200">Admin User</p>
            <p className="text-xs text-slate-500">Security Analyst</p>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
