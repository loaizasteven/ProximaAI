import { useState, useEffect } from "react";
import { Coins, AlertCircle } from "lucide-react";
import { useSupabase, useAuth } from '@/auth/Authentication';

interface CreditBalanceProps {
  className?: string;
  showIcon?: boolean;
  refresh_key?: number;
}

export function CreditBalance({
  className,
  showIcon = true,
  refresh_key,
}: CreditBalanceProps) {
  const supabase = useSupabase();
  const session = useAuth();
  const [credits, setCredits] = useState<number | null>(null);
  const [error, setError] = useState(false);
  const [loading, setLoading] = useState(true);
  const userId = session?.user?.id;

  useEffect(() => {
    if (!userId) return;
    setLoading(true);
    const fetchCredits = async () => {
      const { data, error } = await supabase.rpc('spend_credits', {
        p_user_id: userId,
        p_credits_to_spend: 0,
      });
      if (error) {
        setError(true);
        setCredits(null);
      } else {
        setError(false);
        setCredits(data);
      }
      setLoading(false);
    };
    fetchCredits();
  }, [supabase, userId, refresh_key]);

  if (!session) return null;

  const baseClass = "flex items-center space-x-2 px-3 py-1.5 text-sm font-medium";
  const loadingClass = "bg-gray-200 text-gray-800";

  let badgeClass = baseClass;
  let badgeStyle: React.CSSProperties = {
    padding: '1.2ch', 
    borderRadius: '1ch', 
    alignItems: 'center', 
    display: 'inline-flex',
    fontSize: '0.8pc'
  };

  if (loading) {
    badgeClass += ` ${loadingClass}`;
  } else if (error || credits === null) {
    badgeStyle = { ...badgeStyle, background: 'red', color: 'white' };
  } else if (credits === 0) {
    badgeStyle = { ...badgeStyle, background: 'red', color: 'white'};
  } else {
    // Default badge style (e.g., black background, white text)
    badgeStyle = { ...badgeStyle, background: 'lightgray', color: 'black' };
  }
  if (className) badgeClass += ` ${className}`;

  if (loading) {
    return (
      <span className={badgeClass}>
        {showIcon && <Coins className="h-4 w-4 text-gray-500" style={{ marginRight: '0.5em' }} />}
        <span className="text-sm font-medium">Loading</span>
      </span>
    );
  }

  if (error || credits === null) {
    return (
      <span className={badgeClass} style={badgeStyle}>
        {showIcon && <AlertCircle className="h-4 w-4" style={{ marginRight: '0.5em' }} />}
        <span className="text-sm font-medium">Error</span>
      </span>
    );
  }

  if (credits === 0) {
    return (
      <span className={badgeClass} style={badgeStyle}>
        {showIcon && <AlertCircle className="h-4 w-4" style={{ marginRight: '0.5em' }} />}
        <span className="text-sm font-medium">0 credits</span>
      </span>
    );
  }

  const getIcon = (credits: number) => {
    const iconStyle = { marginRight: '0.5em' };
    if (credits === 0) return <AlertCircle className="h-4 w-4" style={iconStyle} />;
    return <Coins className="h-4 w-4 text-yellow-500" style={iconStyle} />;
  };

  return (
    <span className={badgeClass} style={badgeStyle}>
      {showIcon && getIcon(credits)}
      <span>
        {credits} {credits === 1 ? "credit" : "credits"}
      </span>
    </span>
  );
}