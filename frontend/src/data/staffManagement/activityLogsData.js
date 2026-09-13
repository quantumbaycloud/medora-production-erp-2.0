let activityLogs = [];
export function setRuntimeData(data){ activityLogs=data||[]; }
export function clearRuntimeData(){ activityLogs=[]; }
export { activityLogs as default };
