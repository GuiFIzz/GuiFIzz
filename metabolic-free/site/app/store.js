// Data layer for the client platform. Same interface, two backends:
//   - Supabase (when SUPABASE_URL is set in config.js): real accounts, magic-link login
//   - Demo (otherwise): sample data in this browser only, so the coach can preview everything
(function () {
  const C = window.MF_CONFIG;
  const iso = (d) => d.toISOString().slice(0, 10);
  const daysAgo = (n) => { const d = new Date(); d.setDate(d.getDate() - n); return d; };

  // ---------- Demo backend ----------
  const KEY = "mf_demo_v1";
  function seed() {
    const checkins = {};
    for (let i = 1; i <= 20; i++) {
      if (i % 6 === 0) continue; // a few missed days, like a real client
      checkins[iso(daysAgo(i))] = {
        day: iso(daysAgo(i)), lumen_score: [2, 3, 3, 2, 4, 1][i % 6], weight_lb: +(214 - (20 - i) * 0.35).toFixed(1),
        protein_hit: i % 3 !== 0, walk_done: i % 4 !== 0, steps: 6000 + (i * 397) % 4000, sleep_hours: 7, energy: 3 + (i % 3 === 0 ? 1 : 0), note: "",
      };
    }
    return {
      profile: { first_name: "Demo client", role: "client", start_date: iso(daysAgo(20)), next_session: daysAgo(-3).toISOString(), plan: "foundation" },
      checkins, workouts: { "1-A": 1, "1-B": 1, "1-C": 1, "2-A": 1, "2-B": 1, "2-C": 1, "3-A": 1 },
      roster: [
        { first_name: "Demo client", start_date: iso(daysAgo(20)), last_checkin: iso(daysAgo(1)), adherence7: 86, next_session: daysAgo(-3).toISOString() },
        { first_name: "Maria (sample)", start_date: iso(daysAgo(44)), last_checkin: iso(daysAgo(0)), adherence7: 100, next_session: daysAgo(-1).toISOString() },
        { first_name: "John (sample)", start_date: iso(daysAgo(12)), last_checkin: iso(daysAgo(6)), adherence7: 29, next_session: daysAgo(-6).toISOString() },
      ],
    };
  }
  const load = () => { try { return JSON.parse(localStorage.getItem(KEY)) || seed(); } catch { return seed(); } };
  const save = (s) => { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch {} };

  const demo = {
    mode: "demo",
    async session() { return { email: "demo@example.com" }; },
    async signIn() { return { demo: true }; },
    async signOut() { try { localStorage.removeItem(KEY); } catch {} },
    async profile() { return load().profile; },
    async checkins(n = 30) {
      const s = load(), since = iso(daysAgo(n));
      return Object.values(s.checkins).filter((c) => c.day >= since).sort((a, b) => a.day.localeCompare(b.day));
    },
    async saveCheckin(c) { const s = load(); s.checkins[c.day] = { ...s.checkins[c.day], ...c }; save(s); },
    async workouts() { return load().workouts; },
    async toggleWorkout(week, day, done) {
      const s = load(), k = `${week}-${day}`;
      if (done) s.workouts[k] = 1; else delete s.workouts[k];
      save(s);
    },
    async roster() { return load().roster; },
  };

  // ---------- Supabase backend ----------
  function supa() {
    const sb = window.supabase.createClient(C.SUPABASE_URL, C.SUPABASE_ANON_KEY);
    const uid = async () => (await sb.auth.getUser()).data.user?.id;
    return {
      mode: "live",
      async session() { return (await sb.auth.getSession()).data.session?.user || null; },
      async signIn(email) {
        const { error } = await sb.auth.signInWithOtp({ email, options: { emailRedirectTo: location.href.split("#")[0] } });
        if (error) throw error;
      },
      async signOut() { await sb.auth.signOut(); },
      async profile() { const { data } = await sb.from("profiles").select("*").eq("id", await uid()).single(); return data; },
      async checkins(n = 30) {
        const { data } = await sb.from("checkins").select("*").eq("client_id", await uid())
          .gte("day", iso(daysAgo(n))).order("day");
        return data || [];
      },
      async saveCheckin(c) {
        const { error } = await sb.from("checkins").upsert({ ...c, client_id: await uid() });
        if (error) throw error;
      },
      async workouts() {
        const { data } = await sb.from("workout_logs").select("week,day").eq("client_id", await uid());
        return Object.fromEntries((data || []).map((w) => [`${w.week}-${w.day}`, 1]));
      },
      async toggleWorkout(week, day, done) {
        const id = await uid();
        const q = done
          ? sb.from("workout_logs").upsert({ client_id: id, week, day })
          : sb.from("workout_logs").delete().match({ client_id: id, week, day });
        const { error } = await q; if (error) throw error;
      },
      async roster() {
        const since = iso(daysAgo(6)); // last 7 days including today
        const [{ data: people }, { data: recent }] = await Promise.all([
          sb.from("profiles").select("id,first_name,start_date,next_session").eq("role", "client").eq("active", true),
          sb.from("checkins").select("client_id,day").gte("day", iso(daysAgo(60))),
        ]);
        return (people || []).map((p) => {
          const mine = (recent || []).filter((c) => c.client_id === p.id).map((c) => c.day).sort();
          return { ...p, last_checkin: mine[mine.length - 1] || null,
                   adherence7: Math.round(mine.filter((d) => d >= since).length / 7 * 100) };
        });
      },
    };
  }

  window.MF_STORE = C.SUPABASE_URL && window.supabase ? supa() : demo;
  window.MF_UTIL = { iso, daysAgo };
})();
