-- Metabolic Flex client platform (Supabase). Apply as a migration.
-- Scope: coaching and lifestyle data only. Medication, prescriptions and medical records live
-- in Altrohealth (GFC Lab) and are NEVER stored here.

create table if not exists profiles (
  id              uuid primary key references auth.users(id) on delete cascade,
  role            text not null default 'client' check (role in ('client', 'coach')),
  first_name      text,
  start_date      date,                       -- program week 1 starts here; set when onboarding completes
  next_session    timestamptz,
  plan            text default 'foundation',  -- foundation ($299 x 3) | momentum ($199 x 6)
  active          boolean not null default true,
  created_at      timestamptz not null default now(),
  -- Onboarding intake (coaching context only; medical data stays with Altrohealth)
  onboarded       boolean not null default false,
  fitness_level   text check (fitness_level in ('beginner', 'intermediate', 'advanced')),
  equipment       text[],                     -- e.g. {bodyweight, dumbbells, suspension, home_gym, full_gym}
  schedule_days   text[],                     -- preferred weekdays, e.g. {monday, wednesday, friday}
  goals           text,
  red_flag        boolean not null default false,  -- PAR-Q style screen; true routes to "see your physician first"
  health_notes    text,
  start_weight_lb numeric(5,1)
);

create table if not exists progress_photos (
  id          uuid primary key default gen_random_uuid(),
  client_id   uuid not null references profiles(id) on delete cascade,
  storage_path text not null,                -- path inside the "progress-photos" Storage bucket
  taken_at    date not null default current_date,
  kind        text default 'baseline' check (kind in ('baseline', 'progress')),
  created_at  timestamptz not null default now()
);

create table if not exists checkins (
  client_id     uuid not null references profiles(id) on delete cascade,
  day           date not null,
  lumen_score   int check (lumen_score between 1 and 5),   -- Lumen: 1 = burning fat ... 5 = burning carbs
  weight_lb     numeric(5,1),
  protein_hit   boolean,
  steps         int,
  walk_done     boolean,
  sleep_hours   numeric(3,1),
  energy        int check (energy between 1 and 5),
  note          text,
  created_at    timestamptz not null default now(),
  primary key (client_id, day)
);

create table if not exists workout_logs (
  client_id     uuid not null references profiles(id) on delete cascade,
  week          int not null check (week between 1 and 52),
  day           text not null check (day in ('A', 'B', 'C')),
  done_at       timestamptz not null default now(),
  primary key (client_id, week, day)
);

-- Coach check without recursive RLS
create or replace function is_coach() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from profiles where id = auth.uid() and role = 'coach');
$$;

-- Public founding-spot counter for the website (returns a number only, no personal data)
create or replace function spots_taken() returns int
language sql stable security definer set search_path = public as $$
  select count(*)::int from profiles where role = 'client' and active and start_date is not null;
$$;
grant execute on function spots_taken() to anon, authenticated;

alter table profiles         enable row level security;
alter table checkins         enable row level security;
alter table workout_logs     enable row level security;
alter table progress_photos  enable row level security;

create policy "own profile read"    on profiles for select using (id = auth.uid() or is_coach());
create policy "coach edits profiles" on profiles for update using (is_coach());
-- A client completes their own onboarding (sets onboarded, start_date, fitness_level, equipment,
-- schedule_days, goals, red_flag, health_notes, start_weight_lb) but never their own plan/active/role.
create policy "client completes own onboarding" on profiles for update using (id = auth.uid())
  with check (id = auth.uid() and role = 'client');
create policy "own checkins"        on checkins for all using (client_id = auth.uid() or is_coach())
                                    with check (client_id = auth.uid());
create policy "own workouts"        on workout_logs for all using (client_id = auth.uid() or is_coach())
                                    with check (client_id = auth.uid());
create policy "own progress photos" on progress_photos for all using (client_id = auth.uid() or is_coach())
                                    with check (client_id = auth.uid());

-- New sign-ups get a client profile automatically (the coach sets start_date on enrollment)
create or replace function handle_new_user() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into profiles (id, first_name) values (new.id, new.raw_user_meta_data->>'first_name');
  return new;
end $$;
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users
  for each row execute function handle_new_user();

-- Storage: create a PRIVATE bucket named "progress-photos" in the Supabase dashboard
-- (Storage -> New bucket -> uncheck "Public bucket"), then run this to scope access to
-- each client's own folder (path must start with "<their user id>/").
insert into storage.buckets (id, name, public) values ('progress-photos', 'progress-photos', false)
  on conflict (id) do nothing;
create policy "own progress photo files" on storage.objects for all
  using (bucket_id = 'progress-photos' and (auth.uid()::text = (storage.foldername(name))[1] or is_coach()))
  with check (bucket_id = 'progress-photos' and auth.uid()::text = (storage.foldername(name))[1]);
