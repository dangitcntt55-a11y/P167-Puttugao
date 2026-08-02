import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatPercent(value: number, digits = 1) {
  return `${(value * 100).toFixed(digits)}%`;
}

export function formatNumber(value: number) {
  return value.toLocaleString("vi-VN");
}

export function formatDate(iso: string) {
  return new Date(iso).toLocaleString("vi-VN");
}

export function verdictColor(result: string | null) {
  switch (result) {
    case "improved":
      return "bg-green-100 text-green-800";
    case "regressed":
      return "bg-red-100 text-red-800";
    default:
      return "bg-yellow-100 text-yellow-800";
  }
}

export function verdictText(result: string | null) {
  switch (result) {
    case "improved":
      return "Cải thiện";
    case "regressed":
      return "Suy giảm";
    case "no_evidence":
      return "Chưa rõ";
    default:
      return "Chưa đo";
  }
}

export function severityColor(severity: string) {
  switch (severity) {
    case "critical":
      return "bg-red-100 text-red-800";
    case "high":
      return "bg-orange-100 text-orange-800";
    case "medium":
      return "bg-yellow-100 text-yellow-800";
    default:
      return "bg-gray-100 text-gray-800";
  }
}
