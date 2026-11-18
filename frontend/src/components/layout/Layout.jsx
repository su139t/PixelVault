import { Navbar } from "./Navbar";
import { BottomNav } from "./BottomNav";

export function Layout({ children }) {
  return (
    <div className="min-h-screen bg-bg-deep">
      <Navbar />
      <BottomNav />
      <main className="main-content">
        <div className="main-inner">
          {children}
        </div>
      </main>
    </div>
  );
}
