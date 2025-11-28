import React from "react";
import { Card, CardContent } from "../ui/Card";

const StatsCard = ({ title, value, subtext, icon: Icon, trend }) => {
  return (
    <Card className="bg-slate-900/50 border-slate-800">
      <CardContent className="p-6">
        <p className="text-xs uppercase tracking-wide text-slate-500">
          {title}
        </p>
        <h3 className="text-4xl font-semibold text-slate-100 mt-3">{value}</h3>
        {subtext && (
          <p className="text-xs text-slate-500 mt-3">{subtext}</p>
        )}
      </CardContent>
    </Card>
  );
};

export default StatsCard;
