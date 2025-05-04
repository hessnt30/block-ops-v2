"use client";

import { useSession } from "next-auth/react";
import { redirect } from "next/navigation";

export default function DashboardPage() {
  // check if user is signed in
  const { data: session } = useSession();
  if (!session || !session.user || !session.user.email) {
    redirect("/api/auth/signin");
  }

  return <>Hello, World</>;
}
