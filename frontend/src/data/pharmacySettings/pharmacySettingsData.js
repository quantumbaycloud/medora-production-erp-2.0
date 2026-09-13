export let kpiSummary = [];
export let revenueOverview = { periods: [], bars: [] };
export let branchPerformance = [];
export let categoryDistribution = { totalSkus: "0", categories: [] };
export let recentOrders = [];
export let quickActions = [];
export let lowStockAlerts = [];
export let recentActivity = [];
export let pharmacyProfile = { business: {}, owner: {}, address: {}, license: {} };
export let branches = [];
export let directorySummary = {};
export let directoryBranches = [];
export let branchDeepDive = [];
export function setRuntimeData(data) { for (const [k,v] of Object.entries(data)) { if (k === "kpiSummary") kpiSummary=v; else if(k==="revenueOverview") revenueOverview=v; else if(k==="branchPerformance") branchPerformance=v; else if(k==="categoryDistribution") categoryDistribution=v; else if(k==="recentOrders") recentOrders=v; else if(k==="quickActions") quickActions=v; else if(k==="lowStockAlerts") lowStockAlerts=v; else if(k==="recentActivity") recentActivity=v; else if(k==="pharmacyProfile") pharmacyProfile=v; else if(k==="branches") branches=v; else if(k==="directorySummary") directorySummary=v; else if(k==="directoryBranches") directoryBranches=v; else if(k==="branchDeepDive") branchDeepDive=v; } }
export function clearRuntimeData(){setRuntimeData({kpiSummary:[],revenueOverview:{periods:[],bars:[]},branchPerformance:[],categoryDistribution:{totalSkus:"0",categories:[]},recentOrders:[],quickActions:[],lowStockAlerts:[],recentActivity:[],pharmacyProfile:{business:{},owner:{},address:{},license:{}},branches:[],directorySummary:{},directoryBranches:[],branchDeepDive:[]});}
