"use client";

import { Button } from "@/components/ui/button";
import { useSession } from "next-auth/react";
import Image from "next/image";
import { redirect } from "next/navigation";

export default function Home() {
  const { data: session } = useSession();

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <Button
        size="lg"
        type="submit"
        className="border border-neutral-700 bg-neutral-800 text-white transition-colors hover:bg-neutral-700"
        onClick={() => {
          // check if user is signed in
          if (!session || !session.user) {
            console.log("made it here");
            redirect("/api/auth/signin");
          }

          console.log(session);

          return redirect("/dashboard");
        }}
      >
        Get Started
      </Button>
    </div>
  );
}
