"use client";

import { useState } from "react";
import { RefreshCw, AlertTriangle } from "lucide-react";
import { useTriggerTraining } from "../hooks/use-ai-engine";

export function TrainingControls() {
  const [confirmed, setConfirmed] = useState(false);
  const { mutate: triggerTraining, isPending } = useTriggerTraining();

  const handleTrigger = () => {
    if (!confirmed) {
      setConfirmed(true);
      return;
    }
    triggerTraining({ full_retrain: false, use_feedback: true });
    setConfirmed(false);
  };

  return (
    <div className="glass-card rounded-xl p-5 space-y-4">
      <div>
        <h3 className="text-sm font-semibold text-foreground">Training Controls</h3>
        <p className="mt-0.5 text-xs text-muted-foreground">
          Trigger model retraining with the latest labeled data
        </p>
      </div>

      <div className="rounded-lg border border-amber-500/20 bg-amber-500/5 p-3 flex items-start gap-2.5">
        <AlertTriangle className="h-4 w-4 text-amber-400 mt-0.5 shrink-0" />
        <p className="text-xs text-amber-300/80">
          Training will run asynchronously. The current active model will remain deployed
          until you manually promote a new version.
        </p>
      </div>

      <div className="flex items-center gap-3">
        <button
          onClick={handleTrigger}
          disabled={isPending}
          className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 disabled:opacity-50 transition-all"
        >
          <RefreshCw className={`h-4 w-4 ${isPending ? "animate-spin" : ""}`} />
          {confirmed ? "Confirm — Start Training" : "Start Training Job"}
        </button>
        {confirmed && (
          <button
            onClick={() => setConfirmed(false)}
            className="text-xs text-muted-foreground hover:text-foreground transition-colors"
          >
            Cancel
          </button>
        )}
      </div>
    </div>
  );
}
