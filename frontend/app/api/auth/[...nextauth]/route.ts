import NextAuth, { NextAuthOptions } from "next-auth";
import GitHubProvider from "next-auth/providers/github";
import { MongoDBAdapter } from "@next-auth/mongodb-adapter";
import clientPromise from "@/lib/mongodb";

console.log("[NextAuth] Loading route.ts...");

export const authOptions: NextAuthOptions = {
  secret: process.env.NEXTAUTH_SECRET,

  session: {
    strategy: "jwt",
  },

  providers: [
    GitHubProvider({
      clientId: process.env.GITHUB_ID ?? "",
      clientSecret: process.env.GITHUB_SECRET ?? "",
    }),
  ],

  adapter: MongoDBAdapter(clientPromise),

  callbacks: {
    async jwt({ token, user }) {
      console.log("[callbacks.jwt] incoming token:", token);
      console.log("[callbacks.jwt] incoming user:", user);
      return token;
    },

    async session({ session }) {
      return session;
    },
    async redirect({ url, baseUrl }) {
      return `${baseUrl}/dashboard`;
    },
  },
  events: {
    async signIn({ user }) {
      console.log("[events.signIn] user:", user);
    },
    async createUser({ user }) {
      console.log("[events.createUser] user:", user);
    },
  },
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
