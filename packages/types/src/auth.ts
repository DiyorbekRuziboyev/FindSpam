import type { UUID, ISODateString } from "./common";

export type UserRole = "SUPER_ADMIN" | "ADMIN" | "ANALYST" | "MODERATOR";

export interface User {
  id: UUID;
  email: string;
  role: UserRole;
  isActive: boolean;
  createdAt: ISODateString;
  updatedAt: ISODateString;
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RefreshTokenRequest {
  refreshToken: string;
}

export interface RolePermissions {
  role: UserRole;
  permissions: string[];
}
