import { DefaultSession, DefaultUser, User } from "next-auth";

declare module "next-auth" {
  /**
   * Returned by useSession, getSession, and in the JWT callback
   */
  interface User extends DefaultUser {}

  interface Session {
    user: {} & DefaultSession["user"];
  }
}

declare module "next-auth/jwt" {
  interface JWT {}
}
