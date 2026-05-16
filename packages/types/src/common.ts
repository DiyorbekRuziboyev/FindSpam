export type UUID = string;
export type ISODateString = string;
export type UnixTimestamp = number;

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}

export type SortOrder = "asc" | "desc";

export interface DateRangeFilter {
  from: ISODateString;
  to: ISODateString;
}
