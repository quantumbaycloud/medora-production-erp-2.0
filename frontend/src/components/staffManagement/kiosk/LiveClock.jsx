import { useEffect, useState } from "react";

const LiveClock = () => {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const timeString = currentTime.toLocaleTimeString("en-US", {
    hour12: true,
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });

  const dateString = currentTime.toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric",
  });

  return (
    <div className="mt-8 text-center">
      <p className="text-5xl font-extrabold tracking-tighter text-primary">
        {timeString}
      </p>
      <p className="mt-1 text-xs font-medium uppercase tracking-widest text-on-surface-variant">
        {dateString}
      </p>
    </div>
  );
};

export default LiveClock;