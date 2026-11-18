import { useState, useEffect } from "react";
import api from "../services/api";
import { Users, User } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export default function PeoplePage() {
  const { user } = useAuth();
  const [people, setPeople] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!user?.user_id) return;
    let isActive = true;

    const loadPeople = async () => {
      try {
        setIsLoading(true);
        const response = await api.get(`/people?user_id=${user.user_id}`);
        if (isActive) setPeople(response.data.data?.people || []);
      } catch (error) {
        console.error("Failed to fetch people:", error);
      } finally {
        if (isActive) setIsLoading(false);
      }
    };

    loadPeople();
    return () => { isActive = false; };
  }, [user?.user_id]);

  return (
    <div>
      <div className="page-header">
        <div className="flex items-center gap-3">
          <Users className="w-7 h-7 text-accent-indigo" />
          <h1 className="page-title page-title-gradient">People</h1>
        </div>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-20">
          <div className="spinner" />
        </div>
      ) : people.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">
            <Users className="w-7 h-7 text-accent-indigo" />
          </div>
          <p className="empty-state-title">No people recognized yet</p>
          <p className="empty-state-text">Upload photos with faces to get started</p>
        </div>
      ) : (
        <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 gap-4 md:gap-6">
          {people.map((person, i) => (
            <div
              key={person.person_id}
              className="person-card animate-[fade-in_0.4s_ease_both]"
              style={{ animationDelay: `${i * 0.05}s` }}
            >
              <div className="person-avatar">
                <User className="w-8 h-8 text-accent-indigo/50" />
              </div>
              <h3 className="font-medium text-text-primary text-sm truncate w-full px-1">
                {person.person_name}
              </h3>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
