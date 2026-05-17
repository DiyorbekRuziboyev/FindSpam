"use client";

import { useState } from "react";
import { Plus } from "lucide-react";
import { useAddBlacklistEntry } from "../hooks/use-blacklist";

export function BlacklistEntryForm() {
  const [type, setType] = useState<"DOMAIN" | "PATTERN" | "PHRASE">("DOMAIN");
  const [value, setValue] = useState("");
  const [reason, setReason] = useState("");
  const { mutate: addEntry, isPending } = useAddBlacklistEntry();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!value.trim()) return;
    addEntry(
      { type, value: value.trim(), reason: reason.trim() || null },
      {
        onSuccess: () => {
          setValue("");
          setReason("");
        },
      },
    );
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="glass-card rounded-xl p-5 space-y-4"
    >
      <h3 className="text-sm font-semibold text-foreground">Add Entry</h3>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        <select
          value={type}
          onChange={(e) => setType(e.target.value as typeof type)}
          className="h-9 rounded-lg border border-border/50 bg-muted/30 px-3 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
        >
          <option value="DOMAIN">Domain</option>
          <option value="PATTERN">Pattern (regex)</option>
          <option value="PHRASE">Phrase</option>
        </select>
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder={
            type === "DOMAIN"
              ? "example.com"
              : type === "PATTERN"
              ? "(?i)free\\s+money"
              : "win a prize"
          }
          required
          className="h-9 rounded-lg border border-border/50 bg-muted/30 px-3 text-sm text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:ring-1 focus:ring-ring"
        />
        <input
          type="text"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          placeholder="Reason (optional)"
          className="h-9 rounded-lg border border-border/50 bg-muted/30 px-3 text-sm text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:ring-1 focus:ring-ring"
        />
      </div>
      <button
        type="submit"
        disabled={isPending || !value.trim()}
        className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 disabled:opacity-50 transition-all"
      >
        <Plus className="h-4 w-4" />
        Add to Blacklist
      </button>
    </form>
  );
}
