import Navbar from "@/components/Navbar";
import {
    BarChart3,
    Code2,
    AlertCircle,
    CheckCircle2,
    TrendingUp,
    Clock,
    Zap,
    Shield
} from "lucide-react";
import {
    AreaChart,
    Area,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    PieChart,
    Pie,
    Cell,
} from "recharts";

const reviewData = [
    { name: "Mon", reviews: 12, issues: 8 },
    { name: "Tue", reviews: 19, issues: 14 },
    { name: "Wed", reviews: 15, issues: 9 },
    { name: "Thu", reviews: 22, issues: 16 },
    { name: "Fri", reviews: 28, issues: 18 },
    { name: "Sat", reviews: 8, issues: 5 },
    { name: "Sun", reviews: 6, issues: 3 },
];

const severityData = [
    { name: "Critical", value: 12, color: "#ef4444" },
    { name: "Warning", value: 28, color: "#eab308" },
    { name: "Suggestion", value: 45, color: "#22c55e" },
    { name: "Positive", value: 32, color: "#3b82f6" },
];

const recentReviews = [
    { id: 1, file: "auth.py", issues: 3, time: "2 min ago", status: "critical" },
    { id: 2, file: "api/routes.ts", issues: 1, time: "15 min ago", status: "warning" },
    { id: 3, file: "utils/helpers.js", issues: 0, time: "1 hr ago", status: "clean" },
    { id: 4, file: "database.py", issues: 2, time: "2 hrs ago", status: "warning" },
    { id: 5, file: "config.ts", issues: 5, time: "3 hrs ago", status: "critical" },
];

function StatsCard({ title, value, subtitle, icon: Icon, trend, color = "from-primary to-blue-500", delay = 0 }: any) {
    return (
        <div className="relative group">
            <div className={`absolute -inset-0.5 bg-gradient-to-r ${color} rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-500`} />
            <div className="relative glass rounded-xl p-6 h-full">
                <div className="flex items-start justify-between mb-4">
                    <div className={`p-3 rounded-xl bg-gradient-to-br ${color}`}>
                        <Icon className="w-5 h-5 text-white" />
                    </div>
                    {trend && (
                        <div className={`flex items-center gap-1 text-sm font-medium ${trend.isPositive ? "text-emerald-400" : "text-red-400"
                            }`}>
                            <span>{trend.isPositive ? "+" : ""}{trend.value}%</span>
                        </div>
                    )}
                </div>
                <div>
                    <p className="text-3xl font-display font-bold text-foreground mb-1">
                        {value}
                    </p>
                    <p className="text-sm text-muted-foreground">{title}</p>
                    {subtitle && (
                        <p className="text-xs text-muted-foreground/70 mt-1">{subtitle}</p>
                    )}
                </div>
            </div>
        </div>
    );
}

export default function Stats() {
    return (
        <div className="min-h-screen bg-background bg-grid relative">
            <div className="absolute inset-0 bg-gradient-radial pointer-events-none" />
            <Navbar />

            <main className="relative pt-28 pb-20 px-6">
                <div className="max-w-6xl mx-auto">
                    <div className="mb-10">
                        <h1 className="font-display text-4xl font-bold text-foreground mb-2">
                            Analytics Dashboard
                        </h1>
                        <p className="text-muted-foreground">
                            Track your code review metrics and insights
                        </p>
                    </div>

                    <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                        <StatsCard
                            title="Total Reviews"
                            value="127"
                            subtitle="Last 30 days"
                            icon={Code2}
                            trend={{ value: 12, isPositive: true }}
                            delay={0}
                        />
                        <StatsCard
                            title="Issues Found"
                            value="89"
                            subtitle="Across all reviews"
                            icon={AlertCircle}
                            trend={{ value: 8, isPositive: false }}
                            color="from-red-500 to-orange-500"
                            delay={0.1}
                        />
                        <StatsCard
                            title="Clean Reviews"
                            value="38"
                            subtitle="No critical issues"
                            icon={CheckCircle2}
                            trend={{ value: 15, isPositive: true }}
                            color="from-emerald-500 to-teal-500"
                            delay={0.2}
                        />
                        <StatsCard
                            title="Avg. Response"
                            value="2.3s"
                            subtitle="Analysis time"
                            icon={Zap}
                            color="from-yellow-500 to-amber-500"
                            delay={0.3}
                        />
                    </div>

                    <div className="grid lg:grid-cols-3 gap-6 mb-8">
                        <div className="lg:col-span-2 glass rounded-xl p-6">
                            <h3 className="font-display text-lg font-semibold mb-4 flex items-center gap-2">
                                <TrendingUp className="w-5 h-5 text-primary" />
                                Review Activity
                            </h3>
                            <div className="h-64">
                                <ResponsiveContainer width="100%" height="100%">
                                    <AreaChart data={reviewData}>
                                        <defs>
                                            <linearGradient id="colorReviews" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.4} />
                                                <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
                                            </linearGradient>
                                            <linearGradient id="colorIssues" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.4} />
                                                <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                                            </linearGradient>
                                        </defs>
                                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                                        <XAxis dataKey="name" stroke="rgba(255,255,255,0.5)" fontSize={12} />
                                        <YAxis stroke="rgba(255,255,255,0.5)" fontSize={12} />
                                        <Tooltip
                                            contentStyle={{
                                                backgroundColor: "rgba(30, 41, 59, 0.9)",
                                                border: "1px solid rgba(255,255,255,0.1)",
                                                borderRadius: "8px",
                                            }}
                                        />
                                        <Area
                                            type="monotone"
                                            dataKey="reviews"
                                            stroke="#8b5cf6"
                                            fillOpacity={1}
                                            fill="url(#colorReviews)"
                                            strokeWidth={2}
                                        />
                                        <Area
                                            type="monotone"
                                            dataKey="issues"
                                            stroke="#ef4444"
                                            fillOpacity={1}
                                            fill="url(#colorIssues)"
                                            strokeWidth={2}
                                        />
                                    </AreaChart>
                                </ResponsiveContainer>
                            </div>
                        </div>

                        <div className="glass rounded-xl p-6">
                            <h3 className="font-display text-lg font-semibold mb-4 flex items-center gap-2">
                                <Shield className="w-5 h-5 text-primary" />
                                Issue Breakdown
                            </h3>
                            <div className="h-52">
                                <ResponsiveContainer width="100%" height="100%">
                                    <PieChart>
                                        <Pie
                                            data={severityData}
                                            cx="50%"
                                            cy="50%"
                                            innerRadius={50}
                                            outerRadius={75}
                                            paddingAngle={4}
                                            dataKey="value"
                                        >
                                            {severityData.map((entry, index) => (
                                                <Cell key={`cell-${index}`} fill={entry.color} />
                                            ))}
                                        </Pie>
                                        <Tooltip
                                            contentStyle={{
                                                backgroundColor: "rgba(30, 41, 59, 0.9)",
                                                border: "1px solid rgba(255,255,255,0.1)",
                                                borderRadius: "8px",
                                            }}
                                        />
                                    </PieChart>
                                </ResponsiveContainer>
                            </div>
                            <div className="grid grid-cols-2 gap-2 mt-4">
                                {severityData.map((item) => (
                                    <div key={item.name} className="flex items-center gap-2">
                                        <div
                                            className="w-3 h-3 rounded-full"
                                            style={{ backgroundColor: item.color }}
                                        />
                                        <span className="text-xs text-muted-foreground">{item.name}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    <div className="glass rounded-xl p-6">
                        <h3 className="font-display text-lg font-semibold mb-4 flex items-center gap-2">
                            <Clock className="w-5 h-5 text-primary" />
                            Recent Reviews
                        </h3>
                        <div className="space-y-3">
                            {recentReviews.map((review) => (
                                <div
                                    key={review.id}
                                    className="flex items-center justify-between p-4 rounded-lg bg-white/5 hover:bg-white/10 transition-colors cursor-pointer"
                                >
                                    <div className="flex items-center gap-4">
                                        <div className={`w-2 h-2 rounded-full ${review.status === "critical" ? "bg-red-500" :
                                                review.status === "warning" ? "bg-yellow-500" :
                                                    "bg-emerald-500"
                                            }`} />
                                        <div>
                                            <p className="font-mono text-sm text-foreground">{review.file}</p>
                                            <p className="text-xs text-muted-foreground">{review.time}</p>
                                        </div>
                                    </div>
                                    <div className="text-right">
                                        <p className={`text-sm font-medium ${review.issues === 0 ? "text-emerald-400" :
                                                review.issues <= 2 ? "text-yellow-400" :
                                                    "text-red-400"
                                            }`}>
                                            {review.issues === 0 ? "Clean" : `${review.issues} issues`}
                                        </p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
