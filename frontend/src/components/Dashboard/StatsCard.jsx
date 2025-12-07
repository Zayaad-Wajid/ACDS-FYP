import React from "react";

const StatsCard = ({ title, value }) => {
  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-lg p-6 text-center">
      <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-2">
        {title}
      </p>
      <h3 className="text-4xl font-bold text-slate-100">{value}</h3>
    </div>
  );
};

export default StatsCard;
