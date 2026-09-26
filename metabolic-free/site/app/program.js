// "Metabolic Free Foundations": the 12-week starter program every client gets.
// Muscle-first: 3 full-body strength days + a 10-minute walk after the biggest meal, every day.
// The coach adjusts loads and exercises in the biweekly session.
window.MF_PROGRAM = {
  name: "Metabolic Free Foundations",
  weeks: 12,
  phases: [
    { from: 1, to: 4, name: "Foundation", dose: "2–3 sets × 10–12 reps, stop 3 reps before failure", focus: "Learn the movements, build the habit." },
    { from: 5, to: 8, name: "Build", dose: "3 sets × 8–10 reps, stop 2 reps before failure", focus: "Add load every week you can." },
    { from: 9, to: 12, name: "Strength", dose: "3–4 sets × 6–8 reps, stop 1–2 reps before failure", focus: "Heavier, fewer reps: muscle is metabolism." },
  ],
  // Mon / Wed / Fri
  days: {
    A: { label: "Mon · Full body A", exercises: ["Goblet squat", "Dumbbell bench press", "One-arm dumbbell row", "Romanian deadlift", "Plank 3 × 30–45 s"] },
    B: { label: "Wed · Full body B", exercises: ["Leg press or split squat", "Lat pulldown or assisted pull-up", "Overhead dumbbell press", "Hip thrust", "Farmer carry 3 × 40 m"] },
    C: { label: "Fri · Full body C", exercises: ["Trap-bar or dumbbell deadlift", "Incline push-up or incline press", "Seated cable row", "Walking lunge", "Dead bug 3 × 10/side"] },
  },
  daily: ["10-minute walk after your biggest meal", "Protein at every meal (your target is set by your coach)", "Morning Lumen breath before eating"],
  phaseFor(week) {
    return this.phases.find((p) => week >= p.from && week <= p.to) || this.phases[this.phases.length - 1];
  },
};
